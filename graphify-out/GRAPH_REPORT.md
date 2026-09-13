# Graph Report - ConsumptionMonitor  (2026-09-13)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1416 nodes · 3670 edges · 74 communities (62 shown, 12 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 128 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f982dd75`
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
- Si
- jobs.py
- .update
- SourceError
- controls.js
- updateElements
- jt
- i
- config.py
- 7. Contract addendum (comparison fold wave)
- n
- draw
- ro
- s
- .update
- source.py
- test_jobs.py
- bindEvents
- da
- sn
- api.js
- un
- parse
- upsert_meter_readings
- readings.py
- records.py
- test_api_contract.py
- web/chart.js
- .getDatasetMeta
- l
- series.js
- .getContext
- .isHorizontal
- connection_report.py
- de
- ConsumptionMonitor
- run.sh
- launcher-common.ps1
- .getSortedVisibleDatasetMetas
- xn
- .notifyPlugins
- connect
- test_source_parsing.py
- rn
- hs
- o
- mycitygrid.com portal recon (no credentials)
- Ys
- e
- ne
- timedelta
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

## Communities (74 total, 12 thin omitted)

### Community 0 - "ha_bridge.py"
Cohesion: 0.06
Nodes (62): addon_version(), bridge_enabled(), _config_value(), energy_statistics_enabled(), import_energy_statistics(), _mqtt_publish(), publish_entities(), Any (+54 more)

### Community 1 - "chart.umd.min.js"
Cohesion: 0.04
Nodes (17): at(), beforeUpdate(), Fs(), initialize(), labelColor(), labelPointStyle(), Nn(), pe() (+9 more)

### Community 2 - "ho"
Cohesion: 0.08
Nodes (12): beforeLayout(), buildLookupTable(), _generate(), getDecimalForValue(), _getTimestampsForTable(), getValueForPixel(), Go(), ho() (+4 more)

### Community 3 - "ha_entities.py"
Cohesion: 0.16
Nodes (26): _binary_cmp(), build_discovery(), build_state(), _directions(), _ha_unit(), _latest_scraper_error(), _meter_ids(), _period_total() (+18 more)

### Community 4 - "api.py"
Cohesion: 0.11
Nodes (47): Conn, _AllowedClientIPMiddleware, _directions_for(), _first_stored(), health(), index(), job_status(), _latest_register() (+39 more)

### Community 6 - "app.js"
Cohesion: 0.11
Nodes (36): applyLocale(), chartData, chartWrap, coverage, crumbLabel(), els, exportCsv(), granularityLabel() (+28 more)

### Community 7 - "a"
Cohesion: 0.09
Nodes (14): a(), determineDataLimits(), Di(), io(), no(), oo, pi(), pt() (+6 more)

### Community 8 - "xt"
Cohesion: 0.10
Nodes (6): an(), as(), on, rs(), ts(), xt

### Community 9 - "db.py"
Cohesion: 0.17
Nodes (33): alert_flags(), daily_totals(), due(), _fetch_readings_for_meter(), _first_reading_on_or_after(), _interval_dict(), intervals(), _last_reading_before() (+25 more)

### Community 10 - "secrets.py"
Cohesion: 0.10
Nodes (25): Array, _credentials(), Encrypted store first on Windows; elsewhere env vars only (HA add-on path)., _Blob, clear(), _crypt32(), _dpapi(), _input_blob() (+17 more)

### Community 11 - "test_source_session.py"
Cohesion: 0.15
Nodes (19): _login(), Scaffold Complete, Fetching Unimplemented, Fetching Not Implemented Status, _FakePortal, _FakeResponse, _FakeSession, _raises(), Self-check for the mycitygrid adapter HTTP half: login, token refresh, reading-… (+11 more)

### Community 12 - "Si"
Cohesion: 0.20
Nodes (6): afterUpdate(), Oi(), Si(), va(), ya, zs()

### Community 13 - "jobs.py"
Cohesion: 0.13
Nodes (27): job_states(), _advance_backfill(), _always(), _backfill(), _in_january(), Job, loop(), _month_bounds() (+19 more)

