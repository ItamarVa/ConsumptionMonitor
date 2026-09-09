# Graph Report - ConsumptionMonitor  (2026-09-09)

## Corpus Check
- 32 files · ~74,398 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 376 nodes · 935 edges · 25 communities (17 shown, 8 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 38 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5
- Community 6
- Community 7
- Community 8
- Community 9
- Community 10
- Community 11
- Community 12
- Community 13
- Community 14
- Community 15
- Community 16
- Community 18
- Community 19
- Community 20
- Community 21
- Community 24

## God Nodes (most connected - your core abstractions)
1. `SourceError` - 36 edges
2. `excerpt()` - 21 edges
3. `MeterReading` - 17 edges
4. `parse_reading_row()` - 17 edges
5. `run_job()` - 16 edges
6. `_Portal` - 15 edges
7. `upsert_meter_readings()` - 15 edges
8. `SourceNotReady` - 13 edges
9. `_range()` - 13 edges
10. `summary()` - 13 edges

## Surprising Connections (you probably didn't know these)
- `run_job()` --implements--> `Idempotent Refresh Jobs Convention`  [INFERRED]
  consumption/jobs.py → .cursor/memory/INDEX.md
- `_login()` --conceptually_related_to--> `Undocumented mycitygrid Portal Lesson`  [INFERRED]
  consumption/source.py → .cursor/memory/INDEX.md
- `portal_session()` --implements--> `Lazy Scrapling Import Lesson`  [INFERRED]
  consumption/source.py → .cursor/memory/INDEX.md
- `_range()` --references--> `api.py as Only Trust Boundary`  [EXTRACTED]
  consumption/api.py → .cursor/memory/INDEX.md
- `_login()` --references--> `Fetching Not Implemented Status`  [EXTRACTED]
  consumption/source.py → README.md

## Import Cycles
- None detected.

## Communities (25 total, 8 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (67): credentials_present(), _load_env_file(), Path, Runtime configuration, read once at import from the environment and an optional…, Populate os.environ from a KEY=VALUE file. Real environment variables always…, ConsumptionMonitor - local API for electricity and water consumption from…, Entry point: `python -m consumption` serves the API and runs the refresh…, _bool_value() (+59 more)

### Community 1 - "Community 1"
Cohesion: 0.07
Nodes (37): RuntimeError, The adapter is not implemented or not configured. Not a transient failure., SourceNotReady, _fetch_readings(), _login(), _Portal, portal_session(), date (+29 more)

### Community 2 - "Community 2"
Cohesion: 0.14
Nodes (38): Conn, _directions_for(), _first_stored(), health(), index(), job_status(), _latest_register(), lifespan() (+30 more)

### Community 3 - "Community 3"
Cohesion: 0.18
Nodes (33): Connection, alert_flags(), daily_totals(), due(), _fetch_readings_for_meter(), _first_reading_on_or_after(), get_state(), _interval_dict() (+25 more)

### Community 4 - "Community 4"
Cohesion: 0.12
Nodes (31): _advance_backfill(), _always(), _backfill(), _in_january(), Job, local_today(), loop(), _month_bounds() (+23 more)

### Community 5 - "Community 5"
Cohesion: 0.13
Nodes (22): Array, _credentials(), Encrypted store first; the environment stays available as a manual override., _Blob, clear(), _crypt32(), _dpapi(), _input_blob() (+14 more)

### Community 6 - "Community 6"
Cohesion: 0.21
Nodes (20): MeterReading, Exception, MeterReading, _conn(), _fake_source(), date, datetime, Offline self-checks for the refresh schedule and job bookkeeping. Uses a… (+12 more)

### Community 7 - "Community 7"
Cohesion: 0.14
Nodes (18): get_conn(), connect(), Path, datetime, Path, log(), main(), Run backfill jobs until BACKFILL_DONE or no progress. Logs to… (+10 more)

### Community 8 - "Community 8"
Cohesion: 0.33
Nodes (14): MeterReading, upsert_meter_readings(), _conn(), _elec(), date, datetime, MeterReading, Offline self-checks for raw meter reading storage and exact register deltas. (+6 more)

### Community 9 - "Community 9"
Cohesion: 0.26
Nodes (14): alert_flags(), coverage(), daily_totals(), fetch_readings(), IntervalReading, intervals(), latest_reading(), meter_readings() (+6 more)

### Community 10 - "Community 10"
Cohesion: 0.25
Nodes (8): consumption Package, Console UTF-8 Reconfiguration, main (startup entry), Hebrew Path / cp1252 Console Lesson, fastapi dependency, Exact Pinning, 14-Day-Old Versions, tzdata dependency, uvicorn dependency

### Community 11 - "Community 11"
Cohesion: 0.29
Nodes (6): Best guess at the consumption endpoints, Best guess at the login flow, Dead ends, mycitygrid.com portal recon (no credentials), Unknowns that only credentials can answer, What we know

### Community 12 - "Community 12"
Cohesion: 0.70
Nodes (4): Exit-WithError(), Test-TcpPort(), Wait-ApiReady(), Write-Log()

### Community 13 - "Community 13"
Cohesion: 1.00
Nodes (3): Initialize-Venv(), Show-Phase(), Wait-WithProgress()

## Knowledge Gaps
- **20 isolated node(s):** `IntervalReading`, `Best guess at the consumption endpoints`, `Best guess at the login flow`, `Dead ends`, `Unknowns that only credentials can answer` (+15 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SourceError` connect `Community 0` to `Community 1`, `Community 9`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Why does `MeterReading` connect `Community 6` to `Community 0`, `Community 1`, `Community 3`, `Community 8`, `Community 9`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `portal_session()` connect `Community 1` to `Community 0`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `SourceError` (e.g. with `_Portal` and `test_malformed_row_raises_with_excerpt()`) actually correct?**
  _`SourceError` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `MeterReading` (e.g. with `_reading_to_row()` and `upsert_meter_readings()`) actually correct?**
  _`MeterReading` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `IntervalReading`, `Best guess at the consumption endpoints`, `Best guess at the login flow` to the rest of the system?**
  _20 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.05740740740740741 - nodes in this community are weakly interconnected._