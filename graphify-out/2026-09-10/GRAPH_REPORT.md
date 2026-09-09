# Graph Report - ConsumptionMonitor  (2026-09-09)

## Corpus Check
- 38 files · ~27,516 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1239 nodes · 3281 edges · 69 communities (59 shown, 10 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 130 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `88c96cd1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SourceError
- api.py
- test_source_session.py
- db.py
- jobs.py
- refresh
- secrets.py
- test_api_contract.py
- test_jobs.py
- Si
- e
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
- So
- ua
- a
- ro
- de
- .update
- .update
- records.py
- sn
- n
- .getDatasetMeta
- rn
- .notifyPlugins
- s
- portal_session
- _calculateBarIndexPixels
- parse
- readings.py
- ._computeLabelItems
- .getProps
- .getSortedVisibleDatasetMetas
- connection_report.py
- update
- .isHorizontal
- .getContext
- upsert_meter_readings
- connect
- test_source_parsing.py
- hs
- updateElements
- un
- .buildOrUpdateControllers
- Dashboard frozen contract
- xt
- u
- config.py
- oo
- Vendored third-party assets
- ne
- .register
- timedelta

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

## Communities (69 total, 10 thin omitted)

### Community 0 - "SourceError"
Cohesion: 0.17
Nodes (22): _bool_value(), _optional_float(), _optional_int(), parse_reading_row(), datetime, Pure parsers for the mycitygrid meter reading log (GET meterdata). Maps portal…, Map one portal reading-log row to a MeterReading., _reading_time_utc() (+14 more)

### Community 1 - "api.py"
Cohesion: 0.20
Nodes (32): Conn, _directions_for(), _first_stored(), health(), index(), job_status(), _latest_register(), _meter_ids() (+24 more)

### Community 2 - "test_source_session.py"
Cohesion: 0.15
Nodes (19): _login(), Scaffold Complete, Fetching Unimplemented, Fetching Not Implemented Status, _FakePortal, _FakeResponse, _FakeSession, _raises(), Self-check for the mycitygrid adapter HTTP half: login, token refresh, reading-… (+11 more)

### Community 3 - "db.py"
Cohesion: 0.17
Nodes (31): alert_flags(), daily_totals(), _fetch_readings_for_meter(), _first_reading_on_or_after(), _interval_dict(), intervals(), latest_reading(), _local_midnight() (+23 more)

### Community 4 - "jobs.py"
Cohesion: 0.15
Nodes (27): _advance_backfill(), _always(), _backfill(), _in_january(), Job, local_today(), loop(), _month_bounds() (+19 more)

### Community 5 - "refresh"
Cohesion: 0.25
Nodes (9): Force one job to run now, for testing a freshly implemented source adapter., refresh(), _reject_cross_site_refresh(), security_headers(), middleware, post, Endpoint Reference Table, Module Layout (+1 more)

### Community 6 - "secrets.py"
Cohesion: 0.13
Nodes (22): Array, _credentials(), Encrypted store first; the environment stays available as a manual override., _Blob, clear(), _crypt32(), _dpapi(), _input_blob() (+14 more)

### Community 7 - "test_api_contract.py"
Cohesion: 0.09
Nodes (34): Any, _build_buckets(), _parse_utc(), date, datetime, Proportional hour-bucket spreading for cumulative meter registers. Pure math…, Distribute each consecutive register delta across the local hours it covers., spread_to_hours() (+26 more)

### Community 8 - "test_jobs.py"
Cohesion: 0.21
Nodes (19): get_state(), job_states(), Exception, _conn(), _fake_source(), date, datetime, Offline self-checks for the refresh schedule and job bookkeeping. Uses a… (+11 more)

### Community 9 - "Si"
Cohesion: 0.16
Nodes (7): afterDraw(), ki(), lo(), Si(), wi(), x(), zs()

### Community 10 - "e"
Cohesion: 0.18
Nodes (12): e(), ei(), ha(), je(), K(), la(), li(), qe() (+4 more)

### Community 11 - "source.py"
Cohesion: 0.18
Nodes (14): RuntimeError, The adapter is not implemented or not configured. Not a transient failure., SourceNotReady, _decode(), _fetch_meter_readings(), _fetch_readings(), _Portal, _probe_page() (+6 more)

### Community 12 - "mycitygrid.com portal recon (no credentials)"
Cohesion: 0.29
Nodes (6): Best guess at the consumption endpoints, Best guess at the login flow, Dead ends, mycitygrid.com portal recon (no credentials), Unknowns that only credentials can answer, What we know

### Community 13 - "launcher-common.ps1"
Cohesion: 0.32
Nodes (10): Exit-WithError(), Format-ExitCode(), Get-ConsumptionApiProcessIds(), Get-ProjectRootPath(), Stop-PreviousConsumptionSessions(), Test-IsConsumptionApiProcess(), Test-TcpPort(), Wait-ApiReady() (+2 more)

### Community 14 - "env.ps1"
Cohesion: 1.00
Nodes (3): Initialize-Venv(), Show-Phase(), Wait-WithProgress()

### Community 16 - "app.js"
Cohesion: 0.05
Nodes (82): ApiError, fetchHealth(), fetchLocale(), fetchSeries(), GRANULARITY_PATHS, normalizeDaily(), normalizeHourly(), normalizeMonthly() (+74 more)

### Community 18 - "chart.umd.min.js"
Cohesion: 0.04
Nodes (19): at(), beforeUpdate(), Ee(), getMaxOverflow(), initialize(), labelColor(), labelPointStyle(), Le() (+11 more)

### Community 19 - "jt"
Cohesion: 0.09
Nodes (13): Bt(), color(), Ft(), Gt(), It(), jt(), kt(), qt() (+5 more)

### Community 24 - "ho"
Cohesion: 0.12
Nodes (11): buildLookupTable(), _generate(), getDecimalForValue(), _getTimestampsForTable(), getValueForPixel(), ho(), initOffsets(), jo() (+3 more)

### Community 25 - "So"
Cohesion: 0.10
Nodes (4): bo, H(), j(), So

### Community 26 - "ua"
Cohesion: 0.15
Nodes (13): beforeDatasetDraw(), beforeDatasetsDraw(), ca, ea(), ga(), ia(), ma(), na() (+5 more)

### Community 27 - "a"
Cohesion: 0.14
Nodes (19): a(), draw(), fa(), fo(), gi(), l(), inRange(), mi() (+11 more)

### Community 28 - "ro"
Cohesion: 0.16
Nodes (8): ao(), co(), Do(), inXRange(), inYRange(), Oe(), ro(), Y()

### Community 29 - "de"
Cohesion: 0.23
Nodes (4): ce(), de, dt(), he()

### Community 30 - ".update"
Cohesion: 0.19
Nodes (7): afterEvent(), Ba(), ns(), os(), Ta(), wa, za()

### Community 31 - ".update"
Cohesion: 0.13
Nodes (3): d(), Di(), Pn()

### Community 32 - "records.py"
Cohesion: 0.25
Nodes (15): alert_flags(), coverage(), daily_totals(), fetch_readings(), IntervalReading, intervals(), latest_reading(), meter_readings() (+7 more)

### Community 34 - "n"
Cohesion: 0.16
Nodes (4): fn(), gn(), n(), pi()

### Community 35 - ".getDatasetMeta"
Cohesion: 0.19
Nodes (5): aa(), afterDatasetsUpdate(), da(), getBasePixel(), onClick()

### Community 38 - "s"
Cohesion: 0.11
Nodes (22): bs(), ct(), et(), Fs(), ge(), getRange(), _i(), is() (+14 more)

### Community 39 - "portal_session"
Cohesion: 0.13
Nodes (16): consumption Package, Console UTF-8 Reconfiguration, main(), portal_session(), A logged-in session. The access token lives for the duration of the `with`…, Lazy Scrapling Import Lesson, scrapling[fetchers] Extra Lesson, Undocumented mycitygrid Portal Lesson (+8 more)

### Community 40 - "_calculateBarIndexPixels"
Cohesion: 0.43
Nodes (7): _calculateBarIndexPixels(), _getAxis(), _getAxisCount(), getFirstScaleIdForIndexAxis(), _getStackCount(), _getStackIndex(), _getStacks()

### Community 41 - "parse"
Cohesion: 0.13
Nodes (9): buildTicks(), determineDataLimits(), ii(), mo(), parse(), parseArrayData(), parsePrimitiveData(), po() (+1 more)

### Community 42 - "readings.py"
Cohesion: 0.21
Nodes (15): _buckets(), _exists_locally(), _hour_of_day(), _hour_of_timestamp(), _label(), parse_hourly(), date, datetime (+7 more)

### Community 43 - "._computeLabelItems"
Cohesion: 0.12
Nodes (4): getPixelForTick(), Gs(), Us(), Ys()

### Community 44 - ".getProps"
Cohesion: 0.16
Nodes (16): ai(), average(), beforeDraw(), dataset(), getCenterPoint(), hi(), index(), nearest() (+8 more)

### Community 45 - ".getSortedVisibleDatasetMetas"
Cohesion: 0.22
Nodes (4): es(), generateLabels(), Ie(), Ni()

### Community 46 - "connection_report.py"
Cohesion: 0.22
Nodes (13): credentials_present(), parse_reading_page(), Return the `items` list from one paginated reading-log response., Blank the value of every credential-looking JSON key in `text`., redact(), _dump(), main(), _mask() (+5 more)

### Community 47 - "update"
Cohesion: 0.16
Nodes (17): beforeLayout(), eo(), f(), g(), Go(), g(), ko(), m() (+9 more)

### Community 48 - ".isHorizontal"
Cohesion: 0.18
Nodes (5): afterUpdate(), Oi(), Qs(), va(), ya

### Community 49 - ".getContext"
Cohesion: 0.22
Nodes (5): Ae(), Bi(), Ci(), cs, Fi()

### Community 51 - "upsert_meter_readings"
Cohesion: 0.42
Nodes (12): upsert_meter_readings(), _conn(), _elec(), date, datetime, Offline self-checks for raw meter reading storage and exact register deltas., Portal sometimes emits a new meter_data_id for an unchanged reading_time_utc., test_coverage_counts() (+4 more)

### Community 52 - "connect"
Cohesion: 0.20
Nodes (11): get_conn(), lifespan(), connect(), coverage(), init_schema(), Path, Create tables if this file has not been initialized in this process., FastAPI (+3 more)

### Community 53 - "test_source_parsing.py"
Cohesion: 0.31
Nodes (6): parse_meters(), Map utility -> meter ids from a `user/info` body. An empty list for a utility…, _raises(), Self-check for user/info meter discovery and redaction helpers (offline only).…, test_error_messages_carry_a_short_redacted_excerpt(), test_meter_discovery()

### Community 55 - "updateElements"
Cohesion: 0.14
Nodes (10): Bn(), _calculateBarValuePixels(), getLabelAndValue(), getLabelForValue(), getPixelForValue(), _getRuler(), jn(), resolveDataElementOptions() (+2 more)

### Community 56 - "un"
Cohesion: 0.22
Nodes (7): b(), cn(), dn(), fe(), hn(), init(), un()

### Community 57 - ".buildOrUpdateControllers"
Cohesion: 0.22
Nodes (3): kn(), ln(), qn()

### Community 58 - "Dashboard frozen contract"
Cohesion: 0.18
Nodes (10): 1. Hourly endpoint JSON, 2. The pure function, 3. CSS custom properties, 4. Locale keys and JS module exports, 5. Contract addendum (redesign wave), Canvas box rule, Dashboard frozen contract, `/health` coverage fields (+2 more)

### Community 59 - "xt"
Cohesion: 0.10
Nodes (5): an(), as(), on, ts(), xt

### Community 60 - "u"
Cohesion: 0.23
Nodes (5): addBox(), configure(), reset(), start(), u()

### Community 61 - "config.py"
Cohesion: 0.22
Nodes (6): _load_env_file(), Path, Runtime configuration, read once at import from the environment and an optional…, Populate os.environ from a KEY=VALUE file. Real environment variables always…, ConsumptionMonitor - local API for electricity and water consumption from…, Entry point: `python -m consumption` serves the API and runs the refresh…

### Community 62 - "oo"
Cohesion: 0.24
Nodes (3): io(), no(), oo

### Community 65 - "ne"
Cohesion: 0.29
Nodes (3): Be(), ne(), numeric()

### Community 68 - "timedelta"
Cohesion: 0.47
Nodes (6): due(), datetime, _token_expiry(), test_due(), test_token_expiry_reads_both_forms(), timedelta

## Knowledge Gaps
- **38 isolated node(s):** `IntervalReading`, `GRANULARITY_PATHS`, `dashboardContent`, `els`, `state` (+33 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `tn` connect `tn` to `Si`, `chart.umd.min.js`, `So`, `a`, `.update`, `sn`, `.getDatasetMeta`, `.notifyPlugins`, `s`, `parse`, `._computeLabelItems`, `.getProps`, `.getSortedVisibleDatasetMetas`, `.isHorizontal`, `.getContext`, `updateElements`, `.buildOrUpdateControllers`, `u`, `.register`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Why does `jt()` connect `jt` to `chart.umd.min.js`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Why does `n()` connect `n` to `Si`, `e`, `chart.umd.min.js`, `tn`, `ho`, `ua`, `a`, `ro`, `.update`, `.update`, `.getDatasetMeta`, `rn`, `s`, `parse`, `._computeLabelItems`, `update`, `.isHorizontal`, `.get`, `.buildOrUpdateControllers`, `xt`, `u`, `oo`, `ne`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `s()` (e.g. with `beforeUpdate()` and `bs()`) actually correct?**
  _`s()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `a()` (e.g. with `ai()` and `draw()`) actually correct?**
  _`a()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `SourceError` (e.g. with `_Portal` and `test_malformed_row_raises_with_excerpt()`) actually correct?**
  _`SourceError` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `IntervalReading`, `GRANULARITY_PATHS`, `dashboardContent` to the rest of the system?**
  _38 weakly-connected nodes found - possible documentation gaps or missing edges._