### Community 14 - ".update"
Cohesion: 0.15
Nodes (9): afterDraw(), afterEvent(), Ba(), ki(), os(), Ta(), update(), wa (+1 more)

### Community 15 - "SourceError"
Cohesion: 0.17
Nodes (22): _bool_value(), _optional_float(), _optional_int(), parse_reading_row(), datetime, Pure parsers for the mycitygrid meter reading log (GET meterdata). Maps portal…, Map one portal reading-log row to a MeterReading., _reading_time_utc() (+14 more)

### Community 16 - "controls.js"
Cohesion: 0.17
Nodes (25): onRangeChange(), addDays(), applyPreset(), clampHourSpan(), coverageYears(), daysInclusive(), daysInMonth(), defaultRangeFor() (+17 more)

### Community 17 - "updateElements"
Cohesion: 0.14
Nodes (9): aa(), Bn(), _calculateBarValuePixels(), getLabelAndValue(), getLabelForValue(), jn(), resolveDataElementOptions(), updateElements() (+1 more)

### Community 18 - "jt"
Cohesion: 0.08
Nodes (16): Bt(), color(), Ee(), Ft(), Gt(), It(), jt(), kt() (+8 more)

### Community 19 - "i"
Cohesion: 0.15
Nodes (10): bs(), ct(), ge(), is(), ks(), ms(), ss(), i() (+2 more)

### Community 20 - "config.py"
Cohesion: 0.09
Nodes (20): credentials_present(), Runtime configuration, read once at import from the environment and an optional…, consumption Package, ConsumptionMonitor - local API for electricity and water consumption from…, Console UTF-8 Reconfiguration, main(), Entry point: `python -m consumption` serves the API and runs the refresh…, portal_session() (+12 more)

### Community 21 - "7. Contract addendum (comparison fold wave)"
Cohesion: 0.09
Nodes (23): 1. Hourly endpoint JSON, 2. The pure function, 3. CSS custom properties, 4. Locale keys and JS module exports, 5. Contract addendum (redesign wave), 6. Contract addendum (data-completeness wave), 7. Contract addendum (comparison fold wave), Breadcrumb (+15 more)

### Community 22 - "n"
Cohesion: 0.16
Nodes (3): fn(), gn(), n()

### Community 23 - "draw"
Cohesion: 0.10
Nodes (25): ai(), average(), beforeDraw(), dataset(), draw(), fo(), getCenterPoint(), getMaxOverflow() (+17 more)

### Community 24 - "ro"
Cohesion: 0.14
Nodes (8): ao(), co(), Do(), inXRange(), inYRange(), Oe(), ro(), Y()

### Community 25 - "s"
Cohesion: 0.12
Nodes (20): _calculateBarIndexPixels(), et(), _getAxis(), _getAxisCount(), getFirstScaleIdForIndexAxis(), getPixelForTick(), getPixelForValue(), getRange() (+12 more)

### Community 27 - "source.py"
Cohesion: 0.18
Nodes (14): RuntimeError, The adapter is not implemented or not configured. Not a transient failure., SourceNotReady, _decode(), _fetch_meter_readings(), _fetch_readings(), _Portal, _probe_page() (+6 more)

### Community 28 - "test_jobs.py"
Cohesion: 0.21
Nodes (19): get_state(), Exception, _conn(), _fake_source(), date, datetime, Offline self-checks for the refresh schedule and job bookkeeping. Uses a…, Stand in for the portal: one reading per utility when start falls in those… (+11 more)

### Community 29 - "bindEvents"
Cohesion: 0.16
Nodes (20): applyHash(), bindEvents(), buttonMatchesUtility(), drillDown(), handleBarClick(), init(), initTheme(), parseHash() (+12 more)

### Community 30 - "da"
Cohesion: 0.13
Nodes (18): beforeDatasetDraw(), beforeDatasetsDraw(), ca, da(), ea(), fa(), ga(), getBasePixel() (+10 more)

