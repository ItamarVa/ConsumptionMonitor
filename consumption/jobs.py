"""Refresh schedule: which local date range each job re-fetches, how often, and when it applies.

Every job re-fetches a whole range and overwrites stored readings, so all of them are
idempotent and late corrections from the portal eventually land. Intervals are measured from
the last attempt stored in the DB rather than from process start. `previous_year` only runs
in January; `backfill` walks backwards one month at a time until 2024-01 or an empty month.
Depended on by: __main__.py (the loop) and api.py (job status).
"""

from __future__ import annotations

import asyncio
import sqlite3
import traceback
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone

from . import config, db, ha_bridge, source

Range = tuple[date, date]

# How far backfill walks: the next calendar month to request (YYYY-MM), or DONE once history
# ends. Stored in app_state so a restart resumes rather than starting over.
BACKFILL_KEY = "backfill_next_month"
BACKFILL_DONE = "done"
BACKFILL_EARLIEST = date(2024, 1, 1)


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


def _recent(today: date, conn: sqlite3.Connection) -> Range:
    return today - timedelta(days=1), today


def _recent_week(today: date, conn: sqlite3.Connection) -> Range:
    return today - timedelta(days=6), today


def _previous_year(today: date, conn: sqlite3.Connection) -> Range:
    year = today.year - 1
    return date(year, 1, 1), date(year, 12, 31)


def _in_january(today: date) -> bool:
    return today.month == 1


def _month_bounds(year: int, month: int) -> Range:
    start = date(year, month, 1)
    if month == 12:
        end = date(year, 12, 31)
    else:
        end = date(year, month + 1, 1) - timedelta(days=1)
    return start, end


def _prev_month(year: int, month: int) -> tuple[int, int]:
    if month == 1:
        return year - 1, 12
    return year, month - 1


def _backfill(today: date, conn: sqlite3.Connection) -> Range | None:
    """The next whole month to pull, walking backwards toward BACKFILL_EARLIEST."""
    progress = db.get_state(conn, BACKFILL_KEY)
    if progress == BACKFILL_DONE:
        return None
    if progress:
        year_s, month_s = progress.split("-", 1)
        year, month = int(year_s), int(month_s)
    else:
        stored = [c["first_date"] for c in db.coverage(conn).values() if c["first_date"]]
        if not stored:
            return None  # nothing stored yet — recent must land first
        earliest = date.fromisoformat(min(stored))
        year, month = _prev_month(earliest.year, earliest.month)
    if date(year, month, 1) < BACKFILL_EARLIEST.replace(day=1):
        return None
    return _month_bounds(year, month)


def _advance_backfill(conn: sqlite3.Connection, covered: Range, rows_written: int) -> None:
    """An empty month means the portal has no history left; stop asking for good."""
    if rows_written == 0:
        db.set_state(conn, BACKFILL_KEY, BACKFILL_DONE)
        return
    year, month = covered[0].year, covered[0].month
    prev_y, prev_m = _prev_month(year, month)
    if date(prev_y, prev_m, 1) < BACKFILL_EARLIEST.replace(day=1):
        db.set_state(conn, BACKFILL_KEY, BACKFILL_DONE)
    else:
        db.set_state(conn, BACKFILL_KEY, f"{prev_y:04d}-{prev_m:02d}")


JOBS: dict[str, Job] = {
    "recent": Job(timedelta(hours=1), _recent),
    "recent_week": Job(timedelta(days=1), _recent_week),
    # The portal keeps correcting last year until the end of January and not after it.
    "previous_year": Job(timedelta(days=1), _previous_year, in_season=_in_january),
    # One month per run: slow endpoint, but unattended history still lands in roughly a day.
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
            written += db.upsert_meter_readings(
                conn, source.fetch_readings(utility, start, end)
            )
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
        rows_written = 0
        for job, spec in JOBS.items():
            if not spec.in_season(today) or not db.due(states.get(job), spec.every, moment):
                continue
            if spec.covers(today, conn) is None:
                continue
            rows_written += run_job(conn, job, today)
            ran.append(job)
        ha_bridge.sync(conn, data_changed=rows_written > 0)
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
