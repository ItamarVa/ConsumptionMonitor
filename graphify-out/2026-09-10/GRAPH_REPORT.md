# Graph Report - ConsumptionMonitor  (2026-09-10)

## Corpus Check
- 38 files · ~27,572 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1242 nodes · 3280 edges · 64 communities (53 shown, 11 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 130 edges (avg confidence: 0.83)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fe18d651`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- app.js
- chart.umd.min.js
- ho
- api.py
- test_api_contract.py
- nearest
- tn
- xt
- ua
- db.py
- jobs.py
- updateElements
- jt
- excerpt
- test_source_session.py
- o
- portal_session
- .update
- parse
- secrets.py
- sn
- .update
- n
- .getContext
- ro
- SourceError
- Si
- test_jobs.py
- config.py
- readings.py
- records.py
- .getDatasetMeta
- upsert_meter_readings
- s
- ya
- bo
- launcher-common.ps1
- u
- .getSortedVisibleDatasetMetas
- connection_report.py
- Dashboard frozen contract
- oo
- .buildOrUpdateControllers
- a
- .notifyPlugins
- ._computeLabelItems
- connect
- test_source_parsing.py
- hs
- refresh
- .isHorizontal
- mycitygrid.com portal recon (no credentials)
- timedelta
- env.ps1
- wi
- Vendored third-party assets
- Hourly-Only Granularity Convention
- Double-Clickable Launcher Preference
- Run via run.bat
- Path

## God Nodes (most connected - your core abstractions)
1. `tn` - 124 edges
2. `n()` - 59 edges
3. `s()` - 45 edges
4. `a()` - 36 edges
5. `SourceError` - 35 edges
6. `o()` - 31 edges
7. `l()` - 31 edges
8. `ho()` - 29 edges
9. `d()` - 29 edges
10. `wa` - 28 edges

## Surprising Connections (you probably didn't know these)
- `_login()` --conceptually_related_to--> `Undocumented mycitygrid Portal Lesson`  [INFERRED]
  consumption/source.py → .cursor/memory/INDEX.md
- `run_job()` --implements--> `Idempotent Refresh Jobs Convention`  [INFERRED]
  consumption/jobs.py → .cursor/memory/INDEX.md
- `portal_session()` --implements--> `Lazy Scrapling Import Lesson`  [INFERRED]
  consumption/source.py → .cursor/memory/INDEX.md
- `_range()` --references--> `api.py as Only Trust Boundary`  [EXTRACTED]
  consumption/api.py → .cursor/memory/INDEX.md
- `summary()` --references--> `Endpoint Reference Table`  [EXTRACTED]
  consumption/api.py → README.md

## Import Cycles
- None detected.

## Communities (64 total, 11 thin omitted)

### Community 0 - "app.js"
Cohesion: 0.05
Nodes (82): ApiError, fetchHealth(), fetchLocale(), fetchSeries(), GRANULARITY_PATHS, normalizeDaily(), normalizeHourly(), normalizeMonthly() (+74 more)

### Community 1 - "chart.umd.min.js"
Cohesion: 0.04
Nodes (22): at(), beforeUpdate(), cn(), dn(), Ee(), fe(), getMaxOverflow(), hn() (+14 more)

### Community 2 - "ho"
Cohesion: 0.07
Nodes (14): b(), buildLookupTable(), _generate(), getDecimalForValue(), _getTimestampsForTable(), getValueForPixel(), ho(), init() (+6 more)

### Community 3 - "api.py"
Cohesion: 0.20
Nodes (32): Conn, _directions_for(), _first_stored(), health(), index(), job_status(), _latest_register(), _meter_ids() (+24 more)

### Community 4 - "test_api_contract.py"
Cohesion: 0.09
Nodes (34): Any, _build_buckets(), _parse_utc(), date, datetime, Proportional hour-bucket spreading for cumulative meter registers. Pure math…, Distribute each consecutive register delta across the local hours it covers., spread_to_hours() (+26 more)

### Community 5 - "nearest"
Cohesion: 0.16
Nodes (15): ai(), average(), beforeDraw(), dataset(), getCenterPoint(), hi(), index(), nearest() (+7 more)

### Community 7 - "xt"
Cohesion: 0.10
Nodes (5): an(), as(), on, ts(), xt

### Community 8 - "ua"
Cohesion: 0.11
Nodes (18): beforeDatasetDraw(), beforeDatasetsDraw(), ca, ea(), ga(), ha(), ia(), K() (+10 more)

### Community 9 - "db.py"
Cohesion: 0.16
Nodes (33): alert_flags(), daily_totals(), _fetch_readings_for_meter(), _first_reading_on_or_after(), _interval_dict(), intervals(), job_states(), latest_reading() (+25 more)

### Community 10 - "jobs.py"
Cohesion: 0.15
Nodes (27): _advance_backfill(), _always(), _backfill(), _in_january(), Job, local_today(), loop(), _month_bounds() (+19 more)

### Community 11 - "updateElements"
Cohesion: 0.11
Nodes (19): Bn(), _calculateBarIndexPixels(), _calculateBarValuePixels(), Fs(), _getAxis(), _getAxisCount(), getFirstScaleIdForIndexAxis(), getLabelAndValue() (+11 more)

### Community 12 - "jt"
Cohesion: 0.09
Nodes (13): Bt(), color(), Ft(), Gt(), It(), jt(), kt(), qt() (+5 more)

### Community 13 - "excerpt"
Cohesion: 0.18
Nodes (17): _bool_value(), _optional_float(), _optional_int(), parse_reading_row(), datetime, Pure parsers for the mycitygrid meter reading log (GET meterdata). Maps portal…, Map one portal reading-log row to a MeterReading., _reading_time_utc() (+9 more)

### Community 14 - "test_source_session.py"
Cohesion: 0.15
Nodes (19): _login(), Scaffold Complete, Fetching Unimplemented, Fetching Not Implemented Status, _FakePortal, _FakeResponse, _FakeSession, _raises(), Self-check for the mycitygrid adapter HTTP half: login, token refresh, reading-… (+11 more)

### Community 15 - "o"
Cohesion: 0.10
Nodes (22): bs(), ct(), e(), ei(), ge(), is(), je(), ks() (+14 more)

### Community 16 - "portal_session"
Cohesion: 0.13
Nodes (16): consumption Package, Console UTF-8 Reconfiguration, main(), portal_session(), A logged-in session. The access token lives for the duration of the `with`…, Lazy Scrapling Import Lesson, scrapling[fetchers] Extra Lesson, Undocumented mycitygrid Portal Lesson (+8 more)

### Community 17 - ".update"
Cohesion: 0.18
Nodes (7): afterDraw(), afterEvent(), Ba(), f(), Ta(), wa, za()

### Community 18 - "parse"
Cohesion: 0.16
Nodes (7): buildTicks(), ii(), mo(), parse(), parseArrayData(), parsePrimitiveData(), Vn()

### Community 19 - "secrets.py"
Cohesion: 0.13
Nodes (22): Array, _credentials(), Encrypted store first; the environment stays available as a manual override., _Blob, clear(), _crypt32(), _dpapi(), _input_blob() (+14 more)

### Community 20 - "sn"
Cohesion: 0.08
Nodes (7): addElements(), ce(), de, dt(), en, he(), sn

### Community 21 - ".update"
Cohesion: 0.13
Nodes (3): d(), Di(), Pn()

### Community 22 - "n"
Cohesion: 0.08
Nodes (9): Be(), fn(), gn(), n(), ne(), numeric(), pi(), Ye() (+1 more)

### Community 23 - ".getContext"
Cohesion: 0.18
Nodes (4): Bi(), Ci(), cs, Fi()

### Community 24 - "ro"
Cohesion: 0.13
Nodes (9): ao(), co(), Do(), inXRange(), inYRange(), Oe(), ro(), s() (+1 more)

### Community 25 - "SourceError"
Cohesion: 0.18
Nodes (16): RuntimeError, The adapter is not implemented or not configured. Not a transient failure., The portal was reached but did not answer as expected. Retrying later may work., SourceError, SourceNotReady, _decode(), _fetch_meter_readings(), _fetch_readings() (+8 more)

### Community 26 - "Si"
Cohesion: 0.23
Nodes (7): ki(), lo(), Oi(), Qs(), Si(), x(), zs()

### Community 27 - "test_jobs.py"
Cohesion: 0.23
Nodes (18): get_state(), Exception, _conn(), _fake_source(), date, datetime, Offline self-checks for the refresh schedule and job bookkeeping. Uses a…, Stand in for the portal: one reading per utility when start falls in those… (+10 more)

### Community 28 - "config.py"
Cohesion: 0.22
Nodes (6): _load_env_file(), Path, Runtime configuration, read once at import from the environment and an optional…, Populate os.environ from a KEY=VALUE file. Real environment variables always…, ConsumptionMonitor - local API for electricity and water consumption from…, Entry point: `python -m consumption` serves the API and runs the refresh…

### Community 29 - "readings.py"
Cohesion: 0.18
Nodes (18): _buckets(), _exists_locally(), _hour_of_day(), _hour_of_timestamp(), _label(), _number(), parse_hourly(), date (+10 more)

### Community 30 - "records.py"
Cohesion: 0.25
Nodes (15): alert_flags(), coverage(), daily_totals(), fetch_readings(), IntervalReading, intervals(), latest_reading(), meter_readings() (+7 more)

### Community 31 - ".getDatasetMeta"
Cohesion: 0.19
Nodes (5): aa(), afterDatasetsUpdate(), da(), getBasePixel(), onClick()

### Community 32 - "upsert_meter_readings"
Cohesion: 0.37
Nodes (13): upsert_meter_readings(), _conn(), _elec(), date, datetime, MeterReading, Offline self-checks for raw meter reading storage and exact register deltas., Portal sometimes emits a new meter_data_id for an unchanged reading_time_utc. (+5 more)

### Community 33 - "s"
Cohesion: 0.10
Nodes (26): beforeLayout(), eo(), et(), g(), getRange(), Go(), _i(), ji() (+18 more)

### Community 34 - "ya"
Cohesion: 0.23
Nodes (3): afterUpdate(), va(), ya

### Community 35 - "bo"
Cohesion: 0.17
Nodes (3): bo, H(), j()

### Community 36 - "launcher-common.ps1"
Cohesion: 0.32
Nodes (10): Exit-WithError(), Format-ExitCode(), Get-ConsumptionApiProcessIds(), Get-ProjectRootPath(), Stop-PreviousConsumptionSessions(), Test-IsConsumptionApiProcess(), Test-TcpPort(), Wait-ApiReady() (+2 more)

### Community 37 - "u"
Cohesion: 0.23
Nodes (5): addBox(), configure(), reset(), start(), u()

### Community 38 - ".getSortedVisibleDatasetMetas"
Cohesion: 0.17
Nodes (4): es(), generateLabels(), Ie(), Ni()

### Community 39 - "connection_report.py"
Cohesion: 0.22
Nodes (13): credentials_present(), parse_reading_page(), Return the `items` list from one paginated reading-log response., Blank the value of every credential-looking JSON key in `text`., redact(), _dump(), main(), _mask() (+5 more)

### Community 40 - "Dashboard frozen contract"
Cohesion: 0.18
Nodes (10): 1. Hourly endpoint JSON, 2. The pure function, 3. CSS custom properties, 4. Locale keys and JS module exports, 5. Contract addendum (redesign wave), Canvas box rule, Dashboard frozen contract, `/health` coverage fields (+2 more)

### Community 41 - "oo"
Cohesion: 0.24
Nodes (3): io(), no(), oo

### Community 42 - ".buildOrUpdateControllers"
Cohesion: 0.22
Nodes (3): kn(), ln(), qn()

### Community 43 - "a"
Cohesion: 0.14
Nodes (20): a(), determineDataLimits(), draw(), fa(), fo(), gi(), l(), inRange() (+12 more)

### Community 46 - "connect"
Cohesion: 0.20
Nodes (11): get_conn(), lifespan(), connect(), coverage(), init_schema(), Create tables if this file has not been initialized in this process., FastAPI, Path (+3 more)

### Community 47 - "test_source_parsing.py"
Cohesion: 0.31
Nodes (6): parse_meters(), Map utility -> meter ids from a `user/info` body. An empty list for a utility…, _raises(), Self-check for user/info meter discovery and redaction helpers (offline only).…, test_error_messages_carry_a_short_redacted_excerpt(), test_meter_discovery()

### Community 49 - "refresh"
Cohesion: 0.25
Nodes (9): Force one job to run now, for testing a freshly implemented source adapter., refresh(), _reject_cross_site_refresh(), security_headers(), middleware, post, Endpoint Reference Table, Module Layout (+1 more)

### Community 51 - "mycitygrid.com portal recon (no credentials)"
Cohesion: 0.29
Nodes (6): Best guess at the consumption endpoints, Best guess at the login flow, Dead ends, mycitygrid.com portal recon (no credentials), Unknowns that only credentials can answer, What we know

### Community 52 - "timedelta"
Cohesion: 0.47
Nodes (6): due(), datetime, _token_expiry(), test_due(), test_token_expiry_reads_both_forms(), timedelta

### Community 53 - "env.ps1"
Cohesion: 1.00
Nodes (3): Initialize-Venv(), Show-Phase(), Wait-WithProgress()

## Knowledge Gaps
- **38 isolated node(s):** `1. Hourly endpoint JSON`, `2. The pure function`, `3. CSS custom properties`, `4. Locale keys and JS module exports`, ``/health` coverage fields` (+33 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `tn` connect `tn` to `chart.umd.min.js`, `ho`, `nearest`, `updateElements`, `o`, `parse`, `sn`, `.update`, `n`, `.getContext`, `ro`, `Si`, `.getDatasetMeta`, `bo`, `u`, `.getSortedVisibleDatasetMetas`, `.buildOrUpdateControllers`, `a`, `.notifyPlugins`, `._computeLabelItems`, `.isHorizontal`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `n()` connect `n` to `chart.umd.min.js`, `s`, `ho`, `u`, `tn`, `xt`, `ua`, `oo`, `.buildOrUpdateControllers`, `a`, `._computeLabelItems`, `o`, `.update`, `parse`, `.update`, `ro`, `Si`, `.getDatasetMeta`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Why does `ho()` connect `ho` to `chart.umd.min.js`, `s`, `a`, `o`, `wi`, `ro`, `Si`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `s()` (e.g. with `beforeUpdate()` and `bs()`) actually correct?**
  _`s()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `a()` (e.g. with `ai()` and `draw()`) actually correct?**
  _`a()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `SourceError` (e.g. with `_Portal` and `test_malformed_row_raises_with_excerpt()`) actually correct?**
  _`SourceError` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `1. Hourly endpoint JSON`, `2. The pure function`, `3. CSS custom properties` to the rest of the system?**
  _38 weakly-connected nodes found - possible documentation gaps or missing edges._