"""The Reading type, the source error taxonomy, and the pure parsers for portal responses.

Split out of source.py so the fragile half can be exercised offline: every function here
is a pure function over already-decoded JSON, with no HTTP stack and no credentials.
The response shapes are reverse-engineered guesses (see
`.cursor/memory/topics/mycitygrid-portal.md`), so any mismatch must raise SourceError
naming what was expected - this data becomes stored history, and a silent zero or a
confident misparse would never be noticed. Depended on by: source.py (re-exports the
names below), scripts/connection_report.py.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date, datetime, timezone

from . import config

UNITS = {"electricity": "kWh", "water": "m3"}

# The portal's meter type enum. Only the two the household cares about are mapped; solar,
# gas and the brand-specific variants (3-7) are left out on purpose, so an unexpected
# meter is reported as "no meter of this type" rather than quietly counted as electricity.
METER_TYPES = {1: "electricity", 2: "water"}

# Any JSON value whose key looks like a credential is blanked before it can reach an
# error message, a log line or the diagnostic report.
_SECRET_KEY = re.compile(
    r'("[A-Za-z_.]*(?:token|password|secret|pwd)[A-Za-z_.]*"\s*:\s*)"[^"]*"',
    re.IGNORECASE,
)

_EXCERPT_LIMIT = 240


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


def redact(text: str) -> str:
    """Blank the value of every credential-looking JSON key in `text`."""
    return _SECRET_KEY.sub(r'\1"<redacted>"', text)


def excerpt(value: object, limit: int = _EXCERPT_LIMIT) -> str:
    """A short, redacted, one-line rendering of a payload, safe to put in an error."""
    try:
        text = json.dumps(value, ensure_ascii=False, default=str)
    except (TypeError, ValueError):
        text = str(value)
    text = redact(" ".join(text.split()))
    return text[:limit] + ("..." if len(text) > limit else "")


def parse_meters(payload: object) -> dict[str, list[str]]:
    """Map utility -> meter ids from a `user/info` body.

    An empty list for a utility means the account genuinely has no such meter. A missing
    or unrecognisable structure raises instead, because guessing here would silently
    stop collecting one of the two utilities.
    """
    addresses = payload.get("addresses") if isinstance(payload, dict) else None
    if not isinstance(addresses, list) or not addresses:
        raise SourceError(
            "expected user/info to carry a non-empty 'addresses' list, got: " + excerpt(payload)
        )
    # `isActive is True` mirrors the portal's own strict `!0 === o.isActive` filter.
    active = [a for a in addresses if isinstance(a, dict) and a.get("isActive") is True]
    if not active:
        raise SourceError(
            "expected at least one address with isActive true in user/info, got: "
            + excerpt(payload)
        )

    found: dict[str, list[str]] = {utility: [] for utility in METER_TYPES.values()}
    total = 0
    for address in active:
        meters = address.get("meters")
        if not isinstance(meters, list):
            raise SourceError(
                "expected a 'meters' list on the active address in user/info, got: "
                + excerpt(address)
            )
        for meter in meters:
            if not isinstance(meter, dict) or meter.get("meterId") in (None, ""):
                raise SourceError(
                    "expected every meter in user/info to carry a 'meterId', got: "
                    + excerpt(meter)
                )
            total += 1
            utility = METER_TYPES.get(meter.get("type"))
            meter_id = str(meter["meterId"])
            # A household may hold several meters of one type; keep them all, deduplicated.
            if utility and meter_id not in found[utility]:
                found[utility].append(meter_id)
    if total == 0:
        raise SourceError(
            "the active address in user/info lists no meters at all, got: " + excerpt(payload)
        )
    return found


def parse_hourly(
    payload: object,
    utility: str,
    meter_id: str,
    local_day: date,
) -> list[Reading]:
    """Turn one day of `meterdata/consumption?period=hourly` into Readings.

    `local_day` is the local date that was requested; bucket labels carry only a wall-clock
    hour, so the date has to come from the caller. Values are taken as the consumption of
    that hour, which is what the portal's per-bucket bar chart and its per-point multiplier
    imply - if the portal turns out to report cumulative meter totals instead, this is the
    one place that has to change (`test-connection.bat` flags the cumulative signature).
    """
    if utility not in UNITS:
        raise ValueError(f"unknown utility: {utility!r}")

    readings: list[Reading] = []
    seen_hour: dict[int, int] = {}  # local hour -> how many buckets carried it
    used_utc: dict[datetime, str] = {}
    for bucket in _buckets(payload):
        label = _label(bucket)
        hour = _hour_of_day(label, local_day)
        naive = datetime(local_day.year, local_day.month, local_day.day, hour)
        if not _exists_locally(naive):
            # Spring forward: this wall-clock hour does not exist locally, so no consumption
            # can be attributed to it. The portal should send 23 buckets that day and skip
            # it; if it sends one anyway, dropping it beats corrupting the next real hour.
            continue

        # Autumn fall-back repeats one wall-clock hour. Buckets arrive in chronological
        # order, so the first occurrence is the pre-change hour (fold 0) and the second the
        # post-change one (fold 1) - which is exactly what the repeat means.
        fold = seen_hour.get(hour, 0)
        if fold > 1:
            raise SourceError(
                f"the {local_day} hourly response repeats the {hour:02d}:00 bucket "
                f"{fold + 1} times, which no local day can justify: {excerpt(payload)}"
            )
        seen_hour[hour] = fold + 1

        hour_utc = naive.replace(fold=fold, tzinfo=config.LOCAL_TZ).astimezone(timezone.utc)
        if hour_utc in used_utc:
            raise SourceError(
                f"buckets {used_utc[hour_utc]!r} and {label!r} of the {local_day} hourly "
                f"response both land on {hour_utc:%Y-%m-%dT%H:%M}Z; the bucket labels are "
                f"not the local hours of the requested day: {excerpt(payload)}"
            )
        used_utc[hour_utc] = label
        readings.append(
            Reading(utility, str(meter_id), hour_utc, _value(bucket, payload), UNITS[utility])
        )
    return readings


def _buckets(payload: object) -> list:
    """The list of hourly buckets, or an empty list for a day the portal has no data for."""
    if payload is None or payload == [] or payload == {}:
        return []
    if isinstance(payload, dict):
        buckets = payload.get("values")
        if buckets is None:
            raise SourceError(
                "expected a 'values' list of hourly buckets in the consumption response, "
                "got: " + excerpt(payload)
            )
    else:
        # The endpoint may hand back the bucket array on its own rather than wrapped.
        buckets = payload
    if not isinstance(buckets, list):
        raise SourceError(
            "expected the consumption response's buckets to be a list, got: " + excerpt(payload)
        )
    return buckets


def _label(bucket: object) -> str:
    if not isinstance(bucket, dict) or not isinstance(bucket.get("name"), (str, int, float)):
        raise SourceError(
            "expected every consumption bucket to be an object with a 'name' label, got: "
            + excerpt(bucket)
        )
    return str(bucket["name"]).strip()


def _value(bucket: dict, payload: object) -> float:
    """The consumption of one bucket: the sum of its series, or its single value.

    Grouped bars mean time-of-use bands (the portal branches on six of them), and the
    hour's consumption is all of them together, so the series are summed.
    """
    series = bucket.get("series")
    if isinstance(series, list) and series:
        return sum(
            _number(point.get("value") if isinstance(point, dict) else point, payload)
            for point in series
        )
    if "value" in bucket:
        return _number(bucket["value"], payload)
    raise SourceError(
        "expected a consumption bucket to carry a non-empty 'series' list or a 'value', "
        "got: " + excerpt(bucket)
    )


def _number(value: object, payload: object) -> float:
    # A bool is an int in Python, and a negative hourly consumption is the signature of a
    # misparse rather than a meter reading, so both are refused loudly.
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SourceError(
            f"expected a number for a consumption bucket, got {excerpt(value)} in "
            + excerpt(payload)
        )
    if value < 0:
        raise SourceError(
            f"the portal reported a negative hourly consumption ({value}) in "
            + excerpt(payload)
        )
    return float(value)


def _hour_of_day(label: str, local_day: date) -> int:
    """The 0-23 local hour a bucket label names. The label format is not yet verified."""
    if re.fullmatch(r"\d{1,2}", label):
        hour = int(label)
    elif match := re.fullmatch(r"(\d{1,2}):(\d{2})(?::\d{2})?", label):
        if match.group(2) != "00":
            raise SourceError(
                f"expected hourly buckets to start on the hour, got the label {label!r} for "
                f"{local_day}"
            )
        hour = int(match.group(1))
    else:
        hour = _hour_of_timestamp(label, local_day)
    if not 0 <= hour <= 23:
        raise SourceError(
            f"expected a 0-23 local hour from the bucket label {label!r} for {local_day}, "
            f"got {hour}"
        )
    return hour


def _hour_of_timestamp(label: str, local_day: date) -> int:
    """Last resort: the label is a timestamp. Its date must be the day we asked for."""
    try:
        stamp = datetime.fromisoformat(label.replace("Z", "+00:00"))
    except ValueError as exc:
        raise SourceError(
            f"expected an hourly bucket label like '00:00', '0' or an ISO timestamp for "
            f"{local_day}, got {label!r}"
        ) from exc
    if stamp.tzinfo is not None:
        stamp = stamp.astimezone(config.LOCAL_TZ)
    if stamp.date() != local_day:
        raise SourceError(
            f"the consumption response for {local_day} carries a bucket dated "
            f"{stamp.date()} ({label!r}); the requested day is not what came back"
        )
    if stamp.minute or stamp.second:
        raise SourceError(
            f"expected hourly buckets to start on the hour, got the label {label!r} for "
            f"{local_day}"
        )
    return stamp.hour


def _exists_locally(naive: datetime) -> bool:
    """False for a wall-clock time skipped by the spring-forward jump."""
    local = naive.replace(tzinfo=config.LOCAL_TZ)
    return local.astimezone(timezone.utc).astimezone(config.LOCAL_TZ).replace(tzinfo=None) == naive
