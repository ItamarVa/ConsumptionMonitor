"""Offline self-checks for the refresh schedule and job bookkeeping.

Uses a throwaway SQLite file and a stubbed fetch_readings, so nothing here touches the
portal or the user's credentials. Plain asserts so `python tests/test_jobs.py` works.
"""

from __future__ import annotations

import os
import sys
import tempfile
from contextlib import contextmanager
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from consumption import config, db, jobs, secrets, source  # noqa: E402
from consumption.records import MeterReading  # noqa: E402

UTC = timezone.utc


def _reading(
    meter_data_id: int,
    when: datetime,
    local: date,
    utility: str = "electricity",
    meter_id: str | None = None,
) -> MeterReading:
    if meter_id is None:
        meter_id = "m-e1" if utility == "electricity" else "m-w1"
    return MeterReading(
        meter_data_id=meter_data_id,
        meter_id=meter_id,
        utility=utility,
        reading_time=when,
        local_date=local,
        total_import_kwh=1.0 if utility == "electricity" else None,
        total_water_data=1.0 if utility == "water" else None,
    )


@contextmanager
def _conn():
    with tempfile.TemporaryDirectory() as tmp:
        conn = db.connect(Path(tmp) / "t.sqlite")
        try:
            yield conn
        finally:
            conn.close()


@contextmanager
def _fake_source(fake):
    original = source.fetch_readings
    source.fetch_readings = fake
    try:
        yield
    finally:
        source.fetch_readings = original


def _source_for_months(months: set[tuple[int, int]]):
    """Stand in for the portal: one reading per utility when start falls in those months."""

    def fake(utility: str, start: date, end: date) -> list[MeterReading]:
        key = (start.year, start.month)
        if key not in months:
            return []
        mid = 100 if utility == "electricity" else 200
        return [
            _reading(
                mid,
                datetime(start.year, start.month, 15, 6, tzinfo=UTC),
                date(start.year, start.month, 15),
                utility=utility,
            )
        ]

    return _fake_source(fake)


def _source_raising(exc: Exception):
    def fake(utility: str, start: date, end: date) -> list[MeterReading]:
        raise exc

    return _fake_source(fake)


def test_recent_covers_last_two_days() -> None:
    today = date(2026, 9, 9)
    with _conn() as conn:
        assert jobs.JOBS["recent"].covers(today, conn) == (date(2026, 9, 8), today)


def test_recent_week_covers_seven_days() -> None:
    today = date(2026, 9, 9)
    with _conn() as conn:
        assert jobs.JOBS["recent_week"].covers(today, conn) == (date(2026, 9, 3), today)


def test_previous_year_only_in_january() -> None:
    with _conn() as conn:
        spec = jobs.JOBS["previous_year"]
        assert spec.in_season(date(2026, 9, 9)) is False
        assert spec.in_season(date(2026, 1, 15)) is True
        assert spec.covers(date(2026, 1, 15), conn) == (date(2025, 1, 1), date(2025, 12, 31))


def test_due() -> None:
    now = datetime(2026, 9, 9, 12, tzinfo=UTC)
    assert db.due(None, timedelta(hours=1), now) is True
    assert db.due({"last_run_utc": "2026-09-09T11:30:00Z"}, timedelta(hours=1), now) is False
    assert db.due({"last_run_utc": "2026-09-09T11:00:00Z"}, timedelta(hours=1), now) is True


def test_missing_source_is_recorded_not_raised() -> None:
    unusable = source.SourceNotReady("No mycitygrid credentials stored.")
    with tempfile.TemporaryDirectory() as tmp, _source_raising(unusable):
        conn = db.connect(Path(tmp) / "t.sqlite")
        assert jobs.run_job(conn, "recent", date(2026, 9, 9)) == 0
        state = db.job_states(conn)["recent"]
        assert state["last_ok_utc"] is None
        assert "SourceNotReady" in state["last_error"]
        conn.close()


def test_scheduler_skips_out_of_season_jobs() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        original = config.DB_PATH
        config.DB_PATH = Path(tmp) / "t.sqlite"
        try:
            with _source_for_months(set()):
                september = jobs.run_due(datetime(2026, 9, 9, 9, tzinfo=UTC))
                january = jobs.run_due(datetime(2026, 1, 15, 9, tzinfo=UTC))
        finally:
            config.DB_PATH = original
    assert "previous_year" not in september
    assert "previous_year" in january
    assert "backfill" not in september, "an empty database gives backfill no starting month"


def test_backfill_walks_back_by_month_then_stops() -> None:
    with _conn() as conn, _source_for_months({(2026, 5), (2024, 1)}):
        today = date(2026, 9, 9)
        spec = jobs.JOBS["backfill"]
        assert spec.covers(today, conn) is None

        db.upsert_meter_readings(
            conn,
            [_reading(1, datetime(2026, 6, 1, 6, tzinfo=UTC), date(2026, 6, 1))],
        )
        assert spec.covers(today, conn) == (date(2026, 5, 1), date(2026, 5, 31))
        assert jobs.run_job(conn, "backfill", today) == 2

        assert spec.covers(today, conn) == (date(2026, 4, 1), date(2026, 4, 30))
        assert jobs.run_job(conn, "backfill", today) == 0
        assert db.get_state(conn, jobs.BACKFILL_KEY) == jobs.BACKFILL_DONE
        assert spec.covers(today, conn) is None


def test_backfill_survives_a_failed_fetch() -> None:
    failure = source.SourceError("the portal answered 503")
    with _conn() as conn, _source_raising(failure):
        today = date(2026, 9, 9)
        db.upsert_meter_readings(
            conn,
            [_reading(1, datetime(2026, 6, 1, 6, tzinfo=UTC), date(2026, 6, 1))],
        )
        assert jobs.run_job(conn, "backfill", today) == 0
        assert db.get_state(conn, jobs.BACKFILL_KEY) is None
        assert jobs.JOBS["backfill"].covers(today, conn) == (date(2026, 5, 1), date(2026, 5, 31))


def test_encrypted_credentials_round_trip() -> None:
    if os.name != "nt":
        print("  skip  test_encrypted_credentials_round_trip (Windows only)")
        return
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "credentials.dpapi"
        assert secrets.load(path) is None

        secrets.save("user@example.com", "pa ss:word", path)
        assert b"pa ss:word" not in path.read_bytes()
        assert secrets.load(path) == ("user@example.com", "pa ss:word")

        path.write_bytes(b"this is not a DPAPI blob")
        try:
            secrets.load(path)
        except secrets.SecretsError as exc:
            assert "set-credentials.bat" in str(exc)
        else:
            raise AssertionError("a foreign blob should have raised SecretsError")

        secrets.clear(path)
        assert secrets.load(path) is None


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
        print(f"  ok  {test.__name__}")
    print(f"{len(tests)} job schedule self-checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
