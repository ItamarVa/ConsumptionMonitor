"""First-contact diagnostic: signs in once and writes down what the portal actually returns.

Every response shape in consumption/readings.py is a guess derived from the site's
JavaScript, and this is what replaces the guesses with facts: it dumps `user/info` and one
day of hourly consumption per meter into a git-ignored report, redacted, and says whether
the parser understood them. Reads the credentials through consumption.config only, never
prints the password or a token, and writes nothing to the database.
Run it through test-connection.bat. Depended on by: scripts/test-connection.ps1.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from consumption import config, jobs, readings, source  # noqa: E402

REPORT_PATH = config.ROOT / "data" / "connection-report.txt"

# Enough of a payload to correct the parser from, without a megabyte of JSON in a text file.
PAYLOAD_LIMIT = 8000


def _mask(username: str) -> str:
    """Enough of the email to recognise the account, not enough to reuse it."""
    name, _, domain = username.partition("@")
    return f"{name[:1]}***@{domain}" if domain else "***"


def _dump(value: object, limit: int = PAYLOAD_LIMIT) -> str:
    try:
        text = json.dumps(value, indent=2, ensure_ascii=False, default=str)
    except (TypeError, ValueError):
        text = str(value)
    text = readings.redact(text)
    if len(text) > limit:
        return text[:limit] + f"\n... [truncated, {len(text)} characters in total]"
    return text


def _looks_cumulative(values: list[float]) -> bool:
    """A day that only ever rises is the signature of a meter total, not hourly use."""
    if len(values) < 4 or len(set(values)) < 2:
        return False
    return all(later >= earlier for earlier, later in zip(values, values[1:]))


def _meters_section(portal, lines: list[str]) -> dict[str, list[str]]:
    payload = portal.get_json(source.USER_INFO_PATH)
    lines += ["## user/info (verbatim, credential keys redacted)", "", _dump(payload), ""]
    try:
        meters = readings.parse_meters(payload)
    except readings.SourceError as exc:
        lines += [f"PARSER: did NOT understand user/info - {exc}", ""]
        return {}
    lines += [
        "PARSER: understood user/info.",
        f"  electricity meters (type 1): {meters['electricity'] or 'none'}",
        f"  water meters (type 2):       {meters['water'] or 'none'}",
        "  Any meter of another type is listed above but deliberately not collected.",
        "",
    ]
    return meters


def _day_section(portal, utility: str, meter_id: str, lines: list[str]) -> bool:
    """One day of hourly buckets for one meter. Returns True if the parser understood it."""
    today = jobs.local_today()
    understood = False
    for day in (today - timedelta(days=1), today):
        stamp = day.strftime("%m/%d/%Y")
        params = {
            "meterId": meter_id,
            "period": "hourly",
            "fromDate": stamp,
            "toDate": stamp,
        }
        payload = portal.get_json(source.CONSUMPTION_PATH, params)
        lines += [
            f"### {utility} meter {meter_id}, local day {day}",
            "",
            f"GET {source.CONSUMPTION_PATH}?" + "&".join(f"{k}={v}" for k, v in params.items()),
            "",
            _dump(payload),
            "",
        ]
        try:
            parsed = readings.parse_hourly(payload, utility, meter_id, day)
        except readings.SourceError as exc:
            lines += [f"PARSER: did NOT understand this response - {exc}", ""]
            return False
        understood = True
        values = [r.value for r in parsed]
        lines += [
            f"PARSER: understood the response - {len(parsed)} hourly readings, "
            f"total {round(sum(values), 4)} {readings.UNITS[utility]}.",
        ]
        if parsed:
            lines += [
                f"  first hour {parsed[0].hour_start:%Y-%m-%dT%H:%M}Z, "
                f"last hour {parsed[-1].hour_start:%Y-%m-%dT%H:%M}Z",
            ]
            if _looks_cumulative(values):
                lines += [
                    "  WARNING: the values only ever rise across the day, which is what a",
                    "  cumulative meter total looks like. The parser stores them as per-hour",
                    "  consumption. If this warning appears, consumption/readings.py must",
                    "  subtract each bucket from the previous one instead.",
                ]
            lines.append("")
            return True
        lines += ["  The day came back empty, trying the next one.", ""]
    return understood


def _probe(lines: list[str]) -> tuple[bool, list[str]]:
    """Log in once and fill the report. Returns (everything understood, summary lines)."""
    summary: list[str] = []
    with source.portal_session() as portal:
        lines += ["## Login", "", "Login: OK (the token is not written to this report).", ""]
        summary.append("Login: OK")

        meters = _meters_section(portal, lines)
        if not meters:
            summary.append("user/info: the parser did not understand it - see the report")
            return False, summary
        counts = ", ".join(f"{u} {len(ids)}" for u, ids in meters.items())
        summary.append(f"Meters found: {counts}")

        lines += ["## meterdata/consumption, period=hourly", ""]
        understood = True
        for utility, meter_ids in meters.items():
            for meter_id in meter_ids:
                if not _day_section(portal, utility, meter_id, lines):
                    understood = False
                    summary.append(f"{utility} meter {meter_id}: the parser failed - see report")
                else:
                    summary.append(f"{utility} meter {meter_id}: parsed")
        return understood, summary


def _open_questions() -> list[str]:
    return [
        "## Still unanswered by this report",
        "",
        "- Whether a wider fromDate/toDate window returns more than one day of hourly",
        "  buckets, which would cut the backfill from hundreds of requests to a few.",
        "- What the portal's own water multiplier is: consumption/readings.py stores the",
        "  raw value, so if the portal's screen shows a different water figure, the",
        "  multiplier is the reason.",
        "- How far back fromDate may go before responses come back empty.",
        "",
    ]


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "# mycitygrid connection report",
        "",
        f"Written: {now}",
        f"Portal: {config.MYCITYGRID_BASE_URL}{source.API_PREFIX}",
        f"Account: {_mask(config.MYCITYGRID_USERNAME)}",
        "",
        "The password, the access token and the refresh token are never written here.",
        "",
    ]
    verdict = "FAILED"
    summary: list[str] = []
    if not config.credentials_present():
        lines += ["No credentials are stored, so nothing was requested.", ""]
        summary = ["No credentials are stored. Double-click set-credentials.bat first."]
    else:
        try:
            understood, summary = _probe(lines)
            verdict = "OK" if understood else "PARTIAL"
        except readings.SourceNotReady as exc:
            lines += [f"Login: FAILED - {exc}", ""]
            summary = [f"Login failed: {exc}"]
        except readings.SourceError as exc:
            lines += [f"The portal was reached but answered unusably: {exc}", ""]
            summary = [f"The portal answered unusably: {exc}"]
        except Exception as exc:  # noqa: BLE001 - a diagnostic must report its own crash
            lines += [f"Unexpected failure: {type(exc).__name__}: {exc}", ""]
            summary = [f"Unexpected failure: {type(exc).__name__}: {exc}"]

    lines += _open_questions()
    lines += [
        "## Verdict",
        "",
        {
            "OK": "The parser understood every response. The adapter should work as written.",
            "PARTIAL": "Some responses were not understood - see the PARSER lines above.",
            "FAILED": "Nothing usable came back - see the lines above.",
        }[verdict],
        "",
    ]

    text = "\n".join(lines)
    if config.MYCITYGRID_PASSWORD:
        text = text.replace(config.MYCITYGRID_PASSWORD, "<redacted>")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(text, encoding="utf-8")

    for line in summary:
        print(f"  {line}")
    print(f"\nResult: {verdict}")
    print(f"Full report: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
