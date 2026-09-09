"""Self-check for the mycitygrid adapter's HTTP half: login, token refresh and the day loop.

Every response here comes from a scripted stand-in, so the checks never touch the network
and never read the stored credentials - which matters, because the request shapes are
reverse-engineered and an accidental real request against a portal we have no account for
is exactly what must not happen. `tests/test_source_parsing.py` covers the payload half.
Plain asserts so `python tests/test_source_session.py` and `pytest` both work.
"""

from __future__ import annotations

import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from consumption import config, source  # noqa: E402
from consumption.readings import SourceError, SourceNotReady  # noqa: E402

UTC = timezone.utc


def _raises(exc_type, call, message_contains=""):
    """Kept local, not shared, so each self-check file runs on its own."""
    try:
        call()
    except exc_type as exc:
        assert message_contains in str(exc), f"expected {message_contains!r} in {exc}"
        return str(exc)
    raise AssertionError(f"expected {exc_type.__name__}, nothing was raised")


def _payload(hours, value=1.0):
    return {
        "name": "day",
        "values": [
            {"name": f"{hour:02d}:00", "series": [{"name": "Consumption", "value": value}]}
            for hour in hours
        ],
    }


class _FakeResponse:
    def __init__(self, status: int, payload: object) -> None:
        self.status = status
        self.body = (
            payload.encode("utf-8") if isinstance(payload, str) else json.dumps(payload).encode()
        )


