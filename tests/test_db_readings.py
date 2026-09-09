"""Offline self-checks for raw meter reading storage and exact register deltas."""

from __future__ import annotations

import sys
import tempfile
from contextlib import contextmanager
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from consumption import db  # noqa: E402
from consumption.records import MeterReading  # noqa: E402

UTC = timezone.utc


@contextmanager
def _conn():
    with tempfile.TemporaryDirectory() as tmp:
        conn = db.connect(Path(tmp) / "t.sqlite")
        try:
            yield conn
        finally:
            conn.close()


def _elec(
    meter_data_id: int,
    when: datetime,
    local_date: date,
    *,
    total_import: float,
    tou1_import: float | None = None,
    total_export: float | None = None,
) -> MeterReading:
    return MeterReading(
        meter_data_id=meter_data_id,
        meter_id="30400",
        utility="electricity",
        reading_time=when,
        local_date=local_date,
        total_import_kwh=total_import,
        total_export_kwh=total_export,
        tou1_import_kwh=tou1_import,
    )


def test_upsert_idempotent_on_meter_data_id() -> None:
    with _conn() as conn:
        first = _elec(1, datetime(2026, 6, 1, 6, tzinfo=UTC), date(2026, 6, 1), total_import=100.0)
        second = _elec(1, datetime(2026, 6, 1, 6, tzinfo=UTC), date(2026, 6, 1), total_import=150.0)
        assert db.upsert_meter_readings(conn, [first]) == 1
        assert db.upsert_meter_readings(conn, [second]) == 1
        rows = db.meter_readings(conn, "30400", date(2026, 6, 1), date(2026, 6, 1))
        assert len(rows) == 1
        assert rows[0]["total_import_kwh"] == 150.0


def test_interval_delta_arithmetic() -> None:
    with _conn() as conn:
        readings = [
            _elec(
                1,
                datetime(2026, 6, 1, 6, tzinfo=UTC),
                date(2026, 6, 1),
                total_import=100.0,
                tou1_import=40.0,
                total_export=10.0,
            ),
            _elec(
                2,
                datetime(2026, 6, 1, 12, tzinfo=UTC),
                date(2026, 6, 1),
                total_import=106.5,
                tou1_import=43.0,
                total_export=10.5,
            ),
        ]
        db.upsert_meter_readings(conn, readings)
        import_iv = db.intervals(conn, "30400", "import", date(2026, 6, 1), date(2026, 6, 1))
        export_iv = db.intervals(conn, "30400", "export", date(2026, 6, 1), date(2026, 6, 1))
        total = next(i for i in import_iv if i["tariff_band"] is None)
        tou1 = next(i for i in import_iv if i["tariff_band"] == 1)
        export_total = next(i for i in export_iv if i["tariff_band"] is None)
        assert total == {
            "meter_id": "30400",
            "utility": "electricity",
            "direction": "import",
            "start_time_utc": "2026-06-01T06:00:00Z",
            "end_time_utc": "2026-06-01T12:00:00Z",
            "value": 6.5,
            "unit": "kWh",
            "tariff_band": None,
        }
        assert tou1["value"] == 3.0
        assert export_total["value"] == 0.5


def test_daily_total_uses_first_reading_after_midnight() -> None:
    with _conn() as conn:
        readings = [
            _elec(1, datetime(2026, 6, 1, 6, tzinfo=UTC), date(2026, 6, 1), total_import=100.0),
            _elec(2, datetime(2026, 6, 1, 15, tzinfo=UTC), date(2026, 6, 1), total_import=104.0),
            _elec(3, datetime(2026, 6, 2, 6, tzinfo=UTC), date(2026, 6, 2), total_import=110.0),
        ]
        db.upsert_meter_readings(conn, readings)
        days = db.daily_totals(conn, "electricity", "import", date(2026, 6, 1), date(2026, 6, 1))
        assert days == [
            {
                "date": "2026-06-01",
                "value": 10.0,
                "unit": "kWh",
                "first_reading_time": "2026-06-01T06:00:00Z",
            }
        ]


def test_upsert_replaces_reissued_id_at_same_timestamp() -> None:
    """Portal sometimes emits a new meter_data_id for an unchanged reading_time_utc."""
    ts = datetime(2026, 6, 1, 6, tzinfo=UTC)
    with _conn() as conn:
        first = _elec(1, ts, date(2026, 6, 1), total_import=100.0)
        second = _elec(99, ts, date(2026, 6, 1), total_import=150.0)
        assert db.upsert_meter_readings(conn, [first, second]) == 2
        rows = db.meter_readings(conn, "30400", date(2026, 6, 1), date(2026, 6, 1))
        assert len(rows) == 1
        assert rows[0]["meter_data_id"] == 99
        assert rows[0]["total_import_kwh"] == 150.0


def test_coverage_counts() -> None:
    with _conn() as conn:
        empty = db.coverage(conn)
        assert empty["electricity"] == {
            "first_date": None,
            "last_date": None,
            "reading_count": 0,
        }
        assert set(empty) == {"electricity", "water"}

        db.upsert_meter_readings(
            conn,
            [
                _elec(1, datetime(2024, 3, 10, 6, tzinfo=UTC), date(2024, 3, 10), total_import=1.0),
                _elec(2, datetime(2026, 1, 5, 6, tzinfo=UTC), date(2026, 1, 5), total_import=2.0),
            ],
        )
        cov = db.coverage(conn)
        assert cov["electricity"] == {
            "first_date": "2024-03-10",
            "last_date": "2026-01-05",
            "reading_count": 2,
        }
        assert cov["water"]["reading_count"] == 0


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
        print(f"  ok  {test.__name__}")
    print(f"{len(tests)} self-checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
