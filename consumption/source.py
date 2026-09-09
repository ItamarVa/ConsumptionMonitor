"""Adapter for www.mycitygrid.com - the only module that talks to the portal.

Built on Scrapling's FetcherSession: a plain HTTP session with browser impersonation,
which is all an OAuth-token-then-read-JSON portal needs. The whole request shape is
reverse-engineered from the site's public JavaScript bundle and is unverified against a
real account - see `.cursor/memory/topics/mycitygrid-portal.md`. Response parsing lives
in readings.py so it can be corrected without touching the HTTP side.
Invariant: `fetch_hourly` returns at most one Reading per (utility, meter_id, hour) and
every `hour_start` is timezone-aware UTC on an exact hour boundary.
"""

from __future__ import annotations

import json
import time
from contextlib import contextmanager
from datetime import date, datetime, timedelta, timezone
from email.utils import parsedate_to_datetime  # the stdlib RFC 1123 parser, for `.expires`

from . import config, readings

# Re-exported: db.py, jobs.py, api.py and the self-checks import these names from here.
from .readings import Reading, SourceError, SourceNotReady, UNITS  # noqa: F401

# The adapter is implemented, so jobs.py may run it. config.credentials_present() still
# gates every run, so an install without stored credentials fails clearly instead.
SOURCE_READY = True

# `/api` is a separate ASP.NET Web API app; the SPA's interceptor prefixes every call.
API_PREFIX = "/api/api/"
LOGIN_PATH = "account/login"
USER_INFO_PATH = "user/info"
CONSUMPTION_PATH = "meterdata/consumption"

# The browser really sends the literal string, because the SPA never assigns its clientId.
CLIENT_ID = "undefined"

# A stable fingerprint beats a random one here: the portal sees the same client every
# hour, and one signed-in household making hourly requests is not what bot defences hunt.
IMPERSONATE = "chrome"
TIMEOUT_SECONDS = 60

# Pacing and volume. Hourly data is one request per local day, so the backfill's whole
# year is ~366 requests per utility. One second between requests is slower than a user
# clicking through the portal's own chart, and the ceiling covers a leap year for two
# meters of one type (732) while refusing a decade-wide range outright - a caller asking
# for that should shorten the range, not keep the portal busy for hours.
REQUEST_DELAY_SECONDS = 1.0
MAX_REQUESTS_PER_CALL = 800

# Renew this long before the token expires, so no single request straddles the expiry.
TOKEN_REFRESH_MARGIN = timedelta(minutes=2)
# Used only when the response carries neither `expires_in` nor `.expires`: short enough
# to be harmless, and a 401 forces a refresh anyway.
TOKEN_FALLBACK_LIFETIME = timedelta(minutes=15)

_BAD_CREDENTIALS = (
    "mycitygrid rejected the stored username and password. "
    "Double-click set-credentials.bat to enter them again."
)


def _url(path: str) -> str:
    return config.MYCITYGRID_BASE_URL.rstrip("/") + API_PREFIX + path


