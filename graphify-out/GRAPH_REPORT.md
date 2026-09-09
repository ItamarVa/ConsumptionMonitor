# Graph Report - ConsumptionMonitor  (2026-09-10)

## Corpus Check
- 37 files · ~28,349 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1252 nodes · 3304 edges · 51 communities (41 shown, 10 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 130 edges (avg confidence: 0.83)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2a80ecd4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- app.js
- chart.umd.min.js
- n
- Si
- ho
- tn
- jt
- test_api_contract.py
- xt
- db.py
- .update
- .getContext
- jobs.py
- test_source_session.py
- a
- updateElements
- SourceError
- sn
- s
- secrets.py
- i
- .getDatasetMeta
- .update
- .draw
- source.py
- l
- config.py
- parse
- test_source_parsing.py
- _FakePortal
- draw
- readings.py
- .notifyPlugins
- .configure
- .isHorizontal
- connection_report.py
- launcher-common.ps1
- da
- Dashboard frozen contract
- hs
- mycitygrid.com portal recon (no credentials)
- .buildOrUpdateControllers
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
- `_range()` --references--> `api.py as Only Trust Boundary`  [EXTRACTED]
  consumption/api.py → .cursor/memory/INDEX.md
- `_login()` --references--> `Fetching Not Implemented Status`  [EXTRACTED]
  consumption/source.py → README.md

## Import Cycles
- None detected.

## Communities (51 total, 10 thin omitted)

### Community 0 - "app.js"
Cohesion: 0.05
Nodes (85): ApiError, fetchHealth(), fetchLocale(), fetchSeries(), GRANULARITY_PATHS, normalizeDaily(), normalizeHourly(), normalizeMonthly() (+77 more)

### Community 1 - "chart.umd.min.js"
Cohesion: 0.04
Nodes (16): at(), beforeUpdate(), cn(), et(), getMaxOverflow(), hn(), initialize(), labelColor() (+8 more)

### Community 2 - "n"
Cohesion: 0.05
Nodes (17): Be(), ei(), fn(), gn(), io(), je(), n(), ne() (+9 more)

### Community 3 - "Si"
Cohesion: 0.14
Nodes (8): afterUpdate(), ki(), Oi(), Qs(), Si(), tt(), va(), ya

### Community 4 - "ho"
Cohesion: 0.06
Nodes (15): beforeLayout(), buildLookupTable(), _generate(), getDecimalForValue(), _getTimestampsForTable(), getValueForPixel(), Go(), ho() (+7 more)

### Community 5 - "tn"
Cohesion: 0.07
Nodes (5): es(), generateLabels(), Ie(), Ni(), tn

### Community 6 - "jt"
Cohesion: 0.08
Nodes (16): Bt(), color(), Ee(), Ft(), Gt(), It(), jt(), kt() (+8 more)

### Community 7 - "test_api_contract.py"
Cohesion: 0.09
Nodes (34): Any, _build_buckets(), _parse_utc(), date, datetime, Proportional hour-bucket spreading for cumulative meter registers. Pure math…, Distribute each consecutive register delta across the local hours it covers., spread_to_hours() (+26 more)

### Community 8 - "xt"
Cohesion: 0.09
Nodes (7): an(), as(), ln(), on, rs(), ts(), xt

### Community 9 - "db.py"
Cohesion: 0.06
Nodes (99): Conn, _directions_for(), _first_stored(), get_conn(), health(), index(), job_status(), _latest_register() (+91 more)

### Community 10 - ".update"
Cohesion: 0.19
Nodes (8): afterEvent(), Ba(), os(), Ta(), u(), update(), wa, za()

### Community 11 - ".getContext"
Cohesion: 0.11
Nodes (11): ao(), Bi(), Ci(), co(), cs, Do(), Fi(), inXRange() (+3 more)

### Community 12 - "jobs.py"
Cohesion: 0.06
Nodes (68): get_state(), _advance_backfill(), _always(), _backfill(), _in_january(), Job, local_today(), loop() (+60 more)

### Community 13 - "test_source_session.py"
Cohesion: 0.18
Nodes (18): RuntimeError, The adapter is not implemented or not configured. Not a transient failure., SourceNotReady, _login(), Scaffold Complete, Fetching Unimplemented, Fetching Not Implemented Status, _FakeResponse, _FakeSession (+10 more)

### Community 14 - "a"
Cohesion: 0.14
Nodes (12): a(), determineDataLimits(), Fs(), pe(), pi(), r(), ri(), So (+4 more)

### Community 15 - "updateElements"
Cohesion: 0.10
Nodes (20): aa(), Bn(), _calculateBarIndexPixels(), _calculateBarValuePixels(), _getAxis(), _getAxisCount(), getFirstScaleIdForIndexAxis(), getLabelAndValue() (+12 more)

### Community 16 - "SourceError"
Cohesion: 0.15
Nodes (27): _bool_value(), _optional_float(), _optional_int(), parse_reading_page(), parse_reading_row(), datetime, Pure parsers for the mycitygrid meter reading log (GET meterdata). Maps portal…, Return the `items` list from one paginated reading-log response. (+19 more)

### Community 18 - "s"
Cohesion: 0.11
Nodes (13): bo, getRange(), H(), _i(), j(), ji(), label(), lo() (+5 more)

### Community 19 - "secrets.py"
Cohesion: 0.13
Nodes (22): Array, _credentials(), Encrypted store first; the environment stays available as a manual override., _Blob, clear(), _crypt32(), _dpapi(), _input_blob() (+14 more)

### Community 20 - "i"
Cohesion: 0.06
Nodes (27): bs(), ce(), ct(), de, dn(), dt(), e(), en (+19 more)

### Community 22 - ".update"
Cohesion: 0.13
Nodes (3): d(), Di(), Pn()

### Community 24 - "source.py"
Cohesion: 0.23
Nodes (8): _decode(), _fetch_readings(), _Portal, date, Adapter for www.mycitygrid.com - the only module that talks to the portal.…, Return raw meter readings for local dates start..end inclusive. Re-fetching a…, A logged-in portal session: token lifetime, request pacing and JSON decoding., _url()

### Community 25 - "l"
Cohesion: 0.22
Nodes (16): b(), eo(), f(), g(), l(), g(), ko(), m() (+8 more)

### Community 26 - "config.py"
Cohesion: 0.12
Nodes (14): _load_env_file(), Path, Runtime configuration, read once at import from the environment and an optional…, Populate os.environ from a KEY=VALUE file. Real environment variables always…, consumption Package, ConsumptionMonitor - local API for electricity and water consumption from…, Console UTF-8 Reconfiguration, main() (+6 more)

### Community 27 - "parse"
Cohesion: 0.14
Nodes (8): buildTicks(), ii(), mo(), parse(), parseArrayData(), parsePrimitiveData(), po(), Vn()

### Community 28 - "test_source_parsing.py"
Cohesion: 0.31
Nodes (6): parse_meters(), Map utility -> meter ids from a `user/info` body. An empty list for a utility…, _raises(), Self-check for user/info meter discovery and redaction helpers (offline only).…, test_error_messages_carry_a_short_redacted_excerpt(), test_meter_discovery()

### Community 29 - "_FakePortal"
Cohesion: 0.38
Nodes (4): _FakePortal, _reading_page(), test_missing_meter_type_fetches_nothing(), test_reading_log_uses_date_range_and_paginates()

### Community 30 - "draw"
Cohesion: 0.14
Nodes (19): ai(), average(), beforeDraw(), dataset(), draw(), fo(), getCenterPoint(), hi() (+11 more)

### Community 31 - "readings.py"
Cohesion: 0.21
Nodes (15): _buckets(), _exists_locally(), _hour_of_day(), _hour_of_timestamp(), _label(), parse_hourly(), date, datetime (+7 more)

### Community 34 - ".configure"
Cohesion: 0.15
Nodes (7): addBox(), configure(), Nn(), removeBox(), start(), stop(), wn()

### Community 35 - ".isHorizontal"
Cohesion: 0.14
Nodes (3): Ae(), Us(), Ys()

### Community 36 - "connection_report.py"
Cohesion: 0.14
Nodes (19): credentials_present(), Blank the value of every credential-looking JSON key in `text`., redact(), portal_session(), A logged-in session. The access token lives for the duration of the `with`…, Lazy Scrapling Import Lesson, scrapling[fetchers] Extra Lesson, Undocumented mycitygrid Portal Lesson (+11 more)

### Community 39 - "launcher-common.ps1"
Cohesion: 0.32
Nodes (10): Exit-WithError(), Format-ExitCode(), Get-ConsumptionApiProcessIds(), Get-ProjectRootPath(), Stop-PreviousConsumptionSessions(), Test-IsConsumptionApiProcess(), Test-TcpPort(), Wait-ApiReady() (+2 more)

### Community 40 - "da"
Cohesion: 0.11
Nodes (18): beforeDatasetDraw(), beforeDatasetsDraw(), ca, da(), ea(), fa(), ga(), getBasePixel() (+10 more)

### Community 41 - "Dashboard frozen contract"
Cohesion: 0.12
Nodes (15): 1. Hourly endpoint JSON, 2. The pure function, 3. CSS custom properties, 4. Locale keys and JS module exports, 5. Contract addendum (redesign wave), 6. Contract addendum (data-completeness wave), Breadcrumb, Canvas box rule (+7 more)

### Community 45 - "mycitygrid.com portal recon (no credentials)"
Cohesion: 0.29
Nodes (6): Best guess at the consumption endpoints, Best guess at the login flow, Dead ends, mycitygrid.com portal recon (no credentials), Unknowns that only credentials can answer, What we know

### Community 46 - ".buildOrUpdateControllers"
Cohesion: 0.19
Nodes (4): addElements(), kn(), qn(), rt()

### Community 47 - "env.ps1"
Cohesion: 1.00
Nodes (3): Initialize-Venv(), Show-Phase(), Wait-WithProgress()

## Knowledge Gaps
- **43 isolated node(s):** `1. Hourly endpoint JSON`, `2. The pure function`, `3. CSS custom properties`, `4. Locale keys and JS module exports`, ``/health` coverage fields` (+38 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `tn` connect `tn` to `chart.umd.min.js`, `n`, `Si`, `ho`, `.update`, `.getContext`, `a`, `updateElements`, `sn`, `s`, `i`, `.getDatasetMeta`, `.update`, `.draw`, `l`, `parse`, `draw`, `.notifyPlugins`, `.configure`, `.isHorizontal`, `da`, `.buildOrUpdateControllers`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Why does `n()` connect `n` to `chart.umd.min.js`, `.isHorizontal`, `ho`, `Si`, `tn`, `da`, `xt`, `.update`, `.getContext`, `.buildOrUpdateControllers`, `a`, `i`, `.getDatasetMeta`, `.update`, `l`, `parse`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `wa` connect `.update` to `chart.umd.min.js`, `Si`, `.isHorizontal`, `.getContext`, `updateElements`, `.draw`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `s()` (e.g. with `beforeUpdate()` and `bs()`) actually correct?**
  _`s()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `a()` (e.g. with `ai()` and `draw()`) actually correct?**
  _`a()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `SourceError` (e.g. with `_Portal` and `test_malformed_row_raises_with_excerpt()`) actually correct?**
  _`SourceError` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `1. Hourly endpoint JSON`, `2. The pure function`, `3. CSS custom properties` to the rest of the system?**
  _43 weakly-connected nodes found - possible documentation gaps or missing edges._