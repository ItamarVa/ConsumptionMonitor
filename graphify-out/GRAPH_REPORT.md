# Graph Report - ConsumptionMonitor  (2026-09-13)

## Corpus Check
- 50 files · ~36,168 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1430 nodes · 3682 edges · 75 communities (63 shown, 12 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 127 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cd501687`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ha_bridge.py
- chart.umd.min.js
- ho
- jobs.py
- api.py
- tn
- app.js
- a
- xt
- db.py
- secrets.py
- test_source_session.py
- ya
- spread_to_hours
- .update
- SourceError
- controls.js
- s
- jt
- i
- config.py
- 7. Contract addendum (comparison fold wave)
- n
- inRange
- ro
- So
- Home Assistant add-on
- source.py
- .update
- bindEvents
- da
- sn
- api.js
- u
- parse
- test_jobs.py
- readings.py
- records.py
- test_api_contract.py
- web/chart.js
- .getDatasetMeta
- Si
- series.js
- .getContext
- .isHorizontal
- connection_report.py
- upsert_meter_readings
- ConsumptionMonitor
- run.sh
- launcher-common.ps1
- .buildOrUpdateControllers
- refresh
- .notifyPlugins
- connect
- test_source_parsing.py
- o
- hs
- update
- mycitygrid.com portal recon (no credentials)
- .getSortedVisibleDatasetMetas
- ki
- _AllowedClientIPMiddleware
- Connection
- date
- Changelog
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
- `portal_session()` --implements--> `Lazy Scrapling Import Lesson`  [INFERRED]
  consumption/source.py → .cursor/memory/INDEX.md
- `run_job()` --implements--> `Idempotent Refresh Jobs Convention`  [INFERRED]
  consumption/jobs.py → .cursor/memory/INDEX.md
- `_range()` --references--> `api.py as Only Trust Boundary`  [EXTRACTED]
  consumption/api.py → .cursor/memory/INDEX.md
- `summary()` --references--> `Endpoint Reference Table`  [EXTRACTED]
  consumption/api.py → README.md

## Import Cycles
- 3-file cycle: `consumption/ha_bridge.py -> consumption/ha_entities.py -> consumption/jobs.py -> consumption/ha_bridge.py`

## Communities (75 total, 12 thin omitted)

### Community 0 - "ha_bridge.py"
Cohesion: 0.05
Nodes (73): _load_env_file(), Populate os.environ from a KEY=VALUE file. Real environment variables always…, set_state(), addon_version(), bridge_enabled(), _config_value(), energy_statistics_enabled(), import_energy_statistics() (+65 more)

### Community 1 - "chart.umd.min.js"
Cohesion: 0.04
Nodes (30): at(), b(), beforeUpdate(), cn(), dn(), Ee(), fe(), getMaxOverflow() (+22 more)

### Community 2 - "ho"
Cohesion: 0.07
Nodes (13): buildLookupTable(), _generate(), getDecimalForValue(), _getTimestampsForTable(), getValueForPixel(), ho(), init(), initOffsets() (+5 more)

### Community 3 - "jobs.py"
Cohesion: 0.15
Nodes (27): _advance_backfill(), _always(), _backfill(), _in_january(), Job, local_today(), loop(), _month_bounds() (+19 more)

### Community 4 - "api.py"
Cohesion: 0.21
Nodes (31): Conn, Connection, _directions_for(), _first_stored(), health(), index(), _latest_register(), _meter_ids() (+23 more)

### Community 5 - "tn"
Cohesion: 0.06
Nodes (3): tn, Us(), Ys()

### Community 6 - "app.js"
Cohesion: 0.11
Nodes (36): applyLocale(), chartData, chartWrap, coverage, crumbLabel(), els, exportCsv(), granularityLabel() (+28 more)

### Community 7 - "a"
Cohesion: 0.10
Nodes (18): a(), ai(), beforeDraw(), determineDataLimits(), draw(), fo(), getRange(), hi() (+10 more)

### Community 8 - "xt"
Cohesion: 0.10
Nodes (6): an(), as(), on, rs(), ts(), xt

### Community 9 - "db.py"
Cohesion: 0.15
Nodes (36): alert_flags(), daily_totals(), due(), _fetch_readings_for_meter(), _first_reading_on_or_after(), _interval_dict(), intervals(), _last_reading_before() (+28 more)

### Community 10 - "secrets.py"
Cohesion: 0.10
Nodes (25): Array, _credentials(), Encrypted store first on Windows; elsewhere env vars only (HA add-on path)., _Blob, clear(), _crypt32(), _dpapi(), _input_blob() (+17 more)

### Community 11 - "test_source_session.py"
Cohesion: 0.15
Nodes (19): _login(), Scaffold Complete, Fetching Unimplemented, Fetching Not Implemented Status, _FakePortal, _FakeResponse, _FakeSession, _raises(), Self-check for the mycitygrid adapter HTTP half: login, token refresh, reading-… (+11 more)

### Community 12 - "ya"
Cohesion: 0.21
Nodes (3): afterUpdate(), va(), ya

### Community 13 - "spread_to_hours"
Cohesion: 0.17
Nodes (19): _build_buckets(), _parse_utc(), Any, date, datetime, Proportional hour-bucket spreading for cumulative meter registers. Pure math…, Distribute each consecutive register delta across the local hours it covers., spread_to_hours() (+11 more)

### Community 14 - ".update"
Cohesion: 0.20
Nodes (6): afterDraw(), afterEvent(), Ba(), Ta(), wa, za()

### Community 15 - "SourceError"
Cohesion: 0.17
Nodes (22): _bool_value(), _optional_float(), _optional_int(), parse_reading_row(), datetime, Pure parsers for the mycitygrid meter reading log (GET meterdata). Maps portal…, Map one portal reading-log row to a MeterReading., _reading_time_utc() (+14 more)

### Community 16 - "controls.js"
Cohesion: 0.17
Nodes (25): onRangeChange(), addDays(), applyPreset(), clampHourSpan(), coverageYears(), daysInclusive(), daysInMonth(), defaultRangeFor() (+17 more)

### Community 17 - "s"
Cohesion: 0.08
Nodes (25): Bn(), _calculateBarIndexPixels(), _calculateBarValuePixels(), _getAxis(), _getAxisCount(), getFirstScaleIdForIndexAxis(), getLabelAndValue(), getLabelForValue() (+17 more)

### Community 18 - "jt"
Cohesion: 0.09
Nodes (14): Bt(), color(), Ft(), Gt(), It(), jt(), kt(), mt() (+6 more)

### Community 19 - "i"
Cohesion: 0.14
Nodes (13): bs(), ct(), Fs(), ge(), is(), ks(), ms(), ps() (+5 more)

### Community 20 - "config.py"
Cohesion: 0.09
Nodes (20): credentials_present(), Runtime configuration, read once at import from the environment and an optional…, consumption Package, ConsumptionMonitor - local API for electricity and water consumption from…, Console UTF-8 Reconfiguration, main(), Entry point: `python -m consumption` serves the API and runs the refresh…, portal_session() (+12 more)

### Community 21 - "7. Contract addendum (comparison fold wave)"
Cohesion: 0.09
Nodes (23): 1. Hourly endpoint JSON, 2. The pure function, 3. CSS custom properties, 4. Locale keys and JS module exports, 5. Contract addendum (redesign wave), 6. Contract addendum (data-completeness wave), 7. Contract addendum (comparison fold wave), Breadcrumb (+15 more)

### Community 22 - "n"
Cohesion: 0.07
Nodes (11): Be(), fn(), g(), gn(), n(), ne(), numeric(), Oe() (+3 more)

### Community 23 - "inRange"
Cohesion: 0.20
Nodes (14): average(), dataset(), getCenterPoint(), index(), inRange(), nearest(), qi(), Re() (+6 more)

### Community 24 - "ro"
Cohesion: 0.19
Nodes (7): ao(), co(), Do(), inXRange(), inYRange(), ro(), Y()

### Community 25 - "So"
Cohesion: 0.07
Nodes (10): bo, ce(), de, dt(), en, H(), he(), j() (+2 more)

### Community 26 - "Home Assistant add-on"
Cohesion: 0.33
Nodes (5): Home Assistant add-on, Home Assistant integration, Packaging, Runtime, Windows handoff

### Community 27 - "source.py"
Cohesion: 0.18
Nodes (14): RuntimeError, The adapter is not implemented or not configured. Not a transient failure., SourceNotReady, _decode(), _fetch_meter_readings(), _fetch_readings(), _Portal, _probe_page() (+6 more)

### Community 28 - ".update"
Cohesion: 0.13
Nodes (3): d(), Di(), Pn()

### Community 29 - "bindEvents"
Cohesion: 0.16
Nodes (20): applyHash(), bindEvents(), buttonMatchesUtility(), drillDown(), handleBarClick(), init(), initTheme(), parseHash() (+12 more)

### Community 30 - "da"
Cohesion: 0.14
Nodes (16): beforeDatasetDraw(), beforeDatasetsDraw(), ca, da(), ea(), fa(), ga(), getBasePixel() (+8 more)

### Community 32 - "api.js"
Cohesion: 0.22
Nodes (16): addDaysIso(), API_ROOT, ApiError, daysBetween(), fetchHealth(), fetchHourlyRange(), fetchLocale(), fetchSeries() (+8 more)

### Community 33 - "u"
Cohesion: 0.21
Nodes (5): addBox(), configure(), reset(), start(), u()

### Community 34 - "parse"
Cohesion: 0.14
Nodes (8): buildTicks(), ii(), mo(), parse(), parseArrayData(), parsePrimitiveData(), po(), Vn()

### Community 35 - "test_jobs.py"
Cohesion: 0.21
Nodes (19): get_state(), Exception, _conn(), _fake_source(), date, datetime, Offline self-checks for the refresh schedule and job bookkeeping. Uses a…, Stand in for the portal: one reading per utility when start falls in those… (+11 more)

### Community 36 - "readings.py"
Cohesion: 0.21
Nodes (15): _buckets(), _exists_locally(), _hour_of_day(), _hour_of_timestamp(), _label(), parse_hourly(), date, datetime (+7 more)

### Community 37 - "records.py"
Cohesion: 0.25
Nodes (15): alert_flags(), coverage(), daily_totals(), fetch_readings(), IntervalReading, intervals(), latest_reading(), meter_readings() (+7 more)

### Community 38 - "test_api_contract.py"
Cohesion: 0.12
Nodes (22): _NormalizePathMiddleware, Collapse duplicate slashes in the path (HA Ingress can request //ui)., Offline contract checks for the HTTP API against the records.py storage…, test_alerts_per_meter(), test_allowed_client_ip_allows_listed_peer(), test_allowed_client_ip_rejects_unknown_peer(), test_allowed_client_ip_unset_allows_testclient(), test_bad_utility_returns_422() (+14 more)

### Community 39 - "web/chart.js"
Cohesion: 0.23
Nodes (12): paintChart(), toggleTheme(), barAlpha(), createChart(), cssVar(), hexToRgba(), numberFmt, onBarClick() (+4 more)

### Community 40 - ".getDatasetMeta"
Cohesion: 0.22
Nodes (3): aa(), afterDatasetsUpdate(), onClick()

### Community 41 - "Si"
Cohesion: 0.21
Nodes (5): lo(), Oi(), Si(), wi(), x()

### Community 42 - "series.js"
Cohesion: 0.25
Nodes (13): buildChartData(), buildHourCategories(), buildRunningChart(), capSeries(), foldForComparison(), formatDayLabel(), formatMonthCategory(), formatMonthSeriesLabel() (+5 more)

### Community 43 - ".getContext"
Cohesion: 0.27
Nodes (4): Bi(), Ci(), cs, Fi()

### Community 45 - "connection_report.py"
Cohesion: 0.24
Nodes (12): parse_reading_page(), Return the `items` list from one paginated reading-log response., Blank the value of every credential-looking JSON key in `text`., redact(), _dump(), main(), _mask(), _meters_section() (+4 more)

### Community 46 - "upsert_meter_readings"
Cohesion: 0.38
Nodes (14): upsert_meter_readings(), _conn(), _elec(), date, datetime, Offline self-checks for raw meter reading storage and exact register deltas., A day with no reading past its closing midnight still reports what has accrued., Portal sometimes emits a new meter_data_id for an unchanged reading_time_utc. (+6 more)

### Community 47 - "ConsumptionMonitor"
Cohesion: 0.17
Nodes (11): Add-on options, Adopt existing history (recommended), Automations, ConsumptionMonitor, Daily electricity threshold, Energy dashboard, Entities, Install (+3 more)

### Community 48 - "run.sh"
Cohesion: 0.17
Nodes (11): ADDON_VERSION, ALLOWED_CLIENT_IPS, ALLOWED_HOSTS, DB_PATH, HA_BRIDGE, HOST, LOCAL_TZ, MYCITYGRID_PASSWORD (+3 more)

### Community 49 - "launcher-common.ps1"
Cohesion: 0.32
Nodes (10): Exit-WithError(), Format-ExitCode(), Get-ConsumptionApiProcessIds(), Get-ProjectRootPath(), Stop-PreviousConsumptionSessions(), Test-IsConsumptionApiProcess(), Test-TcpPort(), Wait-ApiReady() (+2 more)

### Community 50 - ".buildOrUpdateControllers"
Cohesion: 0.19
Nodes (4): addElements(), kn(), ln(), qn()

### Community 51 - "refresh"
Cohesion: 0.18
Nodes (12): job_status(), Job names and ranges come from jobs.JOBS (recent, recent_week, previous_year,…, Force one job to run now, for testing a freshly implemented source adapter., refresh(), _reject_cross_site_refresh(), security_headers(), job_states(), middleware (+4 more)

### Community 53 - "connect"
Cohesion: 0.22
Nodes (10): get_conn(), lifespan(), connect(), init_schema(), Path, Create tables if this file has not been initialized in this process., FastAPI, log() (+2 more)

### Community 54 - "test_source_parsing.py"
Cohesion: 0.31
Nodes (6): parse_meters(), Map utility -> meter ids from a `user/info` body. An empty list for a utility…, _raises(), Self-check for user/info meter discovery and redaction helpers (offline only).…, test_error_messages_carry_a_short_redacted_excerpt(), test_meter_discovery()

### Community 55 - "o"
Cohesion: 0.29
Nodes (11): e(), ei(), gi(), je(), mi(), o(), qe(), ti() (+3 more)

### Community 57 - "update"
Cohesion: 0.15
Nodes (18): beforeLayout(), eo(), et(), f(), Go(), g(), ko(), m() (+10 more)

### Community 58 - "mycitygrid.com portal recon (no credentials)"
Cohesion: 0.29
Nodes (6): Best guess at the consumption endpoints, Best guess at the login flow, Dead ends, mycitygrid.com portal recon (no credentials), Unknowns that only credentials can answer, What we know

### Community 59 - ".getSortedVisibleDatasetMetas"
Cohesion: 0.22
Nodes (4): es(), generateLabels(), Ie(), Ni()

### Community 60 - "ki"
Cohesion: 0.40
Nodes (3): ki(), Qs(), zs()

### Community 65 - "Changelog"
Cohesion: 0.40
Nodes (4): 1.0.0, 1.0.1, Changelog, Release process

### Community 66 - "env.ps1"
Cohesion: 1.00
Nodes (3): Initialize-Venv(), Show-Phase(), Wait-WithProgress()

## Knowledge Gaps
- **83 isolated node(s):** `Packaging`, `Runtime`, `Home Assistant integration`, `Windows handoff`, `1.0.1` (+78 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `tn` connect `tn` to `chart.umd.min.js`, `ho`, `a`, `s`, `i`, `n`, `inRange`, `So`, `.update`, `sn`, `u`, `parse`, `.getDatasetMeta`, `Si`, `.getContext`, `.isHorizontal`, `.buildOrUpdateControllers`, `.notifyPlugins`, `.getSortedVisibleDatasetMetas`, `ki`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `n()` connect `n` to `chart.umd.min.js`, `parse`, `ho`, `u`, `tn`, `a`, `.getDatasetMeta`, `xt`, `Si`, `ki`, `.update`, `.buildOrUpdateControllers`, `i`, `o`, `ro`, `.update`, `da`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Why does `bo` connect `So` to `chart.umd.min.js`, `a`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `s()` (e.g. with `beforeUpdate()` and `bs()`) actually correct?**
  _`s()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `a()` (e.g. with `ai()` and `draw()`) actually correct?**
  _`a()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `SourceError` (e.g. with `_Portal` and `test_malformed_row_raises_with_excerpt()`) actually correct?**
  _`SourceError` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Packaging`, `Runtime`, `Home Assistant integration` to the rest of the system?**
  _83 weakly-connected nodes found - possible documentation gaps or missing edges._