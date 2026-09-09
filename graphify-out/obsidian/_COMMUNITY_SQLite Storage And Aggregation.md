---
type: community
cohesion: 0.18
members: 21
---

# SQLite Storage And Aggregation

**Cohesion:** 0.18 - loosely connected
**Members:** 21 nodes

## Members
- [[A job with no recorded run is always due, so a restart catches up on missed…]] - rationale - consumption/db.py
- [[Connection]] - code
- [[Hourly-Only Granularity Convention]] - document - .cursor/memory/INDEX.md
- [[Idempotent Refresh Jobs Convention]] - document - .cursor/memory/INDEX.md
- [[One Row Per Utility, Meter, Hour]] - document - README.md
- [[Refresh Schedule Table]] - document - README.md
- [[SQLite storage for hourly consumption plus the scheduler's job bookkeeping. The…]] - rationale - consumption/db.py
- [[_utc_now()]] - code - consumption/db.py
- [[daily aggregation query]] - code - consumption/db.py
- [[date_1]] - code
- [[datetime]] - code
- [[db.py]] - code - consumption/db.py
- [[due (interval check)]] - code - consumption/db.py
- [[hourly query]] - code - consumption/db.py
- [[job_state table]] - code - consumption/db.py
- [[job_states]] - code - consumption/db.py
- [[latest_hour query]] - code - consumption/db.py
- [[reading table]] - code - consumption/db.py
- [[record_job]] - code - consumption/db.py
- [[test_refetch_overwrites_and_daily_sums]] - code - tests/test_aggregation.py
- [[total aggregation query]] - code - consumption/db.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/SQLite_Storage_And_Aggregation
SORT file.name ASC
```

## Connections to other communities
- 18 edges to [[_COMMUNITY_Self-Check Suite]]
- 8 edges to [[_COMMUNITY_HTTP API Endpoints]]
- 8 edges to [[_COMMUNITY_Refresh Schedule]]
- 4 edges to [[_COMMUNITY_Configuration And Entry Point]]
- 2 edges to [[_COMMUNITY_Mycitygrid Source Adapter]]

## Top bridge nodes
- [[db.py]] - degree 19, connects to 5 communities
- [[job_states]] - degree 8, connects to 3 communities
- [[reading table]] - degree 8, connects to 3 communities
- [[daily aggregation query]] - degree 8, connects to 2 communities
- [[due (interval check)]] - degree 8, connects to 2 communities