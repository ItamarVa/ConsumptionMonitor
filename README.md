# ConsumptionMonitor

A local HTTP API for household electricity and water consumption taken from
`www.mycitygrid.com`, which has no public API. The portal is scraped on a schedule, every
hour is stored in SQLite, and the API serves that history to Home Assistant or anything
else that can read JSON.

## Run it

Double-click `run.bat`. It creates `.venv`, installs the pinned dependencies, runs the
self-checks and starts the API on <http://127.0.0.1:8123> (interactive docs at `/docs`).

Copy `.env.example` to `.env` and fill in `MYCITYGRID_USERNAME` and
`MYCITYGRID_PASSWORD`. Without them the API runs and serves an empty database.

## Status

The scaffold is complete and running. Fetching is **not implemented**: the portal is
undocumented, so `_login` and `_fetch_range` in `consumption/source.py` are empty and
`SOURCE_READY` is `False`. Until they are filled in, `/jobs` reports every job as failing
with `SourceNotReady`, which is the intended scaffold behaviour.

## Refresh schedule

Each job re-fetches a whole date range and overwrites what is stored, so all four are
idempotent and late corrections from the portal eventually land.

| Job              | Runs every | Local date range it re-fetches |
| ---------------- | ---------- | ------------------------------ |
| `today`          | 1 hour     | today                          |
| `yesterday`      | 24 hours   | yesterday                      |
| `last_full_week` | 7 days     | the last complete Sunday-Saturday week |
| `year_to_date`   | 30 days    | 1 January through today        |

Intervals are measured from the last attempt recorded in the database, not from process
start, so a machine that was asleep runs the missed job as soon as it comes back.

## Endpoints

| Endpoint | Purpose |
| -------- | ------- |
| `GET /health` | Liveness, whether the source is implemented and configured, row count |
| `GET /jobs` | Last run, last success and last error per job |
| `GET /summary` | Latest hour, today, yesterday, this week, last full week, year to date - per utility |
| `GET /readings/hourly?utility=&start=&end=` | Raw hourly rows; defaults to the last 7 days |
| `GET /readings/daily?utility=&start=&end=` | Daily totals; defaults to the last 7 days |
| `POST /refresh/{job}` | Force one job to run now |

`utility` is `electricity` or `water`. Dates are `YYYY-MM-DD` in `LOCAL_TZ`.

## Layout

```
consumption/config.py   environment and .env, the only reader of the credentials
consumption/source.py   the mycitygrid adapter (Scrapling) - the part still to write
consumption/db.py       SQLite schema, upserts and the aggregation queries
consumption/jobs.py     the refresh schedule and the scheduler loop
consumption/api.py      the HTTP layer and all input validation
tests/test_aggregation.py  self-checks, no network needed
```

Storage is one row per utility, meter and hour; daily, weekly and year-to-date figures
are `SUM` queries over those rows rather than separate tables. Two utilities at hourly
resolution is roughly 17,500 rows a year.

## Notes

- The API binds to `127.0.0.1` and has no authentication. That is only safe locally -
  the database holds personal consumption data. Do not widen `HOST` without putting
  something that authenticates in front of it.
- `consumption/source.py` uses Scrapling's plain HTTP session. If the portal turns out to
  need a real browser, switch to `StealthySession` and run `scrapling install` once to
  download the browser.
