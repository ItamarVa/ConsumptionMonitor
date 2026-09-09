"""Offline contract checks for the HTTP API against the records.py storage surface.

Uses FastAPI TestClient with mocked db query functions so this stream does not wait
on db.py implementation. Job names still reflect jobs.JOBS until Wave 2 renames them.
"""

from __future__ import annotations

import asyncio
import sqlite3
import sys
import tempfile
import types
from contextlib import contextmanager
from datetime import date
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Wave 1 parallel stub: agent A owns consumption.hourly; use real module when present.
if "consumption.hourly" not in sys.modules:
    try:
        import consumption.hourly  # noqa: F401
    except ImportError:
        _hourly_stub = types.ModuleType("consumption.hourly")

        def _stub_spread_to_hours(readings, field, day, tz):
            return [
                {"hour": "00:00", "value": 0.412, "source_intervals": 1, "partial": False},
                {"hour": "01:00", "value": None, "source_intervals": 0, "partial": True},
            ]

        _hourly_stub.spread_to_hours = _stub_spread_to_hours
        sys.modules["consumption.hourly"] = _hourly_stub

from fastapi.testclient import TestClient  # noqa: E402

from consumption import api, config, db, jobs  # noqa: E402
from consumption.records import SCHEMA  # noqa: E402

TODAY = date(2026, 9, 9)
ELEC_METER = "30400"
WATER_METER = "30399"

_COVERAGE = {
    "electricity": {
        "first_date": "2024-01-01",
        "last_date": "2026-09-09",
        "reading_count": 2,
        "meter_ids": [ELEC_METER],
    },
    "water": {
        "first_date": "2024-06-01",
        "last_date": "2026-09-09",
        "reading_count": 1,
        "meter_ids": [WATER_METER],
    },
}

_LATEST_ELEC = {
    "reading_time_utc": "2026-09-09T17:05:18Z",
    "total_import_kwh": 56580.68,
    "total_export_kwh": 2770.07,
}

_LATEST_WATER = {
    "reading_time_utc": "2026-09-09T17:05:18Z",
    "total_water_data": 2265.308,
}

_DAILY_IMPORT = [{"date": "2026-09-09", "value": 12.5, "unit": "kWh"}]
_DAILY_EXPORT = [{"date": "2026-09-09", "value": 1.2, "unit": "kWh"}]
_DAILY_WATER = [{"date": "2026-09-09", "value": 0.4, "unit": "m3"}]


@contextmanager
def _test_client():
    async def _idle():
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            pass

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "api.sqlite"
        conn_holder: list[sqlite3.Connection] = []

        def _connect(_path=None):
            c = sqlite3.connect(path)
            c.row_factory = sqlite3.Row
            c.executescript(SCHEMA)
            conn_holder.append(c)
            return c

        def _coverage(_conn):
            return _COVERAGE

        def _latest_reading(_conn, meter_id: str):
            if meter_id == ELEC_METER:
                return _LATEST_ELEC
            if meter_id == WATER_METER:
                return _LATEST_WATER
            return None

        def _daily_totals(_conn, utility: str, direction: str, start: date, end: date):
            if utility == "electricity" and direction == "import":
                return _DAILY_IMPORT
            if utility == "electricity" and direction == "export":
                return _DAILY_EXPORT
            if utility == "water" and direction == "water":
                return _DAILY_WATER
            return []

        def _alert_flags(_conn, meter_id: str):
            if meter_id == WATER_METER:
                return {"back_flow": True, "has_leak": False}
            return {"back_flow": False, "has_leak": False}

        stubs = {
            "connect": _connect,
            "coverage": _coverage,
            "job_states": lambda _c: {},
            "meter_readings": lambda _c, _m, _s, _e: [],
            "intervals": lambda _c, _m, _d, _s, _e: [],
            "daily_totals": _daily_totals,
            "monthly_totals": lambda _c, _u, _d, _s, _e: [],
            "yearly_totals": lambda _c, _u, _d, _s, _e: [],
            "latest_reading": _latest_reading,
            "alert_flags": _alert_flags,
        }
        with (
            patch.object(db, "connect", _connect),
            patch.object(db, "coverage", _coverage),
            patch.object(db, "job_states", stubs["job_states"]),
            patch.object(db, "meter_readings", stubs["meter_readings"]),
            patch.object(db, "intervals", stubs["intervals"]),
            patch.object(db, "daily_totals", stubs["daily_totals"]),
            patch.object(db, "monthly_totals", stubs["monthly_totals"]),
            patch.object(db, "yearly_totals", stubs["yearly_totals"]),
            patch.object(db, "latest_reading", stubs["latest_reading"]),
            patch.object(db, "alert_flags", stubs["alert_flags"]),
            patch.object(jobs, "loop", _idle),
            patch.object(jobs, "local_today", lambda _now=None: TODAY),
        ):
            with TestClient(api.app, base_url="http://127.0.0.1") as client:
                yield client


