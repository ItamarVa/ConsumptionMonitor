"""Adapter for www.mycitygrid.com - the only module that talks to the portal.

Built on Scrapling's FetcherSession: a plain HTTP session with browser impersonation,
which is all an OAuth-token-then-read-JSON portal needs. Raw readings come from the
paginated meter reading log (GET meterdata), not the chart endpoint. Row parsing lives
in reading_log.py so it can be corrected without touching the HTTP side.
Invariant: fetch_readings returns one MeterReading per portal meterDataId.
"""

from __future__ import annotations

import json
import time
from contextlib import contextmanager
from datetime import date, datetime, timedelta, timezone
from email.utils import parsedate_to_datetime  # the stdlib RFC 1123 parser, for `.expires`

from . import config, readings
from .records import MeterReading, READING_LOG_PATH
from .reading_log import parse_reading_page, parse_reading_row

# Re-exported: db.py, jobs.py, api.py and the self-checks import these names from here.
from .readings import Reading, SourceError, SourceNotReady, UNITS  # noqa: F401

SOURCE_READY = True

API_PREFIX = "/api/api/"
LOGIN_PATH = "account/login"
USER_INFO_PATH = "user/info"

CLIENT_ID = "undefined"
IMPERSONATE = "chrome"
TIMEOUT_SECONDS = 60

# The reading log is slow (often 20-60s per page); one second between pages is gentler
# than a user paging through the portal UI.
REQUEST_DELAY_SECONDS = 1.0
MAX_REQUESTS_PER_CALL = 800
_PAGE_SIZES = (200, 100, 50)

TOKEN_REFRESH_MARGIN = timedelta(minutes=2)
TOKEN_FALLBACK_LIFETIME = timedelta(minutes=15)

_BAD_CREDENTIALS = (
    "mycitygrid rejected the stored username and password. "
    "Double-click set-credentials.bat to enter them again."
)


def _url(path: str) -> str:
    return config.MYCITYGRID_BASE_URL.rstrip("/") + API_PREFIX + path


