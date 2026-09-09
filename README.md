# ConsumptionMonitor

A local HTTP API for household electricity and water consumption taken from
`www.mycitygrid.com`, which has no public API. The portal is scraped on a schedule, every
hour is stored in SQLite, and the API serves that history to Home Assistant or anything
else that can read JSON.

## Run it

Double-click `run.bat`. It creates `.venv`, installs the pinned dependencies, runs the
self-checks and starts the API on <http://127.0.0.1:8123> (interactive docs at `/docs`).

First, double-click `set-credentials.bat` once per machine. It asks for the mycitygrid
username and password (the password is hidden while typing) and stores them encrypted
with the Windows Data Protection API under `data/`, readable only by the Windows user who
entered them. Without stored credentials the API runs and serves an empty database.

`.env` is now only for non-secret settings such as `PORT`; see `.env.example`.

## Status

The scaffold is complete and running. Fetching is **not implemented**: the portal is
undocumented, so `_login` and `_fetch_range` in `consumption/source.py` are empty and
`SOURCE_READY` is `False`. Until they are filled in, `/jobs` reports every job as failing
with `SourceNotReady`, which is the intended scaffold behaviour.

## Refresh schedule

Each job re-fetches a whole date range and overwrites what is stored, so all of them are
idempotent and late corrections from the portal eventually land.

| Job              | Runs every | Local date range it re-fetches | Active |
| ---------------- | ---------- | ------------------------------ | ------ |
| `today`          | 1 hour     | today                          | always |
| `yesterday`      | 24 hours   | yesterday                      | always |
| `last_full_week` | 7 days     | the last complete Sunday-Saturday week | always |
| `year_to_date`   | 30 days    | 1 January through today        | always |
| `previous_year`  | 24 hours   | all of last year               | in January only |
| `backfill`       | 6 hours    | one whole year, walking backwards | until the portal runs dry |

Intervals are measured from the last attempt recorded in the database, not from process
start, so a machine that was asleep runs the missed job as soon as it comes back.

`previous_year` exists because the portal keeps correcting last year's figures until the
end of January, and stops after that. `backfill` starts at the year before the earliest
stored date and takes one year per run; when a whole year comes back empty it records
that the history has ended and never asks again. Its progress lives in the database, so
a restart resumes rather than starting over. A failed fetch is not an empty year, so it
never ends the walk. `/jobs` reports `in_season` and the range each job would fetch now.

## Endpoints

| Endpoint | Purpose |
| -------- | ------- |
| `GET /health` | Liveness, whether the source is implemented and configured, row count, stored date span per utility |
| `GET /jobs` | Interval, whether the job is in season, the range it covers now, last run, last success and last error |
| `GET /summary` | Latest hour, today, yesterday, this week, last full week, year to date and every stored year - per utility |
| `GET /readings/hourly?utility=&start=&end=` | Raw hourly rows; defaults to the last 7 days, at most 366 days per call |
| `GET /readings/daily?utility=&start=&end=` | Daily totals; defaults to the last 7 days |
| `GET /readings/monthly?utility=&start=&end=` | Monthly totals; defaults to the whole stored history |
| `GET /readings/yearly?utility=&start=&end=` | Yearly totals; defaults to the whole stored history |
| `POST /refresh/{job}` | Force one job to run now |

`utility` is `electricity` or `water`. Dates are `YYYY-MM-DD` in `LOCAL_TZ`. Only the raw
hourly endpoint is capped, because a decade of hourly rows in one response helps nobody;
the aggregated endpoints are meant to span the full history.

## Layout

```
consumption/config.py   settings, and the credentials the rest of the app sees
consumption/secrets.py  the encrypted credential store (Windows DPAPI, no dependency)
consumption/source.py   the mycitygrid adapter (Scrapling) - the part still to write
consumption/db.py       SQLite schema, upserts and the aggregation queries
consumption/jobs.py     the refresh schedule and the scheduler loop
consumption/api.py      the HTTP layer and all input validation
scripts/env.ps1         the .venv bootstrap shared by both launchers
tests/test_aggregation.py  self-checks, no network needed
```

Storage is one row per utility, meter and hour; daily, monthly, yearly and year-to-date
figures are `SUM` queries over those rows rather than separate tables, grouped on a
substring of the denormalised `local_date`. Two utilities at hourly resolution is roughly
17,500 rows a year.

## Notes

- The API binds to `127.0.0.1` and has no authentication. That is only safe locally -
  the database holds personal consumption data. Do not widen `HOST` without putting
  something that authenticates in front of it.
- `consumption/source.py` uses Scrapling's plain HTTP session. If the portal turns out to
  need a real browser, switch to `StealthySession` and run `scrapling install` once to
  download the browser.
- The encrypted credentials are tied to one Windows user on one machine. Copying the
  project to another PC, or a Windows profile reset, means running `set-credentials.bat`
  again. Moving off Windows would mean swapping DPAPI for the `keyring` package.
