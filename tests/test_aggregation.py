"""Self-check for the two things in this project that are easy to get silently wrong:
UTC-to-local day mapping on stored hours, and the date range each scheduled job covers.

Runs against a throwaway SQLite file, needs no network and no credentials, and is what
run.bat executes before starting the API. Plain asserts so `python tests/test_aggregation.py`
and `pytest` both work.
"""

from __future__ import annotations

import sys
import tempfile
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from consumption import db, jobs  # noqa: E402
from consumption.source import Reading  # noqa: E402

UTC = timezone.utc


def _reading(hour_utc: datetime, value: float) -> Reading:
    return Reading("electricity", "meter-1", hour_utc, value, "kWh")


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
    assert jobs.JOBS["today"][1](today) == (today, today)
    assert jobs.JOBS["yesterday"][1](today) == (date(2026, 9, 8), date(2026, 9, 8))
    assert jobs.JOBS["last_full_week"][1](today) == (date(2026, 8, 30), date(2026, 9, 5))
    assert jobs.JOBS["year_to_date"][1](today) == (date(2026, 1, 1), today)

    sunday = date(2026, 9, 6)  # on a Sunday the last full week is the one that just ended
    assert jobs.JOBS["last_full_week"][1](sunday) == (date(2026, 8, 30), date(2026, 9, 5))


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


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
        print(f"  ok  {test.__name__}")
    print(f"{len(tests)} self-checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
