"""Offline self-checks for Home Assistant MQTT discovery and state payloads."""

from __future__ import annotations

import sys
import tempfile
from contextlib import contextmanager
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from consumption import db, jobs  # noqa: E402
from consumption.ha_entities import (  # noqa: E402
    DEVICE_ID,
    DISCOVERY_TOPIC,
    STATE_TOPIC,
    build_discovery,
    build_state,
)
from consumption.records import MeterReading  # noqa: E402

UTC = timezone.utc


@contextmanager
def _conn():
    with tempfile.TemporaryDirectory() as tmp:
        conn = db.connect(Path(tmp) / "t.sqlite")
        try:
            yield conn
        finally:
            conn.close()


def _reading(
    meter_data_id: int,
    when: datetime,
    local: date,
    *,
    utility: str = "electricity",
    meter_id: str = "m-e1",
    import_kwh: float = 10.0,
    export_kwh: float = 1.0,
    water: float | None = None,
    has_leak: bool = False,
) -> MeterReading:
    return MeterReading(
        meter_data_id=meter_data_id,
        meter_id=meter_id,
        utility=utility,
        reading_time=when,
        local_date=local,
        total_import_kwh=import_kwh if utility == "electricity" else None,
        total_export_kwh=export_kwh if utility == "electricity" else None,
        total_water_data=water if utility == "water" else None,
        has_leak=has_leak,
    )


def test_discovery_contract() -> None:
    with _conn() as conn:
        payload = build_discovery(conn, "1.0.0")
    assert payload["state_topic"] == STATE_TOPIC
    assert payload["dev"]["ids"] == [DEVICE_ID]
    assert DISCOVERY_TOPIC == "homeassistant/device/consumptionmonitor/config"
    cmps = payload["cmps"]
    assert cmps["elec_import_register"]["device_class"] == "energy"
    assert cmps["elec_import_register"].get("state_class") is None
    assert cmps["water_register"]["unit_of_measurement"] == "m³"
    assert cmps["water_register"]["device_class"] == "water"
    assert "elec_import_today" in cmps
    assert "water_year_to_date" in cmps


def test_discovery_includes_alert_binary_sensors() -> None:
    with _conn() as conn:
        db.upsert_meter_readings(
            conn,
            [
                _reading(
                    1,
                    datetime(2026, 6, 1, 6, tzinfo=UTC),
                    date(2026, 6, 1),
                    has_leak=True,
                )
            ],
        )
        payload = build_discovery(conn, "1.0.0")
    assert payload["cmps"]["alert_m_e1_has_leak"]["p"] == "binary_sensor"
    assert payload["cmps"]["alert_m_e1_has_leak"]["device_class"] == "problem"


def test_state_registers_and_period_totals() -> None:
    today = jobs.local_today()
    with _conn() as conn:
        db.upsert_meter_readings(
            conn,
            [
                _reading(
                    1,
                    datetime(today.year, today.month, today.day, 6, tzinfo=UTC),
                    today,
                    import_kwh=100.0,
                    export_kwh=5.0,
                ),
                _reading(
                    2,
                    datetime(today.year, today.month, today.day, 12, tzinfo=UTC),
                    today,
                    import_kwh=106.0,
                    export_kwh=5.5,
                ),
                _reading(
                    3,
                    datetime(today.year, today.month, today.day, 8, tzinfo=UTC),
                    today,
                    utility="water",
                    meter_id="m-w1",
                    water=20.0,
                ),
                _reading(
                    4,
                    datetime(today.year, today.month, today.day, 14, tzinfo=UTC),
                    today,
                    utility="water",
                    meter_id="m-w1",
                    water=21.5,
                ),
            ],
        )
        state = build_state(conn)
    assert state["elec_import_register"] == 106.0
    assert state["elec_export_register"] == 5.5
    assert state["water_register"] == 21.5
    assert state["elec_import_today"] == 6.0
    assert state["water_today"] == 1.5
    assert state["last_reading_electricity"] is not None
    assert state["last_reading_water"] is not None


def test_state_reflects_alert_flags() -> None:
    today = jobs.local_today()
    with _conn() as conn:
        db.upsert_meter_readings(
            conn,
            [
                _reading(
                    1,
                    datetime(today.year, today.month, today.day, 6, tzinfo=UTC),
                    today,
                    has_leak=True,
                )
            ],
        )
        state = build_state(conn)
    assert state["alert_m_e1_has_leak"] is True
    assert state["alert_m_e1_back_flow"] is False


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
        print(f"  ok  {test.__name__}")
    print(f"{len(tests)} ha_entities self-checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
