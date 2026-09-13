# Graph Report - ConsumptionMonitor  (2026-09-13)

## Corpus Check
- 50 files · ~36,864 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1440 nodes · 3700 edges · 74 communities (56 shown, 18 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 126 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e186163e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- chart.umd.min.js
- ha_bridge.py
- test_api_contract.py
- ho
- jt
- app.js
- updateElements
- sn
- db.py
- api.py
- xt
- i
- spread_to_hours
- .isHorizontal
- a
- test_jobs.py
- SourceError
- .update
- .getContext
- tn
- test_source_session.py
- jobs.py
- s
- controls.js
- parse
- config.py
- 7. Contract addendum (comparison fold wave)
- n
- .update
- source.py
- ._computeLabelItems
- de
- bindEvents
- api.js
- upsert_meter_readings
- readings.py
- records.py
- .getSortedVisibleDatasetMetas
- series.js
- web/chart.js
- .register
- connect
- .getDatasetMeta
- rn
- .notifyPlugins
- ConsumptionMonitor
- run.sh
- launcher-common.ps1
- .buildOrUpdateControllers
- connection_report.py
- ._resolveElementOptions
- da
- refresh
- test_source_parsing.py
- hs
- yn
- mycitygrid.com portal recon (no credentials)
- .add
- Changelog
- Home Assistant add-on
- _AllowedClientIPMiddleware
- env.ps1
- Vendored third-party assets
- Hourly-Only Granularity Convention
- Connection
- Path
- Double-Clickable Launcher Preference
- date
- Run via run.bat
- MeterReading

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
- 3-file cycle: `consumption/ha_bridge.py -> consumption/ha_entities.py -> consumption/jobs.py -> consumption/ha_bridge.py`

## Communities (74 total, 18 thin omitted)

### Community 0 - "chart.umd.min.js"
Cohesion: 0.04
Nodes (23): at(), beforeLayout(), beforeUpdate(), et(), getMaxOverflow(), Go(), initialize(), j() (+15 more)

### Community 1 - "ha_bridge.py"
Cohesion: 0.05
Nodes (79): _load_env_file(), Populate os.environ from a KEY=VALUE file. Real environment variables always…, get_state(), addon_version(), bridge_enabled(), _config_value(), energy_statistics_enabled(), import_energy_statistics() (+71 more)

### Community 2 - "test_api_contract.py"
Cohesion: 0.12
Nodes (23): _NormalizePathMiddleware, Collapse duplicate slashes in the path (HA Ingress can request //ui)., Offline contract checks for the HTTP API against the records.py storage…, test_alerts_per_meter(), test_allowed_client_ip_allows_listed_peer(), test_allowed_client_ip_rejects_unknown_peer(), test_allowed_client_ip_unset_allows_testclient(), test_bad_utility_returns_422() (+15 more)

### Community 3 - "ho"
Cohesion: 0.06
Nodes (14): buildLookupTable(), _generate(), getDecimalForValue(), _getTimestampsForTable(), getValueForPixel(), ho(), initOffsets(), io() (+6 more)

### Community 4 - "jt"
Cohesion: 0.09
Nodes (14): Bt(), color(), Ft(), Gt(), It(), jt(), kt(), mt() (+6 more)

### Community 5 - "app.js"
Cohesion: 0.11
Nodes (36): applyLocale(), chartData, chartWrap, coverage, crumbLabel(), els, exportCsv(), granularityLabel() (+28 more)

### Community 6 - "updateElements"
Cohesion: 0.13
Nodes (17): aa(), Bn(), _calculateBarIndexPixels(), _calculateBarValuePixels(), Fs(), _getAxis(), _getAxisCount(), getFirstScaleIdForIndexAxis() (+9 more)

### Community 8 - "db.py"
Cohesion: 0.16
Nodes (34): daily_totals(), due(), _fetch_readings_for_meter(), _first_reading_on_or_after(), _interval_dict(), intervals(), _last_reading_before(), latest_reading() (+26 more)

### Community 9 - "api.py"
Cohesion: 0.20
Nodes (32): Conn, _directions_for(), _first_stored(), health(), index(), _latest_register(), _meter_ids(), _period_total() (+24 more)

### Community 10 - "xt"
Cohesion: 0.10
Nodes (5): an(), as(), on, ts(), xt

### Community 11 - "i"
Cohesion: 0.12
Nodes (19): bs(), ct(), dn(), e(), fe(), ge(), is(), K() (+11 more)

### Community 12 - "spread_to_hours"
Cohesion: 0.17
Nodes (19): _build_buckets(), _parse_utc(), Any, date, datetime, Proportional hour-bucket spreading for cumulative meter registers. Pure math…, Distribute each consecutive register delta across the local hours it covers., spread_to_hours() (+11 more)

### Community 13 - ".isHorizontal"
Cohesion: 0.09
Nodes (13): Ae(), afterDraw(), afterEvent(), afterUpdate(), Ee(), Le(), Oi(), Qs() (+5 more)

### Community 14 - "a"
Cohesion: 0.10
Nodes (27): a(), ai(), beforeDraw(), determineDataLimits(), draw(), fo(), getPixelForTick(), gi() (+19 more)

### Community 15 - "test_jobs.py"
Cohesion: 0.07
Nodes (42): Array, _credentials(), Encrypted store first on Windows; elsewhere env vars only (HA add-on path)., _Blob, clear(), _crypt32(), _dpapi(), _input_blob() (+34 more)

### Community 16 - "SourceError"
Cohesion: 0.15
Nodes (27): _bool_value(), _optional_float(), _optional_int(), parse_reading_page(), parse_reading_row(), datetime, Pure parsers for the mycitygrid meter reading log (GET meterdata). Maps portal…, Return the `items` list from one paginated reading-log response. (+19 more)

### Community 17 - ".update"
Cohesion: 0.09
Nodes (17): addBox(), b(), Ba(), cn(), configure(), hn(), init(), ki() (+9 more)

### Community 18 - ".getContext"
Cohesion: 0.06
Nodes (27): ao(), average(), Bi(), bo, Ci(), co(), cs, dataset() (+19 more)

### Community 20 - "test_source_session.py"
Cohesion: 0.15
Nodes (19): _login(), Scaffold Complete, Fetching Unimplemented, Fetching Not Implemented Status, _FakePortal, _FakeResponse, _FakeSession, _raises(), Self-check for the mycitygrid adapter HTTP half: login, token refresh, reading-… (+11 more)

### Community 21 - "jobs.py"
Cohesion: 0.15
Nodes (27): _advance_backfill(), _always(), _backfill(), _in_january(), Job, local_today(), loop(), _month_bounds() (+19 more)

### Community 22 - "s"
Cohesion: 0.14
Nodes (17): eo(), f(), g(), getRange(), H(), _i(), ji(), g() (+9 more)

### Community 23 - "controls.js"
Cohesion: 0.17
Nodes (25): onRangeChange(), addDays(), applyPreset(), clampHourSpan(), coverageYears(), daysInclusive(), daysInMonth(), defaultRangeFor() (+17 more)

### Community 24 - "parse"
Cohesion: 0.14
Nodes (8): buildTicks(), ii(), mo(), parse(), parseArrayData(), parsePrimitiveData(), po(), Vn()

### Community 25 - "config.py"
Cohesion: 0.09
Nodes (20): credentials_present(), Runtime configuration, read once at import from the environment and an optional…, consumption Package, ConsumptionMonitor - local API for electricity and water consumption from…, Console UTF-8 Reconfiguration, main(), Entry point: `python -m consumption` serves the API and runs the refresh…, portal_session() (+12 more)

### Community 26 - "7. Contract addendum (comparison fold wave)"
Cohesion: 0.09
Nodes (23): 1. Hourly endpoint JSON, 2. The pure function, 3. CSS custom properties, 4. Locale keys and JS module exports, 5. Contract addendum (redesign wave), 6. Contract addendum (data-completeness wave), 7. Contract addendum (comparison fold wave), Breadcrumb (+15 more)

### Community 27 - "n"
Cohesion: 0.16
Nodes (4): fn(), gn(), n(), pi()

### Community 28 - ".update"
Cohesion: 0.13
Nodes (3): d(), Di(), Pn()

### Community 29 - "source.py"
Cohesion: 0.16
Nodes (14): RuntimeError, The adapter is not implemented or not configured. Not a transient failure., SourceNotReady, _decode(), _fetch_readings(), _Portal, date, datetime (+6 more)

### Community 31 - "de"
Cohesion: 0.23
Nodes (4): ce(), de, dt(), he()

### Community 32 - "bindEvents"
Cohesion: 0.16
Nodes (20): applyHash(), bindEvents(), buttonMatchesUtility(), drillDown(), handleBarClick(), init(), initTheme(), parseHash() (+12 more)

### Community 33 - "api.js"
Cohesion: 0.22
Nodes (16): addDaysIso(), API_ROOT, ApiError, daysBetween(), fetchHealth(), fetchHourlyRange(), fetchLocale(), fetchSeries() (+8 more)

### Community 34 - "upsert_meter_readings"
Cohesion: 0.38
Nodes (14): upsert_meter_readings(), _conn(), _elec(), date, datetime, Offline self-checks for raw meter reading storage and exact register deltas., A day with no reading past its closing midnight still reports what has accrued., Portal sometimes emits a new meter_data_id for an unchanged reading_time_utc. (+6 more)

### Community 35 - "readings.py"
Cohesion: 0.21
Nodes (15): _buckets(), _exists_locally(), _hour_of_day(), _hour_of_timestamp(), _label(), parse_hourly(), date, datetime (+7 more)

### Community 36 - "records.py"
Cohesion: 0.25
Nodes (15): alert_flags(), coverage(), daily_totals(), fetch_readings(), IntervalReading, intervals(), latest_reading(), meter_readings() (+7 more)

### Community 37 - ".getSortedVisibleDatasetMetas"
Cohesion: 0.20
Nodes (3): es(), Ie(), Ni()

### Community 38 - "series.js"
Cohesion: 0.25
Nodes (13): buildChartData(), buildHourCategories(), buildRunningChart(), capSeries(), foldForComparison(), formatDayLabel(), formatMonthCategory(), formatMonthSeriesLabel() (+5 more)

### Community 39 - "web/chart.js"
Cohesion: 0.23
Nodes (12): paintChart(), toggleTheme(), barAlpha(), createChart(), cssVar(), hexToRgba(), numberFmt, onBarClick() (+4 more)

### Community 41 - "connect"
Cohesion: 0.22
Nodes (10): get_conn(), lifespan(), connect(), init_schema(), Path, Create tables if this file has not been initialized in this process., FastAPI, log() (+2 more)

### Community 42 - ".getDatasetMeta"
Cohesion: 0.13
Nodes (6): afterDatasetsUpdate(), generateLabels(), labelColor(), labelPointStyle(), onClick(), reset()

### Community 45 - "ConsumptionMonitor"
Cohesion: 0.17
Nodes (11): Add-on options, Adopt existing history (recommended), Automations, ConsumptionMonitor, Daily electricity threshold, Energy dashboard, Entities, Install (+3 more)

### Community 46 - "run.sh"
Cohesion: 0.17
Nodes (11): ADDON_VERSION, ALLOWED_CLIENT_IPS, ALLOWED_HOSTS, DB_PATH, HA_BRIDGE, HOST, LOCAL_TZ, MYCITYGRID_PASSWORD (+3 more)

### Community 47 - "launcher-common.ps1"
Cohesion: 0.32
Nodes (10): Exit-WithError(), Format-ExitCode(), Get-ConsumptionApiProcessIds(), Get-ProjectRootPath(), Stop-PreviousConsumptionSessions(), Test-IsConsumptionApiProcess(), Test-TcpPort(), Wait-ApiReady() (+2 more)

### Community 49 - "connection_report.py"
Cohesion: 0.29
Nodes (10): Blank the value of every credential-looking JSON key in `text`., redact(), _dump(), main(), _mask(), _meters_section(), _probe(), First-contact diagnostic: signs in once and writes down what the portal… (+2 more)

### Community 51 - "da"
Cohesion: 0.11
Nodes (19): beforeDatasetDraw(), beforeDatasetsDraw(), ca, da(), ea(), fa(), ga(), getBasePixel() (+11 more)

### Community 52 - "refresh"
Cohesion: 0.18
Nodes (12): job_status(), Job names and ranges come from jobs.JOBS (recent, recent_week, previous_year,…, Force one job to run now, for testing a freshly implemented source adapter., refresh(), _reject_cross_site_refresh(), security_headers(), job_states(), middleware (+4 more)

### Community 53 - "test_source_parsing.py"
Cohesion: 0.31
Nodes (6): parse_meters(), Map utility -> meter ids from a `user/info` body. An empty list for a utility…, _raises(), Self-check for user/info meter discovery and redaction helpers (offline only).…, test_error_messages_carry_a_short_redacted_excerpt(), test_meter_discovery()

### Community 55 - "yn"
Cohesion: 0.18
Nodes (4): Be(), ne(), numeric(), yn()

### Community 56 - "mycitygrid.com portal recon (no credentials)"
Cohesion: 0.29
Nodes (6): Best guess at the consumption endpoints, Best guess at the login flow, Dead ends, mycitygrid.com portal recon (no credentials), Unknowns that only credentials can answer, What we know

### Community 57 - ".add"
Cohesion: 0.60
Nodes (4): ei(), je(), ti(), ze()

### Community 59 - "Changelog"
Cohesion: 0.29
Nodes (6): 1.0.0, 1.0.1, 1.0.2, 1.0.3, Changelog, Release process

### Community 60 - "Home Assistant add-on"
Cohesion: 0.33
Nodes (5): Home Assistant add-on, Home Assistant integration, Packaging, Runtime, Windows handoff

### Community 63 - "env.ps1"
Cohesion: 1.00
Nodes (3): Initialize-Venv(), Show-Phase(), Wait-WithProgress()

## Knowledge Gaps
- **85 isolated node(s):** `Packaging`, `Runtime`, `Home Assistant integration`, `Windows handoff`, `1.0.3` (+80 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `tn` connect `tn` to `chart.umd.min.js`, `ho`, `.getSortedVisibleDatasetMetas`, `updateElements`, `.register`, `.getDatasetMeta`, `i`, `.notifyPlugins`, `.isHorizontal`, `a`, `.buildOrUpdateControllers`, `.update`, `.getContext`, `s`, `yn`, `parse`, `.update`, `._computeLabelItems`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `xt` connect `xt` to `chart.umd.min.js`, `jt`, `.notifyPlugins`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Why does `ho()` connect `ho` to `chart.umd.min.js`, `.update`, `.getContext`, `a`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `s()` (e.g. with `beforeUpdate()` and `bs()`) actually correct?**
  _`s()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `a()` (e.g. with `ai()` and `draw()`) actually correct?**
  _`a()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `SourceError` (e.g. with `_Portal` and `test_malformed_row_raises_with_excerpt()`) actually correct?**
  _`SourceError` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Packaging`, `Runtime`, `Home Assistant integration` to the rest of the system?**
  _85 weakly-connected nodes found - possible documentation gaps or missing edges._