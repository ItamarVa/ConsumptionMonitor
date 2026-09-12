# Graph Report - ConsumptionMonitor  (2026-09-10)

## Corpus Check
- 39 files · ~30,991 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1297 nodes · 3406 edges · 70 communities (60 shown, 10 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 131 edges (avg confidence: 0.83)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `15caa2b3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- chart.umd.min.js
- tn
- test_api_contract.py
- de
- app.js
- updateElements
- jt
- ho
- api.py
- db.py
- xt
- jobs.py
- test_source_session.py
- i
- update
- rn
- SourceError
- n
- secrets.py
- controls.js
- s
- .update
- sn
- test_jobs.py
- source.py
- bindEvents
- .update
- r
- config.py
- Si
- .getDatasetMeta
- ro
- parse
- portal_session
- upsert_meter_readings
- readings.py
- records.py
- api.js
- 7. Contract addendum (comparison fold wave)
- .notifyPlugins
- web/chart.js
- connection_report.py
- series.js
- u
- .buildOrUpdateControllers
- ya
- da
- connect
- launcher-common.ps1
- oo
- un
- .getContext
- .getSortedVisibleDatasetMetas
- hs
- l
- mycitygrid.com portal recon (no credentials)
- ua
- refresh
- env.ps1
- Vendored third-party assets
- Hourly-Only Granularity Convention
- Path
- Double-Clickable Launcher Preference
- Run via run.bat
- o
- ne
- ca

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
- `_login()` --references--> `Fetching Not Implemented Status`  [EXTRACTED]
  consumption/source.py → README.md
- `portal_session()` --references--> `mycitygrid.com Portal`  [EXTRACTED]
  consumption/source.py → README.md

## Import Cycles
- None detected.

## Communities (70 total, 10 thin omitted)

### Community 0 - "chart.umd.min.js"
Cohesion: 0.04
Nodes (30): at(), beforeUpdate(), dn(), e(), fe(), gi(), ha(), initialize() (+22 more)

### Community 1 - "tn"
Cohesion: 0.07
Nodes (3): tn, Us(), Ys()

### Community 2 - "test_api_contract.py"
Cohesion: 0.09
Nodes (34): Any, _build_buckets(), _parse_utc(), date, datetime, Proportional hour-bucket spreading for cumulative meter registers. Pure math…, Distribute each consecutive register delta across the local hours it covers., spread_to_hours() (+26 more)

### Community 3 - "de"
Cohesion: 0.23
Nodes (4): ce(), de, dt(), he()

### Community 4 - "app.js"
Cohesion: 0.11
Nodes (36): applyLocale(), chartData, chartWrap, coverage, crumbLabel(), els, exportCsv(), granularityLabel() (+28 more)

### Community 5 - "updateElements"
Cohesion: 0.13
Nodes (8): Bn(), _calculateBarValuePixels(), getLabelAndValue(), getLabelForValue(), jn(), resolveDataElementOptions(), updateElements(), yn()

### Community 6 - "jt"
Cohesion: 0.08
Nodes (16): Bt(), color(), Ee(), Ft(), Gt(), It(), jt(), kt() (+8 more)

### Community 7 - "ho"
Cohesion: 0.10
Nodes (10): buildLookupTable(), _generate(), getDecimalForValue(), _getTimestampsForTable(), getValueForPixel(), ho(), initOffsets(), jo() (+2 more)

### Community 8 - "api.py"
Cohesion: 0.20
Nodes (32): Conn, _directions_for(), _first_stored(), health(), index(), job_status(), _latest_register(), _meter_ids() (+24 more)

### Community 9 - "db.py"
Cohesion: 0.17
Nodes (32): alert_flags(), daily_totals(), _fetch_readings_for_meter(), _first_reading_on_or_after(), _interval_dict(), intervals(), _last_reading_before(), latest_reading() (+24 more)

### Community 10 - "xt"
Cohesion: 0.10
Nodes (6): an(), as(), on, rs(), ts(), xt

### Community 11 - "jobs.py"
Cohesion: 0.13
Nodes (31): due(), set_state(), _advance_backfill(), _always(), _backfill(), _in_january(), Job, local_today() (+23 more)

### Community 12 - "test_source_session.py"
Cohesion: 0.13
Nodes (22): RuntimeError, The adapter is not implemented or not configured. Not a transient failure., SourceNotReady, _login(), Scaffold Complete, Fetching Unimplemented, Fetching Not Implemented Status, _FakePortal, _FakeResponse (+14 more)

### Community 13 - "i"
Cohesion: 0.15
Nodes (13): bs(), ct(), Fs(), ge(), is(), ks(), ms(), ss() (+5 more)

### Community 14 - "update"
Cohesion: 0.14
Nodes (18): beforeLayout(), eo(), et(), f(), Go(), j(), g(), ko() (+10 more)

### Community 15 - "rn"
Cohesion: 0.12
Nodes (4): ei(), en, rn(), xn()

### Community 16 - "SourceError"
Cohesion: 0.16
Nodes (23): _bool_value(), _optional_float(), _optional_int(), parse_reading_row(), datetime, Pure parsers for the mycitygrid meter reading log (GET meterdata). Maps portal…, Map one portal reading-log row to a MeterReading., _reading_time_utc() (+15 more)

### Community 17 - "n"
Cohesion: 0.15
Nodes (5): fn(), g(), gn(), n(), Oe()

### Community 18 - "secrets.py"
Cohesion: 0.13
Nodes (22): Array, _credentials(), Encrypted store first; the environment stays available as a manual override., _Blob, clear(), _crypt32(), _dpapi(), _input_blob() (+14 more)

### Community 19 - "controls.js"
Cohesion: 0.18
Nodes (24): addDays(), applyPreset(), clampHourSpan(), coverageYears(), daysInclusive(), daysInMonth(), defaultRangeFor(), detectPreset() (+16 more)

### Community 20 - "s"
Cohesion: 0.09
Nodes (14): a(), bo, determineDataLimits(), Di(), getRange(), H(), _i(), ji() (+6 more)

### Community 23 - "test_jobs.py"
Cohesion: 0.21
Nodes (19): get_state(), job_states(), Exception, _conn(), _fake_source(), date, datetime, Offline self-checks for the refresh schedule and job bookkeeping. Uses a… (+11 more)

### Community 24 - "source.py"
Cohesion: 0.18
Nodes (13): _fetch_meter_readings(), _fetch_readings(), _Portal, _probe_page(), date, datetime, Adapter for www.mycitygrid.com - the only module that talks to the portal.…, Pick the largest page size the portal accepts for this meter and date range.… (+5 more)

### Community 25 - "bindEvents"
Cohesion: 0.16
Nodes (21): applyHash(), bindEvents(), buttonMatchesUtility(), drillDown(), handleBarClick(), init(), initTheme(), onRangeChange() (+13 more)

### Community 26 - ".update"
Cohesion: 0.20
Nodes (6): afterDraw(), afterEvent(), Ba(), Ta(), wa, za()

### Community 27 - "r"
Cohesion: 0.11
Nodes (26): ai(), average(), beforeDraw(), dataset(), draw(), fo(), getCenterPoint(), getMaxOverflow() (+18 more)

### Community 28 - "config.py"
Cohesion: 0.13
Nodes (12): _load_env_file(), Path, Runtime configuration, read once at import from the environment and an optional…, Populate os.environ from a KEY=VALUE file. Real environment variables always…, ConsumptionMonitor - local API for electricity and water consumption from…, Entry point: `python -m consumption` serves the API and runs the refresh…, parse_meters(), Map utility -> meter ids from a `user/info` body. An empty list for a utility… (+4 more)

### Community 29 - "Si"
Cohesion: 0.32
Nodes (5): ki(), Oi(), Si(), x(), zs()

### Community 30 - ".getDatasetMeta"
Cohesion: 0.22
Nodes (3): aa(), afterDatasetsUpdate(), onClick()

### Community 31 - "ro"
Cohesion: 0.15
Nodes (7): ao(), co(), Do(), inXRange(), inYRange(), ro(), Y()

### Community 32 - "parse"
Cohesion: 0.15
Nodes (7): buildTicks(), ii(), mo(), parse(), parseArrayData(), parsePrimitiveData(), Vn()

### Community 33 - "portal_session"
Cohesion: 0.12
Nodes (17): credentials_present(), consumption Package, Console UTF-8 Reconfiguration, main(), portal_session(), A logged-in session. The access token lives for the duration of the `with`…, Lazy Scrapling Import Lesson, scrapling[fetchers] Extra Lesson (+9 more)

### Community 34 - "upsert_meter_readings"
Cohesion: 0.34
Nodes (15): upsert_meter_readings(), _conn(), _elec(), date, datetime, MeterReading, Offline self-checks for raw meter reading storage and exact register deltas., A day with no reading past its closing midnight still reports what has accrued. (+7 more)

### Community 35 - "readings.py"
Cohesion: 0.21
Nodes (15): _buckets(), _exists_locally(), _hour_of_day(), _hour_of_timestamp(), _label(), parse_hourly(), date, datetime (+7 more)

### Community 36 - "records.py"
Cohesion: 0.25
Nodes (15): alert_flags(), coverage(), daily_totals(), fetch_readings(), IntervalReading, intervals(), latest_reading(), meter_readings() (+7 more)

### Community 37 - "api.js"
Cohesion: 0.23
Nodes (14): addDaysIso(), ApiError, daysBetween(), fetchHealth(), fetchHourlyRange(), fetchLocale(), fetchSeries(), GRANULARITY_PATHS (+6 more)

### Community 38 - "7. Contract addendum (comparison fold wave)"
Cohesion: 0.08
Nodes (24): 1. Hourly endpoint JSON, 2. The pure function, 3. CSS custom properties, 4. Locale keys and JS module exports, 5. Contract addendum (redesign wave), 6. Contract addendum (data-completeness wave), 7. Contract addendum (comparison fold wave), Breadcrumb (+16 more)

### Community 40 - "web/chart.js"
Cohesion: 0.21
Nodes (12): paintChart(), toggleTheme(), barAlpha(), createChart(), cssVar(), hexToRgba(), numberFmt, onBarClick() (+4 more)

### Community 41 - "connection_report.py"
Cohesion: 0.24
Nodes (12): parse_reading_page(), Return the `items` list from one paginated reading-log response., Blank the value of every credential-looking JSON key in `text`., redact(), _dump(), main(), _mask(), _meters_section() (+4 more)

### Community 42 - "series.js"
Cohesion: 0.25
Nodes (13): buildChartData(), buildHourCategories(), buildRunningChart(), capSeries(), foldForComparison(), formatDayLabel(), formatMonthCategory(), formatMonthSeriesLabel() (+5 more)

### Community 43 - "u"
Cohesion: 0.23
Nodes (5): addBox(), configure(), reset(), start(), u()

### Community 44 - ".buildOrUpdateControllers"
Cohesion: 0.24
Nodes (3): addElements(), kn(), qn()

### Community 45 - "ya"
Cohesion: 0.23
Nodes (3): afterUpdate(), va(), ya

### Community 46 - "da"
Cohesion: 0.13
Nodes (16): _calculateBarIndexPixels(), da(), _getAxis(), _getAxisCount(), getBasePixel(), getFirstScaleIdForIndexAxis(), getPixelForTick(), getPixelForValue() (+8 more)

### Community 47 - "connect"
Cohesion: 0.20
Nodes (11): get_conn(), lifespan(), connect(), coverage(), init_schema(), Create tables if this file has not been initialized in this process., FastAPI, Path (+3 more)

### Community 48 - "launcher-common.ps1"
Cohesion: 0.32
Nodes (10): Exit-WithError(), Format-ExitCode(), Get-ConsumptionApiProcessIds(), Get-ProjectRootPath(), Stop-PreviousConsumptionSessions(), Test-IsConsumptionApiProcess(), Test-TcpPort(), Wait-ApiReady() (+2 more)

### Community 49 - "oo"
Cohesion: 0.27
Nodes (3): io(), no(), oo

### Community 50 - "un"
Cohesion: 0.22
Nodes (6): b(), cn(), hn(), init(), ln(), un()

### Community 51 - ".getContext"
Cohesion: 0.31
Nodes (4): Bi(), Ci(), cs, Fi()

### Community 52 - ".getSortedVisibleDatasetMetas"
Cohesion: 0.17
Nodes (4): es(), generateLabels(), Ie(), Ni()

### Community 54 - "l"
Cohesion: 0.19
Nodes (8): l(), lo(), Ls(), po(), ra(), vi(), wi(), Z()

### Community 55 - "mycitygrid.com portal recon (no credentials)"
Cohesion: 0.29
Nodes (6): Best guess at the consumption endpoints, Best guess at the login flow, Dead ends, mycitygrid.com portal recon (no credentials), Unknowns that only credentials can answer, What we know

### Community 56 - "ua"
Cohesion: 0.23
Nodes (11): beforeDatasetDraw(), beforeDatasetsDraw(), ea(), fa(), ga(), ia(), ma(), oa() (+3 more)

### Community 57 - "refresh"
Cohesion: 0.25
Nodes (9): Force one job to run now, for testing a freshly implemented source adapter., refresh(), _reject_cross_site_refresh(), security_headers(), middleware, post, Endpoint Reference Table, Module Layout (+1 more)

### Community 58 - "env.ps1"
Cohesion: 1.00
Nodes (3): Initialize-Venv(), Show-Phase(), Wait-WithProgress()

### Community 67 - "o"
Cohesion: 0.31
Nodes (3): Ae(), o(), ze()

### Community 68 - "ne"
Cohesion: 0.40
Nodes (3): Be(), ne(), numeric()

## Knowledge Gaps
- **58 isolated node(s):** `1. Hourly endpoint JSON`, `2. The pure function`, `3. CSS custom properties`, `4. Locale keys and JS module exports`, ``/health` coverage fields` (+53 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `tn` connect `tn` to `chart.umd.min.js`, `updateElements`, `ho`, `i`, `rn`, `s`, `.update`, `sn`, `r`, `.getDatasetMeta`, `ro`, `parse`, `.notifyPlugins`, `u`, `.buildOrUpdateControllers`, `da`, `.getContext`, `.getSortedVisibleDatasetMetas`, `o`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Why does `n()` connect `n` to `chart.umd.min.js`, `tn`, `ho`, `xt`, `i`, `rn`, `s`, `.update`, `.update`, `r`, `Si`, `.getDatasetMeta`, `ro`, `parse`, `u`, `.buildOrUpdateControllers`, `da`, `oo`, `o`, `ne`, `ca`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Why does `yn()` connect `updateElements` to `chart.umd.min.js`, `s`, `.getSortedVisibleDatasetMetas`, `rn`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `s()` (e.g. with `beforeUpdate()` and `bs()`) actually correct?**
  _`s()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `a()` (e.g. with `ai()` and `draw()`) actually correct?**
  _`a()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `SourceError` (e.g. with `_Portal` and `test_malformed_row_raises_with_excerpt()`) actually correct?**
  _`SourceError` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `1. Hourly endpoint JSON`, `2. The pure function`, `3. CSS custom properties` to the rest of the system?**
  _58 weakly-connected nodes found - possible documentation gaps or missing edges._