def test_bad_utility_returns_422() -> None:
    with _test_client() as client:
        r = client.get("/readings/daily", params={"utility": "gas", "direction": "import"})
    assert r.status_code == 422, r.text


def test_water_import_direction_rejected() -> None:
    with _test_client() as client:
        r = client.get("/readings/daily", params={"utility": "water", "direction": "import"})
    assert r.status_code == 422, r.text


def test_range_cap_on_intervals() -> None:
    with _test_client() as client:
        r = client.get(
            "/readings/intervals",
            params={
                "utility": "electricity",
                "direction": "import",
                "start": "2020-01-01",
                "end": "2026-09-09",
            },
        )
    assert r.status_code == 422, r.text
    assert "366" in r.json()["detail"]


def test_health_coverage_shape() -> None:
    with _test_client() as client:
        body = client.get("/health").json()
    assert body["reading_count"] == 3
    assert body["coverage"]["electricity"]["reading_count"] == 2
    assert "hours" not in body["coverage"]["electricity"]


def test_summary_shape() -> None:
    with _test_client() as client:
        body = client.get("/summary").json()
    assert body["local_date"] == TODAY.isoformat()
    elec = body["utilities"]["electricity"]
    assert set(elec) == {"import", "export"}
    assert elec["import"]["latest_register"]["value"] == 56580.68
    assert elec["import"]["today"]["value"] == 12.5
    assert elec["export"]["latest_register"]["value"] == 2770.07
    water = body["utilities"]["water"]["water"]
    assert water["latest_register"]["value"] == 2265.308
    assert water["today"]["unit"] == "m3"


def test_alerts_per_meter() -> None:
    with _test_client() as client:
        body = client.get("/alerts", params={"utility": "water"}).json()
    assert len(body["meters"]) == 1
    assert body["meters"][0]["back_flow"] is True


def test_jobs_use_reading_log_schedule() -> None:
    with _test_client() as client:
        body = client.get("/jobs").json()
    assert set(body) == {"recent", "recent_week", "previous_year", "backfill"}
    assert body["recent"]["every"] == "1:00:00"
    assert body["recent"]["covers"]["start"] == "2026-09-08"
    assert body["recent"]["covers"]["end"] == "2026-09-09"


def test_index_lists_new_endpoints() -> None:
    with _test_client() as client:
        body = client.get("/").json()
    assert body["ui"] == "/ui"
    paths = body["endpoints"]
    assert "/readings/raw" in paths
    assert "/readings/intervals" in paths
    assert "/readings/hourly" in paths


def test_hourly_shape_and_bad_direction() -> None:
    with _test_client() as client:
        r = client.get(
            "/readings/hourly",
            params={"utility": "electricity", "direction": "import", "date": "2026-09-09"},
        )
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["utility"] == "electricity"
        assert body["direction"] == "import"
        assert body["date"] == "2026-09-09"
        assert body["unit"] == "kWh"
        assert body["meter_id"] == ELEC_METER
        assert body["estimated"] is True
        assert isinstance(body["hours"], list)
        assert len(body["hours"]) >= 1
        hour = body["hours"][0]
        assert set(hour) == {"hour", "value", "source_intervals", "partial"}

        bad = client.get(
            "/readings/hourly",
            params={"utility": "water", "direction": "import", "date": "2026-09-09"},
        )
    assert bad.status_code == 422, bad.text


def test_untrusted_host_rejected() -> None:
    with _test_client() as client:
        r = client.get("/health", headers={"Host": "evil.com"})
    assert r.status_code == 400, r.text


def test_refresh_sec_fetch_site_guard() -> None:
    with (
        _test_client() as client,
        patch.object(jobs, "run_job", return_value=0),
    ):
        blocked = client.post(
            "/refresh/recent",
            headers={"Sec-Fetch-Site": "cross-site"},
        )
        allowed = client.post("/refresh/recent")
    assert blocked.status_code == 403, blocked.text
    assert allowed.status_code == 200, allowed.text
    assert allowed.json()["job"] == "recent"


def test_ui_index_html() -> None:
    ui_file = config.ROOT / "web" / "index.html"
    if not ui_file.is_file():
        print("  skip test_ui_index_html (web/index.html not yet created)")
        return
    with _test_client() as client:
        r = client.get("/ui/index.html")
    assert r.status_code == 200, r.text


def test_security_headers_present() -> None:
    with _test_client() as client:
        r = client.get("/health")
    assert r.status_code == 200, r.text
    assert "default-src 'self'" in r.headers.get("content-security-policy", "")
    assert r.headers.get("x-content-type-options") == "nosniff"
    assert r.headers.get("x-frame-options") == "DENY"
    assert r.headers.get("referrer-policy") == "no-referrer"


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
        print(f"  ok  {test.__name__}")
    print(f"{len(tests)} API contract checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
