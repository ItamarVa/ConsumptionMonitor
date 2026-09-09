---
source_file: "consumption/jobs.py"
type: "rationale"
community: "Scheduler Loop"
location: "L89"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/Scheduler_Loop
---

# Tick forever, delegating the blocking fetch and SQLite work to a worker thread.

## Connections
- [[loop (scheduler tick)]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/Scheduler_Loop