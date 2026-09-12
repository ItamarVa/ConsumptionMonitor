"""Read-only HTTP API over stored meter readings, shaped for Home Assistant REST sensors.

Binds to 127.0.0.1 by default with no authentication — safe only on loopback.
TrustedHostMiddleware limits Host to ALLOWED_HOSTS (IPv4 loopback only; HOST binds
IPv4). No CORS middleware — the dashboard is same-origin at /ui. Every query parameter
is validated here; this is the trust boundary. Storage queries are in db.py per the
records.py contract. Depended on by: __main__.py.
"""

from __future__ import annotations

import asyncio
import sqlite3
from contextlib import asynccontextmanager
from datetime import date, timedelta
from typing import Annotated, Literal

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from . import config, db, jobs, source
from .hourly import spread_to_hours
from .records import UNITS, UTILITIES

# Raw and interval series can explode in size; aggregated endpoints span full history.
MAX_RANGE_DAYS = 366
DEFAULT_DAYS = 7

Utility = Literal["electricity", "water"]
Direction = Literal["import", "export", "water"]

_ELECTRICITY_DIRECTIONS = ("import", "export")
_WATER_DIRECTIONS = ("water",)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if config.HOST not in ("127.0.0.1", "localhost"):
        print(
            "WARNING: ConsumptionMonitor is bound to a non-loopback address "
            f"({config.HOST}) with no authentication.",
            flush=True,
        )
    db.connect().close()
    task = asyncio.create_task(jobs.loop())
    try:
        yield
    finally:
        task.cancel()


app = FastAPI(
    title="ConsumptionMonitor",
    summary="Local electricity and water consumption API backed by a mycitygrid scraper.",
    lifespan=lifespan,
)

_SECURITY_HEADERS = {
    "Content-Security-Policy": (
        "default-src 'self'; script-src 'self'; style-src 'self'; "
        "img-src 'self' data:; connect-src 'self'; base-uri 'none'; "
        "form-action 'none'; frame-ancestors 'none'"
    ),
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
}


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    for key, value in _SECURITY_HEADERS.items():
        response.headers[key] = value
    return response