class _Portal:
    """A logged-in portal session: token lifetime, request pacing and JSON decoding."""

    def __init__(self, session) -> None:
        self._session = session
        self._access_token = ""
        self._refresh_token = ""
        self._expires_at = datetime.now(timezone.utc)
        self._last_request = 0.0
        self._meters: dict[str, list[str]] | None = None

    def login(self) -> None:
        self._authenticate(
            {
                "grant_type": "password",
                "username": config.MYCITYGRID_USERNAME,
                "password": config.MYCITYGRID_PASSWORD,
                "clientId": CLIENT_ID,
            },
            password_grant=True,
        )

    def get_json(self, path: str, params: dict[str, str] | None = None) -> object:
        self._renew_if_due()
        response = self._request("GET", _url(path), params=params)
        if response.status == 401:
            self._expires_at = datetime.now(timezone.utc)
            self._renew_if_due()
            response = self._request("GET", _url(path), params=params)
        if response.status >= 300:
            raise SourceError(f"the portal answered {response.status} to GET {path}")
        return _decode(response, path)

    def meters(self, utility: str) -> list[str]:
        if self._meters is None:
            self._meters = readings.parse_meters(self.get_json(USER_INFO_PATH))
        return self._meters.get(utility, [])

    def _authenticate(self, form: dict[str, str], *, password_grant: bool) -> None:
        response = self._request(
            "POST",
            _url(LOGIN_PATH),
            authenticated=False,
            data=form,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        if response.status in (400, 401):
            if password_grant:
                raise SourceNotReady(_BAD_CREDENTIALS)
            raise SourceError("the portal rejected the refresh token")
        if response.status >= 300:
            raise SourceError(f"the portal answered {response.status} to the login request")

        payload = _decode(response, LOGIN_PATH, quote_body=False)
        access = payload.get("access_token") if isinstance(payload, dict) else None
        if not isinstance(access, str) or not access:
            raise SourceError("the login response carried no access_token")
        self._access_token = access
        refresh = payload.get("refresh_token")
        self._refresh_token = refresh if isinstance(refresh, str) else ""
        self._expires_at = _token_expiry(payload)

    def _renew_if_due(self) -> None:
        if datetime.now(timezone.utc) + TOKEN_REFRESH_MARGIN < self._expires_at:
            return
        if self._refresh_token:
            try:
                self._authenticate(
                    {
                        "grant_type": "refresh_token",
                        "client_id": CLIENT_ID,
                        "refresh_token": self._refresh_token,
                    },
                    password_grant=False,
                )
                return
            except SourceError:
                self._refresh_token = ""
        self.login()

    def _request(self, method: str, url: str, *, authenticated: bool = True, **kwargs):
        waited = REQUEST_DELAY_SECONDS - (time.monotonic() - self._last_request)
        if self._last_request and waited > 0:
            time.sleep(waited)
        self._last_request = time.monotonic()

        headers = dict(kwargs.pop("headers", None) or {})
        if authenticated and self._access_token:
            headers["Authorization"] = f"Bearer {self._access_token}"
        send = self._session.post if method == "POST" else self._session.get
        try:
            return send(url, headers=headers, **kwargs)
        except Exception as exc:  # noqa: BLE001 - any transport failure is retryable later
            raise SourceError(f"could not reach the portal: {type(exc).__name__}: {exc}") from exc


def _decode(response, path: str, *, quote_body: bool = True) -> object:
    body = response.body.decode("utf-8", "replace").strip()
    try:
        return json.loads(body or "null")
    except ValueError as exc:
        detail = f": {readings.excerpt(body)}" if quote_body else ""
        raise SourceError(
            f"expected JSON from {path}, got {len(response.body)} bytes that do not parse"
            + detail
        ) from exc


def _token_expiry(payload: dict) -> datetime:
    now = datetime.now(timezone.utc)
    seconds = payload.get("expires_in")
    if isinstance(seconds, (int, float)) and not isinstance(seconds, bool) and seconds > 0:
        return now + timedelta(seconds=float(seconds))
    stamp = payload.get(".expires")
    if isinstance(stamp, str) and stamp:
        try:
            return parsedate_to_datetime(stamp).astimezone(timezone.utc)
        except (TypeError, ValueError):
            pass
    return now + TOKEN_FALLBACK_LIFETIME


@contextmanager
def portal_session():
    """A logged-in session. The access token lives for the duration of the `with` block."""
    if not config.credentials_present():
        raise SourceNotReady("No mycitygrid credentials stored. Run set-credentials.bat.")
    from scrapling.fetchers import FetcherSession

    with FetcherSession(
        impersonate=IMPERSONATE,
        stealthy_headers=True,
        timeout=TIMEOUT_SECONDS,
    ) as session:
        yield _login(session)


def _login(session) -> _Portal:
    portal = _Portal(session)
    portal.login()
    return portal


def _probe_page(portal: _Portal, base_params: dict[str, str]) -> tuple[dict, int]:
    """Pick the largest page size the portal accepts for this meter and date range.

    pageNumber is 1-based; sending pageNumber=0 answers HTTP 500.
    Never send orderByProperty — orderByProperty=readingDate also answers HTTP 500.
    """
    last_error: SourceError | None = None
    for size in _PAGE_SIZES:
        try:
            envelope = portal.get_json(
                READING_LOG_PATH,
                {**base_params, "pageNumber": "1", "pageSize": str(size)},
            )
            if not isinstance(envelope, dict):
                raise SourceError(
                    "expected a reading-log page object, got: " + readings.excerpt(envelope)
                )
            parse_reading_page(envelope)
            return envelope, size
        except SourceError as exc:
            last_error = exc
            if size == _PAGE_SIZES[-1]:
                raise
    raise last_error or SourceError("could not fetch the reading log")


def _fetch_meter_readings(
    portal: _Portal, utility: str, meter_id: str, start: date, end: date
) -> list[MeterReading]:
    base_params = {
        "meterId": meter_id,
        "fromDate": start.strftime("%m/%d/%Y"),
        "toDate": end.strftime("%m/%d/%Y"),
    }
    out: list[MeterReading] = []
    page_number = 1
    page_size: int | None = None
    requests = 0

    while True:
        if requests >= MAX_REQUESTS_PER_CALL:
            raise SourceError(
                f"fetching {utility} meter {meter_id} from {start} to {end} needed more than "
                f"{MAX_REQUESTS_PER_CALL} portal pages - fetch a shorter range"
            )
        requests += 1

        if page_number == 1 and page_size is None:
            envelope, page_size = _probe_page(portal, base_params)
        else:
            envelope = portal.get_json(
                READING_LOG_PATH,
                {
                    **base_params,
                    "pageNumber": str(page_number),
                    "pageSize": str(page_size),
                },
            )
            if not isinstance(envelope, dict):
                raise SourceError(
                    "expected a reading-log page object, got: " + readings.excerpt(envelope)
                )

        for item in parse_reading_page(envelope):
            out.append(parse_reading_row(item, utility, meter_id))

        if not envelope.get("hasNextPage"):
            break
        page_number += 1

    return out


def _fetch_readings(portal: _Portal, utility: str, start: date, end: date) -> list[MeterReading]:
    meter_ids = portal.meters(utility)
    if not meter_ids:
        return []

    out: list[MeterReading] = []
    for meter_id in meter_ids:
        out.extend(_fetch_meter_readings(portal, utility, meter_id, start, end))
    return out


def fetch_readings(utility: str, start: date, end: date) -> list[MeterReading]:
    """Return raw meter readings for local dates start..end inclusive.

    Re-fetching a range that is already stored is expected and must be safe: callers
    overwrite existing rows, which is how late corrections from the portal land.
    """
    if utility not in config.UTILITIES:
        raise ValueError(f"unknown utility: {utility!r}")
    if end < start:
        raise ValueError("end date is before start date")
    if not SOURCE_READY:
        raise SourceNotReady("mycitygrid fetching is not ready")

    with portal_session() as portal:
        return _fetch_readings(portal, utility, start, end)
