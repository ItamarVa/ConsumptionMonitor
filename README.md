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

Then double-click `test-connection.bat` once. It signs in, asks the portal for your meters
and for one day of hourly consumption, and writes what came back to
`data/connection-report.txt` (never committed, with the password and the tokens removed).
The window says in plain words whether it worked.

`.env` is now only for non-secret settings such as `PORT`; see `.env.example`.

## Status

Complete and running, and fetching is implemented - but **written against a
reverse-engineered API and unverified**. `www.mycitygrid.com` publishes no documentation,
so every URL, parameter and response shape in `consumption/source.py` and
`consumption/readings.py` was derived by reading the site's public JavaScript bundle
without ever logging in (the write-up is in `.cursor/memory/topics/mycitygrid-portal.md`).
Nothing has been confirmed against a real account yet.

The login and the meter list are on firm ground; the shape of the consumption response is
the guess most likely to be wrong, so the parser refuses anything it does not recognise
instead of storing a zero. That means the first real run either works or fails loudly with
a message naming what it expected. **Run `test-connection.bat` first**: its report is what
turns the remaining guesses into facts. Two known open questions it answers - whether the
values are per-hour amounts (assumed) or cumulative meter totals, and whether water needs
the multiplier the portal's own screen applies.

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
consumption/source.py   the mycitygrid adapter: session, login, token refresh, day loop
consumption/readings.py the Reading type, the error taxonomy and the response parsers
consumption/db.py       SQLite schema, upserts and the aggregation queries
consumption/jobs.py     the refresh schedule and the scheduler loop
consumption/api.py      the HTTP layer and all input validation
scripts/env.ps1         the .venv bootstrap shared by all three launchers
scripts/connection_report.py  the first-contact diagnostic behind test-connection.bat
tests/test_aggregation.py     self-checks for storage and the schedule, no network
tests/test_source_parsing.py  self-checks for the response parsers, no network
tests/test_source_session.py  self-checks for login, token refresh and the day loop
```

Parsing is a separate file from the HTTP side on purpose: it is pure, it is the part most
likely to need correcting once real responses are seen, and it is therefore the part the
self-checks exercise against synthetic payloads.

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
- Hourly data costs one request per local day, as the portal's own chart does, so a
  backfill year is about 366 requests. They are spaced one second apart, and one call
  refuses to make more than 800 requests - a caller asking for a decade gets a clear
  error instead of an hour of traffic. Whether a wider date window works is unknown.
- Israeli daylight saving is handled: the spring-forward day stores 23 hours and the
  autumn day 25, with the repeated wall-clock hour kept as two distinct UTC hours. A
  bucket for the hour that the spring jump removes is dropped rather than folded onto
  its neighbour, because no consumption can belong to an hour that did not happen.
- A wrong username or password is reported as `SourceNotReady`, which the scheduler
  treats as "not worth retrying", and it names `set-credentials.bat` as the fix. A portal
  that answers oddly is `SourceError`, which is retried on the next schedule.
- The encrypted credentials are tied to one Windows user on one machine. Copying the
  project to another PC, or a Windows profile reset, means running `set-credentials.bat`
  again. Moving off Windows would mean swapping DPAPI for the `keyring` package.
