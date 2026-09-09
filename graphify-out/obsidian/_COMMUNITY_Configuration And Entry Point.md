---
type: community
cohesion: 0.14
members: 15
---

# Configuration And Entry Point

**Cohesion:** 0.14 - loosely connected
**Members:** 15 nodes

## Members
- [[ConsumptionMonitor - local API for electricity and water consumption from…]] - rationale - consumption/__init__.py
- [[DB_PATH setting]] - code - consumption/config.py
- [[Entry point `python -m consumption` serves the API and runs the refresh…]] - rationale - consumption/__main__.py
- [[Module Layout]] - document - README.md
- [[Path]] - code
- [[Populate os.environ from a KEY=VALUE file. Real environment variables always…]] - rationale - consumption/config.py
- [[Runtime configuration, read once at import from the environment and an optional…]] - rationale - consumption/config.py
- [[SCHEMA script]] - code - consumption/db.py
- [[__init__.py]] - code - consumption/__init__.py
- [[__main__.py]] - code - consumption/__main__.py
- [[_env()]] - code - consumption/config.py
- [[_load_env_file (.env loader)]] - code - consumption/config.py
- [[config.py]] - code - consumption/config.py
- [[credentials_present]] - code - consumption/config.py
- [[mycitygrid Credentials]] - code - consumption/config.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Configuration_And_Entry_Point
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_HTTP API Endpoints]]
- 4 edges to [[_COMMUNITY_SQLite Storage And Aggregation]]
- 3 edges to [[_COMMUNITY_Mycitygrid Source Adapter]]
- 3 edges to [[_COMMUNITY_Launcher And Dependencies]]
- 2 edges to [[_COMMUNITY_Refresh Schedule]]
- 2 edges to [[_COMMUNITY_Self-Check Suite]]

## Top bridge nodes
- [[config.py]] - degree 9, connects to 4 communities
- [[__init__.py]] - degree 6, connects to 4 communities
- [[credentials_present]] - degree 4, connects to 2 communities
- [[SCHEMA script]] - degree 4, connects to 2 communities
- [[DB_PATH setting]] - degree 3, connects to 2 communities