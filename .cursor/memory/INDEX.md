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

`/docs` interactive — `/ui` Hebrew RTL dashboard (light/dark) — `/summary` Home Assistant
overview — `/health` coverage + `last_reading_utc` — `/readings/raw`, `/intervals`,
`/hourly` (estimate), `/daily|monthly|yearly` (direction=import|export|water) — `/alerts`.
Electricity: import=consumption, export=production (solar return).

## Conventions

- Stored granularity: each portal reading (`meter_data_id`). Aggregates are exact register
  deltas, never interpolated hourly buckets.
- Jobs: `recent` (hourly, 2 days), `recent_week` (daily, 7 days), `previous_year` (daily,
  January only), `backfill` (6h, one month at a time back to 2024-01).
- Backfill state: `app_state.backfill_next_month`; empty month → `done`.
- Credentials: Windows DPAPI in `data/credentials.dpapi`; never logged or returned.
- Launchers: `.bat` uses `if not "%EXITCODE%"=="0"` not `if errorlevel 1`; log at
  `data/launcher.log`; `launch.ps1` stops prior API, opens `/ui` in seconds, self-checks
  run in background to `data/selfcheck.log`.

## Preferences

- User is non-technical: double-clickable `.bat` with progress bar; no terminal.

## State

Production-ready on `master`. Dashboard at `/ui`: running vs comparison fold mode
(multi-series legend), per-granularity range pickers (year/month/day/hour), drill-down,
theme toggle. `/summary` ~700ms via `db.period_total`. Raw reading log live; backfill
to 2024-01 complete (~27k readings). Remote: `https://github.com/ItamarVa/ConsumptionMonitor.git`.

## Lessons

- Hebrew path + cp1252: `__main__.py` UTF-8 stdout, `run.bat` chcp 65001.
- `scrapling[fetchers]` required; lazy import in `portal_session`.
- Reading log: `pageNumber` 1-based; `orderByProperty` → HTTP 500; ~20–60s per request.
- Chart endpoint `meterdata/consumption` returned zeros; reading log `GET meterdata` is correct.
- Portal reissues duplicate `reading_time_utc` with new `meter_data_id`; upsert on
  `(meter_id, reading_time_utc)`.
- `if errorlevel 1 pause` misses negative PowerShell exit codes (-196608).
- `run.bat` always stops previous API PIDs before starting; API stdout/stderr go to `data/api.log` and `data/api.stderr.log`; launcher failures in `data/launcher.log`.
- Dashboard chart was invisible: canvas `height:100%` in auto-height flex parent caused runaway growth; fix is definite `.chart-wrap` height.
- Chart.js runs tick and tooltip callbacks inside `new Chart()`; a callback closing over the
  `const chart` being assigned throws a TDZ ReferenceError that kills the whole page init.
- Aggregates silently dropped every running period (today, this month, this year) because
  `_period_delta` demanded a reading past the closing boundary; it now closes on the newest
  reading and flags `partial`, which the UI dims and footnotes.
- State panels must replace the canvas only. Hiding `.dashboard__content` also hid the
  controls, and `display:flex` on it beat the `[hidden]` attribute anyway.
- Hour granularity stays selectable: choosing it collapses the range to the last covered day
  and leaving it restores the previous range.
- Verify the dashboard with headless Chrome plus CDP over Node's built-in WebSocket — real
  screenshots and console errors, no new dependency.
- Dashboard comparison mode folds the selected range into coloured series (by year/month/day);
  `#mode` toggle replaces the old compare dropdown; `preset.custom` is read-only status.
- Comparison fold needs whole parent units: rolling presets (30d, last_12) straddle two
  partial months/years so series never share a category; `snapRangeForMode` snaps day→full
  months and month→full years on entry; year granularity hides comparison (no sub-unit).
- `/summary` was ~50s because `_period_total` looped daily queries; `db.period_total` uses two boundary reads (~700ms).
- Status pill must read `last_reading_utc` from `/health`, not `/summary`.
- Known data gap: no readings for 2026-09-01..02; jobs only cover the last 7 days and the
  backfill is `done`, so a hole in the middle is never refilled on its own.
- Portal reading cadence ~2h (elec ~120 min, water ~160 min) forces hourly view to be a
  proportional estimate; day/month/year stay exact register deltas.
