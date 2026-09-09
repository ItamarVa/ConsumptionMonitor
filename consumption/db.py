"""SQLite storage for hourly consumption plus the scheduler's job bookkeeping.

The hour is the only granularity ever stored; daily, weekly and year-to-date figures are
SUM queries over the same rows, so a re-fetch can correct history without touching
derived tables. `local_date` is denormalised from `hour_utc` at write time so day
grouping needs no timezone math in SQL.
Invariant: one row per (utility, meter_id, hour_utc); writing the same hour again
overwrites it. Depended on by: jobs.py (writes), api.py (reads).
"""

from __future__ import annotations

import sqlite3
from collections.abc import Iterable
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from . import config
from .source import Reading

SCHEMA = """
CREATE TABLE IF NOT EXISTS reading (
    utility    TEXT NOT NULL,
    meter_id   TEXT NOT NULL,
    hour_utc   TEXT NOT NULL,   -- 'YYYY-MM-DDTHH:00:00Z'
    local_date TEXT NOT NULL,   -- 'YYYY-MM-DD' in config.LOCAL_TZ
    value      REAL NOT NULL,
    unit       TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (utility, meter_id, hour_utc)
) WITHOUT ROWID;

CREATE INDEX IF NOT EXISTS reading_by_local_date ON reading (utility, local_date);

CREATE TABLE IF NOT EXISTS job_state (
    job          TEXT PRIMARY KEY,
    last_run_utc TEXT,
    last_ok_utc  TEXT,
    rows_written INTEGER NOT NULL DEFAULT 0,
    last_error   TEXT
) WITHOUT ROWID;
"""


def connect(path: Path | None = None) -> sqlite3.Connection:
    target = path or config.DB_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(target, timeout=30)
    conn.row_factory = sqlite3.Row
    # WAL lets the API read while the scheduler writes.
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.executescript(SCHEMA)
    return conn


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def upsert_readings(conn: sqlite3.Connection, readings: Iterable[Reading]) -> int:
    now = _utc_now()
    rows = []
    for r in readings:
        if r.hour_start.tzinfo is None:
            raise ValueError(f"naive hour_start for {r.utility} {r.meter_id}")
        hour = r.hour_start.astimezone(timezone.utc).replace(minute=0, second=0, microsecond=0)
        rows.append(
            (
                r.utility,
                r.meter_id,
                hour.strftime("%Y-%m-%dT%H:00:00Z"),
                hour.astimezone(config.LOCAL_TZ).date().isoformat(),
                float(r.value),
                r.unit,
                now,
            )
        )
    with conn:
        conn.executemany(
            """
            INSERT INTO reading (utility, meter_id, hour_utc, local_date, value, unit, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (utility, meter_id, hour_utc) DO UPDATE SET
                value = excluded.value,
                unit = excluded.unit,
                local_date = excluded.local_date,
                updated_at = excluded.updated_at
            """,
            rows,
        )
    return len(rows)


def hourly(conn: sqlite3.Connection, utility: str, start: date, end: date) -> list[dict]:
    cur = conn.execute(
        """
        SELECT hour_utc, local_date, meter_id, value, unit
        FROM reading
        WHERE utility = ? AND local_date BETWEEN ? AND ?
        ORDER BY hour_utc, meter_id
        """,
        (utility, start.isoformat(), end.isoformat()),
    )
    return [dict(row) for row in cur]


def daily(conn: sqlite3.Connection, utility: str, start: date, end: date) -> list[dict]:
    cur = conn.execute(
        """
        SELECT local_date AS date, ROUND(SUM(value), 4) AS value, MIN(unit) AS unit,
               COUNT(*) AS hours
        FROM reading
        WHERE utility = ? AND local_date BETWEEN ? AND ?
        GROUP BY local_date
        ORDER BY local_date
        """,
        (utility, start.isoformat(), end.isoformat()),
    )
    return [dict(row) for row in cur]


def total(conn: sqlite3.Connection, utility: str, start: date, end: date) -> dict:
    row = conn.execute(
        """
        SELECT ROUND(SUM(value), 4) AS value, MIN(unit) AS unit, COUNT(*) AS hours
        FROM reading
        WHERE utility = ? AND local_date BETWEEN ? AND ?
        """,
        (utility, start.isoformat(), end.isoformat()),
    ).fetchone()
    return {"value": row["value"], "unit": row["unit"], "hours": row["hours"]}


def latest_hour(conn: sqlite3.Connection, utility: str) -> dict | None:
    row = conn.execute(
        """
        SELECT hour_utc, ROUND(SUM(value), 4) AS value, MIN(unit) AS unit
        FROM reading WHERE utility = ?
        GROUP BY hour_utc ORDER BY hour_utc DESC LIMIT 1
        """,
        (utility,),
    ).fetchone()
    return dict(row) if row else None


def record_job(
    conn: sqlite3.Connection,
    job: str,
    *,
    rows_written: int = 0,
    error: str | None = None,
) -> None:
    now = _utc_now()
    with conn:
        conn.execute(
            """
            INSERT INTO job_state (job, last_run_utc, last_ok_utc, rows_written, last_error)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT (job) DO UPDATE SET
                last_run_utc = excluded.last_run_utc,
                last_ok_utc = COALESCE(excluded.last_ok_utc, job_state.last_ok_utc),
                rows_written = excluded.rows_written,
                last_error = excluded.last_error
            """,
            (job, now, None if error else now, rows_written, error),
        )


def job_states(conn: sqlite3.Connection) -> dict[str, dict]:
    cur = conn.execute("SELECT * FROM job_state")
    return {row["job"]: dict(row) for row in cur}


def due(state: dict | None, interval: timedelta, now: datetime) -> bool:
    """A job with no recorded run is always due, so a restart catches up on missed work."""
    last = (state or {}).get("last_run_utc")
    if not last:
        return True
    return now - datetime.strptime(last, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc
    ) >= interval
