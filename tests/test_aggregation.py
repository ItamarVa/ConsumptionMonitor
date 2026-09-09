"""Self-check for the things in this project that are easy to get silently wrong:
UTC-to-local day mapping, the range and season of each scheduled job, the backfill's
walk backwards, the aggregation queries, and the encrypted credential store.

Runs against a throwaway SQLite file and a temporary credential file, so it never touches
the real database or the user's stored credentials. Needs no network. This is what
run.bat executes before starting the API. Plain asserts so `python tests/test_aggregation.py`
and `pytest` both work.
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
from consumption.source import Reading  # noqa: E402

UTC = timezone.utc


def _reading(hour_utc: datetime, value: float) -> Reading:
    return Reading("electricity", "meter-1", hour_utc, value, "kWh")


@contextmanager
def _conn():
    with tempfile.TemporaryDirectory() as tmp:
        conn = db.connect(Path(tmp) / "t.sqlite")
        try:
            yield conn
        finally:
            conn.close()


@contextmanager
def _source_with_years(years: set[int]):
    """Stand in for the unimplemented portal: one reading per utility for those years."""
    original = source.fetch_hourly

    def fake(utility: str, start: date, end: date) -> list[Reading]:
        if start.year not in years:
            return []
        return [Reading(utility, "m1", datetime(start.year, 6, 1, 6, tzinfo=UTC), 1.0, "kWh")]

    source.fetch_hourly = fake
    try:
        yield
    finally:
        source.fetch_hourly = original


def test_local_day_mapping() -> None:
    """22:00 UTC in January is already the next day in Asia/Jerusalem (UTC+2)."""
    with tempfile.TemporaryDirectory() as tmp:
        conn = db.connect(Path(tmp) / "t.sqlite")
        db.upsert_readings(conn, [_reading(datetime(2026, 1, 15, 22, tzinfo=UTC), 1.5)])
        rows = db.hourly(conn, "electricity", date(2026, 1, 16), date(2026, 1, 16))
        assert len(rows) == 1, rows
        assert rows[0]["local_date"] == "2026-01-16", rows[0]
        assert db.hourly(conn, "electricity", date(2026, 1, 15), date(2026, 1, 15)) == []
        conn.close()


def test_refetch_overwrites_and_daily_sums() -> None:
    """Re-fetching a stored hour must correct it in place, not duplicate it."""
    with tempfile.TemporaryDirectory() as tmp:
        conn = db.connect(Path(tmp) / "t.sqlite")
        base = datetime(2026, 6, 1, 6, tzinfo=UTC)  # 09:00 local, safely mid-day
        db.upsert_readings(conn, [_reading(base, 2.0), _reading(base + timedelta(hours=1), 3.0)])
        db.upsert_readings(conn, [_reading(base, 5.0)])  # a late correction from the portal

        days = db.daily(conn, "electricity", date(2026, 6, 1), date(2026, 6, 1))
        assert days == [{"date": "2026-06-01", "value": 8.0, "unit": "kWh", "hours": 2}], days

        total = db.total(conn, "electricity", date(2026, 6, 1), date(2026, 6, 1))
        assert total == {"value": 8.0, "unit": "kWh", "hours": 2}, total
        assert db.latest_hour(conn, "electricity")["hour_utc"] == "2026-06-01T07:00:00Z"
        conn.close()


def test_naive_timestamp_rejected() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        conn = db.connect(Path(tmp) / "t.sqlite")
        try:
            db.upsert_readings(conn, [_reading(datetime(2026, 6, 1, 6), 1.0)])
        except ValueError:
            pass
        else:
            raise AssertionError("a naive hour_start should have been rejected")
        conn.close()


def test_job_ranges() -> None:
    """Wednesday 2026-09-09: the last full Sunday-Saturday week is 08-30..09-05."""
    today = date(2026, 9, 9)
    with _conn() as conn:
        assert jobs.JOBS["today"].covers(today, conn) == (today, today)
        assert jobs.JOBS["yesterday"].covers(today, conn) == (date(2026, 9, 8), date(2026, 9, 8))
        assert jobs.JOBS["last_full_week"].covers(today, conn) == (date(2026, 8, 30), date(2026, 9, 5))
        assert jobs.JOBS["year_to_date"].covers(today, conn) == (date(2026, 1, 1), today)

        sunday = date(2026, 9, 6)  # on a Sunday the last full week is the one that just ended
        assert jobs.JOBS["last_full_week"].covers(sunday, conn) == (date(2026, 8, 30), date(2026, 9, 5))


def test_due() -> None:
    now = datetime(2026, 9, 9, 12, tzinfo=UTC)
    assert db.due(None, timedelta(hours=1), now) is True, "never-run jobs must be due"
    assert db.due({"last_run_utc": "2026-09-09T11:30:00Z"}, timedelta(hours=1), now) is False
    assert db.due({"last_run_utc": "2026-09-09T11:00:00Z"}, timedelta(hours=1), now) is True
    assert db.due({"last_run_utc": "2026-09-01T00:00:00Z"}, timedelta(days=30), now) is False


def test_missing_source_is_recorded_not_raised() -> None:
    """A missing adapter must land in job_state as an error, never kill the scheduler."""
    with tempfile.TemporaryDirectory() as tmp:
        conn = db.connect(Path(tmp) / "t.sqlite")
        assert jobs.run_job(conn, "today", date(2026, 9, 9)) == 0
        state = db.job_states(conn)["today"]
        assert state["last_ok_utc"] is None
        assert "SourceNotReady" in state["last_error"], state["last_error"]
        conn.close()


def test_previous_year_only_in_january() -> None:
    """The portal corrects last year until the end of January, so the job sleeps after it."""
    with _conn() as conn:
        spec = jobs.JOBS["previous_year"]
        assert spec.in_season(date(2026, 9, 9)) is False
        assert spec.in_season(date(2026, 1, 1)) is True
        assert spec.in_season(date(2026, 1, 31)) is True
        assert spec.in_season(date(2026, 2, 1)) is False
        assert spec.covers(date(2026, 1, 15), conn) == (date(2025, 1, 1), date(2025, 12, 31))
        assert jobs.JOBS["today"].in_season(date(2026, 9, 9)) is True


def test_scheduler_skips_out_of_season_jobs() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        original = config.DB_PATH
        config.DB_PATH = Path(tmp) / "t.sqlite"  # run_due opens the configured DB itself
        try:
            september = jobs.run_due(datetime(2026, 9, 9, 9, tzinfo=UTC))
            january = jobs.run_due(datetime(2026, 1, 15, 9, tzinfo=UTC))
        finally:
            config.DB_PATH = original
    assert "previous_year" not in september, september
    assert "previous_year" in january, january
    assert "backfill" not in september, "an empty database gives the backfill no starting year"


def test_backfill_walks_back_then_stops_for_good() -> None:
    with _conn() as conn, _source_with_years({2025, 2024}):
        today = date(2026, 9, 9)
        spec = jobs.JOBS["backfill"]
        assert spec.covers(today, conn) is None, "nothing stored yet, so nowhere to walk back from"

        db.upsert_readings(conn, [_reading(datetime(2026, 6, 1, 6, tzinfo=UTC), 1.0)])
        assert spec.covers(today, conn) == (date(2025, 1, 1), date(2025, 12, 31))
        assert jobs.run_job(conn, "backfill", today) == 2, "one reading per utility"

        assert spec.covers(today, conn) == (date(2024, 1, 1), date(2024, 12, 31))
        assert jobs.run_job(conn, "backfill", today) == 2

        assert spec.covers(today, conn) == (date(2023, 1, 1), date(2023, 12, 31))
        assert jobs.run_job(conn, "backfill", today) == 0, "the portal has no 2023"
        assert db.get_state(conn, jobs.BACKFILL_KEY) == jobs.BACKFILL_DONE
        assert spec.covers(today, conn) is None, "a finished backfill must never ask again"
        assert jobs.run_job(conn, "backfill", today) == 0


def test_backfill_survives_a_failed_fetch() -> None:
    """A failure returns no rows too - it must not be mistaken for the end of the history."""
    with _conn() as conn:
        today = date(2026, 9, 9)
        db.upsert_readings(conn, [_reading(datetime(2026, 6, 1, 6, tzinfo=UTC), 1.0)])
        assert jobs.run_job(conn, "backfill", today) == 0  # source.py is not implemented
        assert db.get_state(conn, jobs.BACKFILL_KEY) is None
        assert jobs.JOBS["backfill"].covers(today, conn) == (date(2025, 1, 1), date(2025, 12, 31))


def test_monthly_and_yearly() -> None:
    with _conn() as conn:
        db.upsert_readings(
            conn,
            [
                _reading(datetime(2024, 3, 10, 6, tzinfo=UTC), 1.0),
                _reading(datetime(2024, 3, 11, 6, tzinfo=UTC), 2.0),
                _reading(datetime(2024, 4, 1, 6, tzinfo=UTC), 4.0),
                _reading(datetime(2026, 1, 5, 6, tzinfo=UTC), 8.0),
            ],
        )
        span = (date(2024, 1, 1), date(2026, 12, 31))
        months = db.monthly(conn, "electricity", *span)
        assert [(m["month"], m["value"]) for m in months] == [
            ("2024-03", 3.0),
            ("2024-04", 4.0),
            ("2026-01", 8.0),
        ], months
        years = db.yearly(conn, "electricity", *span)
        assert [(y["year"], y["value"], y["hours"]) for y in years] == [
            ("2024", 7.0, 3),
            ("2026", 8.0, 1),
        ], years
        assert db.yearly(conn, "electricity", date(2026, 1, 1), date(2026, 12, 31)) == [
            {"year": "2026", "value": 8.0, "unit": "kWh", "hours": 1}
        ]


def test_coverage() -> None:
    with _conn() as conn:
        empty = db.coverage(conn)
        assert empty["electricity"] == {"first_date": None, "last_date": None, "hours": 0}
        assert set(empty) == {"electricity", "water"}, empty

        db.upsert_readings(
            conn,
            [
                _reading(datetime(2024, 3, 10, 6, tzinfo=UTC), 1.0),
                _reading(datetime(2026, 1, 5, 6, tzinfo=UTC), 2.0),
            ],
        )
        cov = db.coverage(conn)
        assert cov["electricity"] == {
            "first_date": "2024-03-10",
            "last_date": "2026-01-05",
            "hours": 2,
        }, cov
        assert cov["water"]["hours"] == 0


def test_encrypted_credentials_round_trip() -> None:
    """DPAPI, pointed at a temp file so the user's real credential store is never touched."""
    if os.name != "nt":
        print("  skip  test_encrypted_credentials_round_trip (Windows only)")
        return
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "credentials.dpapi"
        assert secrets.load(path) is None, "an absent store must read as None, not raise"

        secrets.save("user@example.com", "pa ss:word", path)
        assert path.read_bytes() != b"", "nothing was written"
        assert b"pa ss:word" not in path.read_bytes(), "the password must not be stored in clear"
        assert secrets.load(path) == ("user@example.com", "pa ss:word")

        path.write_bytes(b"this is not a DPAPI blob")
        try:
            secrets.load(path)
        except secrets.SecretsError as exc:
            assert "set-credentials.bat" in str(exc), exc
        else:
            raise AssertionError("a foreign blob should have raised SecretsError")

        secrets.clear(path)
        assert secrets.load(path) is None


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
        print(f"  ok  {test.__name__}")
    print(f"{len(tests)} self-checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
