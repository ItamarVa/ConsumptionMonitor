"""Self-check for the mycitygrid payload parsers, which are written against a guessed API.

Every payload here is synthetic: the checks never touch the network and never read the
stored credentials, which matters because the response shapes are unverified and the only
protection against a confident misparse is that a wrong shape raises loudly. Covers the
ngx-charts bucket shape, UTC conversion, both Israeli DST edges, meter discovery and the
credential-free error messages. `tests/test_source_session.py` covers the HTTP half.
Plain asserts so `python tests/test_source_parsing.py` and `pytest` both work.
"""

from __future__ import annotations

import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from consumption import config, readings  # noqa: E402
from consumption.readings import SourceError  # noqa: E402

UTC = timezone.utc


def _payload(hours, value=1.0, label="01/15/2026"):
    """The recon's best guess at the response: ngx-charts grouped bars, one per hour."""
    return {
        "name": label,
        "values": [
            {"name": f"{hour:02d}:00", "series": [{"name": "Consumption", "value": value}]}
            for hour in hours
        ],
    }


def _hours_utc(result):
    return [r.hour_start for r in result]


def _raises(exc_type, call, message_contains=""):
    """Kept local, not shared, so each self-check file runs on its own."""
    try:
        call()
    except exc_type as exc:
        assert message_contains in str(exc), f"expected {message_contains!r} in {exc}"
        return str(exc)
    raise AssertionError(f"expected {exc_type.__name__}, nothing was raised")


def test_well_formed_day_converts_to_utc() -> None:
    """Winter is UTC+2, so local midnight is 22:00 UTC on the previous day."""
    result = readings.parse_hourly(_payload(range(24), 0.5), "electricity", 77, date(2026, 1, 15))
    assert len(result) == 24, len(result)
    assert result[0].hour_start == datetime(2026, 1, 14, 22, tzinfo=UTC), result[0]
    assert result[-1].hour_start == datetime(2026, 1, 15, 21, tzinfo=UTC), result[-1]
    assert result[0].meter_id == "77", "the meter id must be stored as text"
    assert result[0].unit == "kWh" and result[0].value == 0.5
    assert all(r.hour_start.minute == 0 and r.hour_start.second == 0 for r in result)
    assert len({r.hour_start for r in result}) == 24, "one reading per hour, no overwrites"

    summer = readings.parse_hourly(_payload([0]), "water", "w1", date(2026, 6, 15))
    assert summer[0].hour_start == datetime(2026, 6, 14, 21, tzinfo=UTC), summer[0]
    assert summer[0].unit == "m3" and summer[0].utility == "water"


def test_time_of_use_bands_are_summed() -> None:
    """Six series means time-of-use bands; the hour's consumption is all of them."""
    bucket = {
        "name": "07:00",
        "series": [{"name": f"band {i}", "value": i / 10} for i in range(1, 7)],
    }
    result = readings.parse_hourly({"values": [bucket]}, "electricity", "m1", date(2026, 1, 15))
    assert len(result) == 1 and round(result[0].value, 4) == 2.1, result


def test_alternative_bucket_labels() -> None:
    """The label format is unverified, so a bare hour and an ISO timestamp both parse."""
    bare = {"values": [{"name": 5, "value": 2.0}]}
    result = readings.parse_hourly(bare, "electricity", "m1", date(2026, 1, 15))
    assert result[0].hour_start == datetime(2026, 1, 15, 3, tzinfo=UTC), result

    iso = {"values": [{"name": "2026-01-15T05:00:00", "series": [{"value": 2.0}]}]}
    assert _hours_utc(readings.parse_hourly(iso, "electricity", "m1", date(2026, 1, 15))) == [
        datetime(2026, 1, 15, 3, tzinfo=UTC)
    ]


def test_empty_but_valid_day_returns_nothing() -> None:
    for empty in ({"name": "01/15/2026", "values": []}, {}, [], None):
        assert readings.parse_hourly(empty, "electricity", "m1", date(2026, 1, 15)) == []


def test_malformed_payloads_raise_rather_than_return_nothing() -> None:
    day = date(2026, 1, 15)
    cases = [
        ({"name": "x"}, "'values' list"),
        ({"values": "00:00"}, "buckets to be a list"),
        ({"values": ["00:00"]}, "'name' label"),
        ({"values": [{"name": "00:00"}]}, "'series' list or a 'value'"),
        ({"values": [{"name": "00:00", "series": [{"value": "1.0"}]}]}, "expected a number"),
        ({"values": [{"name": "00:00", "value": -3}]}, "negative hourly consumption"),
        ({"values": [{"name": "00:30", "value": 1}]}, "start on the hour"),
        ({"values": [{"name": "24:00", "value": 1}]}, "0-23 local hour"),
        ({"values": [{"name": "teatime", "value": 1}]}, "ISO timestamp"),
        ({"values": [{"name": "2026-01-14T05:00:00", "value": 1}]}, "not what came back"),
        # An ordinary day has no repeated hour, so the second 05:00 is caught as a collision.
        ({"values": [{"name": "05:00", "value": 1}] * 2}, "both land on"),
    ]
    for payload, expected in cases:
        _raises(
            SourceError,
            lambda p=payload: readings.parse_hourly(p, "electricity", "m1", day),
            expected,
        )

    # Even the genuinely ambiguous autumn hour cannot appear a third time.
    _raises(
        SourceError,
        lambda: readings.parse_hourly(
            _payload([0, 1, 1, 1]), "electricity", "m1", date(2026, 10, 25)
        ),
        "repeats the 01:00 bucket 3 times",
    )


