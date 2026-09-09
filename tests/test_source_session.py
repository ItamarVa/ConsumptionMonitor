"""Self-check for the mycitygrid adapter HTTP half: login, token refresh, reading-log fetch.

Every response comes from a scripted stand-in, so these checks never touch the network or
read stored credentials. `tests/test_reading_log.py` covers row parsing.
"""

from __future__ import annotations

import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from consumption import config, source  # noqa: E402
from consumption.readings import SourceError, SourceNotReady  # noqa: E402
from consumption.records import READING_LOG_PATH  # noqa: E402

UTC = timezone.utc


def _raises(exc_type, call, message_contains=""):
    try:
        call()
    except exc_type as exc:
        assert message_contains in str(exc), f"expected {message_contains!r} in {exc}"
        return str(exc)
    raise AssertionError(f"expected {exc_type.__name__}, nothing was raised")


class _FakeResponse:
    def __init__(self, status: int, payload: object) -> None:
        self.status = status
        self.body = (
            payload.encode("utf-8") if isinstance(payload, str) else json.dumps(payload).encode()
        )


class _FakeSession:
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
    session = _FakeSession(script)
    stored = (
        config.MYCITYGRID_USERNAME,
        config.MYCITYGRID_PASSWORD,
        source.REQUEST_DELAY_SECONDS,
    )
    config.MYCITYGRID_USERNAME, config.MYCITYGRID_PASSWORD = "user@example.com", "pa ss:word"
    source.REQUEST_DELAY_SECONDS = 0.0
    return session, stored


def _restore(stored) -> None:
    config.MYCITYGRID_USERNAME, config.MYCITYGRID_PASSWORD = stored[0], stored[1]
    source.REQUEST_DELAY_SECONDS = stored[2]


def _reading_page(meter_data_id: int = 1, has_next: bool = False) -> dict:
    return {
        "totalItemCount": 1,
        "pageCount": 1,
        "hasNextPage": has_next,
        "items": [
            {
                "meterDataId": meter_data_id,
                "readingTime": "2026-01-15T08:00:00+02:00",
                "totalImportKwH": 100.0,
            }
        ],
    }


def test_login_sends_the_password_grant_and_bearers_every_later_request() -> None:
    session, stored = _staged([_FakeResponse(200, _token()), _FakeResponse(200, {})])
    try:
        source._login(session).get_json("user/info")
    finally:
        _restore(stored)

    method, url, kwargs = session.sent[0]
    assert (method, url) == ("POST", "https://www.mycitygrid.com/api/api/account/login")
    assert kwargs["data"]["grant_type"] == "password"
    assert "Authorization" not in kwargs["headers"]

    method, url, kwargs = session.sent[1]
    assert kwargs["headers"]["Authorization"] == "Bearer tok-1"


def test_rejected_credentials_are_not_a_transient_failure() -> None:
    session, stored = _staged([_FakeResponse(400, {"error": "invalid_grant"})])
    try:
        message = _raises(SourceNotReady, lambda: source._login(session), "set-credentials.bat")
    finally:
        _restore(stored)
    assert "pa ss:word" not in message


def test_a_401_refreshes_the_token_once_and_retries() -> None:
    session, stored = _staged(
        [
            _FakeResponse(200, _token()),
            _FakeResponse(401, {}),
            _FakeResponse(200, _token(access="tok-2", refresh="ref-2")),
            _FakeResponse(200, {"ok": True}),
        ]
    )
    try:
        assert source._login(session).get_json("user/info") == {"ok": True}
    finally:
        _restore(stored)
    assert session.sent[3][2]["headers"]["Authorization"] == "Bearer tok-2"
    assert len(session.sent) == 4


def test_the_meter_list_is_fetched_once_per_session() -> None:
    user_info = {"addresses": [{"isActive": True, "meters": [{"meterId": 11, "type": 1}]}]}
    session, stored = _staged([_FakeResponse(200, _token()), _FakeResponse(200, user_info)])
    try:
        portal = source._login(session)
        assert portal.meters("electricity") == ["11"]
        assert portal.meters("water") == []
    finally:
        _restore(stored)
    assert len(session.sent) == 2


def test_token_expiry_reads_both_forms() -> None:
    now = datetime.now(UTC)
    assert source._token_expiry({"expires_in": 3600}) - now > timedelta(minutes=55)
    parsed = source._token_expiry({".expires": "Wed, 09 Sep 2026 21:00:00 GMT"})
    assert parsed == datetime(2026, 9, 9, 21, tzinfo=UTC)
    assert source._token_expiry({}) - now < timedelta(minutes=16)


class _FakePortal:
    def __init__(self, meters: dict[str, list[str]], pages: list[dict] | None = None) -> None:
        self._meters = meters
        self._pages = pages or [_reading_page()]
        self.calls: list[dict] = []

    def meters(self, utility: str) -> list[str]:
        return self._meters.get(utility, [])

    def get_json(self, path: str, params: dict[str, None] | dict[str, str] | None = None) -> object:
        self.calls.append(params or {})
        if path != READING_LOG_PATH:
            return {}
        page_number = int((params or {}).get("pageNumber", "1"))
        if page_number <= len(self._pages):
            return self._pages[page_number - 1]
        return _reading_page(has_next=False)


def test_reading_log_uses_date_range_and_paginates() -> None:
    pages = [_reading_page(1, has_next=True), _reading_page(2, has_next=False)]
    portal = _FakePortal({"electricity": ["11"]}, pages)
    result = source._fetch_meter_readings(
        portal, "electricity", "11", date(2026, 1, 15), date(2026, 1, 15)
    )
    assert len(result) == 2
    assert portal.calls[0]["fromDate"] == "01/15/2026"
    assert portal.calls[0]["toDate"] == "01/15/2026"
    assert portal.calls[0]["pageNumber"] == "1"
    assert portal.calls[1]["pageNumber"] == "2"
    assert "orderByProperty" not in portal.calls[0]


def test_missing_meter_type_fetches_nothing() -> None:
    portal = _FakePortal({"electricity": ["11"]})
    assert source._fetch_readings(portal, "water", date(2026, 1, 15), date(2026, 1, 15)) == []
    assert portal.calls == []


def test_fetch_readings_validates_before_reaching_the_portal() -> None:
    _raises(ValueError, lambda: source.fetch_readings("gas", date(2026, 1, 1), date(2026, 1, 1)))
    _raises(
        ValueError,
        lambda: source.fetch_readings("water", date(2026, 1, 2), date(2026, 1, 1)),
        "end date is before start date",
    )

    stored = (config.MYCITYGRID_USERNAME, config.MYCITYGRID_PASSWORD)
    config.MYCITYGRID_USERNAME, config.MYCITYGRID_PASSWORD = "", ""
    try:
        _raises(
            SourceNotReady,
            lambda: source.fetch_readings("water", date(2026, 1, 1), date(2026, 1, 1)),
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
