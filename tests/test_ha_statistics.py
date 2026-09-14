"""Offline self-checks for Home Assistant external statistics rows."""

from __future__ import annotations

import sys
import tempfile
import time
from contextlib import contextmanager
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from consumption import db  # noqa: E402
from consumption.ha_statistics import (  # noqa: E402
    CHUNK_SIZE,
    FULL_SYNC_KEY,
    REFRESH_HOURS,
    SERIES,
    build_hourly_rows,
    chunk_rows,
    metadata_for,
    refresh_since,
)
from consumption.records import MeterReading  # noqa: E402

UTC = timezone.utc
STAT_ID = "consumptionmonitor:water"


@contextmanager
def _conn():
    with tempfile.TemporaryDirectory() as tmp:
        conn = db.connect(Path(tmp) / "t.sqlite")
        try:
            yield conn
        finally:
            conn.close()


def _water(meter_data_id: int, when: datetime, local: date, total: float) -> MeterReading:
    return MeterReading(
        meter_data_id=meter_data_id,
        meter_id="m-w1",
        utility="water",
        reading_time=when,
        local_date=local,
        total_water_data=total,
    )


def test_metadata_contract() -> None:
    meta = metadata_for("consumptionmonitor:water")
    assert meta["has_sum"] is True
    assert meta["mean_type"] == 0
    assert meta["source"] == "consumptionmonitor"
    assert meta["unit_of_measurement"] == "m³"
    assert meta["unit_class"] == "volume"
    assert meta["statistic_id"] == "consumptionmonitor:water"


def test_hourly_rows_cumulative_sum() -> None:
    day = date(2026, 6, 15)
    with _conn() as conn:
        db.upsert_meter_readings(
            conn,
            [
                _water(1, datetime(2026, 6, 15, 6, tzinfo=UTC), day, 0.0),
                _water(2, datetime(2026, 6, 15, 9, tzinfo=UTC), day, 9.0),
            ],
        )
        rows = build_hourly_rows(conn, STAT_ID)
    assert rows
    assert rows[0]["sum"] == rows[0]["state"] or rows[0]["sum"] > 0
    total = sum(
        rows[i]["sum"] - (rows[i - 1]["sum"] if i else 0.0) for i in range(len(rows))
    )
    assert abs(total - 9.0) < 0.05
    assert all(row["start"].endswith("+00:00") for row in rows)


def test_partial_refresh_filters_rows() -> None:
    day = date(2026, 6, 15)
    with _conn() as conn:
        db.upsert_meter_readings(
            conn,
            [
                _water(1, datetime(2026, 6, 15, 6, tzinfo=UTC), day, 0.0),
                _water(2, datetime(2026, 6, 15, 9, tzinfo=UTC), day, 9.0),
            ],
        )
        full = build_hourly_rows(conn, STAT_ID)
        since = datetime(2026, 6, 15, 8, 0, tzinfo=UTC)
        partial = build_hourly_rows(conn, STAT_ID, since_utc=since)
    assert len(partial) < len(full)
    if partial:
        assert partial[-1]["sum"] == full[-1]["sum"]


def test_refresh_since_full_then_partial() -> None:
    now = datetime(2026, 6, 15, 12, tzinfo=UTC)
    with _conn() as conn:
        assert refresh_since(conn, now) is None
        db.set_state(conn, FULL_SYNC_KEY, "1")
        since = refresh_since(conn, now)
    assert since == now - timedelta(hours=REFRESH_HOURS)


def test_chunk_rows() -> None:
    rows = [{"start": f"2026-01-01T{i:02d}:00:00+00:00", "sum": i} for i in range(5)]
    chunks = chunk_rows(rows, size=2)
    assert chunks == [rows[0:2], rows[2:4], rows[4:5]]
    assert CHUNK_SIZE == 2000


def test_all_series_defined() -> None:
    assert set(SERIES) == {"consumptionmonitor:water"}


def test_two_year_history_builds_quickly_with_monotonic_sum() -> None:
    """Regression: full-history rebuild must not rescan every reading per hour."""
    start = date(2024, 1, 1)
    end = date(2025, 12, 31)
    readings: list[MeterReading] = []
    meter_data_id = 1
    total = 0.0
    day = start
    while day <= end:
        for hour in (6, 12, 18):
            total += 1.5
            readings.append(
                _water(
                    meter_data_id,
                    datetime(day.year, day.month, day.day, hour, tzinfo=UTC),
                    day,
                    total,
                )
            )
            meter_data_id += 1
        day += timedelta(days=1)

    with _conn() as conn:
        db.upsert_meter_readings(conn, readings)
        started = time.perf_counter()
        rows = build_hourly_rows(conn, STAT_ID)
        elapsed = time.perf_counter() - started

    assert elapsed < 2.0, f"build_hourly_rows took {elapsed:.2f}s"
    assert rows
    sums = [row["sum"] for row in rows]
    assert all(sums[i] <= sums[i + 1] for i in range(len(sums) - 1))
    assert sums[-1] > 0


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
        print(f"  ok  {test.__name__}")
    print(f"{len(tests)} ha_statistics self-checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
