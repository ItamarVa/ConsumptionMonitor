# Graph Report - ConsumptionMonitor  (2026-09-09)

## Corpus Check
- 17 files · ~9,013 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 190 nodes · 408 edges · 16 communities (11 shown, 5 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 27 edges (avg confidence: 0.71)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8df8eaeb`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- source.py
- test_aggregation.py
- db.py
- api.py
- jobs.py
- timedelta
- config.py
- secrets.py
- env.ps1
- date
- Double-Clickable Launcher Preference
- Run via run.bat
- RuntimeError
- Path

## God Nodes (most connected - your core abstractions)
1. `run_job()` - 14 edges
2. `summary()` - 13 edges
3. `upsert_readings()` - 13 edges
4. `_range()` - 12 edges
5. `connect()` - 11 edges
6. `test_refetch_overwrites_and_daily_sums()` - 11 edges
7. `run_due()` - 10 edges
8. `_reading()` - 10 edges
9. `portal_session()` - 10 edges
10. `local_today()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `upsert_readings()` --implements--> `One Row Per Utility, Meter, Hour`  [INFERRED]
  consumption/db.py → README.md
- `daily()` --implements--> `Hourly-Only Granularity Convention`  [INFERRED]
  consumption/db.py → .cursor/memory/INDEX.md
- `run_job()` --implements--> `Idempotent Refresh Jobs Convention`  [INFERRED]
  consumption/jobs.py → .cursor/memory/INDEX.md
- `_login()` --conceptually_related_to--> `Undocumented mycitygrid Portal Lesson`  [INFERRED]
  consumption/source.py → .cursor/memory/INDEX.md
- `portal_session()` --implements--> `Lazy Scrapling Import Lesson`  [INFERRED]
  consumption/source.py → .cursor/memory/INDEX.md

## Import Cycles
- None detected.

## Communities (16 total, 5 thin omitted)

### Community 0 - "source.py"
Cohesion: 0.13
Nodes (24): fetch_hourly(), _fetch_range(), _login(), portal_session(), RuntimeError, Adapter for www.mycitygrid.com - the only module that talks to the portal.…, The adapter is not implemented or not configured. Not a transient failure., The portal was reached but did not answer as expected. Retrying later may work. (+16 more)

### Community 1 - "test_aggregation.py"
Cohesion: 0.17
Nodes (27): connect(), upsert_readings(), Path, Reading, _conn(), datetime, Self-check for the things in this project that are easy to get silently wrong:…, Wednesday 2026-09-09: the last full Sunday-Saturday week is 08-30..09-05. (+19 more)

### Community 2 - "db.py"
Cohesion: 0.16
Nodes (21): coverage(), daily(), get_state(), hourly(), job_states(), latest_hour(), monthly(), Connection (+13 more)

### Community 3 - "api.py"
Cohesion: 0.16
Nodes (27): Conn, _first_stored(), get_conn(), health(), index(), job_status(), lifespan(), Connection (+19 more)

### Community 4 - "jobs.py"
Cohesion: 0.15
Nodes (25): _advance_backfill(), _always(), _in_january(), Job, _last_full_week(), local_today(), loop(), _previous_year() (+17 more)

### Community 5 - "timedelta"
Cohesion: 0.50
Nodes (5): due(), datetime, A job with no recorded run is always due, so a restart catches up on missed…, test_due(), timedelta

### Community 6 - "config.py"
Cohesion: 0.10
Nodes (17): _credentials(), credentials_present(), _load_env_file(), Path, Runtime configuration, read once at import from the environment and an optional…, Populate os.environ from a KEY=VALUE file. Real environment variables always…, Encrypted store first; the environment stays available as a manual override., consumption Package (+9 more)

### Community 7 - "secrets.py"
Cohesion: 0.14
Nodes (21): Array, _Blob, clear(), _crypt32(), _dpapi(), _input_blob(), load(), Path (+13 more)

### Community 8 - "env.ps1"
Cohesion: 1.00
Nodes (3): Initialize-Venv(), Show-Phase(), Wait-WithProgress()

## Knowledge Gaps
- **12 isolated node(s):** `Lazy Scrapling Import Lesson`, `Scaffold Complete, Fetching Unimplemented`, `scrapling[fetchers] Extra Lesson`, `Double-Clickable Launcher Preference`, `Run via run.bat` (+7 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `portal_session()` connect `source.py` to `config.py`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Why does `run_job()` connect `jobs.py` to `source.py`, `test_aggregation.py`, `db.py`, `api.py`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Why does `_range()` connect `api.py` to `jobs.py`, `timedelta`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **What connects `Lazy Scrapling Import Lesson`, `Scaffold Complete, Fetching Unimplemented`, `scrapling[fetchers] Extra Lesson` to the rest of the system?**
  _12 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `source.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12666666666666668 - nodes in this community are weakly interconnected._
- **Should `config.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._
- **Should `secrets.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1422924901185771 - nodes in this community are weakly interconnected._