# ConsumptionMonitor

A local HTTP API for household electricity and water consumption taken from
`www.mycitygrid.com`, which has no public API. The portal is scraped on a schedule, every
raw meter reading is stored in SQLite, and the API serves exact aggregates to Home Assistant
or anything else that can read JSON.

## Run it

Double-click `run.bat`. It creates `.venv`, installs the pinned dependencies, runs the
self-checks and starts the API on <http://127.0.0.1:8123> (interactive docs at `/docs`).

First, double-click `set-credentials.bat` once per machine. It asks for the mycitygrid
username and password (the password is hidden while typing) and stores them encrypted
with the Windows Data Protection API under `data/`, readable only by the Windows user who
entered them. Without stored credentials the API runs and serves an empty database.

Then double-click `test-connection.bat` once. It signs in, asks the portal for your meters
and for one page of the meter reading log, and writes what came back to
`data/connection-report.txt` (never committed, with the password and the tokens removed).
The window says in plain words whether it worked.

`.env` is only for non-secret settings such as `PORT`; see `.env.example`.

## Dashboard

After `run.bat` starts the API, open <http://127.0.0.1:8123/ui> (the launcher opens it
automatically). The page is Hebrew RTL, fully offline, and polls the local API every 60
seconds.

- **Granularities** — hour, day, month, and year bar charts. Hour view applies to a single
  calendar day; pick one day in the range or drill into a day from a coarser view.
- **Comparison** — overlay the previous period or the same period last year on the chart and
  KPI cards.
- **Drill-down** — click a year, month, or day bar to zoom in; use the breadcrumb to step
  back up.
- **Hourly estimate** — portal readings arrive roughly every two hours (electricity ~120 min,
  water ~160 min), so the hour view spreads each register delta across the hours it covers.
  It is labeled as estimated in the UI; day/month/year totals remain exact register deltas.

## Status

The adapter uses the paginated meter reading log (`GET meterdata`), verified live against a
real account. Raw readings land with cumulative registers; consumption between readings is
exact subtraction, never interpolation. Run `test-connection.bat` after any credential change.

## Refresh schedule

Each job re-fetches a whole date range and overwrites what is stored, so all of them are
idempotent and late corrections from the portal eventually land.

| Job              | Runs every | Local date range it re-fetches | Active |
| ---------------- | ---------- | ------------------------------ | ------ |
| `recent`         | 1 hour     | yesterday and today            | always |
| `recent_week`    | 24 hours   | the last 7 days                | always |
| `previous_year`  | 24 hours   | all of last calendar year      | in January only |
| `backfill`       | 6 hours    | one whole month, walking backwards to 2024-01 | until an empty month |

Intervals are measured from the last attempt recorded in the database, not from process
start, so a machine that was asleep runs the missed job as soon as it comes back.

`previous_year` exists because the portal keeps correcting last year's figures until the
end of January. `backfill` starts at the month before the earliest stored date and takes
one month per run; when a whole month comes back empty it records that history has ended
and never asks again. Its progress lives in the database (`backfill_next_month`), so a
restart resumes rather than starting over. A failed fetch is not an empty month, so it
never ends the walk. `/jobs` reports `in_season` and the range each job would fetch now.

## Endpoints

| Endpoint | Purpose |
| -------- | ------- |
| `GET /health` | Liveness, credentials status, reading count, stored date span per utility |
| `GET /jobs` | Interval, whether the job is in season, the range it covers now, last run and error |
| `GET /summary` | Latest register, today, this week, this month, year-to-date — per utility and direction |
| `GET /alerts?utility=` | Leak, backflow, tamper and other flags from the latest reading per meter |
| `GET /readings/raw?utility=&meter_id=&start=&end=` | Raw meter readings; defaults to 7 days, at most 366 days |
| `GET /readings/intervals?utility=&direction=&start=&end=` | Exact deltas between consecutive readings |
| `GET /readings/hourly?utility=&direction=&date=` | Proportional hour buckets for one day (estimated) |
| `GET /readings/daily?utility=&direction=&start=&end=` | Daily totals from cumulative registers |
| `GET /readings/monthly?utility=&direction=&start=&end=` | Monthly totals |
| `GET /readings/yearly?utility=&direction=&start=&end=` | Yearly totals |
| `POST /refresh/{job}` | Force one job to run now |

`utility` is `electricity` or `water`. For electricity, `direction` is `import` or `export`;
for water it is `water`. Dates are `YYYY-MM-DD` in `LOCAL_TZ`. Raw and interval endpoints
are capped at 366 days; aggregates span the full stored history.

## Layout

```
consumption/records.py    frozen contract: MeterReading, SCHEMA, function signatures
consumption/config.py     settings and the credentials the rest of the app sees
consumption/secrets.py    the encrypted credential store (Windows DPAPI)
consumption/source.py     the mycitygrid adapter: session, login, reading-log pagination
consumption/reading_log.py pure parsers for meter reading log rows
consumption/readings.py   SourceError types, meter discovery, redaction helpers
consumption/db.py         SQLite schema, upserts, exact register deltas and aggregates
consumption/jobs.py       the refresh schedule and the scheduler loop
consumption/api.py        the HTTP layer and all input validation
scripts/env.ps1           the .venv bootstrap shared by all launchers
scripts/connection_report.py  the first-contact diagnostic behind test-connection.bat
tests/test_db_readings.py     storage and aggregation self-checks
tests/test_reading_log.py     reading-log parser self-checks
tests/test_jobs.py            schedule and backfill self-checks
tests/test_source_parsing.py  meter discovery self-checks
tests/test_source_session.py  login and pagination self-checks
tests/test_api_contract.py    HTTP endpoint shape self-checks
```

## Notes

- The API binds to `127.0.0.1` and has no authentication. That is only safe locally —
  the database holds personal consumption data. Do not widen `HOST` without putting
  something that authenticates in front of it.
- The reading log is slow (often 20–60 seconds per page). Requests are spaced one second
  apart; one fetch refuses more than 800 pages.
- Daily totals use the first reading on or after each local midnight, so a day that starts
  at 00:18 rather than 00:00 is visible in `first_reading_time`, not silently wrong.
- A wrong username or password is `SourceNotReady` (not retried); a portal that answers
  oddly is `SourceError` (retried on the next schedule).