class _Portal:
    """A logged-in portal session: token lifetime, request pacing and JSON decoding.

    The bearer token is held here and sent per request, because the portal has no cookie
    session and Scrapling's session exposes no mutable header map. Refreshing in place is
    what lets a backfill outlive its token without logging in again per request.
    """

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
            # The token can die mid-backfill; force one renewal and retry this request once.
            self._expires_at = datetime.now(timezone.utc)
            self._renew_if_due()
            response = self._request("GET", _url(path), params=params)
        if response.status >= 300:
            raise SourceError(f"the portal answered {response.status} to GET {path}")
        return _decode(response, path)

    def meters(self, utility: str) -> list[str]:
        """Meter ids of one type. Fetched once per session - it cannot change mid-run."""
        if self._meters is None:
            self._meters = readings.parse_meters(self.get_json(USER_INFO_PATH))
        return self._meters.get(utility, [])

    def _authenticate(self, form: dict[str, str], *, password_grant: bool) -> None:
        # `authenticated=False`: sending the expired bearer to the token endpoint could be
        # answered with a 401 and read here as "wrong password", which it would not be.
        response = self._request(
            "POST",
            _url(LOGIN_PATH),
            authenticated=False,
            data=form,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        if response.status in (400, 401):
            # OWIN answers a wrong password with 400 invalid_grant. Nothing about that is
            # transient, so it must not be reported as a blip worth retrying.
            if password_grant:
                raise SourceNotReady(_BAD_CREDENTIALS)
            raise SourceError("the portal rejected the refresh token")
        if response.status >= 300:
            raise SourceError(f"the portal answered {response.status} to the login request")

        # This body carries the tokens, so it is never excerpted into an error message.
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
                self._refresh_token = ""  # stale: fall through to a fresh password login
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
    """When the access token dies, from `expires_in` seconds or the OWIN `.expires` date."""
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
    # Imported here, not at module level: it drags in the whole browser stack, and the
    # API and the self-checks must start without it.
    from scrapling.fetchers import FetcherSession

    with FetcherSession(
        impersonate=IMPERSONATE,
        stealthy_headers=True,
        timeout=TIMEOUT_SECONDS,
    ) as session:
        yield _login(session)


def _login(session) -> _Portal:
    """Authenticate `session` and return the wrapper that keeps it authenticated.

    An OWIN OAuth password grant: a form-encoded POST to `account/login`. There is no
    anti-forgery token, no cookie session and no second factor, so the bearer token in the
    response is the entire credential and is attached to every later request by _Portal.
    """
    portal = _Portal(session)
    portal.login()
    return portal


def _fetch_range(portal: _Portal, utility: str, start: date, end: date) -> list[Reading]:
    """Pull hourly buckets for local dates start..end inclusive from a logged-in session.

    One local day per request, which is what the portal's own hourly chart does. A wider
    window may well be accepted, but nothing has verified that, so the loop stays
    day-at-a-time; widening it is the first optimisation once real responses are known.
    """
    meter_ids = portal.meters(utility)
    if not meter_ids:
        # No meter of this type on the account is a fact, not a failure. Returning nothing
        # keeps a household without a water meter from failing every job forever.
        return []

    days = (end - start).days + 1
    planned = days * len(meter_ids)
    if planned > MAX_REQUESTS_PER_CALL:
        raise SourceError(
            f"{days} days x {len(meter_ids)} {utility} meter(s) is {planned} portal "
            f"requests, over the {MAX_REQUESTS_PER_CALL} allowed in one call - "
            f"fetch a shorter range"
        )

    out: list[Reading] = []
    seen: set[tuple[str, datetime]] = set()
    for offset in range(days):
        day = start + timedelta(days=offset)
        stamp = day.strftime("%m/%d/%Y")  # moment's MM/DD/YYYY, as the SPA sends it
        for meter_id in meter_ids:
            payload = portal.get_json(
                CONSUMPTION_PATH,
                {
                    "meterId": meter_id,
                    "period": "hourly",
                    "fromDate": stamp,
                    "toDate": stamp,
                },
            )
            for reading in readings.parse_hourly(payload, utility, meter_id, day):
                key = (reading.meter_id, reading.hour_start)
                if key in seen:
                    raise SourceError(
                        f"{reading.hour_start:%Y-%m-%dT%H:%M}Z came back twice for "
                        f"{utility} meter {reading.meter_id}, the second time while "
                        f"fetching {day} - the bucket labels are not the local hours of "
                        f"the requested day"
                    )
                seen.add(key)
                out.append(reading)
    return out


def fetch_hourly(utility: str, start: date, end: date) -> list[Reading]:
    """Return hourly consumption for local dates start..end inclusive.

    Re-fetching a range that is already stored is expected and must be safe: callers
    overwrite existing rows, which is how late corrections from the portal land.
    """
    if utility not in config.UTILITIES:
        raise ValueError(f"unknown utility: {utility!r}")
    if end < start:
        raise ValueError("end date is before start date")
    if not SOURCE_READY:
        raise SourceNotReady(
            "mycitygrid fetching is not implemented yet. Fill in _login and _fetch_range "
            "in consumption/source.py, then set SOURCE_READY = True."
        )

    with portal_session() as portal:
        return _fetch_range(portal, utility, start, end)
