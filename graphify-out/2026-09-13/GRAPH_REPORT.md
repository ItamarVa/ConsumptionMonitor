# Graph Report - ConsumptionMonitor  (2026-09-13)

## Corpus Check
- 50 files · ~36,300 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1432 nodes · 3685 edges · 75 communities (61 shown, 14 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 127 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `13e1dd55`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ha_bridge.py
- chart.umd.min.js
- ho
- jt
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
- updateElements
- _t
- i
- portal_session
- 7. Contract addendum (comparison fold wave)
- n
- inRange
- .getContext
- de
- Home Assistant add-on
- source.py
- .update
- bindEvents
- ua
- sn
- api.js
- u
- parse
- un
- readings.py
- .get
- test_api_contract.py
- web/chart.js
- .getDatasetMeta
- l
- series.js
- oo
- .isHorizontal
- connection_report.py
- bo
- ConsumptionMonitor
- run.sh
- launcher-common.ps1
- .buildOrUpdateControllers
- config.py
- .notifyPlugins
- _FakePortal
- test_source_parsing.py
- _calculateBarIndexPixels
- hs
- s
- mycitygrid.com portal recon (no credentials)
- rn
- ne
- ._resolveElementOptions
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
- `_login()` --references--> `Fetching Not Implemented Status`  [EXTRACTED]
  consumption/source.py → README.md

## Import Cycles
- 3-file cycle: `consumption/ha_bridge.py -> consumption/ha_entities.py -> consumption/jobs.py -> consumption/ha_bridge.py`

## Communities (75 total, 14 thin omitted)

### Community 0 - "ha_bridge.py"
Cohesion: 0.05
Nodes (73): _load_env_file(), Populate os.environ from a KEY=VALUE file. Real environment variables always…, set_state(), addon_version(), bridge_enabled(), _config_value(), energy_statistics_enabled(), import_energy_statistics() (+65 more)

### Community 1 - "chart.umd.min.js"
Cohesion: 0.04
Nodes (20): at(), beforeUpdate(), ei(), getMaxOverflow(), initialize(), je(), labelColor(), labelPointStyle() (+12 more)

### Community 2 - "ho"
Cohesion: 0.10
Nodes (10): buildLookupTable(), _generate(), getDecimalForValue(), _getTimestampsForTable(), getValueForPixel(), ho(), initOffsets(), jo() (+2 more)

### Community 3 - "jt"
Cohesion: 0.16
Nodes (3): color(), jt(), te()

### Community 4 - "api.py"
Cohesion: 0.07
Nodes (73): Conn, Connection, _AllowedClientIPMiddleware, _directions_for(), _first_stored(), health(), index(), job_status() (+65 more)

### Community 5 - "tn"
Cohesion: 0.06
Nodes (5): es(), generateLabels(), Ie(), Ni(), tn

### Community 6 - "app.js"
Cohesion: 0.11
Nodes (36): applyLocale(), chartData, chartWrap, coverage, crumbLabel(), els, exportCsv(), granularityLabel() (+28 more)

### Community 7 - "a"
Cohesion: 0.14
Nodes (15): a(), determineDataLimits(), e(), gi(), mi(), o(), pi(), pt() (+7 more)

### Community 8 - "xt"
Cohesion: 0.10
Nodes (6): an(), as(), on, rs(), ts(), xt

### Community 9 - "db.py"
Cohesion: 0.06
Nodes (90): get_conn(), alert_flags(), connect(), daily_totals(), due(), _fetch_readings_for_meter(), _first_reading_on_or_after(), get_state() (+82 more)

### Community 10 - "secrets.py"
Cohesion: 0.10
Nodes (25): Array, _credentials(), Encrypted store first on Windows; elsewhere env vars only (HA add-on path)., _Blob, clear(), _crypt32(), _dpapi(), _input_blob() (+17 more)

### Community 11 - "test_source_session.py"
Cohesion: 0.19
Nodes (17): The adapter is not implemented or not configured. Not a transient failure., SourceNotReady, _login(), Scaffold Complete, Fetching Unimplemented, Fetching Not Implemented Status, _FakeResponse, _FakeSession, _raises() (+9 more)

### Community 12 - "ya"
Cohesion: 0.21
Nodes (3): afterUpdate(), va(), ya

### Community 13 - "spread_to_hours"
Cohesion: 0.17
Nodes (19): _build_buckets(), _parse_utc(), Any, date, datetime, Proportional hour-bucket spreading for cumulative meter registers. Pure math…, Distribute each consecutive register delta across the local hours it covers., spread_to_hours() (+11 more)

### Community 14 - ".update"
Cohesion: 0.17
Nodes (6): afterDraw(), afterEvent(), Ba(), Ta(), wa, za()

### Community 15 - "SourceError"
Cohesion: 0.16
Nodes (23): _bool_value(), _optional_float(), _optional_int(), parse_reading_row(), datetime, Pure parsers for the mycitygrid meter reading log (GET meterdata). Maps portal…, Map one portal reading-log row to a MeterReading., _reading_time_utc() (+15 more)

### Community 16 - "controls.js"
Cohesion: 0.17
Nodes (25): onRangeChange(), addDays(), applyPreset(), clampHourSpan(), coverageYears(), daysInclusive(), daysInMonth(), defaultRangeFor() (+17 more)

### Community 17 - "updateElements"
Cohesion: 0.13
Nodes (9): Bn(), _calculateBarValuePixels(), getBasePixel(), getLabelAndValue(), getLabelForValue(), jn(), resolveDataElementOptions(), updateElements() (+1 more)

### Community 18 - "_t"
Cohesion: 0.15
Nodes (11): Bt(), Ft(), Gt(), It(), kt(), mt(), qt(), _t() (+3 more)

### Community 19 - "i"
Cohesion: 0.13
Nodes (14): bs(), ct(), Fs(), ge(), is(), ks(), ms(), ps() (+6 more)

### Community 20 - "portal_session"
Cohesion: 0.13
Nodes (16): consumption Package, Console UTF-8 Reconfiguration, main(), portal_session(), A logged-in session. The access token lives for the duration of the `with`…, Lazy Scrapling Import Lesson, scrapling[fetchers] Extra Lesson, Undocumented mycitygrid Portal Lesson (+8 more)

### Community 21 - "7. Contract addendum (comparison fold wave)"
Cohesion: 0.09
Nodes (23): 1. Hourly endpoint JSON, 2. The pure function, 3. CSS custom properties, 4. Locale keys and JS module exports, 5. Contract addendum (redesign wave), 6. Contract addendum (data-completeness wave), 7. Contract addendum (comparison fold wave), Breadcrumb (+15 more)

### Community 22 - "n"
Cohesion: 0.17
Nodes (3): fn(), gn(), n()

### Community 23 - "inRange"
Cohesion: 0.19
Nodes (15): average(), dataset(), getCenterPoint(), index(), inRange(), nearest(), qi(), Re() (+7 more)

### Community 24 - ".getContext"
Cohesion: 0.10
Nodes (13): ao(), Bi(), Ci(), co(), cs, da(), Do(), Fi() (+5 more)

### Community 25 - "de"
Cohesion: 0.24
Nodes (3): ce(), de, he()

### Community 26 - "Home Assistant add-on"
Cohesion: 0.33
Nodes (5): Home Assistant add-on, Home Assistant integration, Packaging, Runtime, Windows handoff

### Community 27 - "source.py"
Cohesion: 0.17
Nodes (14): _decode(), _fetch_meter_readings(), _fetch_readings(), _Portal, _probe_page(), date, datetime, Adapter for www.mycitygrid.com - the only module that talks to the portal.… (+6 more)

### Community 28 - ".update"
Cohesion: 0.13
Nodes (4): d(), Di(), dt(), Pn()

### Community 29 - "bindEvents"
Cohesion: 0.16
Nodes (20): applyHash(), bindEvents(), buttonMatchesUtility(), drillDown(), handleBarClick(), init(), initTheme(), parseHash() (+12 more)

### Community 30 - "ua"
Cohesion: 0.09
Nodes (23): ai(), beforeDatasetDraw(), beforeDatasetsDraw(), beforeDraw(), ca, ea(), fa(), ga() (+15 more)

### Community 32 - "api.js"
Cohesion: 0.22
Nodes (16): addDaysIso(), API_ROOT, ApiError, daysBetween(), fetchHealth(), fetchHourlyRange(), fetchLocale(), fetchSeries() (+8 more)

### Community 33 - "u"
Cohesion: 0.23
Nodes (5): addBox(), configure(), reset(), start(), u()

### Community 34 - "parse"
Cohesion: 0.14
Nodes (8): buildTicks(), ii(), mo(), parse(), parseArrayData(), parseObjectData(), parsePrimitiveData(), Vn()

### Community 35 - "un"
Cohesion: 0.18
Nodes (8): b(), cn(), dn(), fe(), hn(), init(), ln(), un()

### Community 36 - "readings.py"
Cohesion: 0.21
Nodes (15): _buckets(), _exists_locally(), _hour_of_day(), _hour_of_timestamp(), _label(), parse_hourly(), date, datetime (+7 more)

### Community 38 - "test_api_contract.py"
Cohesion: 0.12
Nodes (23): _NormalizePathMiddleware, Collapse duplicate slashes in the path (HA Ingress can request //ui)., Offline contract checks for the HTTP API against the records.py storage…, test_alerts_per_meter(), test_allowed_client_ip_allows_listed_peer(), test_allowed_client_ip_rejects_unknown_peer(), test_allowed_client_ip_unset_allows_testclient(), test_bad_utility_returns_422() (+15 more)

### Community 39 - "web/chart.js"
Cohesion: 0.23
Nodes (12): paintChart(), toggleTheme(), barAlpha(), createChart(), cssVar(), hexToRgba(), numberFmt, onBarClick() (+4 more)

### Community 40 - ".getDatasetMeta"
Cohesion: 0.19
Nodes (4): aa(), afterDatasetsUpdate(), f(), onClick()

### Community 41 - "l"
Cohesion: 0.15
Nodes (15): draw(), Ee(), fo(), l(), ki(), Le(), lo(), Oi() (+7 more)

### Community 42 - "series.js"
Cohesion: 0.25
Nodes (13): buildChartData(), buildHourCategories(), buildRunningChart(), capSeries(), foldForComparison(), formatDayLabel(), formatMonthCategory(), formatMonthSeriesLabel() (+5 more)

### Community 43 - "oo"
Cohesion: 0.24
Nodes (3): io(), no(), oo

### Community 44 - ".isHorizontal"
Cohesion: 0.09
Nodes (9): Ae(), getPixelForTick(), getPixelForValue(), _getRuler(), Gs(), lt(), Us(), Ys() (+1 more)

### Community 45 - "connection_report.py"
Cohesion: 0.22
Nodes (13): credentials_present(), parse_reading_page(), Return the `items` list from one paginated reading-log response., Blank the value of every credential-looking JSON key in `text`., redact(), _dump(), main(), _mask() (+5 more)

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
Cohesion: 0.18
Nodes (5): addElements(), kn(), qn(), removeBox(), stop()

### Community 51 - "config.py"
Cohesion: 0.33
Nodes (3): Runtime configuration, read once at import from the environment and an optional…, ConsumptionMonitor - local API for electricity and water consumption from…, Entry point: `python -m consumption` serves the API and runs the refresh…

### Community 53 - "_FakePortal"
Cohesion: 0.38
Nodes (4): _FakePortal, _reading_page(), test_missing_meter_type_fetches_nothing(), test_reading_log_uses_date_range_and_paginates()

### Community 54 - "test_source_parsing.py"
Cohesion: 0.31
Nodes (6): parse_meters(), Map utility -> meter ids from a `user/info` body. An empty list for a utility…, _raises(), Self-check for user/info meter discovery and redaction helpers (offline only).…, test_error_messages_carry_a_short_redacted_excerpt(), test_meter_discovery()

### Community 55 - "_calculateBarIndexPixels"
Cohesion: 0.43
Nodes (7): _calculateBarIndexPixels(), _getAxis(), _getAxisCount(), getFirstScaleIdForIndexAxis(), _getStackCount(), _getStackIndex(), _getStacks()

### Community 57 - "s"
Cohesion: 0.10
Nodes (24): beforeLayout(), eo(), et(), g(), getRange(), Go(), H(), _i() (+16 more)

### Community 58 - "mycitygrid.com portal recon (no credentials)"
Cohesion: 0.29
Nodes (6): Best guess at the consumption endpoints, Best guess at the login flow, Dead ends, mycitygrid.com portal recon (no credentials), Unknowns that only credentials can answer, What we know

### Community 60 - "ne"
Cohesion: 0.33
Nodes (3): Be(), ne(), numeric()

### Community 65 - "Changelog"
Cohesion: 0.33
Nodes (5): 1.0.0, 1.0.1, 1.0.2, Changelog, Release process

### Community 66 - "env.ps1"
Cohesion: 1.00
Nodes (3): Initialize-Venv(), Show-Phase(), Wait-WithProgress()

## Knowledge Gaps
- **84 isolated node(s):** `1.0.2`, `1.0.1`, `Release process`, `IntervalReading`, `HOUR_OPTIONS` (+79 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `tn` connect `tn` to `chart.umd.min.js`, `u`, `ho`, `parse`, `a`, `.getDatasetMeta`, `l`, `.isHorizontal`, `updateElements`, `.buildOrUpdateControllers`, `i`, `.notifyPlugins`, `inRange`, `.getContext`, `s`, `.update`, `de`, `sn`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Why does `n()` connect `n` to `chart.umd.min.js`, `ho`, `tn`, `a`, `xt`, `.update`, `i`, `.getContext`, `.update`, `ua`, `u`, `parse`, `.get`, `.getDatasetMeta`, `l`, `oo`, `.isHorizontal`, `.buildOrUpdateControllers`, `s`, `rn`, `ne`, `._resolveElementOptions`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `sn` connect `sn` to `chart.umd.min.js`, `.buildOrUpdateControllers`, `.update`, `.notifyPlugins`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `s()` (e.g. with `beforeUpdate()` and `bs()`) actually correct?**
  _`s()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `a()` (e.g. with `ai()` and `draw()`) actually correct?**
  _`a()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `SourceError` (e.g. with `_Portal` and `test_malformed_row_raises_with_excerpt()`) actually correct?**
  _`SourceError` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `1.0.2`, `1.0.1`, `Release process` to the rest of the system?**
  _84 weakly-connected nodes found - possible documentation gaps or missing edges._