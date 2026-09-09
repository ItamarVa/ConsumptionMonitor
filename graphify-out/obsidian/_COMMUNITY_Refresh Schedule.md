---
type: community
cohesion: 0.19
members: 20
---

# Refresh Schedule

**Cohesion:** 0.19 - loosely connected
**Members:** 20 nodes

## Members
- [[Connection_1]] - code
- [[Fetch and store one job's range for every utility. Returns rows written.]] - rationale - consumption/jobs.py
- [[JOBS schedule table]] - code - consumption/jobs.py
- [[Refresh schedule which local date range each job re-fetches, and how often.…]] - rationale - consumption/jobs.py
- [[Run every job whose interval has elapsed. Safe to call as often as you like.]] - rationale - consumption/jobs.py
- [[SourceNotReady error]] - code - consumption/source.py
- [[_DAYS_SINCE_SUNDAY helper]] - code - consumption/jobs.py
- [[_last_full_week range]] - code - consumption/jobs.py
- [[_today range]] - code - consumption/jobs.py
- [[_year_to_date range]] - code - consumption/jobs.py
- [[_yesterday range]] - code - consumption/jobs.py
- [[date_2]] - code
- [[datetime_1]] - code
- [[jobs.py]] - code - consumption/jobs.py
- [[local_today]] - code - consumption/jobs.py
- [[run_due]] - code - consumption/jobs.py
- [[run_job]] - code - consumption/jobs.py
- [[test_job_ranges]] - code - tests/test_aggregation.py
- [[test_missing_source_is_recorded_not_raised]] - code - tests/test_aggregation.py
- [[timedelta]] - code

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Refresh_Schedule
SORT file.name ASC
```

## Connections to other communities
- 11 edges to [[_COMMUNITY_HTTP API Endpoints]]
- 9 edges to [[_COMMUNITY_Self-Check Suite]]
- 8 edges to [[_COMMUNITY_SQLite Storage And Aggregation]]
- 5 edges to [[_COMMUNITY_Mycitygrid Source Adapter]]
- 2 edges to [[_COMMUNITY_Configuration And Entry Point]]
- 2 edges to [[_COMMUNITY_Scheduler Loop]]

## Top bridge nodes
- [[jobs.py]] - degree 16, connects to 6 communities
- [[run_job]] - degree 16, connects to 4 communities
- [[run_due]] - degree 9, connects to 3 communities
- [[timedelta]] - degree 7, connects to 3 communities
- [[local_today]] - degree 10, connects to 2 communities