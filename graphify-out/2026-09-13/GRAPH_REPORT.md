# Graph Report - ConsumptionMonitor  (2026-09-13)

## Corpus Check
- 50 files · ~35,942 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1421 nodes · 3674 edges · 69 communities (57 shown, 12 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 128 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a86bc9c2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ha_bridge.py
- chart.umd.min.js
- ho
- ha_entities.py
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
- excerpt
- controls.js
- updateElements
- jt
- i
- config.py
- 7. Contract addendum (comparison fold wave)
- n
- .getProps
- ro
- s
- Home Assistant add-on
- source.py
- Bt
- bindEvents
- .apply
- sn
- api.js
- .configure
- parse
- ._resolveElementOptions
- SourceError
- records.py
- test_api_contract.py
- web/chart.js
- .getDatasetMeta
- o
- series.js
- .getContext
- .isHorizontal
- connection_report.py
- de
- ConsumptionMonitor
- run.sh
- launcher-common.ps1
- cs
- rn
- .notifyPlugins
- .add
- hs
- m
- mycitygrid.com portal recon (no credentials)
- yn
- 1.0.0
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
- 3-file cycle: `consumption/ha_bridge.py -> consumption/ha_entities.py -> consumption/jobs.py -> consumption/ha_bridge.py`

## Communities (69 total, 12 thin omitted)

### Community 0 - "ha_bridge.py"
Cohesion: 0.09
Nodes (44): set_state(), addon_version(), bridge_enabled(), _config_value(), energy_statistics_enabled(), import_energy_statistics(), _mqtt_publish(), publish_entities() (+36 more)

### Community 1 - "chart.umd.min.js"
Cohesion: 0.04
Nodes (27): beforeDatasetDraw(), beforeDatasetsDraw(), beforeLayout(), ea(), ga(), getMaxOverflow(), Go(), ia() (+19 more)

### Community 2 - "ho"
Cohesion: 0.07
Nodes (14): buildLookupTable(), _generate(), getDecimalForValue(), _getTimestampsForTable(), getValueForPixel(), ho(), initOffsets(), io() (+6 more)

### Community 3 - "ha_entities.py"
Cohesion: 0.15
Nodes (27): alert_flags(), _binary_cmp(), build_discovery(), build_state(), _directions(), _ha_unit(), _latest_scraper_error(), _meter_ids() (+19 more)

### Community 4 - "api.py"
Cohesion: 0.11
Nodes (47): Conn, _AllowedClientIPMiddleware, _directions_for(), _first_stored(), health(), index(), job_status(), _latest_register() (+39 more)

### Community 5 - "tn"
Cohesion: 0.06
Nodes (7): d(), Di(), es(), generateLabels(), Pn(), reset(), tn

### Community 6 - "app.js"
Cohesion: 0.11
Nodes (36): applyLocale(), chartData, chartWrap, coverage, crumbLabel(), els, exportCsv(), granularityLabel() (+28 more)

### Community 7 - "a"
Cohesion: 0.15
Nodes (17): a(), determineDataLimits(), draw(), fa(), fo(), gi(), l(), inRange() (+9 more)

### Community 8 - "xt"
Cohesion: 0.09
Nodes (7): an(), as(), ln(), on, rs(), ts(), xt

### Community 9 - "db.py"
Cohesion: 0.05
Nodes (99): get_conn(), connect(), daily_totals(), due(), _fetch_readings_for_meter(), _first_reading_on_or_after(), get_state(), init_schema() (+91 more)

### Community 10 - "secrets.py"
Cohesion: 0.10
Nodes (25): Array, _credentials(), Encrypted store first on Windows; elsewhere env vars only (HA add-on path)., _Blob, clear(), _crypt32(), _dpapi(), _input_blob() (+17 more)

### Community 11 - "test_source_session.py"
Cohesion: 0.14
Nodes (21): The adapter is not implemented or not configured. Not a transient failure., SourceNotReady, _login(), Scaffold Complete, Fetching Unimplemented, Fetching Not Implemented Status, _FakePortal, _FakeResponse, _FakeSession (+13 more)

### Community 12 - "ya"
Cohesion: 0.27
Nodes (3): afterUpdate(), va(), ya

### Community 13 - "spread_to_hours"
Cohesion: 0.17
Nodes (19): _build_buckets(), _parse_utc(), Any, date, datetime, Proportional hour-bucket spreading for cumulative meter registers. Pure math…, Distribute each consecutive register delta across the local hours it covers., spread_to_hours() (+11 more)

### Community 14 - ".update"
Cohesion: 0.15
Nodes (10): afterEvent(), Ba(), f(), os(), Ta(), to(), u(), update() (+2 more)

### Community 15 - "excerpt"
Cohesion: 0.18
Nodes (17): _bool_value(), _optional_float(), _optional_int(), parse_reading_row(), datetime, Pure parsers for the mycitygrid meter reading log (GET meterdata). Maps portal…, Map one portal reading-log row to a MeterReading., _reading_time_utc() (+9 more)

### Community 16 - "controls.js"
Cohesion: 0.17
Nodes (25): onRangeChange(), addDays(), applyPreset(), clampHourSpan(), coverageYears(), daysInclusive(), daysInMonth(), defaultRangeFor() (+17 more)

### Community 17 - "updateElements"
Cohesion: 0.14
Nodes (15): Bn(), _calculateBarIndexPixels(), _calculateBarValuePixels(), _getAxis(), _getAxisCount(), getFirstScaleIdForIndexAxis(), getLabelAndValue(), getLabelForValue() (+7 more)

### Community 18 - "jt"
Cohesion: 0.09
Nodes (11): color(), Ee(), It(), jt(), kt(), Le(), mt(), qt() (+3 more)

### Community 19 - "i"
Cohesion: 0.10
Nodes (21): at(), bs(), ct(), dn(), e(), fe(), Fs(), ge() (+13 more)

### Community 20 - "config.py"
Cohesion: 0.09
Nodes (20): credentials_present(), Runtime configuration, read once at import from the environment and an optional…, consumption Package, ConsumptionMonitor - local API for electricity and water consumption from…, Console UTF-8 Reconfiguration, main(), Entry point: `python -m consumption` serves the API and runs the refresh…, portal_session() (+12 more)

### Community 21 - "7. Contract addendum (comparison fold wave)"
Cohesion: 0.09
Nodes (23): 1. Hourly endpoint JSON, 2. The pure function, 3. CSS custom properties, 4. Locale keys and JS module exports, 5. Contract addendum (redesign wave), 6. Contract addendum (data-completeness wave), 7. Contract addendum (comparison fold wave), Breadcrumb (+15 more)

### Community 22 - "n"
Cohesion: 0.16
Nodes (4): fn(), gn(), n(), pi()

### Community 23 - ".getProps"
Cohesion: 0.16
Nodes (15): ai(), average(), beforeDraw(), dataset(), getCenterPoint(), hi(), index(), nearest() (+7 more)

### Community 24 - "ro"
Cohesion: 0.13
Nodes (10): ao(), co(), da(), Do(), getBasePixel(), inXRange(), inYRange(), Oe() (+2 more)

### Community 25 - "s"
Cohesion: 0.10
Nodes (14): bo, et(), getRange(), H(), _i(), j(), ji(), label() (+6 more)

### Community 26 - "Home Assistant add-on"
Cohesion: 0.33
Nodes (5): Home Assistant add-on, Home Assistant integration, Packaging, Runtime, Windows handoff

### Community 27 - "source.py"
Cohesion: 0.17
Nodes (15): _decode(), _fetch_meter_readings(), _fetch_readings(), _Portal, _probe_page(), date, datetime, Adapter for www.mycitygrid.com - the only module that talks to the portal.… (+7 more)

### Community 28 - "Bt"
Cohesion: 0.47
Nodes (5): Bt(), Ft(), Gt(), vt(), zt()

### Community 29 - "bindEvents"
Cohesion: 0.16
Nodes (20): applyHash(), bindEvents(), buttonMatchesUtility(), drillDown(), handleBarClick(), init(), initTheme(), parseHash() (+12 more)

### Community 30 - ".apply"
Cohesion: 0.13
Nodes (8): ca, dt(), ha(), K(), la(), li(), tt(), xa()

### Community 32 - "api.js"
Cohesion: 0.22
Nodes (16): addDaysIso(), API_ROOT, ApiError, daysBetween(), fetchHealth(), fetchHourlyRange(), fetchLocale(), fetchSeries() (+8 more)

### Community 33 - ".configure"
Cohesion: 0.11
Nodes (12): addBox(), b(), beforeUpdate(), cn(), configure(), hn(), init(), initialize() (+4 more)

### Community 34 - "parse"
Cohesion: 0.14
Nodes (8): buildTicks(), ii(), mo(), parse(), parseArrayData(), parsePrimitiveData(), po(), Vn()

### Community 36 - "SourceError"
Cohesion: 0.12
Nodes (27): _buckets(), _exists_locally(), _hour_of_day(), _hour_of_timestamp(), _label(), _number(), parse_hourly(), parse_meters() (+19 more)

### Community 37 - "records.py"
Cohesion: 0.25
Nodes (15): alert_flags(), coverage(), daily_totals(), fetch_readings(), IntervalReading, intervals(), latest_reading(), meter_readings() (+7 more)

### Community 38 - "test_api_contract.py"
Cohesion: 0.14
Nodes (21): _load_env_file(), Populate os.environ from a KEY=VALUE file. Real environment variables always…, Path, Offline contract checks for the HTTP API against the records.py storage…, test_alerts_per_meter(), test_allowed_client_ip_allows_listed_peer(), test_allowed_client_ip_rejects_unknown_peer(), test_allowed_client_ip_unset_allows_testclient() (+13 more)

### Community 39 - "web/chart.js"
Cohesion: 0.23
Nodes (12): paintChart(), toggleTheme(), barAlpha(), createChart(), cssVar(), hexToRgba(), numberFmt, onBarClick() (+4 more)

### Community 40 - ".getDatasetMeta"
Cohesion: 0.20
Nodes (4): aa(), afterDatasetsUpdate(), ko(), onClick()

### Community 41 - "o"
Cohesion: 0.16
Nodes (12): Ie(), ki(), lo(), o(), Oi(), ra(), Si(), wi() (+4 more)

### Community 42 - "series.js"
Cohesion: 0.25
Nodes (13): buildChartData(), buildHourCategories(), buildRunningChart(), capSeries(), foldForComparison(), formatDayLabel(), formatMonthCategory(), formatMonthSeriesLabel() (+5 more)

### Community 43 - ".getContext"
Cohesion: 0.16
Nodes (6): Ae(), Bi(), Ci(), Fi(), getPixelForValue(), pt()

### Community 45 - "connection_report.py"
Cohesion: 0.24
Nodes (12): parse_reading_page(), Return the `items` list from one paginated reading-log response., Blank the value of every credential-looking JSON key in `text`., redact(), _dump(), main(), _mask(), _meters_section() (+4 more)

### Community 46 - "de"
Cohesion: 0.31
Nodes (3): ce(), de, he()

### Community 47 - "ConsumptionMonitor"
Cohesion: 0.17
Nodes (11): Add-on options, Adopt existing history (recommended), Automations, ConsumptionMonitor, Daily electricity threshold, Energy dashboard, Entities, Install (+3 more)

### Community 48 - "run.sh"
Cohesion: 0.17
Nodes (11): ADDON_VERSION, ALLOWED_CLIENT_IPS, ALLOWED_HOSTS, DB_PATH, HA_BRIDGE, HOST, LOCAL_TZ, MYCITYGRID_PASSWORD (+3 more)

### Community 49 - "launcher-common.ps1"
Cohesion: 0.32
Nodes (10): Exit-WithError(), Format-ExitCode(), Get-ConsumptionApiProcessIds(), Get-ProjectRootPath(), Stop-PreviousConsumptionSessions(), Test-IsConsumptionApiProcess(), Test-TcpPort(), Wait-ApiReady() (+2 more)

### Community 55 - ".add"
Cohesion: 0.20
Nodes (5): ei(), en, je(), qe(), ti()

### Community 57 - "m"
Cohesion: 0.24
Nodes (8): eo(), g(), g(), m(), p(), parseObjectData(), updateRangeFromParsed(), v()

### Community 58 - "mycitygrid.com portal recon (no credentials)"
Cohesion: 0.29
Nodes (6): Best guess at the consumption endpoints, Best guess at the login flow, Dead ends, mycitygrid.com portal recon (no credentials), Unknowns that only credentials can answer, What we know

### Community 63 - "yn"
Cohesion: 0.17
Nodes (4): Be(), ne(), numeric(), yn()

### Community 65 - "1.0.0"
Cohesion: 0.50
Nodes (3): 1.0.0, Changelog, Release process

### Community 66 - "env.ps1"
Cohesion: 1.00
Nodes (3): Initialize-Venv(), Show-Phase(), Wait-WithProgress()

## Knowledge Gaps
- **82 isolated node(s):** `Packaging`, `Runtime`, `Home Assistant integration`, `Windows handoff`, `IntervalReading` (+77 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `tn` connect `tn` to `chart.umd.min.js`, `ho`, `a`, `.update`, `updateElements`, `i`, `.getProps`, `ro`, `s`, `sn`, `.configure`, `parse`, `.getDatasetMeta`, `o`, `.getContext`, `.isHorizontal`, `.notifyPlugins`, `.add`, `yn`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Why does `n()` connect `n` to `chart.umd.min.js`, `parse`, `ho`, `._resolveElementOptions`, `tn`, `a`, `.getDatasetMeta`, `o`, `xt`, `.isHorizontal`, `.update`, `i`, `rn`, `ro`, `m`, `sn`, `.apply`, `yn`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Why does `xt` connect `xt` to `chart.umd.min.js`, `jt`, `Bt`, `.notifyPlugins`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `s()` (e.g. with `beforeUpdate()` and `bs()`) actually correct?**
  _`s()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `a()` (e.g. with `ai()` and `draw()`) actually correct?**
  _`a()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `SourceError` (e.g. with `_Portal` and `test_malformed_row_raises_with_excerpt()`) actually correct?**
  _`SourceError` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Packaging`, `Runtime`, `Home Assistant integration` to the rest of the system?**
  _82 weakly-connected nodes found - possible documentation gaps or missing edges._