"""Self-check for user/info meter discovery and redaction helpers (offline only).

Hourly chart parsing is obsolete — raw readings come from the meter reading log instead.
This file keeps the checks that still matter for login and meter discovery.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from consumption import config, readings  # noqa: E402
from consumption.readings import SourceError  # noqa: E402


def _raises(exc_type, call, message_contains=""):
    try:
        call()
    except exc_type as exc:
        assert message_contains in str(exc), f"expected {message_contains!r} in {exc}"
        return str(exc)
    raise AssertionError(f"expected {exc_type.__name__}, nothing was raised")


def test_meter_discovery() -> None:
    payload = {
        "roles": ["User"],
        "addresses": [
            {"isActive": False, "meters": [{"meterId": 1, "type": 1}]},
            {
                "isActive": True,
                "meters": [
                    {"meterId": 11, "type": 1},
                    {"meterId": 12, "type": 1},
                    {"meterId": 21, "type": 2},
                    {"meterId": 31, "type": 3},
                ],
            },
        ],
    }
    assert readings.parse_meters(payload) == {"electricity": ["11", "12"], "water": ["21"]}

    no_water = {"addresses": [{"isActive": True, "meters": [{"meterId": 11, "type": 1}]}]}
    assert readings.parse_meters(no_water)["water"] == []

    for payload, expected in [
        ({}, "non-empty 'addresses' list"),
        ({"addresses": []}, "non-empty 'addresses' list"),
        ({"addresses": [{"isActive": False, "meters": []}]}, "isActive true"),
        ({"addresses": [{"isActive": True}]}, "'meters' list"),
        ({"addresses": [{"isActive": True, "meters": [{"type": 1}]}]}, "'meterId'"),
        ({"addresses": [{"isActive": True, "meters": []}]}, "lists no meters at all"),
    ]:
        _raises(SourceError, lambda p=payload: readings.parse_meters(p), expected)


def test_error_messages_carry_a_short_redacted_excerpt() -> None:
    payload = {
        "access_token": "secret-token-value",
        "password": "hunter2",
        "addresses": [],
    }
    message = _raises(
        SourceError,
        lambda: readings.parse_meters(payload),
        "non-empty 'addresses' list",
    )
    assert "secret-token-value" not in message and "hunter2" not in message

    long_excerpt = readings.excerpt({"items": [{"meterDataId": i} for i in range(24)]})
    assert len(long_excerpt) <= 244 and long_excerpt.endswith("...")
    assert "\n" not in long_excerpt


def test_local_timezone_is_the_one_the_parser_assumes() -> None:
    assert str(config.LOCAL_TZ) == "Asia/Jerusalem"


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
        print(f"  ok  {test.__name__}")
    print(f"{len(tests)} parser self-checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
