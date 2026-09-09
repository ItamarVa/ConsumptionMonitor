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
<http://127.0.0.1:8123>). Self-checks alone: `.venv\Scripts\python.exe` on each of
`tests\test_aggregation.py`, `tests\test_source_parsing.py`, `tests\test_source_session.py`;
`run.bat` runs all three. Credentials: double-click `set-credentials.bat` once per machine.
`test-connection.bat` signs in once and reports what the portal actually returns. `.env`
holds only non-secret settings now.

## Layout

`consumption/config.py` settings and the credentials the app sees - `secrets.py` the
encrypted store - `source.py` the mycitygrid adapter (session, login, token refresh, day
loop) - `readings.py` the `Reading` type, the error taxonomy and the pure response parsers
- `db.py` schema, upserts, aggregation - `jobs.py` schedule and loop - `api.py` HTTP and
input validation. `scripts/env.ps1` is the `.venv` bootstrap all three launchers
dot-source; `scripts/connection_report.py` is the diagnostic behind `test-connection.bat`.
Full endpoint and schedule tables live in `README.md`.

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
- Portal response parsing stays pure and in `readings.py`, never in `source.py`: it is the
  guessed half, so it must be correctable and testable with synthetic payloads offline.
- A response the parser does not recognise raises `SourceError` naming what was expected
  plus a redacted excerpt. Never a zero, never a skipped bucket - this becomes history.
- `SourceNotReady` is "do not retry" (no credentials, or credentials rejected);
  `SourceError` is "retry later" (reached the portal, got something unusable).
- Every error message and excerpt goes through `readings.redact` first.

## Preferences

- User is non-technical and avoids the terminal: every flow needs a double-clickable
  `.bat` with a percentage progress bar.
- Minimal solution, stdlib first. Scrapling was requested explicitly by the user.

## State

Complete end to end, including the adapter: OWIN password grant, token refresh, meter
discovery from `user/info`, one request per local day of hourly buckets, `SOURCE_READY`
is `True`. It is written entirely against the reverse-engineered API in
`topics/mycitygrid-portal.md` and **has never made one real request** - no credentials
existed when it was written. The login and meter shapes are on firm ground; the
consumption response shape is the guess most likely to be wrong. Next: the user stores
credentials, runs `test-connection.bat`, and its report corrects `readings.py`.

## Lessons

- The project path contains Hebrew (`...\פרטי\...`), so any Windows console print of a
  path crashes under cp1252. `__main__.py` reconfigures stdout/stderr to UTF-8 and
  `run.bat` sets `chcp 65001`.
- `pip install scrapling` is not enough - `curl_cffi` lives in the `[fetchers]` extra, so
  even the plain HTTP session needs `scrapling[fetchers]`.
- Scrapling is imported lazily inside `source.py:portal_session`; at module level it
  drags the browser stack into the API and the self-checks.
- No public information exists about `mycitygrid.com`, but "credentialed portal" did not
  mean "opaque": its whole Angular bundle is public, and the endpoints, parameters and
  token handling were read straight out of it without logging in. Response *bodies* are
  the only thing the bundle cannot prove.
- The user's `scrapling` MCP server is configured in `~/.cursor/mcp.json` and the CLI
  works, but MCP servers are only picked up on window reload.
- "No rows" and "the fetch failed" look identical to a caller, so anything that stops
  permanently on an empty result must only advance on the success path.
- `ctypes.wintypes` cannot be imported on non-Windows, so `secrets.py` declares DWORD as
  `c_uint32` and stays importable everywhere; it only fails when actually used.
- A DPAPI input buffer must be kept referenced for the whole call - letting Python free
  it mid-call is a silent memory corruption, not an exception.
- Scrapling's `FetcherSession.__enter__` returns a `_SyncSessionLogic` object with
  `.get`/`.post`, and its `Response` exposes `.status` and `.body` (bytes) but no mutable
  header map - so a bearer token has to be passed per request, not stashed on the session.
  Decode with stdlib `json.loads(response.body)` for a predictable `ValueError`.
- Once `SOURCE_READY` became `True`, any self-check that called `jobs.run_job` or
  `run_due` would have hit the real portal as soon as credentials existed. Tests must stub
  `source.fetch_hourly`, never rely on it being unimplemented.
- `zoneinfo` fold: the autumn repeat hour is `fold=0`/`fold=1` on the same wall clock, and
  a spring-forward hour is detectable by round-tripping local -> UTC -> local and comparing
  the naive wall clock. Verified for Asia/Jerusalem 2026-03-27 and 2026-10-25.
- Port 8123 may already be held by an API the user left running; test on another `PORT`
  rather than killing their process.
