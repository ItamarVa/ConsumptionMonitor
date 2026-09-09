# Graph Report - ConsumptionMonitor  (2026-09-09)

## Corpus Check
- 42 files · ~25,904 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1215 nodes · 3215 edges · 60 communities (51 shown, 9 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 128 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4f54e569`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SourceError
- api.py
- test_source_session.py
- db.py
- jobs.py
- portal_session
- secrets.py
- test_api_contract.py
- test_jobs.py
- upsert_meter_readings
- records.py
- source.py
- mycitygrid.com portal recon (no credentials)
- launcher-common.ps1
- env.ps1
- Hourly-Only Granularity Convention
- app.js
- Double-Clickable Launcher Preference
- chart.umd.min.js
- jt
- Run via run.bat
- tn
- ho
- xt
- ua
- a
- .getContext
- oo
- o
- .update
- ._computeLabelItems
- sn
- n
- .getDatasetMeta
- updateElements
- .notifyPlugins
- i
- config.py
- s
- l
- readings.py
- inRange
- connection_report.py
- .configure
- yn
- connect
- refresh
- hs
- .buildOrUpdateControllers
- Dashboard frozen contract
- e
- Vendored third-party assets

## God Nodes (most connected - your core abstractions)
1. `tn` - 124 edges
2. `n()` - 59 edges
3. `s()` - 45 edges
4. `a()` - 36 edges
5. `SourceError` - 35 edges
6. `o()` - 31 edges
7. `l()` - 31 edges
8. `d()` - 29 edges
9. `ho()` - 29 edges
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

## Communities (60 total, 9 thin omitted)

### Community 0 - "SourceError"
Cohesion: 0.16
Nodes (23): _bool_value(), _optional_float(), _optional_int(), parse_reading_row(), datetime, Pure parsers for the mycitygrid meter reading log (GET meterdata). Maps portal…, Map one portal reading-log row to a MeterReading., _reading_time_utc() (+15 more)

### Community 1 - "api.py"
Cohesion: 0.20
Nodes (32): Conn, _directions_for(), _first_stored(), health(), index(), job_status(), _latest_register(), _meter_ids() (+24 more)

### Community 2 - "test_source_session.py"
Cohesion: 0.13
Nodes (22): RuntimeError, The adapter is not implemented or not configured. Not a transient failure., SourceNotReady, _login(), Scaffold Complete, Fetching Unimplemented, Fetching Not Implemented Status, _FakePortal, _FakeResponse (+14 more)

### Community 3 - "db.py"
Cohesion: 0.17
Nodes (30): alert_flags(), daily_totals(), _fetch_readings_for_meter(), _first_reading_on_or_after(), _interval_dict(), intervals(), job_states(), latest_reading() (+22 more)

### Community 4 - "jobs.py"
Cohesion: 0.13
Nodes (30): due(), _advance_backfill(), _always(), _backfill(), _in_january(), Job, local_today(), loop() (+22 more)

### Community 5 - "portal_session"
Cohesion: 0.12
Nodes (17): credentials_present(), consumption Package, Console UTF-8 Reconfiguration, main(), portal_session(), A logged-in session. The access token lives for the duration of the `with`…, Lazy Scrapling Import Lesson, scrapling[fetchers] Extra Lesson (+9 more)

### Community 6 - "secrets.py"
Cohesion: 0.13
Nodes (22): Array, _credentials(), Encrypted store first; the environment stays available as a manual override., _Blob, clear(), _crypt32(), _dpapi(), _input_blob() (+14 more)

### Community 7 - "test_api_contract.py"
Cohesion: 0.09
Nodes (34): Any, _build_buckets(), _parse_utc(), date, datetime, Proportional hour-bucket spreading for cumulative meter registers. Pure math…, Distribute each consecutive register delta across the local hours it covers., spread_to_hours() (+26 more)

### Community 8 - "test_jobs.py"
Cohesion: 0.23
Nodes (18): get_state(), Exception, _conn(), _fake_source(), date, datetime, Offline self-checks for the refresh schedule and job bookkeeping. Uses a…, Stand in for the portal: one reading per utility when start falls in those… (+10 more)

### Community 9 - "upsert_meter_readings"
Cohesion: 0.42
Nodes (12): upsert_meter_readings(), _conn(), _elec(), date, datetime, Offline self-checks for raw meter reading storage and exact register deltas., Portal sometimes emits a new meter_data_id for an unchanged reading_time_utc., test_coverage_counts() (+4 more)

### Community 10 - "records.py"
Cohesion: 0.25
Nodes (15): alert_flags(), coverage(), daily_totals(), fetch_readings(), IntervalReading, intervals(), latest_reading(), meter_readings() (+7 more)

### Community 11 - "source.py"
Cohesion: 0.18
Nodes (13): _fetch_meter_readings(), _fetch_readings(), _Portal, _probe_page(), date, datetime, Adapter for www.mycitygrid.com - the only module that talks to the portal.…, Pick the largest page size the portal accepts for this meter and date range.… (+5 more)

### Community 12 - "mycitygrid.com portal recon (no credentials)"
Cohesion: 0.29
Nodes (6): Best guess at the consumption endpoints, Best guess at the login flow, Dead ends, mycitygrid.com portal recon (no credentials), Unknowns that only credentials can answer, What we know

### Community 13 - "launcher-common.ps1"
Cohesion: 0.70
Nodes (4): Exit-WithError(), Test-TcpPort(), Wait-ApiReady(), Write-Log()

### Community 14 - "env.ps1"
Cohesion: 1.00
Nodes (3): Initialize-Venv(), Show-Phase(), Wait-WithProgress()

### Community 16 - "app.js"
Cohesion: 0.06
Nodes (70): ApiError, fetchHealth(), fetchLocale(), fetchSeries(), GRANULARITY_PATHS, normalizeDaily(), normalizeHourly(), normalizeMonthly() (+62 more)

### Community 18 - "chart.umd.min.js"
Cohesion: 0.04
Nodes (20): beforeUpdate(), cn(), dn(), fe(), Fs(), getMaxOverflow(), hn(), initialize() (+12 more)

### Community 19 - "jt"
Cohesion: 0.08
Nodes (16): Bt(), color(), Ee(), Ft(), Gt(), It(), jt(), kt() (+8 more)

### Community 24 - "ho"
Cohesion: 0.06
Nodes (16): b(), beforeLayout(), buildLookupTable(), _generate(), getDecimalForValue(), _getTimestampsForTable(), getValueForPixel(), Go() (+8 more)

### Community 25 - "xt"
Cohesion: 0.09
Nodes (7): an(), as(), ln(), on, rs(), ts(), xt

### Community 26 - "ua"
Cohesion: 0.15
Nodes (15): beforeDatasetDraw(), beforeDatasetsDraw(), ca, ea(), fa(), ga(), ia(), ma() (+7 more)

### Community 27 - "a"
Cohesion: 0.14
Nodes (15): a(), determineDataLimits(), draw(), fo(), getRange(), ji(), pe(), pi() (+7 more)

### Community 28 - ".getContext"
Cohesion: 0.10
Nodes (13): ao(), Bi(), Ci(), co(), cs, da(), Do(), Fi() (+5 more)

### Community 29 - "oo"
Cohesion: 0.24
Nodes (3): io(), no(), oo

### Community 30 - "o"
Cohesion: 0.07
Nodes (30): Ae(), afterDraw(), afterEvent(), afterUpdate(), Ba(), eo(), f(), g() (+22 more)

### Community 31 - ".update"
Cohesion: 0.13
Nodes (3): d(), Di(), Pn()

### Community 32 - "._computeLabelItems"
Cohesion: 0.11
Nodes (6): getPixelForTick(), Gs(), Ie(), Us(), Y(), Ys()

### Community 34 - "n"
Cohesion: 0.16
Nodes (3): fn(), gn(), n()

### Community 36 - "updateElements"
Cohesion: 0.13
Nodes (18): aa(), afterDatasetsUpdate(), Bn(), _calculateBarIndexPixels(), _calculateBarValuePixels(), _getAxis(), _getAxisCount(), getBasePixel() (+10 more)

### Community 38 - "i"
Cohesion: 0.08
Nodes (16): bs(), ce(), ct(), de, dt(), en, et(), ge() (+8 more)

### Community 39 - "config.py"
Cohesion: 0.13
Nodes (12): _load_env_file(), Path, Runtime configuration, read once at import from the environment and an optional…, Populate os.environ from a KEY=VALUE file. Real environment variables always…, ConsumptionMonitor - local API for electricity and water consumption from…, Entry point: `python -m consumption` serves the API and runs the refresh…, parse_meters(), Map utility -> meter ids from a `user/info` body. An empty list for a utility… (+4 more)

### Community 40 - "s"
Cohesion: 0.09
Nodes (13): Be(), bo, H(), j(), label(), lo(), ne(), s() (+5 more)

### Community 41 - "l"
Cohesion: 0.15
Nodes (11): buildTicks(), l(), ii(), mo(), parse(), parseArrayData(), parseObjectData(), parsePrimitiveData() (+3 more)

### Community 42 - "readings.py"
Cohesion: 0.21
Nodes (15): _buckets(), _exists_locally(), _hour_of_day(), _hour_of_timestamp(), _label(), parse_hourly(), date, datetime (+7 more)

### Community 44 - "inRange"
Cohesion: 0.11
Nodes (22): ai(), average(), dataset(), getCenterPoint(), ha(), hi(), index(), inRange() (+14 more)

### Community 46 - "connection_report.py"
Cohesion: 0.24
Nodes (12): parse_reading_page(), Return the `items` list from one paginated reading-log response., Blank the value of every credential-looking JSON key in `text`., redact(), _dump(), main(), _mask(), _meters_section() (+4 more)

### Community 47 - ".configure"
Cohesion: 0.22
Nodes (5): addBox(), configure(), Nn(), start(), wn()

### Community 50 - "yn"
Cohesion: 0.15
Nodes (5): beforeDraw(), es(), generateLabels(), _i(), yn()

### Community 52 - "connect"
Cohesion: 0.22
Nodes (9): get_conn(), lifespan(), connect(), coverage(), Path, FastAPI, log(), main() (+1 more)

### Community 53 - "refresh"
Cohesion: 0.25
Nodes (9): Force one job to run now, for testing a freshly implemented source adapter., refresh(), _reject_cross_site_refresh(), security_headers(), middleware, post, Endpoint Reference Table, Module Layout (+1 more)

### Community 57 - ".buildOrUpdateControllers"
Cohesion: 0.16
Nodes (4): kn(), qn(), removeBox(), stop()

### Community 58 - "Dashboard frozen contract"
Cohesion: 0.33
Nodes (5): 1. Hourly endpoint JSON, 2. The pure function, 3. CSS custom properties, 4. Locale keys and JS module exports, Dashboard frozen contract

### Community 61 - "e"
Cohesion: 0.09
Nodes (13): at(), e(), ei(), gi(), je(), mi(), qe(), ti() (+5 more)

## Knowledge Gaps
- **33 isolated node(s):** `IntervalReading`, `GRANULARITY_PATHS`, `els`, `state`, `t` (+28 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `tn` connect `tn` to `._computeLabelItems`, `.getDatasetMeta`, `.notifyPlugins`, `i`, `s`, `l`, `inRange`, `.configure`, `chart.umd.min.js`, `yn`, `ho`, `.buildOrUpdateControllers`, `a`, `.getContext`, `o`, `.update`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Why does `n()` connect `n` to `._computeLabelItems`, `.getDatasetMeta`, `i`, `s`, `l`, `.configure`, `chart.umd.min.js`, `oo`, `tn`, `ho`, `xt`, `ua`, `a`, `.getContext`, `e`, `o`, `.update`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `SourceError` connect `SourceError` to `test_source_session.py`, `config.py`, `records.py`, `readings.py`, `source.py`, `connection_report.py`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `s()` (e.g. with `beforeUpdate()` and `bs()`) actually correct?**
  _`s()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `a()` (e.g. with `ai()` and `draw()`) actually correct?**
  _`a()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `SourceError` (e.g. with `_Portal` and `test_malformed_row_raises_with_excerpt()`) actually correct?**
  _`SourceError` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `IntervalReading`, `GRANULARITY_PATHS`, `els` to the rest of the system?**
  _33 weakly-connected nodes found - possible documentation gaps or missing edges._