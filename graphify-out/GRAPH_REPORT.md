# Graph Report - ConsumptionMonitor  (2026-09-09)

## Corpus Check
- 29 files · ~16,519 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 365 nodes · 850 edges · 27 communities (18 shown, 9 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 21 edges (avg confidence: 0.71)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f3cd27bd`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- readings.py
- db.py
- RuntimeError
- api.py
- jobs.py
- test_source_session.py
- records.py
- secrets.py
- env.ps1
- config.py
- Double-Clickable Launcher Preference
- Run via run.bat
- launcher-common.ps1
- Path
- mycitygrid.com portal recon (no credentials)
- test_db_readings.py
- test_api_contract.py
- Hourly-Only Granularity Convention
- test_jobs.py
- Reading
- datetime
- Connection
- date

## God Nodes (most connected - your core abstractions)
1. `SourceError` - 24 edges
2. `excerpt()` - 20 edges
3. `parse_reading_row()` - 16 edges
4. `run_job()` - 14 edges
5. `_Portal` - 13 edges
6. `MeterReading` - 13 edges
7. `_range()` - 13 edges
8. `summary()` - 13 edges
9. `parse_hourly()` - 12 edges
10. `upsert_meter_readings()` - 12 edges

## Surprising Connections (you probably didn't know these)
- `_login()` --conceptually_related_to--> `Undocumented mycitygrid Portal Lesson`  [INFERRED]
  consumption/source.py → .cursor/memory/INDEX.md
- `portal_session()` --implements--> `Lazy Scrapling Import Lesson`  [INFERRED]
  consumption/source.py → .cursor/memory/INDEX.md
- `run_job()` --implements--> `Idempotent Refresh Jobs Convention`  [INFERRED]
  consumption/jobs.py → .cursor/memory/INDEX.md
- `mycitygrid.com Portal` --references--> `portal_session()`  [EXTRACTED]
  README.md → consumption/source.py
- `StealthySession Fallback Note` --references--> `portal_session()`  [EXTRACTED]
  README.md → consumption/source.py

## Import Cycles
- None detected.

## Communities (27 total, 9 thin omitted)

### Community 0 - "readings.py"
Cohesion: 0.06
Nodes (59): ConsumptionMonitor - local API for electricity and water consumption from…, _bool_value(), _optional_float(), _optional_int(), parse_reading_page(), parse_reading_row(), datetime, Pure parsers for the mycitygrid meter reading log (GET meterdata). Maps portal… (+51 more)

### Community 1 - "db.py"
Cohesion: 0.16
Nodes (32): alert_flags(), daily_totals(), due(), _fetch_readings_for_meter(), _first_reading_on_or_after(), _interval_dict(), intervals(), job_states() (+24 more)

### Community 3 - "api.py"
Cohesion: 0.14
Nodes (38): Conn, _directions_for(), _first_stored(), health(), index(), job_status(), _latest_register(), lifespan() (+30 more)

### Community 4 - "jobs.py"
Cohesion: 0.15
Nodes (27): Connection, _advance_backfill(), _always(), _backfill(), _in_january(), Job, local_today(), loop() (+19 more)

### Community 5 - "test_source_session.py"
Cohesion: 0.15
Nodes (19): _login(), Scaffold Complete, Fetching Unimplemented, Fetching Not Implemented Status, _FakePortal, _FakeResponse, _FakeSession, _raises(), Self-check for the mycitygrid adapter HTTP half: login, token refresh, reading-… (+11 more)

### Community 6 - "records.py"
Cohesion: 0.25
Nodes (15): alert_flags(), coverage(), daily_totals(), fetch_readings(), IntervalReading, intervals(), latest_reading(), meter_readings() (+7 more)

### Community 7 - "secrets.py"
Cohesion: 0.15
Nodes (20): Array, _Blob, clear(), _crypt32(), _dpapi(), _input_blob(), load(), Path (+12 more)

### Community 8 - "env.ps1"
Cohesion: 1.00
Nodes (3): Initialize-Venv(), Show-Phase(), Wait-WithProgress()

### Community 9 - "config.py"
Cohesion: 0.07
Nodes (32): _credentials(), credentials_present(), _load_env_file(), Path, Runtime configuration, read once at import from the environment and an optional…, Populate os.environ from a KEY=VALUE file. Real environment variables always…, Encrypted store first; the environment stays available as a manual override., consumption Package (+24 more)

### Community 12 - "launcher-common.ps1"
Cohesion: 0.70
Nodes (4): Exit-WithError(), Test-TcpPort(), Wait-ApiReady(), Write-Log()

### Community 16 - "mycitygrid.com portal recon (no credentials)"
Cohesion: 0.29
Nodes (6): Best guess at the consumption endpoints, Best guess at the login flow, Dead ends, mycitygrid.com portal recon (no credentials), Unknowns that only credentials can answer, What we know

### Community 18 - "test_db_readings.py"
Cohesion: 0.33
Nodes (13): get_conn(), connect(), upsert_meter_readings(), Path, _conn(), _elec(), date, datetime (+5 more)

### Community 20 - "test_api_contract.py"
Cohesion: 0.13
Nodes (17): datetime, Offline contract checks for the HTTP API against the records.py storage…, test_alerts_per_meter(), test_bad_utility_returns_422(), _test_client(), test_health_coverage_shape(), test_index_lists_new_endpoints(), test_jobs_use_reading_log_schedule() (+9 more)

### Community 22 - "test_jobs.py"
Cohesion: 0.20
Nodes (20): get_state(), Exception, MeterReading, _conn(), _fake_source(), date, datetime, Offline self-checks for the refresh schedule and job bookkeeping. Uses a… (+12 more)

## Knowledge Gaps
- **20 isolated node(s):** `IntervalReading`, `Best guess at the consumption endpoints`, `Best guess at the login flow`, `Dead ends`, `Unknowns that only credentials can answer` (+15 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `portal_session()` connect `config.py` to `readings.py`, `test_source_session.py`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Why does `run_job()` connect `jobs.py` to `readings.py`, `db.py`, `api.py`, `test_db_readings.py`, `test_jobs.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `MeterReading` connect `records.py` to `readings.py`, `db.py`, `test_db_readings.py`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **What connects `IntervalReading`, `Best guess at the consumption endpoints`, `Best guess at the login flow` to the rest of the system?**
  _20 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `readings.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06202435312024353 - nodes in this community are weakly interconnected._
- **Should `api.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14304993252361672 - nodes in this community are weakly interconnected._
- **Should `jobs.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1455026455026455 - nodes in this community are weakly interconnected._