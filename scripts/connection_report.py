"""First-contact diagnostic: signs in once and writes down what the portal actually returns.

Probes user/info and the paginated meter reading log (GET meterdata), not the chart feed.
Dumps redacted payloads into a git-ignored report and says whether the parser understood them.
Reads credentials through consumption.config only; never prints the password or a token.
Run through test-connection.bat. Depended on by: scripts/test-connection.ps1.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from consumption import config, jobs, readings, source  # noqa: E402
from consumption.reading_log import parse_reading_page, parse_reading_row  # noqa: E402
from consumption.records import READING_LOG_PATH  # noqa: E402

REPORT_PATH = config.ROOT / "data" / "connection-report.txt"
PAYLOAD_LIMIT = 8000


def _mask(username: str) -> str:
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
        "",
    ]
    return meters


def _reading_log_section(portal, utility: str, meter_id: str, lines: list[str]) -> bool:
    """One page of the reading log for a recent local day. Returns True if parsed."""
    today = jobs.local_today()
    for day in (today - timedelta(days=1), today):
        stamp = day.strftime("%m/%d/%Y")
        params = {
            "meterId": meter_id,
            "fromDate": stamp,
            "toDate": stamp,
            "pageNumber": "1",
            "pageSize": "50",
        }
        payload = portal.get_json(READING_LOG_PATH, params)
        lines += [
            f"### {utility} meter {meter_id}, local day {day}",
            "",
            f"GET {READING_LOG_PATH}?" + "&".join(f"{k}={v}" for k, v in params.items()),
            "",
            _dump(payload),
            "",
        ]
        try:
            rows = parse_reading_page(payload)
            parsed = [parse_reading_row(item, utility, meter_id) for item in rows]
        except readings.SourceError as exc:
            lines += [f"PARSER: did NOT understand this response - {exc}", ""]
            return False
        if not parsed:
            lines += ["  The day came back empty, trying the next one.", ""]
            continue
        import_total = sum(r.total_import_kwh or 0 for r in parsed if utility == "electricity")
        water_total = sum(r.total_water_data or 0 for r in parsed if utility == "water")
        lines += [
            f"PARSER: understood the response - {len(parsed)} raw readings.",
            f"  first reading {parsed[0].reading_time.isoformat()}",
            f"  last reading  {parsed[-1].reading_time.isoformat()}",
        ]
        if utility == "electricity" and parsed[0].total_import_kwh is not None:
            lines += [f"  sample cumulative import register: {parsed[0].total_import_kwh}"]
        if utility == "water" and parsed[0].total_water_data is not None:
            lines += [f"  sample cumulative water register: {parsed[0].total_water_data}"]
        if any(r.back_flow for r in parsed):
            lines += ["  NOTE: backFlow is true on at least one reading."]
        lines.append("")
        return True
    return False


def _probe(lines: list[str]) -> tuple[bool, list[str]]:
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

        lines += ["## meter reading log (GET meterdata)", ""]
        understood = True
        for utility, meter_ids in meters.items():
            for meter_id in meter_ids:
                if not _reading_log_section(portal, utility, meter_id, lines):
                    understood = False
                    summary.append(f"{utility} meter {meter_id}: the parser failed - see report")
                else:
                    summary.append(f"{utility} meter {meter_id}: parsed")
        return understood, summary


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
        except Exception as exc:  # noqa: BLE001
            lines += [f"Unexpected failure: {type(exc).__name__}: {exc}", ""]
            summary = [f"Unexpected failure: {type(exc).__name__}: {exc}"]

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
