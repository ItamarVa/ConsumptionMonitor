"""Self-check for the meter reading-log parsers (offline only).

Payload shapes follow the live probe in the raw-meter-reading plan and the meter ids
from connection-report.txt are replaced with synthetic values. No network, no credentials.
Plain asserts so `python tests/test_reading_log.py` and `pytest` both work.
"""

from __future__ import annotations

import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from consumption import config, reading_log  # noqa: E402
from consumption.readings import SourceError  # noqa: E402

UTC = timezone.utc

# Sanitized shapes: real probe values, fictional meter ids.
ELECTRICITY_ROW = {
    "meterDataId": 90001,
    "readingTime": "2026-09-09T20:05:18.59+03:00",
    "totalImportKwH": 56580.68,
    "totalExportKwH": 2770.07,
    "tou1ImportKwH": 40100.1,
    "tou2ImportKwH": 12000.2,
    "tou3ImportKwH": 4480.38,
    "tou1ExportKwH": 1500.0,
    "tou2ExportKwH": 800.0,
    "tou3ExportKwH": 470.07,
    "totalConsumption": 1.42,
    "totalProduction": 0.18,
    "consumption1": 0.9,
    "consumption2": 0.32,
    "consumption3": 0.2,
    "production1": 0.1,
    "production3": 0.08,
    "v1": 231.4,
    "v2": 230.9,
    "v3": 232.1,
    "a1": 2.1,
    "a2": 1.8,
    "a3": 0.4,
    "cos": 0.97,
    "kvarH": 12.5,
    "maxDmd": 4.2,
    "hasLeak": False,
    "backFlow": False,
    "brokenPipe": False,
    "emptyPipe": False,
    "lowBattery": False,
    "magneticTamper": False,
    "meterError": False,
    "multiplierSymbolCount": 2,
    "addedManually": False,
}

WATER_ROW = {
    "meterDataId": 90002,
    "readingTime": "2026-09-08T14:30:00+03:00",
    "totalWaterData": 2265.308,
    "totalConsumption": 0.12,
    "backFlow": True,
    "hasLeak": False,
    "brokenPipe": False,
    "emptyPipe": False,
    "lowBattery": False,
    "magneticTamper": False,
    "meterError": False,
    "addedManually": False,
}


def _raises(exc_type, call, message_contains=""):
    try:
        call()
    except exc_type as exc:
        assert message_contains in str(exc), f"expected {message_contains!r} in {exc}"
        return str(exc)
    raise AssertionError(f"expected {exc_type.__name__}, nothing was raised")


def test_parse_electricity_row() -> None:
    reading = reading_log.parse_reading_row(ELECTRICITY_ROW, "electricity", "m-e1")
    assert reading.meter_data_id == 90001
    assert reading.meter_id == "m-e1"
    assert reading.utility == "electricity"
    assert reading.reading_time == datetime(2026, 9, 9, 17, 5, 18, 590000, tzinfo=UTC)
    assert reading.local_date == date(2026, 9, 9)
    assert reading.total_import_kwh == 56580.68
    assert reading.total_export_kwh == 2770.07
    assert reading.tou1_import_kwh == 40100.1
    assert reading.tou3_export_kwh == 470.07
    assert reading.total_consumption == 1.42
    assert reading.production3 == 0.08
    assert reading.v2 == 230.9 and reading.kvar_h == 12.5
    assert reading.multiplier_symbol_count == 2
    assert reading.back_flow is False
    assert reading.raw_json == json.dumps(ELECTRICITY_ROW, separators=(",", ":"), ensure_ascii=False)


def test_parse_water_row() -> None:
    reading = reading_log.parse_reading_row(WATER_ROW, "water", "m-w1")
    assert reading.total_water_data == 2265.308
    assert reading.back_flow is True
    assert reading.total_import_kwh is None
    assert reading.local_date == date(2026, 9, 8)


def test_malformed_row_raises_with_excerpt() -> None:
    bad = {"meterDataId": "not-an-id", "readingTime": "2026-09-09T20:05:18.59+03:00"}
    message = _raises(
        SourceError,
        lambda: reading_log.parse_reading_row(bad, "electricity", "m-e1"),
        "meterDataId",
    )
    assert "not-an-id" in message
    assert len(message) <= 400


def test_parse_reading_page_envelope() -> None:
    envelope = {
        "totalItemCount": 2,
        "pageCount": 1,
        "hasNextPage": False,
        "items": [ELECTRICITY_ROW, WATER_ROW],
        "multiplier": 0.01,
        "size": 2,
    }
    items = reading_log.parse_reading_page(envelope)
    assert len(items) == 2
    assert items[0]["meterDataId"] == 90001

    _raises(
        SourceError,
        lambda: reading_log.parse_reading_page({"totalItemCount": 0}),
        "'items' list",
    )
    _raises(
        SourceError,
        lambda: reading_log.parse_reading_page({"items": ["x"]}),
        "items[0]",
    )


def test_local_timezone_matches_config() -> None:
    assert str(config.LOCAL_TZ) == "Asia/Jerusalem"


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
        print(f"  ok  {test.__name__}")
    print(f"{len(tests)} reading-log self-checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
