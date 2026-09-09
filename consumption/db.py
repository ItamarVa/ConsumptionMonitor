"""SQLite storage for raw meter readings plus the scheduler's job bookkeeping.

Each row is one portal reading keyed on meter_data_id; aggregates are exact deltas on
cumulative registers, never interpolated. `local_date` is denormalised at write time so
day/month/year grouping needs no timezone math in SQL.
Invariant: one row per meter_data_id; re-fetch overwrites in place. Depended on by:
jobs.py (writes), api.py (reads).
"""

from __future__ import annotations

import sqlite3
from collections.abc import Iterable
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from . import config
from .records import SCHEMA, UNITS, MeterReading

_METER_READING_COLS = (
    "meter_data_id",
    "meter_id",
    "utility",
    "reading_time_utc",
    "local_date",
    "total_import_kwh",
    "total_export_kwh",
    "tou1_import_kwh",
    "tou2_import_kwh",
    "tou3_import_kwh",
    "tou1_export_kwh",
    "tou2_export_kwh",
    "tou3_export_kwh",
    "total_water_data",
    "total_consumption",
    "total_production",
    "consumption1",
    "consumption2",
    "consumption3",
    "production1",
    "production3",
    "v1",
    "v2",
    "v3",
    "a1",
    "a2",
    "a3",
    "cos",
    "kvar_h",
    "max_dmd",
    "has_leak",
    "back_flow",
    "broken_pipe",
    "empty_pipe",
    "low_battery",
    "magnetic_tamper",
    "meter_error",
    "multiplier_symbol_count",
    "added_manually",
    "raw_json",
    "updated_at",
)

_BOOL_COLS = frozenset(
    {
        "has_leak",
        "back_flow",
        "broken_pipe",
        "empty_pipe",
        "low_battery",
        "magnetic_tamper",
        "meter_error",
        "added_manually",
    }
)

_ELECTRICITY_INTERVAL_FIELDS: dict[str, tuple[str, ...]] = {
    "import": (
        "total_import_kwh",
        "tou1_import_kwh",
        "tou2_import_kwh",
        "tou3_import_kwh",
    ),
    "export": (
        "total_export_kwh",
        "tou1_export_kwh",
        "tou2_export_kwh",
        "tou3_export_kwh",
    ),
}

_TARIFF_BANDS = (None, 1, 2, 3)