def test_error_messages_carry_a_short_redacted_excerpt() -> None:
    payload = {
        "access_token": "secret-token-value",
        "password": "hunter2",
        "values": [{"name": "00:00"}],
    }
    message = _raises(
        SourceError,
        lambda: readings.parse_hourly(payload, "electricity", "m1", date(2026, 1, 15)),
        "'series' list or a 'value'",
    )
    assert "secret-token-value" not in message and "hunter2" not in message, message

    long_excerpt = readings.excerpt({"values": [{"name": f"{i:02d}:00"} for i in range(24)]})
    assert len(long_excerpt) <= 244 and long_excerpt.endswith("..."), long_excerpt
    assert "\n" not in long_excerpt, "an excerpt must stay on one line"


def test_spring_forward_day_has_23_hours() -> None:
    """2026-03-27: 02:00 local never happens, so the portal should send 23 buckets."""
    hours = [h for h in range(24) if h != 2]
    result = readings.parse_hourly(_payload(hours), "electricity", "m1", date(2026, 3, 27))
    assert len(result) == 23, len(result)
    assert len(set(_hours_utc(result))) == 23, "no two local hours may share a UTC hour"
    assert result[0].hour_start == datetime(2026, 3, 26, 22, tzinfo=UTC), result[0]
    assert result[2].hour_start == datetime(2026, 3, 27, 0, tzinfo=UTC), "03:00 local is 00:00 UTC"

    # A bucket for the hour that does not exist is dropped, not folded onto its neighbour.
    with_ghost = _payload(range(24))
    result = readings.parse_hourly(with_ghost, "electricity", "m1", date(2026, 3, 27))
    assert len(result) == 23, "the 02:00 bucket must not overwrite 03:00"
    assert len(set(_hours_utc(result))) == 23


def test_autumn_repeat_hour_keeps_both() -> None:
    """2026-10-25: 01:00 local happens twice, and the two are different UTC hours."""
    hours = [0, 1, 1] + list(range(2, 24))
    result = readings.parse_hourly(_payload(hours), "electricity", "m1", date(2026, 10, 25))
    assert len(result) == 25, len(result)
    assert len(set(_hours_utc(result))) == 25, "the repeat hour must not overwrite itself"
    assert _hours_utc(result)[1:3] == [
        datetime(2026, 10, 24, 22, tzinfo=UTC),
        datetime(2026, 10, 24, 23, tzinfo=UTC),
    ], result[1:3]
    assert result[-1].hour_start == datetime(2026, 10, 25, 21, tzinfo=UTC), result[-1]


def test_meter_discovery() -> None:
    payload = {
        "roles": ["User"],
        "addresses": [
            {"isActive": False, "meters": [{"meterId": 1, "type": 1}]},
            {
                "isActive": True,
                "meters": [
                    {"meterId": 11, "type": 1},
                    {"meterId": 12, "type": 1},  # a household may hold two of a type
                    {"meterId": 21, "type": 2},
                    {"meterId": 31, "type": 3},  # solar: not one of our utilities
                ],
            },
        ],
    }
    assert readings.parse_meters(payload) == {"electricity": ["11", "12"], "water": ["21"]}

    no_water = {"addresses": [{"isActive": True, "meters": [{"meterId": 11, "type": 1}]}]}
    assert readings.parse_meters(no_water)["water"] == [], "no water meter is a fact, not an error"

    for payload, expected in [
        ({}, "non-empty 'addresses' list"),
        ({"addresses": []}, "non-empty 'addresses' list"),
        ({"addresses": [{"isActive": False, "meters": []}]}, "isActive true"),
        ({"addresses": [{"isActive": True}]}, "'meters' list"),
        ({"addresses": [{"isActive": True, "meters": [{"type": 1}]}]}, "'meterId'"),
        ({"addresses": [{"isActive": True, "meters": []}]}, "lists no meters at all"),
    ]:
        _raises(SourceError, lambda p=payload: readings.parse_meters(p), expected)


def test_local_timezone_is_the_one_the_parser_assumes() -> None:
    assert str(config.LOCAL_TZ) == "Asia/Jerusalem", config.LOCAL_TZ


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
        print(f"  ok  {test.__name__}")
    print(f"{len(tests)} payload-parsing self-checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
