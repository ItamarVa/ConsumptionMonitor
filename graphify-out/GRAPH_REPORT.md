# Graph Report - ConsumptionMonitor  (2026-09-09)

## Corpus Check
- Corpus is ~4,436 words - fits in a single context window. You may not need a graph.

## Summary
- 156 nodes · 348 edges · 8 communities
- Extraction: 87% EXTRACTED · 12% INFERRED · 1% AMBIGUOUS · INFERRED: 43 edges (avg confidence: 0.59)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Mycitygrid Source Adapter
- Self-Check Suite
- SQLite Storage And Aggregation
- HTTP API Endpoints
- Refresh Schedule
- Launcher And Dependencies
- Configuration And Entry Point
- Scheduler Loop

## God Nodes (most connected - your core abstractions)
1. `run_job` - 16 edges
2. `upsert_readings` - 14 edges
3. `connect (SQLite connection)` - 13 edges
4. `GET /summary` - 12 edges
5. `portal_session` - 12 edges
6. `fetch_hourly` - 11 edges
7. `local_today` - 10 edges
8. `test_refetch_overwrites_and_daily_sums()` - 10 edges
9. `_range (date range validation)` - 9 edges
10. `run_due` - 9 edges

## Surprising Connections (you probably didn't know these)
- `api.py as Only Trust Boundary` --references--> `_range (date range validation)`  [EXTRACTED]
  .cursor/memory/INDEX.md → consumption/api.py
- `upsert_readings` --implements--> `One Row Per Utility, Meter, Hour`  [INFERRED]
  consumption/db.py → README.md
- `daily aggregation query` --implements--> `Hourly-Only Granularity Convention`  [INFERRED]
  consumption/db.py → .cursor/memory/INDEX.md
- `run_job` --implements--> `Idempotent Refresh Jobs Convention`  [INFERRED]
  consumption/jobs.py → .cursor/memory/INDEX.md
- `portal_session` --implements--> `Lazy Scrapling Import Lesson`  [INFERRED]
  consumption/source.py → .cursor/memory/INDEX.md

## Import Cycles
- None detected.

## Communities (8 total, 0 thin omitted)

### Community 0 - "Mycitygrid Source Adapter"
Cohesion: 0.10
Nodes (30): MYCITYGRID_BASE_URL setting, UTILITIES tuple, SourceError error, fetch_hourly, _fetch_range (unimplemented), IMPERSONATE fingerprint, _login (unimplemented), portal_session (+22 more)

### Community 1 - "Self-Check Suite"
Cohesion: 0.14
Nodes (24): get_conn dependency, LOCAL_TZ setting, connect (SQLite connection), Path, upsert_readings, tzdata dependency, test_due, test_local_day_mapping (+16 more)

### Community 2 - "SQLite Storage And Aggregation"
Cohesion: 0.18
Nodes (20): daily aggregation query, due (interval check), hourly query, job_state table, job_states, latest_hour query, Connection, date (+12 more)

### Community 3 - "HTTP API Endpoints"
Cohesion: 0.21
Nodes (19): Conn, GET /health, GET / (endpoint index), GET /jobs, MAX_RANGE_DAYS limit, date, _range (date range validation), Read-only HTTP API over the stored readings, shaped for Home Assistant REST… (+11 more)

### Community 4 - "Refresh Schedule"
Cohesion: 0.19
Nodes (19): _DAYS_SINCE_SUNDAY helper, JOBS schedule table, _last_full_week range, local_today, Connection, date, datetime, Refresh schedule: which local date range each job re-fetches, and how often.… (+11 more)

### Community 5 - "Launcher And Dependencies"
Cohesion: 0.16
Nodes (18): FastAPI app, HOST and PORT settings, consumption Package, Console UTF-8 Reconfiguration, main (startup entry), Double-Clickable Launcher Preference, api.py as Only Trust Boundary, Hebrew Path / cp1252 Console Lesson (+10 more)

### Community 6 - "Configuration And Entry Point"
Cohesion: 0.14
Nodes (11): credentials_present, DB_PATH setting, _load_env_file (.env loader), mycitygrid Credentials, Path, Runtime configuration, read once at import from the environment and an optional…, Populate os.environ from a KEY=VALUE file. Real environment variables always…, SCHEMA script (+3 more)

### Community 7 - "Scheduler Loop"
Cohesion: 0.40
Nodes (5): lifespan (startup/shutdown), TICK_SECONDS setting, loop (scheduler tick), Tick forever, delegating the blocking fetch and SQLite work to a worker thread., FastAPI

## Ambiguous Edges - Review These
- `Reading dataclass` → `UNITS map`  [AMBIGUOUS]
  consumption/source.py · relation: shares_data_with
- `_login (unimplemented)` → `SourceError error`  [AMBIGUOUS]
  consumption/source.py · relation: references
- `_fetch_range (unimplemented)` → `LOCAL_TZ setting`  [AMBIGUOUS]
  consumption/source.py · relation: references

## Knowledge Gaps
- **7 isolated node(s):** `MAX_RANGE_DAYS limit`, `TICK_SECONDS setting`, `_DAYS_SINCE_SUNDAY helper`, `IMPERSONATE fingerprint`, `SourceError error` (+2 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Reading dataclass` and `UNITS map`?**
  _Edge tagged AMBIGUOUS (relation: shares_data_with) - confidence is low._
- **What is the exact relationship between `_login (unimplemented)` and `SourceError error`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `_fetch_range (unimplemented)` and `LOCAL_TZ setting`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `Launcher startup flow` connect `Launcher And Dependencies` to `Self-Check Suite`, `Configuration And Entry Point`?**
  _High betweenness centrality (0.109) - this node is a cross-community bridge._
- **Why does `portal_session` connect `Mycitygrid Source Adapter` to `Refresh Schedule`, `Configuration And Entry Point`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Why does `run_job` connect `Refresh Schedule` to `Mycitygrid Source Adapter`, `Self-Check Suite`, `SQLite Storage And Aggregation`, `HTTP API Endpoints`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **What connects `MAX_RANGE_DAYS limit`, `TICK_SECONDS setting`, `_DAYS_SINCE_SUNDAY helper` to the rest of the system?**
  _7 weakly-connected nodes found - possible documentation gaps or missing edges._