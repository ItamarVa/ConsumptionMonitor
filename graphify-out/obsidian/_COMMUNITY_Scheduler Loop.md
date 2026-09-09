---
type: community
cohesion: 0.40
members: 5
---

# Scheduler Loop

**Cohesion:** 0.40 - moderately connected
**Members:** 5 nodes

## Members
- [[FastAPI]] - code
- [[TICK_SECONDS setting]] - code - consumption/config.py
- [[Tick forever, delegating the blocking fetch and SQLite work to a worker thread.]] - rationale - consumption/jobs.py
- [[lifespan (startupshutdown)]] - code - consumption/api.py
- [[loop (scheduler tick)]] - code - consumption/jobs.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Scheduler_Loop
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_HTTP API Endpoints]]
- 2 edges to [[_COMMUNITY_Refresh Schedule]]
- 1 edge to [[_COMMUNITY_Launcher And Dependencies]]
- 1 edge to [[_COMMUNITY_Self-Check Suite]]

## Top bridge nodes
- [[lifespan (startupshutdown)]] - degree 5, connects to 3 communities
- [[loop (scheduler tick)]] - degree 5, connects to 1 community
- [[FastAPI]] - degree 2, connects to 1 community