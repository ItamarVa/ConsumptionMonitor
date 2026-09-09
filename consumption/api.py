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

MAX_RANGE_DAYS = 731  # two years per request, so one call cannot read the whole DB

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


def _range(start: date | None, end: date | None) -> tuple[date, date]:
    """Default to the last 7 local days and reject anything unbounded or backwards."""
    today = jobs.local_today()
    end = end or today
    start = start or end - timedelta(days=6)
    if start > end:
        raise HTTPException(422, "start must not be after end")
    if (end - start).days + 1 > MAX_RANGE_DAYS:
        raise HTTPException(422, f"range must not exceed {MAX_RANGE_DAYS} days")
    return start, end


@app.get("/health")
def health(conn: Conn) -> dict:
    return {
        "status": "ok",
        "source_ready": source.SOURCE_READY,
        "credentials_present": config.credentials_present(),
        "stored_hours": conn.execute("SELECT COUNT(*) FROM reading").fetchone()[0],
        "local_date": jobs.local_today().isoformat(),
    }


@app.get("/jobs")
def job_status(conn: Conn) -> dict:
    states = db.job_states(conn)
    today = jobs.local_today()
    return {
        job: {
            "every": str(interval),
            "covers": {"start": rng(today)[0].isoformat(), "end": rng(today)[1].isoformat()},
            **states.get(job, {"last_run_utc": None, "last_ok_utc": None, "last_error": None}),
        }
        for job, (interval, rng) in jobs.JOBS.items()
    }


@app.get("/readings/hourly")
def read_hourly(
    conn: Conn,
    utility: Utility,
    start: date | None = None,
    end: date | None = None,
) -> dict:
    start, end = _range(start, end)
    return {"utility": utility, "start": start, "end": end, "readings": db.hourly(conn, utility, start, end)}


@app.get("/readings/daily")
def read_daily(
    conn: Conn,
    utility: Utility,
    start: date | None = None,
    end: date | None = None,
) -> dict:
    start, end = _range(start, end)
    return {"utility": utility, "start": start, "end": end, "days": db.daily(conn, utility, start, end)}


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
            "last_full_week": db.total(conn, utility, *jobs.JOBS["last_full_week"][1](today)),
            "year_to_date": db.total(conn, utility, date(today.year, 1, 1), today),
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
    return {"docs": "/docs", "endpoints": ["/health", "/jobs", "/summary", "/readings/hourly", "/readings/daily"]}