def connect(path: Path | None = None) -> sqlite3.Connection:
    target = path or config.DB_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(target, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("DROP TABLE IF EXISTS reading")
    conn.executescript(SCHEMA)
    return conn


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _require_aware(dt: datetime, label: str) -> datetime:
    if dt.tzinfo is None:
        raise ValueError(f"naive {label}")
    return dt


def _to_utc_str(dt: datetime) -> str:
    return _require_aware(dt, "reading_time").astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _local_midnight(d: date) -> datetime:
    return datetime(d.year, d.month, d.day, tzinfo=config.LOCAL_TZ)


def _reading_to_row(r: MeterReading, updated_at: str) -> tuple:
    rt = _require_aware(r.reading_time, f"reading_time for {r.meter_data_id}")
    return (
        r.meter_data_id,
        r.meter_id,
        r.utility,
        _to_utc_str(rt),
        r.local_date.isoformat(),
        r.total_import_kwh,
        r.total_export_kwh,
        r.tou1_import_kwh,
        r.tou2_import_kwh,
        r.tou3_import_kwh,
        r.tou1_export_kwh,
        r.tou2_export_kwh,
        r.tou3_export_kwh,
        r.total_water_data,
        r.total_consumption,
        r.total_production,
        r.consumption1,
        r.consumption2,
        r.consumption3,
        r.production1,
        r.production3,
        r.v1,
        r.v2,
        r.v3,
        r.a1,
        r.a2,
        r.a3,
        r.cos,
        r.kvar_h,
        r.max_dmd,
        int(r.has_leak),
        int(r.back_flow),
        int(r.broken_pipe),
        int(r.empty_pipe),
        int(r.low_battery),
        int(r.magnetic_tamper),
        int(r.meter_error),
        r.multiplier_symbol_count,
        int(r.added_manually),
        r.raw_json,
        updated_at,
    )


def _row_to_dict(row: sqlite3.Row) -> dict:
    out = dict(row)
    for key in _BOOL_COLS:
        if key in out:
            out[key] = bool(out[key])
    return out


def upsert_meter_readings(conn: sqlite3.Connection, readings: Iterable[MeterReading]) -> int:
    now = _utc_now()
    rows = [_reading_to_row(r, now) for r in readings]
    if not rows:
        return 0
    placeholders = ", ".join("?" for _ in _METER_READING_COLS)
    updates = ", ".join(f"{c} = excluded.{c}" for c in _METER_READING_COLS if c != "meter_data_id")
    with conn:
        conn.executemany(
            f"""
            INSERT INTO meter_reading ({", ".join(_METER_READING_COLS)})
            VALUES ({placeholders})
            ON CONFLICT (meter_data_id) DO UPDATE SET {updates}
            """,
            rows,
        )
    return len(rows)


def meter_readings(
    conn: sqlite3.Connection, meter_id: str, start: date, end: date
) -> list[dict]:
    cur = conn.execute(
        """
        SELECT * FROM meter_reading
        WHERE meter_id = ? AND local_date BETWEEN ? AND ?
        ORDER BY reading_time_utc
        """,
        (meter_id, start.isoformat(), end.isoformat()),
    )
    return [_row_to_dict(row) for row in cur]


def _fetch_readings_for_meter(
    conn: sqlite3.Connection, meter_id: str, start: date, end: date, *, include_prior: bool
) -> list[sqlite3.Row]:
    if include_prior:
        prior = conn.execute(
            """
            SELECT * FROM meter_reading
            WHERE meter_id = ? AND local_date < ?
            ORDER BY reading_time_utc DESC LIMIT 1
            """,
            (meter_id, start.isoformat()),
        ).fetchone()
        cur = conn.execute(
            """
            SELECT * FROM meter_reading
            WHERE meter_id = ? AND local_date BETWEEN ? AND ?
            ORDER BY reading_time_utc
            """,
            (meter_id, start.isoformat(), end.isoformat()),
        )
        rows = list(cur)
        if prior is not None:
            return [prior, *rows]
        return rows
    cur = conn.execute(
        """
        SELECT * FROM meter_reading
        WHERE meter_id = ? AND local_date BETWEEN ? AND ?
        ORDER BY reading_time_utc
        """,
        (meter_id, start.isoformat(), end.isoformat()),
    )
    return list(cur)


def _register_value(row: sqlite3.Row, field: str) -> float | None:
    value = row[field]
    return float(value) if value is not None else None


def _interval_dict(
    row_a: sqlite3.Row,
    row_b: sqlite3.Row,
    direction: str,
    field: str,
    tariff_band: int | None,
) -> dict | None:
    start_val = _register_value(row_a, field)
    end_val = _register_value(row_b, field)
    if start_val is None or end_val is None:
        return None
    utility = row_a["utility"]
    unit_key = (utility, direction)
    return {
        "meter_id": row_a["meter_id"],
        "utility": utility,
        "direction": direction,
        "start_time_utc": row_a["reading_time_utc"],
        "end_time_utc": row_b["reading_time_utc"],
        "value": round(end_val - start_val, 6),
        "unit": UNITS[unit_key],
        "tariff_band": tariff_band,
    }


def intervals(
    conn: sqlite3.Connection, meter_id: str, direction: str, start: date, end: date
) -> list[dict]:
    rows = _fetch_readings_for_meter(conn, meter_id, start, end, include_prior=True)
    if len(rows) < 2:
        return []

    out: list[dict] = []
    for prev, curr in zip(rows, rows[1:]):
        end_local = date.fromisoformat(curr["local_date"])
        if end_local < start or end_local > end:
            continue
        if direction == "water":
            item = _interval_dict(prev, curr, direction, "total_water_data", None)
            if item is not None:
                out.append(item)
            continue
        for field, band in zip(_ELECTRICITY_INTERVAL_FIELDS[direction], _TARIFF_BANDS):
            item = _interval_dict(prev, curr, direction, field, band)
            if item is not None:
                out.append(item)
    return out


def _meter_ids(conn: sqlite3.Connection, utility: str) -> list[str]:
    cur = conn.execute(
        "SELECT DISTINCT meter_id FROM meter_reading WHERE utility = ? ORDER BY meter_id",
        (utility,),
    )
    return [row["meter_id"] for row in cur]


def _register_field(utility: str, direction: str) -> str:
    if utility == "water":
        return "total_water_data"
    if direction == "import":
        return "total_import_kwh"
    if direction == "export":
        return "total_export_kwh"
    raise ValueError(f"unknown utility/direction: {utility}/{direction}")


def _first_reading_on_or_after(conn: sqlite3.Connection, meter_id: str, boundary: datetime) -> sqlite3.Row | None:
    return conn.execute(
        """
        SELECT * FROM meter_reading
        WHERE meter_id = ? AND reading_time_utc >= ?
        ORDER BY reading_time_utc LIMIT 1
        """,
        (meter_id, _to_utc_str(boundary)),
    ).fetchone()


def _period_delta(
    conn: sqlite3.Connection,
    meter_id: str,
    utility: str,
    direction: str,
    period_start: datetime,
    period_end: datetime,
) -> tuple[float | None, str | None]:
    """Return (value, first_reading_time_utc) for one meter and one period boundary pair."""
    start_row = _first_reading_on_or_after(conn, meter_id, period_start)
    end_row = _first_reading_on_or_after(conn, meter_id, period_end)
    if start_row is None or end_row is None:
        return None, None
    if start_row["reading_time_utc"] >= end_row["reading_time_utc"]:
        return None, None
    field = _register_field(utility, direction)
    start_val = _register_value(start_row, field)
    end_val = _register_value(end_row, field)
    if start_val is None or end_val is None:
        return None, None
    return round(end_val - start_val, 6), start_row["reading_time_utc"]


def _sum_period(
    conn: sqlite3.Connection,
    utility: str,
    direction: str,
    period_start: datetime,
    period_end: datetime,
) -> dict | None:
    meters = _meter_ids(conn, utility)
    if not meters:
        return None
    total = 0.0
    first_times: list[str] = []
    for meter_id in meters:
        value, first_time = _period_delta(conn, meter_id, utility, direction, period_start, period_end)
        if value is not None and first_time is not None:
            total += value
            first_times.append(first_time)
    if not first_times:
        return None
    return {
        "value": round(total, 6),
        "unit": UNITS[(utility, direction)],
        "first_reading_time": min(first_times),
    }


def daily_totals(
    conn: sqlite3.Connection, utility: str, direction: str, start: date, end: date
) -> list[dict]:
    out: list[dict] = []
    day = start
    while day <= end:
        row = _sum_period(
            conn,
            utility,
            direction,
            _local_midnight(day),
            _local_midnight(day + timedelta(days=1)),
        )
        if row:
            out.append({"date": day.isoformat(), **row})
        day += timedelta(days=1)
    return out


def monthly_totals(
    conn: sqlite3.Connection, utility: str, direction: str, start: date, end: date
) -> list[dict]:
    out: list[dict] = []
    month = date(start.year, start.month, 1)
    last = date(end.year, end.month, 1)
    while month <= last:
        if month.month == 12:
            next_month = date(month.year + 1, 1, 1)
        else:
            next_month = date(month.year, month.month + 1, 1)
        row = _sum_period(
            conn,
            utility,
            direction,
            _local_midnight(month),
            _local_midnight(next_month),
        )
        if row:
            out.append({"month": f"{month.year:04d}-{month.month:02d}", **row})
        month = next_month
    return out


def yearly_totals(
    conn: sqlite3.Connection, utility: str, direction: str, start: date, end: date
) -> list[dict]:
    out: list[dict] = []
    year = start.year
    while year <= end.year:
        row = _sum_period(
            conn,
            utility,
            direction,
            _local_midnight(date(year, 1, 1)),
            _local_midnight(date(year + 1, 1, 1)),
        )
        if row:
            out.append({"year": f"{year:04d}", **row})
        year += 1
    return out


def latest_reading(conn: sqlite3.Connection, meter_id: str) -> dict | None:
    row = conn.execute(
        """
        SELECT * FROM meter_reading
        WHERE meter_id = ?
        ORDER BY reading_time_utc DESC LIMIT 1
        """,
        (meter_id,),
    ).fetchone()
    return _row_to_dict(row) if row else None


def alert_flags(conn: sqlite3.Connection, meter_id: str) -> dict:
    row = conn.execute(
        """
        SELECT has_leak, back_flow, broken_pipe, empty_pipe, low_battery,
               magnetic_tamper, meter_error
        FROM meter_reading
        WHERE meter_id = ?
        ORDER BY reading_time_utc DESC LIMIT 1
        """,
        (meter_id,),
    ).fetchone()
    if row is None:
        return {
            "has_leak": False,
            "back_flow": False,
            "broken_pipe": False,
            "empty_pipe": False,
            "low_battery": False,
            "magnetic_tamper": False,
            "meter_error": False,
        }
    return {key: bool(row[key]) for key in row.keys()}


def coverage(conn: sqlite3.Connection) -> dict[str, dict]:
    out = {
        u: {"first_date": None, "last_date": None, "reading_count": 0}
        for u in config.UTILITIES
    }
    cur = conn.execute(
        """
        SELECT utility, MIN(local_date) AS first_date, MAX(local_date) AS last_date,
               COUNT(*) AS reading_count
        FROM meter_reading GROUP BY utility
        """
    )
    for row in cur:
        out[row["utility"]] = {
            "first_date": row["first_date"],
            "last_date": row["last_date"],
            "reading_count": row["reading_count"],
        }
    return out


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


def get_state(conn: sqlite3.Connection, key: str) -> str | None:
    row = conn.execute("SELECT value FROM app_state WHERE key = ?", (key,)).fetchone()
    return row["value"] if row else None


def set_state(conn: sqlite3.Connection, key: str, value: str) -> None:
    with conn:
        conn.execute(
            "INSERT INTO app_state (key, value) VALUES (?, ?) "
            "ON CONFLICT (key) DO UPDATE SET value = excluded.value",
            (key, value),
        )


def due(state: dict | None, interval: timedelta, now: datetime) -> bool:
    last = (state or {}).get("last_run_utc")
    if not last:
        return True
    return now - datetime.strptime(last, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc
    ) >= interval
