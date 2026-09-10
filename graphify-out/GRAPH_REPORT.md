# Graph Report - ConsumptionMonitor  (2026-09-10)

## Corpus Check
- 39 files · ~30,814 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1294 nodes · 3400 edges · 65 communities (57 shown, 8 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 131 edges (avg confidence: 0.83)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2bb8b6ee`
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
- a
- SourceError
- n
- secrets.py
- controls.js
- ko
- .update
- sn
- test_jobs.py
- source.py
- bindEvents
- .update
- r
- test_source_parsing.py
- .isHorizontal
- .getDatasetMeta
- ro
- s
- config.py
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
- .getDataset
- connect
- launcher-common.ps1
- oo
- un
- .getContext
- .getSortedVisibleDatasetMetas
- hs
- .draw
- mycitygrid.com portal recon (no credentials)
- env.ps1
- Vendored third-party assets
- Hourly-Only Granularity Convention
- Path
- Double-Clickable Launcher Preference
- Run via run.bat

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

## Communities (65 total, 8 thin omitted)

### Community 0 - "chart.umd.min.js"
Cohesion: 0.04
Nodes (33): beforeDatasetDraw(), beforeDatasetsDraw(), beforeDraw(), ca, draw(), ea(), Ee(), fo() (+25 more)

### Community 1 - "tn"
Cohesion: 0.06
Nodes (4): Ie(), tn, Us(), Ys()

### Community 2 - "test_api_contract.py"
Cohesion: 0.09
Nodes (34): Any, _build_buckets(), _parse_utc(), date, datetime, Proportional hour-bucket spreading for cumulative meter registers. Pure math…, Distribute each consecutive register delta across the local hours it covers., spread_to_hours() (+26 more)

### Community 3 - "de"
Cohesion: 0.16
Nodes (5): ce(), de, dt(), en, he()

### Community 4 - "app.js"
Cohesion: 0.10
Nodes (37): applyLocale(), chartData, chartWrap, coverage, crumbLabel(), els, exportCsv(), granularityLabel() (+29 more)

### Community 5 - "updateElements"
Cohesion: 0.07
Nodes (21): Bn(), _calculateBarIndexPixels(), _calculateBarValuePixels(), da(), _getAxis(), _getAxisCount(), getBasePixel(), getFirstScaleIdForIndexAxis() (+13 more)

### Community 6 - "jt"
Cohesion: 0.09
Nodes (14): Bt(), color(), Ft(), Gt(), It(), jt(), kt(), mt() (+6 more)

### Community 7 - "ho"
Cohesion: 0.09
Nodes (11): beforeLayout(), buildLookupTable(), _generate(), getDecimalForValue(), _getTimestampsForTable(), getValueForPixel(), Go(), ho() (+3 more)

### Community 8 - "api.py"
Cohesion: 0.13
Nodes (44): Conn, _directions_for(), _first_stored(), health(), index(), job_status(), _latest_register(), lifespan() (+36 more)

### Community 9 - "db.py"
Cohesion: 0.17
Nodes (32): alert_flags(), daily_totals(), _fetch_readings_for_meter(), _first_reading_on_or_after(), _interval_dict(), intervals(), _last_reading_before(), latest_reading() (+24 more)

### Community 10 - "xt"
Cohesion: 0.10
Nodes (6): an(), as(), on, rs(), ts(), xt

### Community 11 - "jobs.py"
Cohesion: 0.12
Nodes (32): due(), job_states(), set_state(), _advance_backfill(), _always(), _backfill(), _in_january(), Job (+24 more)

### Community 12 - "test_source_session.py"
Cohesion: 0.14
Nodes (20): _login(), Scaffold Complete, Fetching Unimplemented, Fetching Not Implemented Status, _FakePortal, _FakeResponse, _FakeSession, _raises(), Self-check for the mycitygrid adapter HTTP half: login, token refresh, reading-… (+12 more)

### Community 13 - "i"
Cohesion: 0.14
Nodes (14): bs(), ct(), Fs(), ge(), is(), ks(), ms(), ps() (+6 more)

### Community 14 - "update"
Cohesion: 0.24
Nodes (9): eo(), g(), g(), m(), ns(), os(), p(), update() (+1 more)

### Community 15 - "a"
Cohesion: 0.10
Nodes (19): a(), ai(), determineDataLimits(), e(), ei(), gi(), je(), mi() (+11 more)

### Community 16 - "SourceError"
Cohesion: 0.15
Nodes (27): _bool_value(), _optional_float(), _optional_int(), parse_reading_page(), parse_reading_row(), datetime, Pure parsers for the mycitygrid meter reading log (GET meterdata). Maps portal…, Return the `items` list from one paginated reading-log response. (+19 more)

### Community 17 - "n"
Cohesion: 0.07
Nodes (10): Be(), bo, fn(), gn(), H(), lt(), n(), ne() (+2 more)

### Community 18 - "secrets.py"
Cohesion: 0.13
Nodes (22): Array, _credentials(), Encrypted store first; the environment stays available as a manual override., _Blob, clear(), _crypt32(), _dpapi(), _input_blob() (+14 more)

### Community 19 - "controls.js"
Cohesion: 0.19
Nodes (23): addDays(), applyPreset(), clampHourSpan(), coverageYears(), daysInclusive(), daysInMonth(), defaultRangeFor(), detectPreset() (+15 more)

### Community 20 - "ko"
Cohesion: 0.20
Nodes (7): et(), j(), ko(), qo(), So, wo(), Zo()

### Community 21 - ".update"
Cohesion: 0.13
Nodes (3): d(), Di(), Pn()

### Community 23 - "test_jobs.py"
Cohesion: 0.22
Nodes (19): get_state(), MeterReading, Exception, _conn(), _fake_source(), date, datetime, Offline self-checks for the refresh schedule and job bookkeeping. Uses a… (+11 more)

### Community 24 - "source.py"
Cohesion: 0.18
Nodes (13): RuntimeError, The adapter is not implemented or not configured. Not a transient failure., SourceNotReady, _decode(), _fetch_readings(), _Portal, date, datetime (+5 more)

### Community 25 - "bindEvents"
Cohesion: 0.17
Nodes (21): applyHash(), bindEvents(), buttonMatchesUtility(), drillDown(), handleBarClick(), init(), initTheme(), onRangeChange() (+13 more)

### Community 26 - ".update"
Cohesion: 0.22
Nodes (6): afterEvent(), Ba(), f(), Ta(), wa, za()

### Community 27 - "r"
Cohesion: 0.17
Nodes (17): average(), dataset(), getCenterPoint(), index(), inRange(), nearest(), qi(), r() (+9 more)

### Community 28 - "test_source_parsing.py"
Cohesion: 0.31
Nodes (6): parse_meters(), Map utility -> meter ids from a `user/info` body. An empty list for a utility…, _raises(), Self-check for user/info meter discovery and redaction helpers (offline only).…, test_error_messages_carry_a_short_redacted_excerpt(), test_meter_discovery()

### Community 29 - ".isHorizontal"
Cohesion: 0.26
Nodes (6): ki(), Oi(), Qs(), Si(), x(), zs()

### Community 30 - ".getDatasetMeta"
Cohesion: 0.19
Nodes (3): aa(), afterDatasetsUpdate(), onClick()

### Community 31 - "ro"
Cohesion: 0.16
Nodes (8): ao(), co(), Do(), inXRange(), inYRange(), Oe(), ro(), Y()

### Community 32 - "s"
Cohesion: 0.10
Nodes (18): buildTicks(), fa(), l(), ii(), label(), mo(), s(), parse() (+10 more)

### Community 33 - "config.py"
Cohesion: 0.08
Nodes (23): credentials_present(), _load_env_file(), Path, Runtime configuration, read once at import from the environment and an optional…, Populate os.environ from a KEY=VALUE file. Real environment variables always…, consumption Package, ConsumptionMonitor - local API for electricity and water consumption from…, Console UTF-8 Reconfiguration (+15 more)

### Community 34 - "upsert_meter_readings"
Cohesion: 0.34
Nodes (15): upsert_meter_readings(), _conn(), _elec(), date, datetime, MeterReading, Offline self-checks for raw meter reading storage and exact register deltas., A day with no reading past its closing midnight still reports what has accrued. (+7 more)

### Community 35 - "readings.py"
Cohesion: 0.21
Nodes (15): _buckets(), _exists_locally(), _hour_of_day(), _hour_of_timestamp(), _label(), parse_hourly(), date, datetime (+7 more)

### Community 36 - "records.py"
Cohesion: 0.26
Nodes (14): alert_flags(), coverage(), daily_totals(), fetch_readings(), IntervalReading, intervals(), latest_reading(), meter_readings() (+6 more)

### Community 37 - "api.js"
Cohesion: 0.23
Nodes (14): addDaysIso(), ApiError, daysBetween(), fetchHealth(), fetchHourlyRange(), fetchLocale(), fetchSeries(), GRANULARITY_PATHS (+6 more)

### Community 38 - "7. Contract addendum (comparison fold wave)"
Cohesion: 0.08
Nodes (23): 1. Hourly endpoint JSON, 2. The pure function, 3. CSS custom properties, 4. Locale keys and JS module exports, 5. Contract addendum (redesign wave), 6. Contract addendum (data-completeness wave), 7. Contract addendum (comparison fold wave), Breadcrumb (+15 more)

### Community 40 - "web/chart.js"
Cohesion: 0.22
Nodes (11): toggleTheme(), barAlpha(), createChart(), cssVar(), hexToRgba(), numberFmt, onBarClick(), reducedMotion() (+3 more)

### Community 41 - "connection_report.py"
Cohesion: 0.29
Nodes (10): Blank the value of every credential-looking JSON key in `text`., redact(), _dump(), main(), _mask(), _meters_section(), _probe(), First-contact diagnostic: signs in once and writes down what the portal… (+2 more)

### Community 42 - "series.js"
Cohesion: 0.27
Nodes (12): buildChartData(), buildHourCategories(), buildRunningChart(), capSeries(), foldForComparison(), formatDayLabel(), formatMonthCategory(), formatMonthSeriesLabel() (+4 more)

### Community 43 - "u"
Cohesion: 0.21
Nodes (5): addBox(), configure(), reset(), start(), u()

### Community 44 - ".buildOrUpdateControllers"
Cohesion: 0.14
Nodes (6): addElements(), kn(), ln(), qn(), removeBox(), stop()

### Community 45 - "ya"
Cohesion: 0.23
Nodes (3): afterUpdate(), va(), ya

### Community 46 - ".getDataset"
Cohesion: 0.11
Nodes (6): at(), beforeUpdate(), initialize(), rt(), w(), Ye()

### Community 47 - "connect"
Cohesion: 0.28
Nodes (8): get_conn(), connect(), init_schema(), Create tables if this file has not been initialized in this process., Path, log(), main(), Run backfill jobs until BACKFILL_DONE or no progress. Logs to…

### Community 48 - "launcher-common.ps1"
Cohesion: 0.32
Nodes (10): Exit-WithError(), Format-ExitCode(), Get-ConsumptionApiProcessIds(), Get-ProjectRootPath(), Stop-PreviousConsumptionSessions(), Test-IsConsumptionApiProcess(), Test-TcpPort(), Wait-ApiReady() (+2 more)

### Community 49 - "oo"
Cohesion: 0.24
Nodes (3): io(), no(), oo

### Community 50 - "un"
Cohesion: 0.22
Nodes (7): b(), cn(), dn(), fe(), hn(), init(), un()

### Community 51 - ".getContext"
Cohesion: 0.22
Nodes (5): Ae(), Bi(), Ci(), cs, Fi()

### Community 52 - ".getSortedVisibleDatasetMetas"
Cohesion: 0.25
Nodes (5): es(), generateLabels(), getRange(), _i(), ji()

### Community 54 - ".draw"
Cohesion: 0.19
Nodes (3): afterDraw(), lo(), wi()

### Community 55 - "mycitygrid.com portal recon (no credentials)"
Cohesion: 0.29
Nodes (6): Best guess at the consumption endpoints, Best guess at the login flow, Dead ends, mycitygrid.com portal recon (no credentials), Unknowns that only credentials can answer, What we know

### Community 58 - "env.ps1"
Cohesion: 1.00
Nodes (3): Initialize-Venv(), Show-Phase(), Wait-WithProgress()

## Knowledge Gaps
- **57 isolated node(s):** `1. Hourly endpoint JSON`, `2. The pure function`, `3. CSS custom properties`, `4. Locale keys and JS module exports`, ``/health` coverage fields` (+52 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `tn` connect `tn` to `chart.umd.min.js`, `de`, `updateElements`, `ho`, `i`, `a`, `n`, `.update`, `sn`, `r`, `.isHorizontal`, `.getDatasetMeta`, `ro`, `s`, `.notifyPlugins`, `u`, `.buildOrUpdateControllers`, `.getContext`, `.getSortedVisibleDatasetMetas`, `.draw`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Why does `xt` connect `xt` to `chart.umd.min.js`, `jt`, `.notifyPlugins`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Why does `sn` connect `sn` to `chart.umd.min.js`, `.buildOrUpdateControllers`, `.update`, `.notifyPlugins`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `s()` (e.g. with `beforeUpdate()` and `bs()`) actually correct?**
  _`s()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `a()` (e.g. with `ai()` and `draw()`) actually correct?**
  _`a()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `SourceError` (e.g. with `_Portal` and `test_malformed_row_raises_with_excerpt()`) actually correct?**
  _`SourceError` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `1. Hourly endpoint JSON`, `2. The pure function`, `3. CSS custom properties` to the rest of the system?**
  _57 weakly-connected nodes found - possible documentation gaps or missing edges._