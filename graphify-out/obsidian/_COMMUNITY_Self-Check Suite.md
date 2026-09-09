---
type: community
cohesion: 0.14
members: 25
---

# Self-Check Suite

**Cohesion:** 0.14 - loosely connected
**Members:** 25 nodes

## Members
- [[2200 UTC in January is already the next day in AsiaJerusalem (UTC+2).]] - rationale - tests/test_aggregation.py
- [[A missing adapter must land in job_state as an error, never kill the scheduler.]] - rationale - tests/test_aggregation.py
- [[LOCAL_TZ setting]] - code - consumption/config.py
- [[Path_1]] - code
- [[Re-fetching a stored hour must correct it in place, not duplicate it.]] - rationale - tests/test_aggregation.py
- [[Self-check for the two things in this project that are easy to get silently…]] - rationale - tests/test_aggregation.py
- [[Self-check runner main]] - code - tests/test_aggregation.py
- [[Wednesday 2026-09-09 the last full Sunday-Saturday week is 08-30..09-05.]] - rationale - tests/test_aggregation.py
- [[_reading test helper]] - code - tests/test_aggregation.py
- [[_reading()]] - code - tests/test_aggregation.py
- [[connect (SQLite connection)]] - code - consumption/db.py
- [[datetime_2]] - code
- [[get_conn dependency]] - code - consumption/api.py
- [[test_aggregation.py]] - code - tests/test_aggregation.py
- [[test_due]] - code - tests/test_aggregation.py
- [[test_due()]] - code - tests/test_aggregation.py
- [[test_job_ranges()]] - code - tests/test_aggregation.py
- [[test_local_day_mapping]] - code - tests/test_aggregation.py
- [[test_local_day_mapping()]] - code - tests/test_aggregation.py
- [[test_missing_source_is_recorded_not_raised()]] - code - tests/test_aggregation.py
- [[test_naive_timestamp_rejected]] - code - tests/test_aggregation.py
- [[test_naive_timestamp_rejected()]] - code - tests/test_aggregation.py
- [[test_refetch_overwrites_and_daily_sums()]] - code - tests/test_aggregation.py
- [[tzdata dependency]] - document - requirements.txt
- [[upsert_readings]] - code - consumption/db.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Self-Check_Suite
SORT file.name ASC
```

## Connections to other communities
- 18 edges to [[_COMMUNITY_SQLite Storage And Aggregation]]
- 9 edges to [[_COMMUNITY_Refresh Schedule]]
- 6 edges to [[_COMMUNITY_Mycitygrid Source Adapter]]
- 2 edges to [[_COMMUNITY_Configuration And Entry Point]]
- 2 edges to [[_COMMUNITY_Launcher And Dependencies]]
- 1 edge to [[_COMMUNITY_HTTP API Endpoints]]
- 1 edge to [[_COMMUNITY_Scheduler Loop]]

## Top bridge nodes
- [[connect (SQLite connection)]] - degree 13, connects to 4 communities
- [[upsert_readings]] - degree 14, connects to 3 communities
- [[test_aggregation.py]] - degree 14, connects to 3 communities
- [[Self-check runner main]] - degree 8, connects to 3 communities
- [[test_refetch_overwrites_and_daily_sums()]] - degree 10, connects to 2 communities