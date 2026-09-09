# ConsumptionMonitor

## Purpose

Local HTTP API for household electricity and water consumption from `www.mycitygrid.com`,
which has no public API. Scrape on a schedule, store every raw meter reading in SQLite,
serve exact aggregates to Home Assistant or a future custom tool.

## Stack

Python 3.14, FastAPI + uvicorn + httpx (TestClient), SQLite (stdlib), Scrapling for
scraping, `zoneinfo` + `tzdata` for Asia/Jerusalem. Runs on the user's Windows machine.
Dependencies pinned exactly in `requirements.txt`.

## How to run

Double-click `run.bat` (creates `.venv`, installs, self-checks, serves on
<http://127.0.0.1:8123>, starts the refresh scheduler). Credentials: `set-credentials.bat`
once per machine. `test-connection.bat` signs in and writes `data/connection-report.txt`.
History backfill: `python scripts/backfill-loop.py` or wait for the `backfill` job (every 6h).

## Layout

`consumption/records.py` frozen contract — `config.py` / `secrets.py` — `source.py` +
`reading_log.py` (GET meterdata reading log) — `db.py` exact aggregates — `jobs.py` schedule
— `api.py` HTTP. Portal recon: `.cursor/memory/topics/mycitygrid-portal.md`.

## API (browser)

`/docs` interactive — `/summary` Home Assistant overview — `/health` coverage counts —
`/readings/raw`, `/intervals`, `/daily|monthly|yearly` (direction=import|export|water) —
`/alerts`. Electricity: import=consumption, export=production (solar return).

## Conventions

- Stored granularity: each portal reading (`meter_data_id`). Aggregates are exact register
  deltas, never interpolated hourly buckets.
- Jobs: `recent` (hourly, 2 days), `recent_week` (daily, 7 days), `previous_year` (daily,
  January only), `backfill` (6h, one month at a time back to 2024-01).
- Backfill state: `app_state.backfill_next_month`; empty month → `done`.
- Credentials: Windows DPAPI in `data/credentials.dpapi`; never logged or returned.
- Launchers: `.bat` uses `if not "%EXITCODE%"=="0"` not `if errorlevel 1`; log at
  `data/launcher.log`.

## Preferences

- User is non-technical: double-clickable `.bat` with progress bar; no terminal.

## State

Production-ready on `master`. Raw reading log adapter live; spot-checked against portal
2026-09-09. Full history backfill to 2024-01 runs in background (~27k readings total);
`run.bat` keeps recent data fresh. Remote: `https://github.com/ItamarVa/ConsumptionMonitor.git`.

## Lessons

- Hebrew path + cp1252: `__main__.py` UTF-8 stdout, `run.bat` chcp 65001.
- `scrapling[fetchers]` required; lazy import in `portal_session`.
- Reading log: `pageNumber` 1-based; `orderByProperty` → HTTP 500; ~20–60s per request.
- Chart endpoint `meterdata/consumption` returned zeros; reading log `GET meterdata` is correct.
- Portal reissues duplicate `reading_time_utc` with new `meter_data_id`; upsert on
  `(meter_id, reading_time_utc)`.
- `if errorlevel 1 pause` misses negative PowerShell exit codes (-196608).
