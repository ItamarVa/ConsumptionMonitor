# ConsumptionMonitor

## Purpose

Local HTTP API for household electricity and water consumption from `www.mycitygrid.com`,
which has no public API. Scrape on a schedule, store every raw meter reading in SQLite,
serve exact aggregates to Home Assistant or a future custom tool.

## Stack

Python 3.14, FastAPI + uvicorn, SQLite (stdlib), Scrapling for scraping, `zoneinfo` +
`tzdata` for Asia/Jerusalem. Runs on the user's Windows machine. Dependencies pinned
exactly in `requirements.txt`; no lockfile beyond that.

## How to run

Double-click `run.bat` (creates `.venv`, installs, self-checks, serves on
<http://127.0.0.1:8123>). Self-checks: `tests/test_db_readings.py`, `test_reading_log.py`,
`test_jobs.py`, `test_source_parsing.py`, `test_source_session.py`, `test_api_contract.py`.
Credentials: double-click `set-credentials.bat` once per machine.
`test-connection.bat` signs in once and probes the meter reading log. `.env`
holds only non-secret settings now.

## Layout

`consumption/records.py` frozen contract — `config.py` settings — `secrets.py` encrypted
store — `source.py` mycitygrid adapter (reading log pagination) — `reading_log.py` row
parsers — `readings.py` errors and meter discovery — `db.py` schema and exact aggregates —
`jobs.py` schedule — `api.py` HTTP. Full endpoint and schedule tables in `README.md`.

## Conventions

- One granularity is stored: each portal reading (`meter_data_id`). Daily, monthly, yearly
  are exact deltas on cumulative registers, never interpolated or summed hourly buckets.
- Every scheduled job re-fetches a whole range and overwrites it. Jobs must stay idempotent.
- Job intervals are measured from the last attempt recorded in the DB.
- Jobs: `recent` (hourly, last 2 days), `recent_week` (daily, 7 days), `previous_year`
  (daily, January only), `backfill` (6h, one month at a time to 2024-01).
- Backfill progress lives in `app_state` key `backfill_next_month`; empty month stops forever.
- Timestamps stored as UTC text; `local_date` denormalised at write time for grouping.
- All input validation lives in `api.py`. Raw/interval endpoints capped at 366 days.
- Credentials encrypted in `data/credentials.dpapi` via Windows DPAPI; never logged or returned.
- Row parsing pure in `reading_log.py`; HTTP in `source.py`.
- `SourceNotReady` = do not retry; `SourceError` = retry later. Errors redacted via `readings.redact`.

## Preferences

- User is non-technical and avoids the terminal: every flow needs a double-clickable
  `.bat` with a percentage progress bar.

## State

Raw meter reading pipeline integrated (Wave 2). Adapter uses GET meterdata reading log;
chart endpoint dropped. Live verification and full backfill are Wave 3.

## Lessons

- The project path contains Hebrew (`...\פרטי\...`), so any Windows console print of a
  path crashes under cp1252. `__main__.py` reconfigures stdout/stderr to UTF-8 and
  `run.bat` sets `chcp 65001`.
- `pip install scrapling` is not enough - `curl_cffi` lives in the `[fetchers]` extra.
- Scrapling imported lazily inside `source.py:portal_session`.
- "No rows" and "the fetch failed" look identical — backfill advances only on success.
- Scrapling bearer token passed per request, not stashed on the session.
- Tests stub `source.fetch_readings`, never hit the portal.
- Port 8123 may already be held; test on another `PORT` rather than killing their process.
- Reading log: `pageNumber` is 1-based; `orderByProperty` causes HTTP 500.
- Portal may emit duplicate `reading_time_utc` with new `meter_data_id`; upsert keys on `(meter_id, reading_time_utc)`.