class _FakeSession:
    """A Scrapling session stand-in: hands out scripted responses, records what was sent."""

    def __init__(self, script: list[_FakeResponse]) -> None:
        self._script = script
        self.sent: list[tuple[str, str, dict]] = []

    def _respond(self, method: str, url: str, **kwargs) -> _FakeResponse:
        self.sent.append((method, url, kwargs))
        return self._script.pop(0) if self._script else _FakeResponse(200, {})

    def get(self, url: str, **kwargs) -> _FakeResponse:
        return self._respond("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> _FakeResponse:
        return self._respond("POST", url, **kwargs)


def _token(access="tok-1", refresh="ref-1", expires_in=3600):
    return {"access_token": access, "refresh_token": refresh, "expires_in": expires_in}


def _staged(script):
    """A scripted session plus stored credentials, with the pacing delay stood down."""
    session = _FakeSession(script)
    stored = (
        config.MYCITYGRID_USERNAME,
        config.MYCITYGRID_PASSWORD,
        source.REQUEST_DELAY_SECONDS,
    )
    config.MYCITYGRID_USERNAME, config.MYCITYGRID_PASSWORD = "user@example.com", "pa ss:word"
    source.REQUEST_DELAY_SECONDS = 0.0  # these checks must not spend a second per request
    return session, stored


def _restore(stored) -> None:
    config.MYCITYGRID_USERNAME, config.MYCITYGRID_PASSWORD = stored[0], stored[1]
    source.REQUEST_DELAY_SECONDS = stored[2]


def test_login_sends_the_password_grant_and_bearers_every_later_request() -> None:
    session, stored = _staged([_FakeResponse(200, _token()), _FakeResponse(200, {})])
    try:
        source._login(session).get_json("user/info")
    finally:
        _restore(stored)

    method, url, kwargs = session.sent[0]
    assert (method, url) == ("POST", "https://www.mycitygrid.com/api/api/account/login")
    assert kwargs["data"] == {
        "grant_type": "password",
        "username": "user@example.com",
        "password": "pa ss:word",
        "clientId": "undefined",
    }, kwargs["data"]
    assert "Authorization" not in kwargs["headers"], "the token endpoint must get no bearer"
    assert kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"

    method, url, kwargs = session.sent[1]
    assert (method, url) == ("GET", "https://www.mycitygrid.com/api/api/user/info")
    assert kwargs["headers"]["Authorization"] == "Bearer tok-1", kwargs["headers"]


def test_rejected_credentials_are_not_a_transient_failure() -> None:
    session, stored = _staged([_FakeResponse(400, {"error": "invalid_grant"})])
    try:
        message = _raises(SourceNotReady, lambda: source._login(session), "set-credentials.bat")
    finally:
        _restore(stored)
    assert "pa ss:word" not in message, "the password must never reach an error message"


def test_a_401_refreshes_the_token_once_and_retries() -> None:
    session, stored = _staged(
        [
            _FakeResponse(200, _token()),
            _FakeResponse(401, {}),  # the token died mid-run
            _FakeResponse(200, _token(access="tok-2", refresh="ref-2")),
            _FakeResponse(200, {"ok": True}),
        ]
    )
    try:
        assert source._login(session).get_json("user/info") == {"ok": True}
    finally:
        _restore(stored)

    assert session.sent[2][2]["data"] == {
        "grant_type": "refresh_token",
        "client_id": "undefined",
        "refresh_token": "ref-1",
    }, session.sent[2][2]["data"]
    assert session.sent[3][2]["headers"]["Authorization"] == "Bearer tok-2"
    assert len(session.sent) == 4, "one refresh and one retry, not a login per request"


def test_a_stale_refresh_token_falls_back_to_one_password_login() -> None:
    session, stored = _staged(
        [
            _FakeResponse(200, _token()),
            _FakeResponse(401, {}),
            _FakeResponse(400, {"error": "invalid_grant"}),  # the refresh token is stale too
            _FakeResponse(200, _token(access="tok-3")),
            _FakeResponse(200, {"ok": True}),
        ]
    )
    try:
        assert source._login(session).get_json("user/info") == {"ok": True}
    finally:
        _restore(stored)
    assert session.sent[3][2]["data"]["grant_type"] == "password", session.sent[3][2]["data"]


def test_unusable_answers_are_source_errors() -> None:
    cases = [
        ([_FakeResponse(200, _token()), _FakeResponse(500, {})], "answered 500 to GET user/info"),
        ([_FakeResponse(200, _token()), _FakeResponse(200, "<html>login</html>")], "do not parse"),
        ([_FakeResponse(200, {"token_type": "bearer"})], "no access_token"),
        ([_FakeResponse(503, {})], "answered 503 to the login request"),
    ]
    for script, expected in cases:
        session, stored = _staged(script)
        try:
            _raises(SourceError, lambda s=session: source._login(s).get_json("user/info"), expected)
        finally:
            _restore(stored)


def test_the_meter_list_is_fetched_once_per_session() -> None:
    user_info = {"addresses": [{"isActive": True, "meters": [{"meterId": 11, "type": 1}]}]}
    session, stored = _staged([_FakeResponse(200, _token()), _FakeResponse(200, user_info)])
    try:
        portal = source._login(session)
        assert portal.meters("electricity") == ["11"]
        assert portal.meters("water") == []
    finally:
        _restore(stored)
    assert len(session.sent) == 2, "user/info must not be re-fetched for the second utility"


def test_token_expiry_reads_both_forms() -> None:
    now = datetime.now(UTC)
    assert source._token_expiry({"expires_in": 3600}) - now > timedelta(minutes=55)
    parsed = source._token_expiry({".expires": "Wed, 09 Sep 2026 21:00:00 GMT"})
    assert parsed == datetime(2026, 9, 9, 21, tzinfo=UTC), parsed
    # Neither field present: a short lifetime, so the next request renews rather than 401s.
    assert source._token_expiry({}) - now < timedelta(minutes=16)


class _FakePortal:
    """A logged-in session stand-in: records every request instead of making one."""

    def __init__(self, meters: dict[str, list[str]], payloads: dict | None = None) -> None:
        self._meters = meters
        self._payloads = payloads or {}
        self.calls: list[dict] = []

    def meters(self, utility: str) -> list[str]:
        return self._meters.get(utility, [])

    def get_json(self, path: str, params: dict | None = None) -> object:
        self.calls.append(params or {})
        return self._payloads.get((params or {})["fromDate"], _payload([0]))


def test_day_loop_asks_one_local_day_at_a_time() -> None:
    portal = _FakePortal({"electricity": ["11", "12"]})
    result = source._fetch_range(portal, "electricity", date(2026, 1, 15), date(2026, 1, 17))
    assert len(portal.calls) == 6, "three days times two meters"
    assert portal.calls[0] == {
        "meterId": "11",
        "period": "hourly",
        "fromDate": "01/15/2026",
        "toDate": "01/15/2026",
    }, portal.calls[0]
    assert len(result) == 6 and len({(r.meter_id, r.hour_start) for r in result}) == 6


def test_missing_meter_type_fetches_nothing() -> None:
    portal = _FakePortal({"electricity": ["11"]})
    assert source._fetch_range(portal, "water", date(2026, 1, 15), date(2026, 1, 15)) == []
    assert portal.calls == [], "a utility with no meter must not cost a request"


def test_request_ceiling_refuses_an_oversized_range() -> None:
    portal = _FakePortal({"electricity": ["11", "12"]})
    start = date(2020, 1, 1)
    _raises(
        SourceError,
        lambda: source._fetch_range(portal, "electricity", start, start + timedelta(days=800)),
        "over the 800 allowed in one call",
    )
    assert portal.calls == [], "the ceiling must be checked before any request is sent"


def test_repeated_hour_across_days_is_refused() -> None:
    """If bucket labels were not the requested day, two days would collide. Fail loudly."""
    same_day_twice = {
        "01/15/2026": _payload([0]),
        "01/16/2026": {"values": [{"name": "2026-01-15T00:00:00", "value": 1.0}]},
    }
    portal = _FakePortal({"electricity": ["11"]}, same_day_twice)
    _raises(
        SourceError,
        lambda: source._fetch_range(portal, "electricity", date(2026, 1, 15), date(2026, 1, 16)),
        "not what came back",
    )


def test_fetch_hourly_validates_before_reaching_the_portal() -> None:
    """None of these may open a session, so no credential is read and no request is sent."""
    _raises(ValueError, lambda: source.fetch_hourly("gas", date(2026, 1, 1), date(2026, 1, 1)))
    _raises(
        ValueError,
        lambda: source.fetch_hourly("water", date(2026, 1, 2), date(2026, 1, 1)),
        "end date is before start date",
    )

    stored = (config.MYCITYGRID_USERNAME, config.MYCITYGRID_PASSWORD)
    config.MYCITYGRID_USERNAME, config.MYCITYGRID_PASSWORD = "", ""
    try:
        _raises(
            SourceNotReady,
            lambda: source.fetch_hourly("water", date(2026, 1, 1), date(2026, 1, 1)),
            "set-credentials.bat",
        )
    finally:
        config.MYCITYGRID_USERNAME, config.MYCITYGRID_PASSWORD = stored


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
        print(f"  ok  {test.__name__}")
    print(f"{len(tests)} adapter session self-checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
