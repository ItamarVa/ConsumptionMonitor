"""Offline self-checks for proportional hourly register spreading."""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from consumption.hourly import spread_to_hours  # noqa: E402

TZ = ZoneInfo("Asia/Jerusalem")
FIELD = "total_import_kwh"


def _row(ts: str, value: float | None) -> dict:
    return {"reading_time_utc": ts, FIELD: value}


def _values(hours: list[dict]) -> list[float | None]:
    return [h["value"] for h in hours]


def test_three_hour_interval_splits_proportionally() -> None:
    day = date(2026, 6, 15)
    readings = [
        _row("2026-06-15T06:00:00Z", 0.0),
        _row("2026-06-15T09:00:00Z", 9.0),
    ]
    hours = spread_to_hours(readings, FIELD, day, TZ)
    assert len(hours) == 24
    by_hour = {h["hour"]: h for h in hours}
    assert by_hour["09:00"]["value"] == 3.0
    assert by_hour["10:00"]["value"] == 3.0
    assert by_hour["11:00"]["value"] == 3.0
    assert sum(h["value"] or 0 for h in hours) == 9.0


def test_interval_inside_one_hour() -> None:
    day = date(2026, 6, 15)
    readings = [
        _row("2026-06-15T07:15:00Z", 10.0),
        _row("2026-06-15T07:45:00Z", 12.5),
    ]
    hours = spread_to_hours(readings, FIELD, day, TZ)
    by_hour = {h["hour"]: h for h in hours}
    assert by_hour["10:00"]["value"] == 2.5
    assert by_hour["10:00"]["source_intervals"] == 1
    assert by_hour["09:00"]["value"] is None
    assert by_hour["11:00"]["value"] is None


def test_no_readings_returns_twenty_four_nulls() -> None:
    day = date(2026, 6, 15)
    hours = spread_to_hours([], FIELD, day, TZ)
    assert len(hours) == 24
    assert all(h["value"] is None for h in hours)
    assert all(h["source_intervals"] == 0 for h in hours)
    assert all(h["partial"] for h in hours)


def test_midnight_reading_not_double_counted() -> None:
    day_before = date(2026, 6, 15)
    day_after = date(2026, 6, 16)
    readings = [
        _row("2026-06-15T20:00:00Z", 100.0),
        _row("2026-06-15T21:00:00Z", 105.0),
    ]
    before = spread_to_hours(readings, FIELD, day_before, TZ)
    after = spread_to_hours(readings, FIELD, day_after, TZ)
    by_hour_before = {h["hour"]: h for h in before}
    assert by_hour_before["23:00"]["value"] == 5.0
    assert sum(h["value"] or 0 for h in after) == 0.0


def test_negative_delta_skipped() -> None:
    day = date(2026, 6, 15)
    readings = [
        _row("2026-06-15T06:00:00Z", 100.0),
        _row("2026-06-15T09:00:00Z", 95.0),
        _row("2026-06-15T10:00:00Z", 98.0),
    ]
    hours = spread_to_hours(readings, FIELD, day, TZ)
    by_hour = {h["hour"]: h for h in hours}
    assert by_hour["09:00"]["value"] is None
    assert by_hour["10:00"]["value"] is None
    assert by_hour["11:00"]["value"] is None
    assert by_hour["12:00"]["value"] == 3.0


def test_spring_forward_has_twenty_three_buckets() -> None:
    day = date(2026, 3, 27)
    hours = spread_to_hours([], FIELD, day, TZ)
    labels = [h["hour"] for h in hours]
    assert len(hours) == 23
    assert "02:00" not in labels


def test_fall_back_has_twenty_five_buckets() -> None:
    day = date(2026, 10, 25)
    hours = spread_to_hours([], FIELD, day, TZ)
    labels = [h["hour"] for h in hours]
    assert len(hours) == 25
    assert labels.count("01:00") == 2


def test_whole_day_total_within_rounding_tolerance() -> None:
    day = date(2026, 6, 15)
    readings = [
        _row("2026-06-14T21:00:00Z", 1000.0),
        _row("2026-06-15T21:00:00Z", 1024.6789),
    ]
    hours = spread_to_hours(readings, FIELD, day, TZ)
    bucket_sum = sum(h["value"] or 0 for h in hours)
    assert abs(bucket_sum - 24.6789) < 0.002


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
        print(f"  ok  {test.__name__}")
    print(f"{len(tests)} hourly self-checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