### Community 31 - "sn"
Cohesion: 0.08
Nodes (6): addBox(), addElements(), bo, configure(), sn, start()

### Community 32 - "api.js"
Cohesion: 0.22
Nodes (16): addDaysIso(), API_ROOT, ApiError, daysBetween(), fetchHealth(), fetchHourlyRange(), fetchLocale(), fetchSeries() (+8 more)

### Community 33 - "un"
Cohesion: 0.22
Nodes (6): b(), cn(), hn(), init(), ln(), un()

### Community 34 - "parse"
Cohesion: 0.14
Nodes (8): buildTicks(), ii(), mo(), parse(), parseArrayData(), parseObjectData(), parsePrimitiveData(), Vn()

### Community 35 - "upsert_meter_readings"
Cohesion: 0.38
Nodes (14): upsert_meter_readings(), _conn(), _elec(), date, datetime, Offline self-checks for raw meter reading storage and exact register deltas., A day with no reading past its closing midnight still reports what has accrued., Portal sometimes emits a new meter_data_id for an unchanged reading_time_utc. (+6 more)

### Community 36 - "readings.py"
Cohesion: 0.21
Nodes (15): _buckets(), _exists_locally(), _hour_of_day(), _hour_of_timestamp(), _label(), parse_hourly(), date, datetime (+7 more)

### Community 37 - "records.py"
Cohesion: 0.25
Nodes (15): alert_flags(), coverage(), daily_totals(), fetch_readings(), IntervalReading, intervals(), latest_reading(), meter_readings() (+7 more)

### Community 38 - "test_api_contract.py"
Cohesion: 0.14
Nodes (21): _load_env_file(), Populate os.environ from a KEY=VALUE file. Real environment variables always…, Path, Offline contract checks for the HTTP API against the records.py storage…, test_alerts_per_meter(), test_allowed_client_ip_allows_listed_peer(), test_allowed_client_ip_rejects_unknown_peer(), test_allowed_client_ip_unset_allows_testclient() (+13 more)

### Community 39 - "web/chart.js"
Cohesion: 0.21
Nodes (12): paintChart(), toggleTheme(), barAlpha(), createChart(), cssVar(), hexToRgba(), numberFmt, onBarClick() (+4 more)

### Community 40 - ".getDatasetMeta"
Cohesion: 0.13
Nodes (4): afterDatasetsUpdate(), kn(), onClick(), qn()

### Community 41 - "l"
Cohesion: 0.18
Nodes (10): gi(), l(), lo(), Ls(), mi(), po(), ra(), vi() (+2 more)

### Community 42 - "series.js"
Cohesion: 0.25
Nodes (13): buildChartData(), buildHourCategories(), buildRunningChart(), capSeries(), foldForComparison(), formatDayLabel(), formatMonthCategory(), formatMonthSeriesLabel() (+5 more)

### Community 43 - ".getContext"
Cohesion: 0.23
Nodes (5): Ae(), Bi(), Ci(), cs, Fi()

### Community 44 - ".isHorizontal"
Cohesion: 0.20
Nodes (3): H(), Qs(), xo()

### Community 45 - "connection_report.py"
Cohesion: 0.24
Nodes (12): parse_reading_page(), Return the `items` list from one paginated reading-log response., Blank the value of every credential-looking JSON key in `text`., redact(), _dump(), main(), _mask(), _meters_section() (+4 more)

### Community 46 - "de"
Cohesion: 0.23
Nodes (4): ce(), de, dt(), he()

### Community 47 - "ConsumptionMonitor"
Cohesion: 0.17
Nodes (11): Add-on options, Adopt existing history (recommended), Automations, ConsumptionMonitor, Daily electricity threshold, Energy dashboard, Entities, Install (+3 more)

### Community 48 - "run.sh"
Cohesion: 0.17
Nodes (11): ADDON_VERSION, ALLOWED_CLIENT_IPS, ALLOWED_HOSTS, DB_PATH, HA_BRIDGE, HOST, LOCAL_TZ, MYCITYGRID_PASSWORD (+3 more)

