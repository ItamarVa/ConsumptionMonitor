"""Frozen contract for raw meter readings and the storage/adapter surface.

Every Wave 1 stream imports from here only; this file is not edited after Wave 0.
Defines MeterReading, IntervalReading, SCHEMA, function signatures, and shared constants.
Storage and adapter modules implement the signatures; readings.py owns SourceError types
(re-exported here as the public import path).
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal

import sqlite3

from .readings import SourceError, SourceNotReady

Utility = Literal["electricity", "water"]
Direction = Literal["import", "export", "water"]
TariffBand = Literal[1, 2, 3] | None

UTILITIES: tuple[Utility, ...] = ("electricity", "water")
UNITS: dict[tuple[str, str], str] = {
    ("electricity", "import"): "kWh",
    ("electricity", "export"): "kWh",
    ("water", "water"): "m3",
}
READING_LOG_PATH = "meterdata"


@dataclass(frozen=True, slots=True)
class MeterReading:
    meter_data_id: int
    meter_id: str
    utility: str
    reading_time: datetime
    local_date: date
    total_import_kwh: float | None = None
    total_export_kwh: float | None = None
    tou1_import_kwh: float | None = None
    tou2_import_kwh: float | None = None
    tou3_import_kwh: float | None = None
    tou1_export_kwh: float | None = None
    tou2_export_kwh: float | None = None
    tou3_export_kwh: float | None = None
    total_water_data: float | None = None
    total_consumption: float | None = None
    total_production: float | None = None
    consumption1: float | None = None
    consumption2: float | None = None
    consumption3: float | None = None
    production1: float | None = None
    production3: float | None = None
    v1: float | None = None
    v2: float | None = None
    v3: float | None = None
    a1: float | None = None
    a2: float | None = None
    a3: float | None = None
    cos: float | None = None
    kvar_h: float | None = None
    max_dmd: float | None = None
    has_leak: bool = False
    back_flow: bool = False
    broken_pipe: bool = False
    empty_pipe: bool = False
    low_battery: bool = False
    magnetic_tamper: bool = False
    meter_error: bool = False
    multiplier_symbol_count: int | None = None
    added_manually: bool = False
    raw_json: str | None = None
    updated_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class IntervalReading:
    meter_id: str
    utility: str
    direction: str
    start_time_utc: datetime
    end_time_utc: datetime
    value: float
    unit: str
    tariff_band: TariffBand = None


# Migration: DROP TABLE IF EXISTS reading; the old hourly table is abandoned.
SCHEMA = """
CREATE TABLE IF NOT EXISTS meter_reading (
    meter_data_id INTEGER PRIMARY KEY,
    meter_id TEXT NOT NULL,
    utility TEXT NOT NULL,
    reading_time_utc TEXT NOT NULL,
    local_date TEXT NOT NULL,
    total_import_kwh REAL,
    total_export_kwh REAL,
    tou1_import_kwh REAL, tou2_import_kwh REAL, tou3_import_kwh REAL,
    tou1_export_kwh REAL, tou2_export_kwh REAL, tou3_export_kwh REAL,
    total_water_data REAL,
    total_consumption REAL, total_production REAL,
    consumption1 REAL, consumption2 REAL, consumption3 REAL,
    production1 REAL, production3 REAL,
    v1 REAL, v2 REAL, v3 REAL, a1 REAL, a2 REAL, a3 REAL,
    cos REAL, kvar_h REAL, max_dmd REAL,
    has_leak INTEGER NOT NULL DEFAULT 0, back_flow INTEGER NOT NULL DEFAULT 0,
    broken_pipe INTEGER NOT NULL DEFAULT 0, empty_pipe INTEGER NOT NULL DEFAULT 0,
    low_battery INTEGER NOT NULL DEFAULT 0, magnetic_tamper INTEGER NOT NULL DEFAULT 0,
    meter_error INTEGER NOT NULL DEFAULT 0,
    multiplier_symbol_count INTEGER,
    added_manually INTEGER NOT NULL DEFAULT 0,
    raw_json TEXT,
    updated_at TEXT NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS meter_reading_by_meter_time
    ON meter_reading (meter_id, reading_time_utc);
CREATE INDEX IF NOT EXISTS meter_reading_by_local_date
    ON meter_reading (utility, local_date);

CREATE TABLE IF NOT EXISTS job_state (
    job          TEXT PRIMARY KEY,
    last_run_utc TEXT,
    last_ok_utc  TEXT,
    rows_written INTEGER NOT NULL DEFAULT 0,
    last_error   TEXT
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS app_state (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
) WITHOUT ROWID;
"""


def upsert_meter_readings(conn: sqlite3.Connection, readings: Iterable[MeterReading]) -> int:
    raise NotImplementedError


def meter_readings(
    conn: sqlite3.Connection, meter_id: str, start: date, end: date
) -> list[dict]:
    raise NotImplementedError


def intervals(
    conn: sqlite3.Connection, meter_id: str, direction: str, start: date, end: date
) -> list[dict]:
    raise NotImplementedError


def daily_totals(
    conn: sqlite3.Connection, utility: str, direction: str, start: date, end: date
) -> list[dict]:
    raise NotImplementedError


def monthly_totals(
    conn: sqlite3.Connection, utility: str, direction: str, start: date, end: date
) -> list[dict]:
    raise NotImplementedError


def yearly_totals(
    conn: sqlite3.Connection, utility: str, direction: str, start: date, end: date
) -> list[dict]:
    raise NotImplementedError


def latest_reading(conn: sqlite3.Connection, meter_id: str) -> dict | None:
    raise NotImplementedError


def alert_flags(conn: sqlite3.Connection, meter_id: str) -> dict:
    raise NotImplementedError


def coverage(conn: sqlite3.Connection) -> dict:
    raise NotImplementedError


def fetch_readings(utility: str, start: date, end: date) -> list[MeterReading]:
    raise NotImplementedError
