"""Refresh schedule: which local date range each job re-fetches, how often, and when it applies.

Every job re-fetches a whole range and overwrites it, so all of them are idempotent and a
late correction from the portal eventually lands. Intervals are measured from the last
attempt stored in the DB rather than from process start, so closing the laptop overnight
makes the missed job due immediately instead of skipping it. Two jobs are not always
applicable: `previous_year` only in January, `backfill` only until the portal runs dry.
Depended on by: __main__.py (the loop) and api.py (job status).
"""

from __future__ import annotations

import asyncio
import sqlite3
import traceback
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone

from . import config, db, source

Range = tuple[date, date]

# Sunday-Saturday, matching the Israeli calendar the portal reports against.
_DAYS_SINCE_SUNDAY = lambda d: (d.weekday() + 1) % 7  # noqa: E731

# How far back the backfill has left to walk: the next calendar year to request, or DONE
# once a whole year came back empty. Stored in the DB so a restart resumes where it was.
BACKFILL_KEY = "backfill_next_year"
BACKFILL_DONE = "done"


def _always(today: date) -> bool:
    return True


@dataclass(frozen=True, slots=True)
class Job:
    """One scheduled refresh.

    `covers` takes the connection because the backfill's next range depends on progress
    stored in the DB; it returns None when the job has nothing left to fetch.
    """

    every: timedelta
    covers: Callable[[date, sqlite3.Connection], Range | None]
    in_season: Callable[[date], bool] = _always
    # Runs only after a successful fetch, so a failure can never be read as "no data".
    after: Callable[[sqlite3.Connection, Range, int], None] | None = None


def _today(today: date, conn: sqlite3.Connection) -> Range:
    return today, today


def _yesterday(today: date, conn: sqlite3.Connection) -> Range:
    day = today - timedelta(days=1)
    return day, day


def _last_full_week(today: date, conn: sqlite3.Connection) -> Range:
    this_week_start = today - timedelta(days=_DAYS_SINCE_SUNDAY(today))
    return this_week_start - timedelta(days=7), this_week_start - timedelta(days=1)


def _year_to_date(today: date, conn: sqlite3.Connection) -> Range:
    return date(today.year, 1, 1), today


def _previous_year(today: date, conn: sqlite3.Connection) -> Range:
    return date(today.year - 1, 1, 1), date(today.year - 1, 12, 31)


def _in_january(today: date) -> bool:
    return today.month == 1


def _backfill(today: date, conn: sqlite3.Connection) -> Range | None:
    """The next whole year to pull, walking backwards from the earliest year stored."""
    progress = db.get_state(conn, BACKFILL_KEY)
    if progress == BACKFILL_DONE:
        return None
    if progress:
        year = int(progress)
    else:
        stored = [c["first_date"] for c in db.coverage(conn).values() if c["first_date"]]
        if not stored:
            return None  # nothing stored yet - year_to_date has to land first
        year = int(min(stored)[:4]) - 1
    return date(year, 1, 1), date(year, 12, 31)


def _advance_backfill(conn: sqlite3.Connection, covered: Range, rows_written: int) -> None:
    """An empty year means the portal has no history left, so stop asking for good."""
    year = covered[0].year
    db.set_state(conn, BACKFILL_KEY, BACKFILL_DONE if rows_written == 0 else str(year - 1))


JOBS: dict[str, Job] = {
    "today": Job(timedelta(hours=1), _today),
    "yesterday": Job(timedelta(days=1), _yesterday),
    "last_full_week": Job(timedelta(days=7), _last_full_week),
    "year_to_date": Job(timedelta(days=30), _year_to_date),
    # The portal keeps correcting last year until the end of January and not after it.
    "previous_year": Job(timedelta(days=1), _previous_year, in_season=_in_january),
    # One year per run: nobody is waiting for it, and a decade still lands in a few days.
    "backfill": Job(timedelta(hours=6), _backfill, after=_advance_backfill),
}


def local_today(now: datetime | None = None) -> date:
    return (now or datetime.now(timezone.utc)).astimezone(config.LOCAL_TZ).date()


def run_job(conn: sqlite3.Connection, job: str, today: date | None = None) -> int:
    """Fetch and store one job's range for every utility. Returns rows written."""
    if job not in JOBS:
        raise ValueError(f"unknown job: {job!r}")
    spec = JOBS[job]
    covered = spec.covers(today or local_today(), conn)
    if covered is None:
        return 0
    start, end = covered
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
    if spec.after is not None:
        spec.after(conn, covered, written)
    return written


def run_due(now: datetime | None = None) -> list[str]:
    """Run every job that is in season and whose interval has elapsed."""
    moment = now or datetime.now(timezone.utc)
    today = local_today(moment)
    conn = db.connect()
    try:
        states = db.job_states(conn)
        ran = []
        for job, spec in JOBS.items():
            if not spec.in_season(today) or not db.due(states.get(job), spec.every, moment):
                continue
            if spec.covers(today, conn) is None:
                continue
            run_job(conn, job, today)
            ran.append(job)
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
