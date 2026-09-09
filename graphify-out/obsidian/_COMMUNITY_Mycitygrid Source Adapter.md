---
type: community
cohesion: 0.10
members: 31
---

# Mycitygrid Source Adapter

**Cohesion:** 0.10 - loosely connected
**Members:** 31 nodes

## Members
- [[A logged-in session. Cookies live for the duration of the `with` block only.]] - rationale - consumption/source.py
- [[Adapter for www.mycitygrid.com - the only module that talks to the portal.…]] - rationale - consumption/source.py
- [[Authenticate `session` against config.MYCITYGRID_BASE_URL. To implement open…]] - rationale - consumption/source.py
- [[Fetching Not Implemented Status]] - document - README.md
- [[IMPERSONATE fingerprint]] - code - consumption/source.py
- [[Lazy Scrapling Import Lesson]] - document - .cursor/memory/INDEX.md
- [[MYCITYGRID_BASE_URL setting]] - code - consumption/config.py
- [[Pull hourly buckets for local dates start..end inclusive from a logged-in…]] - rationale - consumption/source.py
- [[Reading dataclass]] - code - consumption/source.py
- [[Return hourly consumption for local dates start..end inclusive. Re-fetching a…]] - rationale - consumption/source.py
- [[RuntimeError]] - code
- [[SOURCE_READY flag]] - code - consumption/source.py
- [[Scaffold Complete, Fetching Unimplemented]] - document - .cursor/memory/INDEX.md
- [[SourceError]] - code - consumption/source.py
- [[SourceError error]] - code - consumption/source.py
- [[SourceNotReady]] - code - consumption/source.py
- [[StealthySession Fallback Note]] - document - README.md
- [[The adapter is not implemented or not configured. Not a transient failure.]] - rationale - consumption/source.py
- [[The portal was reached but did not answer as expected. Retrying later may work.]] - rationale - consumption/source.py
- [[UNITS map]] - code - consumption/source.py
- [[UTILITIES tuple]] - code - consumption/config.py
- [[Undocumented mycitygrid Portal Lesson]] - document - .cursor/memory/INDEX.md
- [[_fetch_range (unimplemented)]] - code - consumption/source.py
- [[_login (unimplemented)]] - code - consumption/source.py
- [[date_3]] - code
- [[fetch_hourly]] - code - consumption/source.py
- [[mycitygrid.com Portal]] - document - README.md
- [[portal_session]] - code - consumption/source.py
- [[scraplingfetchers Extra Lesson]] - document - .cursor/memory/INDEX.md
- [[scraplingfetchers dependency]] - document - requirements.txt
- [[source.py]] - code - consumption/source.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Mycitygrid_Source_Adapter
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_Self-Check Suite]]
- 5 edges to [[_COMMUNITY_Refresh Schedule]]
- 3 edges to [[_COMMUNITY_Configuration And Entry Point]]
- 3 edges to [[_COMMUNITY_HTTP API Endpoints]]
- 2 edges to [[_COMMUNITY_SQLite Storage And Aggregation]]
- 1 edge to [[_COMMUNITY_Launcher And Dependencies]]

## Top bridge nodes
- [[source.py]] - degree 14, connects to 5 communities
- [[portal_session]] - degree 12, connects to 2 communities
- [[Reading dataclass]] - degree 9, connects to 2 communities
- [[UTILITIES tuple]] - degree 4, connects to 2 communities
- [[fetch_hourly]] - degree 11, connects to 1 community