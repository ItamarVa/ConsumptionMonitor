"""Adapter for www.mycitygrid.com - the only module that talks to the portal.

Built on Scrapling's FetcherSession: a plain HTTP session with browser impersonation and
cookies that persist across requests, which is all a login-then-read-JSON portal needs.
Two functions are still empty because the portal is undocumented and no credentials
exist yet - `_login` and `_fetch_range`. Nothing else in the project should need changing.
Invariant: `fetch_hourly` returns at most one Reading per (utility, meter_id, hour) and
every `hour_start` is timezone-aware UTC on an exact hour boundary.
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date, datetime

from . import config

# Flip to True once _login and _fetch_range really work. jobs.py checks this so a
# scaffold install records a clear "source not implemented" status instead of a crash loop.
SOURCE_READY = False

UNITS = {"electricity": "kWh", "water": "m3"}

# A stable fingerprint beats a random one here: the portal sees the same client every
# hour, and one signed-in household making hourly requests is not what bot defences hunt.
IMPERSONATE = "chrome"
TIMEOUT_SECONDS = 60


@dataclass(frozen=True, slots=True)
class Reading:
    utility: str  # one of config.UTILITIES
    meter_id: str
    hour_start: datetime  # timezone-aware, UTC, minutes/seconds zeroed
    value: float  # consumption during that hour, not a cumulative meter total
    unit: str


class SourceNotReady(RuntimeError):
    """The adapter is not implemented or not configured. Not a transient failure."""


class SourceError(RuntimeError):
    """The portal was reached but did not answer as expected. Retrying later may work."""


@contextmanager
def portal_session():
    """A logged-in session. Cookies live for the duration of the `with` block only."""
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
        _login(session)
        yield session


def _login(session) -> None:
    """Authenticate `session` against config.MYCITYGRID_BASE_URL.

    To implement: open the portal's login page in a browser with the network tab
    recording, sign in, and copy the shape of the request that succeeds - URL, method,
    field names, and any CSRF token that has to be scraped from the form first
    (`session.get(...).css('input[name=__RequestVerificationToken]::attr(value)').get()`).
    Then POST it here and raise SourceError on any non-2xx or on a response that still
    shows the login form.
    """
    raise SourceNotReady("consumption/source.py:_login is not implemented yet")


def _fetch_range(session, utility: str, start: date, end: date) -> list[Reading]:
    """Pull hourly buckets for local dates start..end inclusive from a logged-in session.

    To implement: find the request the portal's own consumption chart makes and reuse it.
    `response.json()` parses a JSON endpoint; `response.css(...)` handles an HTML table.
    Convert each bucket to a per-hour delta if the portal reports cumulative meter
    totals, and localise its timestamp with config.LOCAL_TZ before converting to UTC.
    """
    raise SourceNotReady("consumption/source.py:_fetch_range is not implemented yet")


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

    with portal_session() as session:
        return _fetch_range(session, utility, start, end)
