"""Read-only HTTP API over the stored readings, shaped for Home Assistant REST sensors.

Binds to 127.0.0.1 by default and has no authentication, which is only safe because of
that: the DB holds personal consumption data. Widen HOST only behind something that
authenticates. Every query parameter is validated here - this is the trust boundary.
Depended on by: __main__.py.
"""

from __future__ import annotations

import asyncio
import sqlite3
from contextlib import asynccontextmanager
from datetime import date, timedelta
from typing import Annotated, Literal

from fastapi import Depends, FastAPI, HTTPException

from . import config, db, jobs, source

# Only the raw hourly endpoint is capped: a decade of hourly rows in one JSON response is
# useless to anyone. The aggregated endpoints are meant to span the whole stored history.
HOURLY_MAX_DAYS = 366
DEFAULT_DAYS = 7

Utility = Literal["electricity", "water"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.connect().close()  # create the file and schema before serving anything
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


def get_conn():
    conn = db.connect()
    try:
        yield conn
    finally:
        conn.close()


Conn = Annotated[sqlite3.Connection, Depends(get_conn)]


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
    """Fill in the defaults, then reject a backwards range or one over an endpoint's cap.

    Without `default_days` a missing start means the whole stored history.
    """
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


@app.get("/health")
def health(conn: Conn) -> dict:
    return {
        "status": "ok",
        "source_ready": source.SOURCE_READY,
        "credentials_present": config.credentials_present(),
        "credentials_error": config.CREDENTIALS_ERROR,
        "stored_hours": conn.execute("SELECT COUNT(*) FROM reading").fetchone()[0],
        "coverage": db.coverage(conn),
        "local_date": jobs.local_today().isoformat(),
    }


@app.get("/jobs")
def job_status(conn: Conn) -> dict:
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


@app.get("/readings/hourly")
def read_hourly(
    conn: Conn,
    utility: Utility,
    start: date | None = None,
    end: date | None = None,
) -> dict:
    start, end = _range(conn, utility, start, end, max_days=HOURLY_MAX_DAYS, default_days=DEFAULT_DAYS)
    return {"utility": utility, "start": start, "end": end, "readings": db.hourly(conn, utility, start, end)}


@app.get("/readings/daily")
def read_daily(
    conn: Conn,
    utility: Utility,
    start: date | None = None,
    end: date | None = None,
) -> dict:
    start, end = _range(conn, utility, start, end, default_days=DEFAULT_DAYS)
    return {"utility": utility, "start": start, "end": end, "days": db.daily(conn, utility, start, end)}


@app.get("/readings/monthly")
def read_monthly(
    conn: Conn,
    utility: Utility,
    start: date | None = None,
    end: date | None = None,
) -> dict:
    start, end = _range(conn, utility, start, end)
    return {"utility": utility, "start": start, "end": end, "months": db.monthly(conn, utility, start, end)}


@app.get("/readings/yearly")
def read_yearly(
    conn: Conn,
    utility: Utility,
    start: date | None = None,
    end: date | None = None,
) -> dict:
    start, end = _range(conn, utility, start, end)
    return {"utility": utility, "start": start, "end": end, "years": db.yearly(conn, utility, start, end)}


@app.get("/summary")
def summary(conn: Conn) -> dict:
    today = jobs.local_today()
    week_start = today - timedelta(days=(today.weekday() + 1) % 7)
    out: dict[str, dict] = {}
    for utility in config.UTILITIES:
        out[utility] = {
            "latest_hour": db.latest_hour(conn, utility),
            "today": db.total(conn, utility, today, today),
            "yesterday": db.total(conn, utility, today - timedelta(days=1), today - timedelta(days=1)),
            "this_week": db.total(conn, utility, week_start, today),
            "last_full_week": db.total(conn, utility, *jobs.JOBS["last_full_week"].covers(today, conn)),
            "year_to_date": db.total(conn, utility, date(today.year, 1, 1), today),
            # Whole stored history, one row per year, for a per-year Home Assistant sensor.
            "by_year": db.yearly(conn, utility, _first_stored(conn, utility) or today, today),
        }
    return {"local_date": today.isoformat(), "utilities": out}


@app.post("/refresh/{job}")
def refresh(conn: Conn, job: str) -> dict:
    """Force one job to run now, for testing a freshly implemented source adapter."""
    if job not in jobs.JOBS:
        raise HTTPException(404, f"unknown job: {job}")
    rows = jobs.run_job(conn, job)
    return {"job": job, "rows_written": rows, **db.job_states(conn).get(job, {})}


@app.get("/")
def index() -> dict:
    return {
        "docs": "/docs",
        "endpoints": [
            "/health",
            "/jobs",
            "/summary",
            "/readings/hourly",
            "/readings/daily",
            "/readings/monthly",
            "/readings/yearly",
        ],
    }
