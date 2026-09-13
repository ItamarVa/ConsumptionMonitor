"""Home Assistant MQTT device discovery and state payloads for ConsumptionMonitor.

Builds one retained device-discovery document and a single JSON state object that
feeds every entity via value_template. Register sensors deliberately omit
state_class so the recorder does not compile them; the Energy dashboard uses
external statistics from ha_statistics instead. Depends on db.py and jobs.py.
"""

from __future__ import annotations

import re
import sqlite3
from datetime import date

from . import config, db, jobs
from .records import UNITS, UTILITIES

DEVICE_ID = "consumptionmonitor"
DISCOVERY_TOPIC = f"homeassistant/device/{DEVICE_ID}/config"
STATE_TOPIC = f"{DEVICE_ID}/state"

_ALERT_FLAGS = (
    "has_leak",
    "back_flow",
    "broken_pipe",
    "empty_pipe",
    "low_battery",
    "magnetic_tamper",
    "meter_error",
)

def _ha_unit(utility: str, direction: str) -> str:
    unit = UNITS[(utility, direction)]
    return "m³" if unit == "m3" else unit


def _safe_key(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]", "_", text)


def _meter_ids(conn: sqlite3.Connection, utility: str) -> list[str]:
    cur = conn.execute(
        "SELECT DISTINCT meter_id FROM meter_reading WHERE utility = ? ORDER BY meter_id",
        (utility,),
    )
    return [row[0] for row in cur]


def _directions(utility: str) -> tuple[str, ...]:
    return ("water",) if utility == "water" else ("import", "export")


def _register_value(latest: dict | None, utility: str, direction: str) -> float | None:
    if not latest:
        return None
    if utility == "water":
        return latest.get("total_water_data")
    if direction == "export":
        return latest.get("total_export_kwh")
    return latest.get("total_import_kwh")


def _period_total(
    conn: sqlite3.Connection, utility: str, direction: str, start: date, end: date
) -> float | None:
    row = db.period_total(conn, utility, direction, start, end)
    if not row:
        return None
    return round(row["value"], 4)


def _latest_scraper_error(conn: sqlite3.Connection) -> str | None:
    states = db.job_states(conn)
    errors = [s["last_error"] for s in states.values() if s.get("last_error")]
    return errors[-1] if errors else None


def _sensor_cmp(
    key: str,
    name: str,
    *,
    unit: str | None = None,
    device_class: str | None = None,
) -> dict:
    cmp: dict = {
        "p": "sensor",
        "unique_id": f"{DEVICE_ID}_{key}",
        "name": name,
        "value_template": f"{{{{ value_json.{key} }}}}",
    }
    if unit:
        cmp["unit_of_measurement"] = unit
    if device_class:
        cmp["device_class"] = device_class
    return cmp


def _binary_cmp(key: str, name: str) -> dict:
    return {
        "p": "binary_sensor",
        "unique_id": f"{DEVICE_ID}_{key}",
        "name": name,
        "device_class": "problem",
        "value_template": f"{{{{ 'ON' if value_json.{key} else 'OFF' }}}}",
    }


def _timestamp_cmp(key: str, name: str) -> dict:
    return {
        "p": "sensor",
        "unique_id": f"{DEVICE_ID}_{key}",
        "name": name,
        "device_class": "timestamp",
        "value_template": f"{{{{ value_json.{key} | default('', true) }}}}",
    }


def build_discovery(conn: sqlite3.Connection, addon_version: str = "") -> dict:
    """Return the retained MQTT device-discovery payload."""
    cmps: dict[str, dict] = {
        "elec_import_register": _sensor_cmp(
            "elec_import_register",
            "Electricity import register",
            unit="kWh",
            device_class="energy",
        ),
        "elec_export_register": _sensor_cmp(
            "elec_export_register",
            "Electricity export register",
            unit="kWh",
            device_class="energy",
        ),
        "water_register": _sensor_cmp(
            "water_register",
            "Water register",
            unit="m³",
            device_class="water",
        ),
    }

    for utility in UTILITIES:
        for direction in _directions(utility):
            prefix = "water" if utility == "water" else f"elec_{direction}"
            unit = _ha_unit(utility, direction)
            labels = {
                "today": "today",
                "this_month": "this month",
                "year_to_date": "year to date",
            }
            for period_key, label in labels.items():
                key = f"{prefix}_{period_key}"
                title = f"{utility.title()} {direction} {label}".replace("water water", "water")
                cmps[key] = _sensor_cmp(key, title, unit=unit)

    for utility in UTILITIES:
        for meter_id in _meter_ids(conn, utility):
            safe = _safe_key(meter_id)
            for flag in _ALERT_FLAGS:
                key = f"alert_{safe}_{flag}"
                name = f"{meter_id} {flag.replace('_', ' ')}"
                cmps[key] = _binary_cmp(key, name)

    cmps["last_reading_electricity"] = _timestamp_cmp(
        "last_reading_electricity",
        "Last electricity reading",
    )
    cmps["last_reading_water"] = _timestamp_cmp(
        "last_reading_water",
        "Last water reading",
    )
    cmps["last_scraper_error"] = _sensor_cmp(
        "last_scraper_error",
        "Last scraper error",
    )

    return {
        "dev": {
            "ids": [DEVICE_ID],
            "name": "ConsumptionMonitor",
            "sw": addon_version or "dev",
        },
        "o": {
            "name": "ConsumptionMonitor",
            "sw": addon_version or "dev",
        },
        "state_topic": STATE_TOPIC,
        "qos": 0,
        "cmps": cmps,
    }


def build_state(conn: sqlite3.Connection) -> dict:
    """Return the single JSON object published to STATE_TOPIC."""
    today = jobs.local_today()
    month_start = date(today.year, today.month, 1)
    year_start = date(today.year, 1, 1)
    cov = db.coverage(conn)
    state: dict = {}

    for utility in UTILITIES:
        meters = _meter_ids(conn, utility)
        latest = db.latest_reading(conn, meters[0]) if meters else None
        for direction in _directions(utility):
            prefix = "water" if utility == "water" else f"elec_{direction}"
            reg = _register_value(latest, utility, direction)
            if prefix == "water":
                state["water_register"] = reg
            elif direction == "import":
                state["elec_import_register"] = reg
            else:
                state["elec_export_register"] = reg
            for period_key, start in (
                ("today", today),
                ("this_month", month_start),
                ("year_to_date", year_start),
            ):
                state[f"{prefix}_{period_key}"] = _period_total(
                    conn, utility, direction, start, today
                )

        last_utc = cov.get(utility, {}).get("last_reading_utc")
        if utility == "electricity":
            state["last_reading_electricity"] = last_utc
        else:
            state["last_reading_water"] = last_utc

        for meter_id in meters:
            safe = _safe_key(meter_id)
            flags = db.alert_flags(conn, meter_id)
            for flag in _ALERT_FLAGS:
                state[f"alert_{safe}_{flag}"] = flags[flag]

    err = _latest_scraper_error(conn)
    state["last_scraper_error"] = err[:255] if err else None
    return state
