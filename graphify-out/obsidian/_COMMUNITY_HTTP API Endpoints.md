---
type: community
cohesion: 0.21
members: 20
---

# HTTP API Endpoints

**Cohesion:** 0.21 - loosely connected
**Members:** 20 nodes

## Members
- [[Conn]] - code
- [[Default to the last 7 local days and reject anything unbounded or backwards.]] - rationale - consumption/api.py
- [[Endpoint Reference Table]] - document - README.md
- [[Force one job to run now, for testing a freshly implemented source adapter.]] - rationale - consumption/api.py
- [[GET  (endpoint index)]] - code - consumption/api.py
- [[GET health]] - code - consumption/api.py
- [[GET jobs]] - code - consumption/api.py
- [[GET readingsdaily]] - code - consumption/api.py
- [[GET readingshourly]] - code - consumption/api.py
- [[GET summary]] - code - consumption/api.py
- [[MAX_RANGE_DAYS limit]] - code - consumption/api.py
- [[POST refresh{job}]] - code - consumption/api.py
- [[Read-only HTTP API over the stored readings, shaped for Home Assistant REST…]] - rationale - consumption/api.py
- [[Utility]] - code
- [[Utility literal type]] - code - consumption/api.py
- [[_range (date range validation)]] - code - consumption/api.py
- [[api.py]] - code - consumption/api.py
- [[date]] - code
- [[get]] - code
- [[post]] - code

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/HTTP_API_Endpoints
SORT file.name ASC
```

## Connections to other communities
- 11 edges to [[_COMMUNITY_Refresh Schedule]]
- 8 edges to [[_COMMUNITY_SQLite Storage And Aggregation]]
- 4 edges to [[_COMMUNITY_Configuration And Entry Point]]
- 3 edges to [[_COMMUNITY_Mycitygrid Source Adapter]]
- 2 edges to [[_COMMUNITY_Scheduler Loop]]
- 2 edges to [[_COMMUNITY_Launcher And Dependencies]]
- 1 edge to [[_COMMUNITY_Self-Check Suite]]

## Top bridge nodes
- [[api.py]] - degree 17, connects to 6 communities
- [[GET health]] - degree 8, connects to 4 communities
- [[GET summary]] - degree 12, connects to 3 communities
- [[_range (date range validation)]] - degree 9, connects to 2 communities
- [[POST refresh{job}]] - degree 8, connects to 2 communities