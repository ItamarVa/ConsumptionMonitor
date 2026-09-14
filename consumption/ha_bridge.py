"""Orchestrates Home Assistant entity publish and water statistics import after refresh.

MQTT discovery and state go through the Supervisor mqtt.publish proxy (httpx).
Electricity Energy-dashboard history comes from MQTT register sensors; only water
uses recorder/import_statistics on the Supervisor WebSocket proxy. Active only when
HA_BRIDGE is enabled; water statistics honor ENERGY_STATISTICS.
Depends on ha_entities.py, ha_statistics.py, config.py, db.py.
"""

from __future__ import annotations

import asyncio
import json
import os
import sqlite3
import threading
import traceback
from typing import Any

import httpx

from . import config, db
from .ha_entities import DISCOVERY_TOPIC, STATE_TOPIC, build_discovery, build_state
from .ha_statistics import (
    FULL_SYNC_KEY,
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


def _mqtt_publish(token: str, topic: str, payload: Any, *, retain: bool) -> bool:
    body = {
        "topic": topic,
        "payload": json.dumps(payload) if not isinstance(payload, str) else payload,
        "retain": retain,
    }
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = httpx.post(
            SUPERVISOR_PUBLISH_URL,
            json=body,
            headers=headers,
            timeout=30.0,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(
            "HA bridge: mqtt.publish failed "
            f"({exc.response.status_code}); is the MQTT integration configured?"
        )
        return False
    except httpx.RequestError as exc:
        print(f"HA bridge: mqtt.publish failed ({exc}); is the MQTT integration configured?")
        return False
    return True


def publish_entities(conn: sqlite3.Connection, token: str) -> None:
    """Publish retained discovery when the add-on version changes, then current state."""
    version = addon_version()
    if db.get_state(conn, _DISCOVERY_SENT_KEY) != version:
        if _mqtt_publish(token, DISCOVERY_TOPIC, build_discovery(conn, version), retain=True):
            db.set_state(conn, _DISCOVERY_SENT_KEY, version)
    _mqtt_publish(token, STATE_TOPIC, build_state(conn), retain=True)


async def import_water_statistics(conn: sqlite3.Connection, token: str) -> None:
    since = refresh_since(conn)
    full_sync = since is None
    for statistic_id in SERIES:
        rows = build_hourly_rows(conn, statistic_id, since_utc=since)
        await import_statistics_ws(token, statistic_id, rows)
    if full_sync:
        mark_full_sync_done(conn)


async def sync_async(conn: sqlite3.Connection, *, data_changed: bool = False) -> None:
    """Publish MQTT entities and optionally refresh external statistics."""
    if not bridge_enabled():
        return
    token = supervisor_token()
    if not token:
        return
    try:
        publish_entities(conn, token)
        should_import = data_changed or db.get_state(conn, FULL_SYNC_KEY) != "1"
        if energy_statistics_enabled() and should_import:
            await import_water_statistics(conn, token)
    except Exception:  # noqa: BLE001 - bridge must never break the scheduler
        traceback.print_exc()


def sync(conn: sqlite3.Connection, *, data_changed: bool = False) -> None:
    """Start HA bridge work on a daemon thread so scraping never waits on HA."""
    if not bridge_enabled():
        return
    if not supervisor_token():
        return

    def _run() -> None:
        thread_conn = db.connect()
        try:
            asyncio.run(sync_async(thread_conn, data_changed=data_changed))
        except Exception:  # noqa: BLE001
            traceback.print_exc()
        finally:
            thread_conn.close()

    threading.Thread(target=_run, daemon=True, name="ha-bridge").start()
