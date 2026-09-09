# ConsumptionMonitor

## Purpose

Local HTTP API for household electricity and water consumption from `www.mycitygrid.com`,
which has no public API. Scrape on a schedule, store every hour in SQLite, serve the
history to Home Assistant or a future custom tool.

## Stack

Python 3.14, FastAPI + uvicorn, SQLite (stdlib), Scrapling for scraping, `zoneinfo` +
`tzdata` for Asia/Jerusalem. Runs on the user's Windows machine. Dependencies pinned
exactly in `requirements.txt`; no lockfile beyond that.

## How to run

Double-click `run.bat` (creates `.venv`, installs, self-checks, serves on
<http://127.0.0.1:8123>). Self-checks alone: `.venv\Scripts\python.exe tests\test_aggregation.py`.
Credentials: double-click `set-credentials.bat` once per machine; `.env` holds only
non-secret settings now.

## Layout

`consumption/config.py` settings and the credentials the app sees - `secrets.py` the
encrypted store - `source.py` the mycitygrid adapter - `db.py` schema, upserts,
aggregation - `jobs.py` schedule and loop - `api.py` HTTP and input validation.
`scripts/env.ps1` is the `.venv` bootstrap both launchers dot-source. Full endpoint and
schedule tables live in `README.md`.

## Conventions

- One granularity is stored: the hour. Daily, monthly, yearly and year-to-date are `SUM`
  queries, never derived tables, so a re-fetch corrects history in one place.
- Every scheduled job re-fetches a whole range and overwrites it. Jobs must stay
  idempotent.
- Job intervals are measured from the last attempt recorded in the DB, so a machine that
  slept catches up instead of skipping.
- A job is a `jobs.Job` dataclass: `every`, `covers(today, conn)`, `in_season(today)` and
  an optional `after` hook that runs only on success. `covers` returning None means there
  is nothing left to fetch, and `/jobs` reports both honestly.
- Scheduler bookkeeping that is not per-job goes in the `app_state` key/value table
  (currently only the backfill's next year).
- Timestamps are stored as UTC text; `local_date` is denormalised at write time so day,
  month and year grouping are substrings of it, with no timezone math in SQL.
- All input validation lives in `api.py` - it is the only trust boundary. Only the raw
  hourly endpoint is range-capped (366 days); aggregates span the whole history.
- Credentials live encrypted in `data/credentials.dpapi` via Windows DPAPI; `secrets.py`
  is the only module that touches the blob and must never import `config` (config imports
  it). Never log them, never return them from an endpoint, never write them to memory files.

## Preferences

- User is non-technical and avoids the terminal: every flow needs a double-clickable
  `.bat` with a percentage progress bar.
- Minimal solution, stdlib first. Scrapling was requested explicitly by the user.

## State

Scaffold complete and verified end to end, now with multi-year history (`previous_year`
and `backfill` jobs, monthly/yearly aggregation, coverage on `/health`) and encrypted
credential storage. Fetching is still deliberately unimplemented: `_login` and
`_fetch_range` in `consumption/source.py` raise `SourceNotReady` and `SOURCE_READY` is
`False`, pending credentials and the portal's request shapes.

## Lessons

- The project path contains Hebrew (`...\פרטי\...`), so any Windows console print of a
  path crashes under cp1252. `__main__.py` reconfigures stdout/stderr to UTF-8 and
  `run.bat` sets `chcp 65001`.
- `pip install scrapling` is not enough - `curl_cffi` lives in the `[fetchers]` extra, so
  even the plain HTTP session needs `scrapling[fetchers]`.
- Scrapling is imported lazily inside `source.py:portal_session`; at module level it
  drags the browser stack into the API and the self-checks.
- No public information exists about `mycitygrid.com`; it is a credentialed portal, so the
  request shapes can only be found from a logged-in browser's network tab.
- The user's `scrapling` MCP server is configured in `~/.cursor/mcp.json` and the CLI
  works, but MCP servers are only picked up on window reload.
- "No rows" and "the fetch failed" look identical to a caller, so anything that stops
  permanently on an empty result must only advance on the success path.
- `ctypes.wintypes` cannot be imported on non-Windows, so `secrets.py` declares DWORD as
  `c_uint32` and stays importable everywhere; it only fails when actually used.
- A DPAPI input buffer must be kept referenced for the whole call - letting Python free
  it mid-call is a silent memory corruption, not an exception.
