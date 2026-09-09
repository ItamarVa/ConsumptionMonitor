"""Proportional hour-bucket spreading for cumulative meter registers.

Pure math only: callers pass ordered db.meter_readings rows (including the last
reading before local midnight). DST transitions are handled by stepping bucket
boundaries in absolute time, which yields 23 or 25 buckets on Israeli transition
days without constructing invalid local wall times. Depends on nothing in db.py.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import date, datetime, timedelta, timezone
from typing import Any
from zoneinfo import ZoneInfo

_UTC = timezone.utc


def spread_to_hours(
    readings: Sequence[Mapping[str, Any]],
    field: str,
    day: date,
    tz: ZoneInfo,
) -> list[dict]:
    """Distribute each consecutive register delta across the local hours it covers."""
    day_start = datetime(day.year, day.month, day.day, tzinfo=tz)
    day_end = day_start + timedelta(days=1)
    buckets = _build_buckets(day_start, day_end)

    for earlier, later in zip(readings, readings[1:]):
        v0 = earlier.get(field)
        v1 = later.get(field)
        if v0 is None or v1 is None:
            continue
        delta = v1 - v0
        if delta < 0:
            continue
        t0 = _parse_utc(earlier["reading_time_utc"])
        t1 = _parse_utc(later["reading_time_utc"])
        if t1 <= t0:
            continue
        interval_seconds = (t1 - t0).total_seconds()
        clamp_start = max(t0, day_start)
        clamp_end = min(t1, day_end)
        if clamp_end <= clamp_start:
            continue
        for bucket in buckets:
            overlap_start = max(clamp_start, bucket["start"])
            overlap_end = min(clamp_end, bucket["end"])
            if overlap_end <= overlap_start:
                continue
            overlap_seconds = (overlap_end - overlap_start).total_seconds()
            bucket["value"] += delta * overlap_seconds / interval_seconds
            bucket["covered_seconds"] += overlap_seconds
            bucket["source_intervals"] += 1

    return [
        {
            "hour": bucket["hour"],
            "value": round(bucket["value"], 4) if bucket["source_intervals"] else None,
            "source_intervals": bucket["source_intervals"],
            "partial": bucket["covered_seconds"] < bucket["duration"],
        }
        for bucket in buckets
    ]


def _build_buckets(day_start: datetime, day_end: datetime) -> list[dict]:
    tz = day_start.tzinfo
    cursor = day_start.astimezone(_UTC)
    end = day_end.astimezone(_UTC)
    buckets: list[dict] = []
    while cursor < end:
        nxt = cursor + timedelta(hours=1)
        start_local = cursor.astimezone(tz)
        end_local = nxt.astimezone(tz)
        buckets.append(
            {
                "hour": start_local.strftime("%H:00"),
                "start": start_local,
                "end": end_local,
                "duration": (nxt - cursor).total_seconds(),
                "value": 0.0,
                "source_intervals": 0,
                "covered_seconds": 0.0,
            }
        )
        cursor = nxt
    return buckets


def _parse_utc(raw: Any) -> datetime:
    if isinstance(raw, datetime):
        dt = raw
    else:
        text = str(raw)
        if text.endswith("Z"):
            text = f"{text[:-1]}+00:00"
        dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=_UTC)
    return dt.astimezone(_UTC)
