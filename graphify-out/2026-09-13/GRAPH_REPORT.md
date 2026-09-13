# Graph Report - ConsumptionMonitor  (2026-09-13)

## Corpus Check
- 49 files · ~35,600 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1414 nodes · 3681 edges · 74 communities (64 shown, 10 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 134 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f982dd75`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- chart.umd.min.js
- i
- ha_bridge.py
- updateElements
- sn
- app.js
- tn
- db.py
- ho
- a
- jt
- api.py
- SourceError
- test_source_session.py
- jobs.py
- config.py
- da
- controls.js
- secrets.py
- 7. Contract addendum (comparison fold wave)
- o
- .update
- test_jobs.py
- source.py
- bindEvents
- .update
- s
- ro
- l
- upsert_meter_readings
- xt
- readings.py
- api.js
- web/chart.js
- records.py
- run.sh
- n
- 1.0.0
- series.js
- .getDatasetMeta
- .buildOrUpdateControllers
- test_api_contract.py
- _AllowedClientIPMiddleware
- refresh
- launcher-common.ps1
- u
- connect
- connection_report.py
- .getContext
- ha_entities.py
- de
- .notifyPlugins
- bo
- test_source_parsing.py
- hs
- .isHorizontal
- Z
- mycitygrid.com portal recon (no credentials)
- rn
- ConsumptionMonitor
- env.ps1
- yn
- Vendored third-party assets
- Hourly-Only Granularity Convention
- ne
- Double-Clickable Launcher Preference
- Run via run.bat
- .add
- Si
- ki

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
- 3-file cycle: `consumption/ha_bridge.py -> consumption/ha_entities.py -> consumption/jobs.py -> consumption/ha_bridge.py`

## Communities (74 total, 10 thin omitted)

### Community 0 - "chart.umd.min.js"
Cohesion: 0.05
Nodes (15): beforeUpdate(), getMaxOverflow(), initialize(), labelColor(), labelPointStyle(), Ls(), Nn(), pe() (+7 more)

### Community 1 - "i"
Cohesion: 0.13
Nodes (17): bs(), ct(), et(), Fs(), ge(), j(), ko(), ks() (+9 more)

### Community 2 - "ha_bridge.py"
Cohesion: 0.06
Nodes (62): set_state(), addon_version(), bridge_enabled(), _config_value(), energy_statistics_enabled(), import_energy_statistics(), _mqtt_publish(), publish_entities() (+54 more)

### Community 3 - "updateElements"
Cohesion: 0.10
Nodes (19): Ae(), Bn(), _calculateBarIndexPixels(), _calculateBarValuePixels(), _getAxis(), _getAxisCount(), getFirstScaleIdForIndexAxis(), getLabelAndValue() (+11 more)

### Community 5 - "app.js"
Cohesion: 0.11
Nodes (36): applyLocale(), chartData, chartWrap, coverage, crumbLabel(), els, exportCsv(), granularityLabel() (+28 more)

### Community 6 - "tn"
Cohesion: 0.06
Nodes (5): Ie(), tn, Us(), Y(), Ys()

### Community 7 - "db.py"
Cohesion: 0.18
Nodes (31): daily_totals(), due(), _fetch_readings_for_meter(), _first_reading_on_or_after(), _interval_dict(), intervals(), _last_reading_before(), latest_reading() (+23 more)

### Community 8 - "ho"
Cohesion: 0.06
Nodes (15): buildLookupTable(), _generate(), getDecimalForValue(), _getTimestampsForTable(), getValueForPixel(), ho(), init(), initOffsets() (+7 more)

### Community 9 - "a"
Cohesion: 0.13
Nodes (14): a(), determineDataLimits(), draw(), dt(), fo(), getRange(), inRange(), ji() (+6 more)

### Community 10 - "jt"
Cohesion: 0.09
Nodes (14): Bt(), color(), Ft(), Gt(), It(), jt(), kt(), mt() (+6 more)

### Community 11 - "api.py"
Cohesion: 0.19
Nodes (33): Conn, _directions_for(), _first_stored(), health(), index(), job_status(), _latest_register(), _meter_ids() (+25 more)

### Community 12 - "SourceError"
Cohesion: 0.15
Nodes (27): _bool_value(), _optional_float(), _optional_int(), parse_reading_page(), parse_reading_row(), datetime, Pure parsers for the mycitygrid meter reading log (GET meterdata). Maps portal…, Return the `items` list from one paginated reading-log response. (+19 more)

### Community 13 - "test_source_session.py"
Cohesion: 0.14
Nodes (20): _login(), Scaffold Complete, Fetching Unimplemented, Fetching Not Implemented Status, _FakePortal, _FakeResponse, _FakeSession, _raises(), Self-check for the mycitygrid adapter HTTP half: login, token refresh, reading-… (+12 more)

### Community 14 - "jobs.py"
Cohesion: 0.14
Nodes (28): _advance_backfill(), _always(), _backfill(), _in_january(), Job, local_today(), loop(), _month_bounds() (+20 more)

### Community 15 - "config.py"
Cohesion: 0.08
Nodes (23): credentials_present(), _load_env_file(), Path, Runtime configuration, read once at import from the environment and an optional…, Populate os.environ from a KEY=VALUE file. Real environment variables always…, consumption Package, ConsumptionMonitor - local API for electricity and water consumption from…, Console UTF-8 Reconfiguration (+15 more)

### Community 16 - "da"
Cohesion: 0.12
Nodes (19): beforeDatasetDraw(), beforeDatasetsDraw(), ca, da(), ea(), fa(), ga(), getBasePixel() (+11 more)

### Community 17 - "controls.js"
Cohesion: 0.17
Nodes (25): onRangeChange(), addDays(), applyPreset(), clampHourSpan(), coverageYears(), daysInclusive(), daysInMonth(), defaultRangeFor() (+17 more)

### Community 18 - "secrets.py"
Cohesion: 0.10
Nodes (25): Array, _credentials(), Encrypted store first on Windows; elsewhere env vars only (HA add-on path)., _Blob, clear(), _crypt32(), _dpapi(), _input_blob() (+17 more)

### Community 19 - "7. Contract addendum (comparison fold wave)"
Cohesion: 0.08
Nodes (24): 1. Hourly endpoint JSON, 2. The pure function, 3. CSS custom properties, 4. Locale keys and JS module exports, 5. Contract addendum (redesign wave), 6. Contract addendum (data-completeness wave), 7. Contract addendum (comparison fold wave), Breadcrumb (+16 more)

### Community 20 - "o"
Cohesion: 0.12
Nodes (15): at(), b(), cn(), dn(), e(), fe(), gi(), hn() (+7 more)

### Community 21 - ".update"
Cohesion: 0.13
Nodes (3): d(), Di(), Pn()

### Community 22 - "test_jobs.py"
Cohesion: 0.21
Nodes (20): get_state(), MeterReading, Exception, _conn(), _fake_source(), date, datetime, Offline self-checks for the refresh schedule and job bookkeeping. Uses a… (+12 more)

### Community 23 - "source.py"
Cohesion: 0.18
Nodes (13): RuntimeError, The adapter is not implemented or not configured. Not a transient failure., SourceNotReady, _decode(), _fetch_readings(), _Portal, date, datetime (+5 more)

### Community 24 - "bindEvents"
Cohesion: 0.16
Nodes (20): applyHash(), bindEvents(), buttonMatchesUtility(), drillDown(), handleBarClick(), init(), initTheme(), parseHash() (+12 more)

### Community 25 - ".update"
Cohesion: 0.19
Nodes (7): afterDraw(), afterEvent(), Ba(), f(), Ta(), wa, za()

### Community 26 - "s"
Cohesion: 0.10
Nodes (16): beforeLayout(), eo(), g(), Go(), is(), g(), label(), m() (+8 more)

### Community 27 - "ro"
Cohesion: 0.14
Nodes (8): ao(), co(), Do(), inXRange(), inYRange(), Oe(), ro(), s()

### Community 28 - "l"
Cohesion: 0.15
Nodes (11): buildTicks(), l(), ii(), mo(), parse(), parseArrayData(), parseObjectData(), parsePrimitiveData() (+3 more)

### Community 29 - "upsert_meter_readings"
Cohesion: 0.38
Nodes (14): upsert_meter_readings(), _conn(), _elec(), date, datetime, Offline self-checks for raw meter reading storage and exact register deltas., A day with no reading past its closing midnight still reports what has accrued., Portal sometimes emits a new meter_data_id for an unchanged reading_time_utc. (+6 more)

### Community 30 - "xt"
Cohesion: 0.10
Nodes (6): an(), as(), on, rs(), ts(), xt

### Community 31 - "readings.py"
Cohesion: 0.21
Nodes (15): _buckets(), _exists_locally(), _hour_of_day(), _hour_of_timestamp(), _label(), parse_hourly(), date, datetime (+7 more)

### Community 32 - "api.js"
Cohesion: 0.22
Nodes (16): addDaysIso(), API_ROOT, ApiError, daysBetween(), fetchHealth(), fetchHourlyRange(), fetchLocale(), fetchSeries() (+8 more)

### Community 33 - "web/chart.js"
Cohesion: 0.21
Nodes (12): paintChart(), toggleTheme(), barAlpha(), createChart(), cssVar(), hexToRgba(), numberFmt, onBarClick() (+4 more)

### Community 34 - "records.py"
Cohesion: 0.26
Nodes (14): alert_flags(), coverage(), daily_totals(), fetch_readings(), IntervalReading, intervals(), latest_reading(), meter_readings() (+6 more)

### Community 35 - "run.sh"
Cohesion: 0.17
Nodes (11): ADDON_VERSION, ALLOWED_CLIENT_IPS, ALLOWED_HOSTS, DB_PATH, HA_BRIDGE, HOST, LOCAL_TZ, MYCITYGRID_PASSWORD (+3 more)

### Community 36 - "n"
Cohesion: 0.16
Nodes (4): fn(), gn(), n(), pi()

### Community 37 - "1.0.0"
Cohesion: 0.50
Nodes (3): 1.0.0, Changelog, Release process

### Community 38 - "series.js"
Cohesion: 0.25
Nodes (13): buildChartData(), buildHourCategories(), buildRunningChart(), capSeries(), foldForComparison(), formatDayLabel(), formatMonthCategory(), formatMonthSeriesLabel() (+5 more)

### Community 39 - ".getDatasetMeta"
Cohesion: 0.16
Nodes (4): aa(), afterDatasetsUpdate(), generateLabels(), onClick()

### Community 40 - ".buildOrUpdateControllers"
Cohesion: 0.19
Nodes (4): addElements(), kn(), ln(), qn()

### Community 41 - "test_api_contract.py"
Cohesion: 0.17
Nodes (18): Offline contract checks for the HTTP API against the records.py storage…, test_alerts_per_meter(), test_allowed_client_ip_allows_listed_peer(), test_allowed_client_ip_rejects_unknown_peer(), test_allowed_client_ip_unset_allows_testclient(), test_bad_utility_returns_422(), _test_client(), test_health_coverage_shape() (+10 more)

### Community 43 - "refresh"
Cohesion: 0.22
Nodes (10): Force one job to run now, for testing a freshly implemented source adapter., refresh(), _reject_cross_site_refresh(), security_headers(), job_states(), middleware, post, Endpoint Reference Table (+2 more)

### Community 44 - "launcher-common.ps1"
Cohesion: 0.32
Nodes (10): Exit-WithError(), Format-ExitCode(), Get-ConsumptionApiProcessIds(), Get-ProjectRootPath(), Stop-PreviousConsumptionSessions(), Test-IsConsumptionApiProcess(), Test-TcpPort(), Wait-ApiReady() (+2 more)

### Community 45 - "u"
Cohesion: 0.23
Nodes (5): addBox(), configure(), reset(), start(), u()

### Community 46 - "connect"
Cohesion: 0.22
Nodes (10): get_conn(), lifespan(), connect(), init_schema(), Path, Create tables if this file has not been initialized in this process., FastAPI, log() (+2 more)

### Community 47 - "connection_report.py"
Cohesion: 0.29
Nodes (10): Blank the value of every credential-looking JSON key in `text`., redact(), _dump(), main(), _mask(), _meters_section(), _probe(), First-contact diagnostic: signs in once and writes down what the portal… (+2 more)

### Community 48 - ".getContext"
Cohesion: 0.27
Nodes (4): Bi(), Ci(), cs, Fi()

### Community 49 - "ha_entities.py"
Cohesion: 0.16
Nodes (26): alert_flags(), _binary_cmp(), build_discovery(), build_state(), _directions(), _ha_unit(), _latest_scraper_error(), _meter_ids() (+18 more)

### Community 50 - "de"
Cohesion: 0.17
Nodes (4): ce(), de, en, he()

### Community 52 - "bo"
Cohesion: 0.18
Nodes (3): bo, H(), xo()

### Community 54 - "test_source_parsing.py"
Cohesion: 0.31
Nodes (6): parse_meters(), Map utility -> meter ids from a `user/info` body. An empty list for a utility…, _raises(), Self-check for user/info meter discovery and redaction helpers (offline only).…, test_error_messages_carry_a_short_redacted_excerpt(), test_meter_discovery()

### Community 56 - ".isHorizontal"
Cohesion: 0.18
Nodes (4): afterUpdate(), tt(), va(), ya

### Community 57 - "Z"
Cohesion: 0.10
Nodes (23): ai(), average(), beforeDraw(), dataset(), es(), getCenterPoint(), hi(), _i() (+15 more)

### Community 58 - "mycitygrid.com portal recon (no credentials)"
Cohesion: 0.29
Nodes (6): Best guess at the consumption endpoints, Best guess at the login flow, Dead ends, mycitygrid.com portal recon (no credentials), Unknowns that only credentials can answer, What we know

### Community 60 - "ConsumptionMonitor"
Cohesion: 0.17
Nodes (11): Add-on options, Adopt existing history (recommended), Automations, ConsumptionMonitor, Daily electricity threshold, Energy dashboard, Entities, Install (+3 more)

### Community 61 - "env.ps1"
Cohesion: 1.00
Nodes (3): Initialize-Venv(), Show-Phase(), Wait-WithProgress()

### Community 65 - "ne"
Cohesion: 0.40
Nodes (3): Be(), ne(), numeric()

### Community 71 - ".add"
Cohesion: 0.60
Nodes (4): ei(), je(), ti(), ze()

### Community 72 - "Si"
Cohesion: 0.22
Nodes (6): Ee(), Le(), Oi(), Si(), wi(), x()

### Community 73 - "ki"
Cohesion: 0.40
Nodes (3): ki(), Qs(), zs()

## Knowledge Gaps
- **80 isolated node(s):** `IntervalReading`, `run.sh script`, `HOST`, `PORT`, `DB_PATH` (+75 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `tn` connect `tn` to `chart.umd.min.js`, `i`, `updateElements`, `sn`, `ho`, `a`, `.update`, `s`, `l`, `.getDatasetMeta`, `.buildOrUpdateControllers`, `u`, `.getContext`, `de`, `.notifyPlugins`, `bo`, `Z`, `yn`, `Si`, `ki`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `n()` connect `n` to `chart.umd.min.js`, `i`, `tn`, `ho`, `a`, `da`, `o`, `.update`, `.update`, `s`, `ro`, `l`, `xt`, `.getDatasetMeta`, `.buildOrUpdateControllers`, `u`, `rn`, `ne`, `.add`, `Si`, `ki`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Why does `wa` connect `.update` to `chart.umd.min.js`, `updateElements`, `Si`, `.getContext`, `.isHorizontal`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `s()` (e.g. with `beforeUpdate()` and `bs()`) actually correct?**
  _`s()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `a()` (e.g. with `ai()` and `draw()`) actually correct?**
  _`a()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `SourceError` (e.g. with `_Portal` and `test_malformed_row_raises_with_excerpt()`) actually correct?**
  _`SourceError` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `IntervalReading`, `run.sh script`, `HOST` to the rest of the system?**
  _80 weakly-connected nodes found - possible documentation gaps or missing edges._