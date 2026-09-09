"""Refresh schedule: which local date range each job re-fetches, and how often.

Every job re-fetches a whole range and overwrites it, so all four are idempotent and a
late correction from the portal eventually lands. Intervals are measured from the last
attempt stored in the DB rather than from process start, so closing the laptop overnight
makes the missed job due immediately instead of skipping it.
Depended on by: __main__.py (the loop) and api.py (job status).
"""

from __future__ import annotations

import asyncio
import sqlite3
import traceback
from collections.abc import Callable
from datetime import date, datetime, timedelta, timezone

from . import config, db, source

# Sunday-Saturday, matching the Israeli calendar the portal reports against.
_DAYS_SINCE_SUNDAY = lambda d: (d.weekday() + 1) % 7  # noqa: E731


def _today(today: date) -> tuple[date, date]:
    return today, today


def _yesterday(today: date) -> tuple[date, date]:
    day = today - timedelta(days=1)
    return day, day


def _last_full_week(today: date) -> tuple[date, date]:
    this_week_start = today - timedelta(days=_DAYS_SINCE_SUNDAY(today))
    return this_week_start - timedelta(days=7), this_week_start - timedelta(days=1)


def _year_to_date(today: date) -> tuple[date, date]:
    return date(today.year, 1, 1), today


# job name -> (how often it runs, local date range it re-fetches)
JOBS: dict[str, tuple[timedelta, Callable[[date], tuple[date, date]]]] = {
    "today": (timedelta(hours=1), _today),
    "yesterday": (timedelta(days=1), _yesterday),
    "last_full_week": (timedelta(days=7), _last_full_week),
    "year_to_date": (timedelta(days=30), _year_to_date),
}


def local_today(now: datetime | None = None) -> date:
    return (now or datetime.now(timezone.utc)).astimezone(config.LOCAL_TZ).date()


def run_job(conn: sqlite3.Connection, job: str, today: date | None = None) -> int:
    """Fetch and store one job's range for every utility. Returns rows written."""
    if job not in JOBS:
        raise ValueError(f"unknown job: {job!r}")
    start, end = JOBS[job][1](today or local_today())
    written = 0
    try:
        for utility in config.UTILITIES:
            written += db.upsert_readings(conn, source.fetch_hourly(utility, start, end))
    except Exception as exc:  # noqa: BLE001 - one bad job must not kill the loop
        detail = f"{type(exc).__name__}: {exc}"
        if not isinstance(exc, source.SourceNotReady):
            detail += "\n" + traceback.format_exc(limit=3)
        db.record_job(conn, job, rows_written=written, error=detail)
        return written
    db.record_job(conn, job, rows_written=written)
    return written


def run_due(now: datetime | None = None) -> list[str]:
    """Run every job whose interval has elapsed. Safe to call as often as you like."""
    moment = now or datetime.now(timezone.utc)
    conn = db.connect()
    try:
        states = db.job_states(conn)
        ran = [job for job, (interval, _) in JOBS.items() if db.due(states.get(job), interval, moment)]
        for job in ran:
            run_job(conn, job, local_today(moment))
        return ran
    finally:
        conn.close()


async def loop() -> None:
    """Tick forever, delegating the blocking fetch and SQLite work to a worker thread."""
    while True:
        try:
            await asyncio.to_thread(run_due)
        except Exception:  # noqa: BLE001 - the scheduler outlives any single failure
            traceback.print_exc()
        await asyncio.sleep(config.TICK_SECONDS)
