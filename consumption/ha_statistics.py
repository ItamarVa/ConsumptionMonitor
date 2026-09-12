"""Hourly external statistics for the Home Assistant Energy dashboard.

Spreads register deltas across local hours via hourly.spread_to_hours, then
builds recorder/import_statistics rows with cumulative sum and end-of-hour
register state. First sync uploads full history in chunks; later syncs only
re-send the last 48 hours (same start overwrites). Depends on db.py, hourly.py.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import date, datetime, timedelta, timezone
from typing import Any

from . import config, db
from .hourly import _build_buckets, spread_to_hours

UTC = timezone.utc
SOURCE = "consumptionmonitor"
FULL_SYNC_KEY = "ha_stats_full_sync_done"
REFRESH_HOURS = 48
CHUNK_SIZE = 2000
WS_URL = "ws://supervisor/core/websocket"

SERIES: dict[str, dict[str, str]] = {
    "consumptionmonitor:electricity_import": {
        "utility": "electricity",
        "direction": "import",
        "field": "total_import_kwh",
        "unit": "kWh",
        "unit_class": "energy",
        "name": "Electricity import",
    },
    "consumptionmonitor:electricity_export": {
        "utility": "electricity",
        "direction": "export",
        "field": "total_export_kwh",
        "unit": "kWh",
        "unit_class": "energy",
        "name": "Electricity export",
    },
    "consumptionmonitor:water": {
        "utility": "water",
        "direction": "water",
        "field": "total_water_data",
        "unit": "m³",
        "unit_class": "volume",
        "name": "Water",
    },
}


def _parse_utc(raw: Any) -> datetime:
    if isinstance(raw, datetime):
        dt = raw
    else:
        text = str(raw)
        if text.endswith("Z"):
            text = f"{text[:-1]}+00:00"
        dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def _primary_meter(conn: sqlite3.Connection, utility: str) -> str | None:
    cur = conn.execute(
        "SELECT DISTINCT meter_id FROM meter_reading WHERE utility = ? ORDER BY meter_id",
        (utility,),
    )
    row = cur.fetchone()
    return row[0] if row else None


def _register_at(rows: list[dict], field: str, moment: datetime) -> float | None:
    best: float | None = None
    for row in rows:
        if _parse_utc(row["reading_time_utc"]) <= moment:
            value = row.get(field)
            if value is not None:
                best = float(value)
        else:
            break
    return best


def metadata_for(statistic_id: str) -> dict:
    spec = SERIES[statistic_id]
    return {
        "has_sum": True,
        "mean_type": 0,
        "name": spec["name"],
        "source": SOURCE,
        "statistic_id": statistic_id,
        "unit_of_measurement": spec["unit"],
        "unit_class": spec["unit_class"],
    }


def build_hourly_rows(
    conn: sqlite3.Connection,
    statistic_id: str,
    *,
    since_utc: datetime | None = None,
) -> list[dict]:
    """Build import_statistics rows; filter to since_utc when doing a partial refresh."""
    spec = SERIES[statistic_id]
    utility = spec["utility"]
    field = spec["field"]
    meter_id = _primary_meter(conn, utility)
    if meter_id is None:
        return []

    cov = db.coverage(conn).get(utility, {})
    first_date_raw = cov.get("first_date")
    last_date_raw = cov.get("last_date")
    if not first_date_raw or not last_date_raw:
        return []

    first_date = date.fromisoformat(first_date_raw)
    last_date = date.fromisoformat(last_date_raw)
    readings = db.meter_readings(conn, meter_id, first_date - timedelta(days=1), last_date)
    if len(readings) < 2:
        return []

    running_sum = 0.0
    out: list[dict] = []
    day = first_date
    while day <= last_date:
        day_start = datetime(day.year, day.month, day.day, tzinfo=config.LOCAL_TZ)
        day_end = day_start + timedelta(days=1)
        buckets = _build_buckets(day_start, day_end)
        hours = spread_to_hours(readings, field, day, config.LOCAL_TZ)
        for bucket, hour_row in zip(buckets, hours, strict=True):
            value = hour_row.get("value")
            if value is None:
                continue
            hour_start = bucket["start"]
            if since_utc is not None and hour_start.astimezone(UTC) < since_utc:
                running_sum += float(value)
                continue
            running_sum += float(value)
            hour_end = bucket["end"]
            state = _register_at(readings, field, hour_end.astimezone(UTC))
            if state is None:
                continue
            out.append(
                {
                    "start": hour_start.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                    "state": round(state, 4),
                    "sum": round(running_sum, 4),
                }
            )
        day += timedelta(days=1)
    return out


def chunk_rows(rows: list[dict], size: int = CHUNK_SIZE) -> list[list[dict]]:
    return [rows[i : i + size] for i in range(0, len(rows), size)]


def refresh_since(conn: sqlite3.Connection, now: datetime | None = None) -> datetime | None:
    """Return the UTC cutoff for a partial refresh, or None for a full history import."""
    if db.get_state(conn, FULL_SYNC_KEY) != "1":
        return None
    moment = now or datetime.now(UTC)
    return moment - timedelta(hours=REFRESH_HOURS)


def mark_full_sync_done(conn: sqlite3.Connection) -> None:
    db.set_state(conn, FULL_SYNC_KEY, "1")


async def import_statistics_ws(
    token: str,
    statistic_id: str,
    rows: list[dict],
    *,
    ws_url: str = WS_URL,
) -> None:
    """Send one recorder/import_statistics message over the Supervisor WebSocket proxy."""
    if not rows:
        return
    import websockets

    metadata = metadata_for(statistic_id)
    msg_id = 1
    async with websockets.connect(
        ws_url,
        additional_headers={"Authorization": f"Bearer {token}"},
        open_timeout=10,
    ) as ws:
        auth_required = json.loads(await ws.recv())
        if auth_required.get("type") != "auth_required":
            raise RuntimeError(f"unexpected websocket greeting: {auth_required}")
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        auth_result = json.loads(await ws.recv())
        if auth_result.get("type") != "auth_ok":
            raise RuntimeError(f"websocket auth failed: {auth_result}")

        for chunk in chunk_rows(rows):
            payload = {
                "id": msg_id,
                "type": "recorder/import_statistics",
                "metadata": metadata,
                "stats": chunk,
            }
            await ws.send(json.dumps(payload))
            result = json.loads(await ws.recv())
            if result.get("type") == "result" and not result.get("success", True):
                raise RuntimeError(f"import_statistics failed: {result}")
            msg_id += 1
