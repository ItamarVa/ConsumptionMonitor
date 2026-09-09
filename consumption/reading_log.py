"""Pure parsers for the mycitygrid meter reading log (GET meterdata).

Maps portal JSON rows to MeterReading without HTTP or credentials. Every field name
comes from the live probe documented in the raw-meter-reading plan. A mismatch must
raise SourceError with a redacted excerpt — this data becomes stored history.
Depended on by: source.py (fetch path), tests/test_reading_log.py.
"""

from __future__ import annotations

import json
from datetime import date, datetime, timezone

from . import config
from .readings import SourceError, excerpt
from .records import MeterReading

_FLOAT_FIELDS: tuple[tuple[str, str], ...] = (
    ("totalImportKwH", "total_import_kwh"),
    ("totalExportKwH", "total_export_kwh"),
    ("tou1ImportKwH", "tou1_import_kwh"),
    ("tou2ImportKwH", "tou2_import_kwh"),
    ("tou3ImportKwH", "tou3_import_kwh"),
    ("tou1ExportKwH", "tou1_export_kwh"),
    ("tou2ExportKwH", "tou2_export_kwh"),
    ("tou3ExportKwH", "tou3_export_kwh"),
    ("totalWaterData", "total_water_data"),
    ("totalConsumption", "total_consumption"),
    ("totalProduction", "total_production"),
    ("consumption1", "consumption1"),
    ("consumption2", "consumption2"),
    ("consumption3", "consumption3"),
    ("production1", "production1"),
    ("production3", "production3"),
    ("v1", "v1"),
    ("v2", "v2"),
    ("v3", "v3"),
    ("a1", "a1"),
    ("a2", "a2"),
    ("a3", "a3"),
    ("cos", "cos"),
    ("kvarH", "kvar_h"),
    ("maxDmd", "max_dmd"),
)

_BOOL_FIELDS: tuple[tuple[str, str], ...] = (
    ("hasLeak", "has_leak"),
    ("backFlow", "back_flow"),
    ("brokenPipe", "broken_pipe"),
    ("emptyPipe", "empty_pipe"),
    ("lowBattery", "low_battery"),
    ("magneticTamper", "magnetic_tamper"),
    ("meterError", "meter_error"),
    ("addedManually", "added_manually"),
)


def parse_reading_page(envelope: dict) -> list[dict]:
    """Return the `items` list from one paginated reading-log response."""
    if not isinstance(envelope, dict):
        raise SourceError("expected a reading-log page object, got: " + excerpt(envelope))
    items = envelope.get("items")
    if items is None:
        raise SourceError("expected an 'items' list in the reading-log page, got: " + excerpt(envelope))
    if not isinstance(items, list):
        raise SourceError("expected 'items' to be a list, got: " + excerpt(envelope))
    rows: list[dict] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise SourceError(f"expected items[{index}] to be an object, got: " + excerpt(item))
        rows.append(item)
    return rows


def parse_reading_row(item: dict, utility: str, meter_id: str) -> MeterReading:
    """Map one portal reading-log row to a MeterReading."""
    if not isinstance(item, dict):
        raise SourceError("expected a reading-log row object, got: " + excerpt(item))

    reading_time = _reading_time_utc(item.get("readingTime"), item)
    local = reading_time.astimezone(config.LOCAL_TZ).date()

    fields: dict[str, object] = {
        "meter_data_id": _required_int(item.get("meterDataId"), "meterDataId", item),
        "meter_id": str(meter_id),
        "utility": utility,
        "reading_time": reading_time,
        "local_date": local,
        "raw_json": json.dumps(item, separators=(",", ":"), ensure_ascii=False),
        "updated_at": None,
    }
    for portal_key, attr in _FLOAT_FIELDS:
        fields[attr] = _optional_float(item.get(portal_key), portal_key, item)
    for portal_key, attr in _BOOL_FIELDS:
        fields[attr] = _bool_value(item.get(portal_key), portal_key, item)
    fields["multiplier_symbol_count"] = _optional_int(
        item.get("multiplierSymbolCount"), "multiplierSymbolCount", item
    )

    return MeterReading(**fields)


def _reading_time_utc(value: object, item: dict) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise SourceError("expected readingTime as an ISO string with offset, got: " + excerpt(item))
    try:
        stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise SourceError("expected readingTime as an ISO string with offset, got: " + excerpt(item)) from exc
    if stamp.tzinfo is None:
        raise SourceError("expected readingTime with a timezone offset, got: " + excerpt(item))
    return stamp.astimezone(timezone.utc)


def _required_int(value: object, field: str, item: dict) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise SourceError(f"expected {field} as an integer, got: " + excerpt(item))
    return value


def _optional_int(value: object, field: str, item: dict) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        raise SourceError(f"expected {field} as an integer or null, got: " + excerpt(item))
    return value


def _optional_float(value: object, field: str, item: dict) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SourceError(f"expected {field} as a number or null, got: " + excerpt(item))
    return float(value)


def _bool_value(value: object, field: str, item: dict) -> bool:
    if value is None:
        return False
    if not isinstance(value, bool):
        raise SourceError(f"expected {field} as a boolean or null, got: " + excerpt(item))
    return value