class _AllowedClientIPMiddleware:
    """Reject peers outside ALLOWED_CLIENT_IPS when that list is non-empty."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and config.ALLOWED_CLIENT_IPS:
            client = scope.get("client")
            host = client[0] if client else ""
            if host not in config.ALLOWED_CLIENT_IPS:
                response = JSONResponse({"detail": "Forbidden"}, status_code=403)
                await response(scope, receive, send)
                return
        await self.app(scope, receive, send)


app.add_middleware(_AllowedClientIPMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=config.ALLOWED_HOSTS)


def get_conn():
    conn = db.connect()
    try:
        yield conn
    finally:
        conn.close()


Conn = Annotated[sqlite3.Connection, Depends(get_conn)]


def _directions_for(utility: str) -> tuple[str, ...]:
    return _WATER_DIRECTIONS if utility == "water" else _ELECTRICITY_DIRECTIONS


def _validate_direction(utility: str, direction: str) -> None:
    if direction not in _directions_for(utility):
        raise HTTPException(
            422,
            f"direction must be one of {', '.join(_directions_for(utility))} for {utility}",
        )


def _first_stored(conn: sqlite3.Connection, utility: str) -> date | None:
    first = db.coverage(conn).get(utility, {}).get("first_date")
    return date.fromisoformat(first) if first else None


def _range(
    conn: sqlite3.Connection,
    utility: str,
    start: date | None,
    end: date | None,
    *,
    max_days: int | None = None,
    default_days: int | None = None,
) -> tuple[date, date]:
    """Fill defaults, then reject a backwards range or one over an endpoint cap."""
    end = end or jobs.local_today()
    if start is None:
        start = (
            end - timedelta(days=default_days - 1)
            if default_days
            else _first_stored(conn, utility) or end
        )
    if start > end:
        raise HTTPException(422, "start must not be after end")
    if max_days and (end - start).days + 1 > max_days:
        raise HTTPException(422, f"range must not exceed {max_days} days")
    return start, end


def _meter_ids(conn: sqlite3.Connection, utility: str) -> list[str]:
    cov = db.coverage(conn).get(utility, {})
    raw = cov.get("meter_ids") or cov.get("meters")
    if raw:
        return [str(m) for m in (raw if isinstance(raw, list) else [raw])]
    try:
        cur = conn.execute(
            "SELECT DISTINCT meter_id FROM meter_reading WHERE utility = ? ORDER BY meter_id",
            (utility,),
        )
        return [row[0] for row in cur]
    except sqlite3.OperationalError:
        return []


def _primary_meter(conn: sqlite3.Connection, utility: str) -> str:
    ids = _meter_ids(conn, utility)
    if not ids:
        raise HTTPException(404, f"no readings stored for utility {utility}")
    return ids[0]


def _unit(utility: str, direction: str) -> str:
    return UNITS.get((utility, direction), "")


def _register_field(utility: str, direction: str) -> str:
    if utility == "water":
        return "total_water_data"
    if direction == "import":
        return "total_import_kwh"
    if direction == "export":
        return "total_export_kwh"
    raise ValueError(f"unknown utility/direction: {utility}/{direction}")


def _reject_cross_site_refresh(request: Request) -> None:
    site = request.headers.get("sec-fetch-site")
    if site is not None and site not in ("same-origin", "none"):
        raise HTTPException(403, "cross-site refresh not allowed")


def _period_total(
    conn: sqlite3.Connection, utility: str, direction: str, start: date, end: date
) -> dict:
    unit = _unit(utility, direction)
    span = (end - start).days + 1
    row = db.period_total(conn, utility, direction, start, end)
    if not row:
        return {"value": None, "unit": unit, "days": 0, "partial": False}
    return {
        "value": round(row["value"], 4),
        "unit": row.get("unit") or unit,
        "days": span,
        "partial": bool(row.get("partial")),
    }


def _latest_register(latest: dict | None, utility: str, direction: str) -> dict | None:
    if not latest:
        return None
    if utility == "water":
        value = latest.get("total_water_data")
    elif direction == "export":
        value = latest.get("total_export_kwh")
    else:
        value = latest.get("total_import_kwh")
    return {
        "reading_time_utc": latest.get("reading_time_utc"),
        "value": value,
        "unit": _unit(utility, direction),
    }


@app.get("/health")
def health(conn: Conn) -> dict:
    cov = db.coverage(conn)
    return {
        "status": "ok",
        "source_ready": source.SOURCE_READY,
        "credentials_present": config.credentials_present(),
        "credentials_error": config.CREDENTIALS_ERROR,
        "reading_count": sum(int(c.get("reading_count") or 0) for c in cov.values()),
        "coverage": cov,
        "local_date": jobs.local_today().isoformat(),
    }


@app.get("/jobs")
def job_status(conn: Conn) -> dict:
    """Job names and ranges come from jobs.JOBS (recent, recent_week, previous_year, backfill)."""
    states = db.job_states(conn)
    today = jobs.local_today()
    out = {}
    for job, spec in jobs.JOBS.items():
        covers = spec.covers(today, conn) if spec.in_season(today) else None
        out[job] = {
            "every": str(spec.every),
            "in_season": spec.in_season(today),
            "covers": (
                {"start": covers[0].isoformat(), "end": covers[1].isoformat()} if covers else None
            ),
            **states.get(job, {"last_run_utc": None, "last_ok_utc": None, "last_error": None}),
        }
    return out


@app.get("/readings/raw")
def read_raw(
    conn: Conn,
    utility: Utility,
    meter_id: str = Query(..., min_length=1),
    start: date | None = None,
    end: date | None = None,
) -> dict:
    start, end = _range(
        conn, utility, start, end, max_days=MAX_RANGE_DAYS, default_days=DEFAULT_DAYS
    )
    return {
        "utility": utility,
        "meter_id": meter_id,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "readings": db.meter_readings(conn, meter_id, start, end),
    }


@app.get("/readings/hourly")
def read_hourly(
    conn: Conn,
    utility: Utility,
    direction: Direction,
    date_: date = Query(alias="date"),
) -> dict:
    _validate_direction(utility, direction)
    meter_id = _primary_meter(conn, utility)
    rows = db.meter_readings(conn, meter_id, date_ - timedelta(days=1), date_)
    hours = spread_to_hours(rows, _register_field(utility, direction), date_, config.LOCAL_TZ)
    return {
        "utility": utility,
        "direction": direction,
        "date": date_.isoformat(),
        "unit": _unit(utility, direction),
        "meter_id": meter_id,
        "estimated": True,
        "hours": hours,
    }


@app.get("/readings/intervals")
def read_intervals(
    conn: Conn,
    utility: Utility,
    direction: Direction,
    start: date | None = None,
    end: date | None = None,
) -> dict:
    _validate_direction(utility, direction)
    start, end = _range(
        conn, utility, start, end, max_days=MAX_RANGE_DAYS, default_days=DEFAULT_DAYS
    )
    meter_id = _primary_meter(conn, utility)
    rows = db.intervals(conn, meter_id, direction, start, end)
    return {
        "utility": utility,
        "direction": direction,
        "meter_id": meter_id,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "unit": _unit(utility, direction),
        "intervals": rows,
    }


@app.get("/readings/daily")
def read_daily(
    conn: Conn,
    utility: Utility,
    direction: Direction,
    start: date | None = None,
    end: date | None = None,
) -> dict:
    _validate_direction(utility, direction)
    start, end = _range(conn, utility, start, end, default_days=DEFAULT_DAYS)
    return {
        "utility": utility,
        "direction": direction,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "unit": _unit(utility, direction),
        "days": db.daily_totals(conn, utility, direction, start, end),
    }


@app.get("/readings/monthly")
def read_monthly(
    conn: Conn,
    utility: Utility,
    direction: Direction,
    start: date | None = None,
    end: date | None = None,
) -> dict:
    _validate_direction(utility, direction)
    start, end = _range(conn, utility, start, end)
    return {
        "utility": utility,
        "direction": direction,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "unit": _unit(utility, direction),
        "months": db.monthly_totals(conn, utility, direction, start, end),
    }


@app.get("/readings/yearly")
def read_yearly(
    conn: Conn,
    utility: Utility,
    direction: Direction,
    start: date | None = None,
    end: date | None = None,
) -> dict:
    _validate_direction(utility, direction)
    start, end = _range(conn, utility, start, end)
    return {
        "utility": utility,
        "direction": direction,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "unit": _unit(utility, direction),
        "years": db.yearly_totals(conn, utility, direction, start, end),
    }


@app.get("/alerts")
def read_alerts(conn: Conn, utility: Utility) -> dict:
    meters = []
    for meter_id in _meter_ids(conn, utility):
        flags = db.alert_flags(conn, meter_id)
        meters.append({"meter_id": meter_id, **flags})
    return {"utility": utility, "meters": meters}


@app.get("/summary")
def summary(conn: Conn) -> dict:
    today = jobs.local_today()
    week_start = today - timedelta(days=(today.weekday() + 1) % 7)
    month_start = date(today.year, today.month, 1)
    year_start = date(today.year, 1, 1)
    out: dict[str, dict] = {}
    for utility in UTILITIES:
        meter_id = _meter_ids(conn, utility)
        latest = db.latest_reading(conn, meter_id[0]) if meter_id else None
        directions: dict[str, dict] = {}
        for direction in _directions_for(utility):
            directions[direction] = {
                "latest_register": _latest_register(latest, utility, direction),
                "today": _period_total(conn, utility, direction, today, today),
                "this_week": _period_total(conn, utility, direction, week_start, today),
                "this_month": _period_total(conn, utility, direction, month_start, today),
                "year_to_date": _period_total(conn, utility, direction, year_start, today),
            }
        out[utility] = directions
    return {"local_date": today.isoformat(), "utilities": out}


@app.post("/refresh/{job}")
def refresh(conn: Conn, job: str, request: Request) -> dict:
    """Force one job to run now, for testing a freshly implemented source adapter."""
    _reject_cross_site_refresh(request)
    if job not in jobs.JOBS:
        raise HTTPException(404, f"unknown job: {job}")
    rows = jobs.run_job(conn, job)
    return {"job": job, "rows_written": rows, **db.job_states(conn).get(job, {})}


@app.get("/")
def index() -> dict:
    return {
        "docs": "/docs",
        "ui": "/ui",
        "endpoints": [
            "/health",
            "/jobs",
            "/summary",
            "/alerts",
            "/readings/raw",
            "/readings/intervals",
            "/readings/hourly",
            "/readings/daily",
            "/readings/monthly",
            "/readings/yearly",
        ],
    }


_ui_dir = config.ROOT / "web"
_ui_dir.mkdir(exist_ok=True)
app.mount("/ui", StaticFiles(directory=_ui_dir, html=True), name="ui")
