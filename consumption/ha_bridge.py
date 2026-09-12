"""Orchestrates Home Assistant entity publish and statistics import after refresh.

MQTT discovery and state go through the Supervisor mqtt.publish proxy (httpx).
Statistics use recorder/import_statistics on the Supervisor WebSocket proxy.
Active only when HA_BRIDGE is enabled; statistics honor ENERGY_STATISTICS.
Depends on ha_entities.py, ha_statistics.py, config.py, db.py.
"""

from __future__ import annotations

import json
import os
import sqlite3
import traceback
from typing import Any

import httpx

from . import config, db
from .ha_entities import DISCOVERY_TOPIC, STATE_TOPIC, build_discovery, build_state
from .ha_statistics import (
    SERIES,
    build_hourly_rows,
    import_statistics_ws,
    mark_full_sync_done,
    refresh_since,
)

SUPERVISOR_PUBLISH_URL = "http://supervisor/core/api/services/mqtt/publish"

_DISCOVERY_SENT_KEY = "ha_mqtt_discovery_sent"


def _config_value(name: str, default: str = "") -> str:
    value = getattr(config, name, None)
    if value is None:
        value = os.environ.get(name, default)
    return str(value).strip() if value is not None else default


def bridge_enabled() -> bool:
    return _config_value("HA_BRIDGE").lower() in ("1", "true", "yes")


def energy_statistics_enabled() -> bool:
    return _config_value("ENERGY_STATISTICS", "1").lower() in ("1", "true", "yes")


def supervisor_token() -> str:
    return _config_value("SUPERVISOR_TOKEN")


def addon_version() -> str:
    return _config_value("ADDON_VERSION", "dev")


def _mqtt_publish(token: str, topic: str, payload: Any, *, retain: bool) -> None:
    body = {
        "topic": topic,
        "payload": json.dumps(payload) if not isinstance(payload, str) else payload,
        "retain": retain,
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = httpx.post(
        SUPERVISOR_PUBLISH_URL,
        json=body,
        headers=headers,
        timeout=30.0,
    )
    response.raise_for_status()


def publish_entities(conn: sqlite3.Connection, token: str) -> None:
    """Publish retained discovery once, then current device state."""
    version = addon_version()
    if db.get_state(conn, _DISCOVERY_SENT_KEY) != "1":
        _mqtt_publish(token, DISCOVERY_TOPIC, build_discovery(conn, version), retain=True)
        db.set_state(conn, _DISCOVERY_SENT_KEY, "1")
    _mqtt_publish(token, STATE_TOPIC, build_state(conn), retain=True)


async def import_energy_statistics(conn: sqlite3.Connection, token: str) -> None:
    since = refresh_since(conn)
    full_sync = since is None
    for statistic_id in SERIES:
        rows = build_hourly_rows(conn, statistic_id, since_utc=since)
        await import_statistics_ws(token, statistic_id, rows)
    if full_sync:
        mark_full_sync_done(conn)


async def sync_async(conn: sqlite3.Connection) -> None:
    """Publish MQTT entities and optionally refresh external statistics."""
    if not bridge_enabled():
        return
    token = supervisor_token()
    if not token:
        return
    try:
        publish_entities(conn, token)
        if energy_statistics_enabled():
            await import_energy_statistics(conn, token)
    except Exception:  # noqa: BLE001 - bridge must never break the scheduler
        traceback.print_exc()


def sync(conn: sqlite3.Connection) -> None:
    """Synchronous entry point for jobs.run_due (runs the async bridge in a loop)."""
    if not bridge_enabled():
        return
    import asyncio

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        asyncio.run(sync_async(conn))
        return
    loop.create_task(sync_async(conn))
