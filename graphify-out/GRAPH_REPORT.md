# Graph Report - ConsumptionMonitor  (2026-09-09)

## Corpus Check
- 22 files · ~15,683 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 317 nodes · 691 edges · 19 communities (13 shown, 6 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 37 edges (avg confidence: 0.74)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `db7f8e39`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- readings.py
- test_aggregation.py
- RuntimeError
- api.py
- jobs.py
- test_source_session.py
- date
- secrets.py
- env.ps1
- source.py
- Double-Clickable Launcher Preference
- Run via run.bat
- config.py
- Path
- mycitygrid.com portal recon (no credentials)
- datetime

## God Nodes (most connected - your core abstractions)
1. `parse_hourly()` - 22 edges
2. `SourceError` - 16 edges
3. `run_job()` - 14 edges
4. `_fetch_range()` - 13 edges
5. `upsert_readings()` - 13 edges
6. `summary()` - 13 edges
7. `_login()` - 12 edges
8. `_FakeResponse` - 12 edges
9. `_range()` - 12 edges
10. `_Portal` - 11 edges

## Surprising Connections (you probably didn't know these)
- `_login()` --conceptually_related_to--> `Undocumented mycitygrid Portal Lesson`  [INFERRED]
  consumption/source.py → .cursor/memory/INDEX.md
- `portal_session()` --implements--> `Lazy Scrapling Import Lesson`  [INFERRED]
  consumption/source.py → .cursor/memory/INDEX.md
- `daily()` --implements--> `Hourly-Only Granularity Convention`  [INFERRED]
  consumption/db.py → .cursor/memory/INDEX.md
- `upsert_readings()` --implements--> `One Row Per Utility, Meter, Hour`  [INFERRED]
  consumption/db.py → README.md
- `run_job()` --implements--> `Idempotent Refresh Jobs Convention`  [INFERRED]
  consumption/jobs.py → .cursor/memory/INDEX.md

## Import Cycles
- None detected.

## Communities (19 total, 6 thin omitted)

### Community 0 - "readings.py"
Cohesion: 0.09
Nodes (35): _buckets(), excerpt(), _exists_locally(), _hour_of_day(), _hour_of_timestamp(), _label(), _number(), parse_hourly() (+27 more)

### Community 1 - "test_aggregation.py"
Cohesion: 0.08
Nodes (52): connect(), daily(), due(), get_state(), hourly(), job_states(), latest_hour(), monthly() (+44 more)

### Community 3 - "api.py"
Cohesion: 0.15
Nodes (29): Conn, _first_stored(), get_conn(), health(), index(), job_status(), lifespan(), Connection (+21 more)

### Community 4 - "jobs.py"
Cohesion: 0.14
Nodes (28): _advance_backfill(), _always(), _backfill(), _in_january(), Job, _last_full_week(), local_today(), loop() (+20 more)

### Community 5 - "test_source_session.py"
Cohesion: 0.09
Nodes (38): fetch_hourly(), _fetch_range(), _login(), Authenticate `session` and return the wrapper that keeps it authenticated. An…, Pull hourly buckets for local dates start..end inclusive from a logged-in…, Return hourly consumption for local dates start..end inclusive. Re-fetching a…, Scaffold Complete, Fetching Unimplemented, date (+30 more)

### Community 7 - "secrets.py"
Cohesion: 0.13
Nodes (23): Array, _credentials(), Encrypted store first; the environment stays available as a manual override., _Blob, clear(), _crypt32(), _dpapi(), _input_blob() (+15 more)

### Community 8 - "env.ps1"
Cohesion: 1.00
Nodes (3): Initialize-Venv(), Show-Phase(), Wait-WithProgress()

### Community 9 - "source.py"
Cohesion: 0.12
Nodes (22): Adapter for www.mycitygrid.com - the only module that talks to the portal.…, When the access token dies, from `expires_in` seconds or the OWIN `.expires`…, _token_expiry(), datetime, _hours_utc(), _payload(), _raises(), Self-check for the mycitygrid payload parsers, which are written against a… (+14 more)

### Community 12 - "config.py"
Cohesion: 0.06
Nodes (36): credentials_present(), _load_env_file(), Path, Runtime configuration, read once at import from the environment and an optional…, Populate os.environ from a KEY=VALUE file. Real environment variables always…, consumption Package, ConsumptionMonitor - local API for electricity and water consumption from…, Console UTF-8 Reconfiguration (+28 more)

### Community 16 - "mycitygrid.com portal recon (no credentials)"
Cohesion: 0.29
Nodes (6): Best guess at the consumption endpoints, Best guess at the login flow, Dead ends, mycitygrid.com portal recon (no credentials), Unknowns that only credentials can answer, What we know

## Knowledge Gaps
- **17 isolated node(s):** `What we know`, `Best guess at the login flow`, `Best guess at the consumption endpoints`, `Unknowns that only credentials can answer`, `Dead ends` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `portal_session()` connect `config.py` to `readings.py`, `source.py`, `test_source_session.py`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `run_job()` connect `jobs.py` to `test_aggregation.py`, `api.py`, `test_source_session.py`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `_Portal` connect `readings.py` to `source.py`, `test_source_session.py`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `date` (e.g. with `test_alternative_bucket_labels()` and `test_autumn_repeat_hour_keeps_both()`) actually correct?**
  _`date` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `What we know`, `Best guess at the login flow`, `Best guess at the consumption endpoints` to the rest of the system?**
  _17 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `readings.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09413067552602436 - nodes in this community are weakly interconnected._
- **Should `test_aggregation.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08350168350168351 - nodes in this community are weakly interconnected._