### Community 49 - "launcher-common.ps1"
Cohesion: 0.32
Nodes (10): Exit-WithError(), Format-ExitCode(), Get-ConsumptionApiProcessIds(), Get-ProjectRootPath(), Stop-PreviousConsumptionSessions(), Test-IsConsumptionApiProcess(), Test-TcpPort(), Wait-ApiReady() (+2 more)

### Community 50 - ".getSortedVisibleDatasetMetas"
Cohesion: 0.22
Nodes (4): es(), generateLabels(), Ie(), Ni()

### Community 53 - "connect"
Cohesion: 0.28
Nodes (8): get_conn(), connect(), init_schema(), Path, Create tables if this file has not been initialized in this process., log(), main(), Run backfill jobs until BACKFILL_DONE or no progress. Logs to…

### Community 54 - "test_source_parsing.py"
Cohesion: 0.31
Nodes (6): parse_meters(), Map utility -> meter ids from a `user/info` body. An empty list for a utility…, _raises(), Self-check for user/info meter discovery and redaction helpers (offline only).…, test_error_messages_carry_a_short_redacted_excerpt(), test_meter_discovery()

### Community 57 - "o"
Cohesion: 0.21
Nodes (12): eo(), f(), g(), j(), g(), ko(), m(), o() (+4 more)

### Community 58 - "mycitygrid.com portal recon (no credentials)"
Cohesion: 0.29
Nodes (6): Best guess at the consumption endpoints, Best guess at the login flow, Dead ends, mycitygrid.com portal recon (no credentials), Unknowns that only credentials can answer, What we know

### Community 62 - "e"
Cohesion: 0.23
Nodes (11): dn(), e(), ei(), fe(), je(), ps(), qe(), removeBox() (+3 more)

### Community 63 - "ne"
Cohesion: 0.33
Nodes (3): Be(), ne(), numeric()

### Community 64 - "timedelta"
Cohesion: 0.67
Nodes (4): datetime, _token_expiry(), test_token_expiry_reads_both_forms(), timedelta

### Community 65 - "1.0.0"
Cohesion: 0.50
Nodes (3): 1.0.0, Changelog, Release process

### Community 66 - "env.ps1"
Cohesion: 1.00
Nodes (3): Initialize-Venv(), Show-Phase(), Wait-WithProgress()

## Knowledge Gaps
- **78 isolated node(s):** `IntervalReading`, `HOUR_OPTIONS`, `MAX_HOUR_SPAN_DAYS`, `PRESETS`, `1. Hourly endpoint JSON` (+73 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `tn` connect `tn` to `chart.umd.min.js`, `ho`, `a`, `updateElements`, `i`, `draw`, `ro`, `s`, `.update`, `sn`, `parse`, `.getDatasetMeta`, `.getContext`, `.isHorizontal`, `.getSortedVisibleDatasetMetas`, `.notifyPlugins`, `rn`, `o`, `Ys`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `n()` connect `n` to `chart.umd.min.js`, `ho`, `tn`, `a`, `xt`, `Si`, `.update`, `i`, `ro`, `.update`, `da`, `sn`, `parse`, `.getDatasetMeta`, `.isHorizontal`, `xn`, `o`, `e`, `ne`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Why does `sn` connect `sn` to `.getDatasetMeta`, `chart.umd.min.js`, `.update`, `.notifyPlugins`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `s()` (e.g. with `beforeUpdate()` and `bs()`) actually correct?**
  _`s()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `a()` (e.g. with `ai()` and `draw()`) actually correct?**
  _`a()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `SourceError` (e.g. with `_Portal` and `test_malformed_row_raises_with_excerpt()`) actually correct?**
  _`SourceError` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `IntervalReading`, `HOUR_OPTIONS`, `MAX_HOUR_SPAN_DAYS` to the rest of the system?**
  _78 weakly-connected nodes found - possible documentation gaps or missing edges._