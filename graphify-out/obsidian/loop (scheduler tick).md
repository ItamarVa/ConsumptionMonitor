---
source_file: "consumption/jobs.py"
type: "code"
community: "Scheduler Loop"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/Scheduler_Loop
---

# loop (scheduler tick)

## Connections
- [[TICK_SECONDS setting]] - `references` [EXTRACTED]
- [[Tick forever, delegating the blocking fetch and SQLite work to a worker thread.]] - `rationale_for` [EXTRACTED]
- [[jobs.py]] - `contains` [EXTRACTED]
- [[lifespan (startupshutdown)]] - `calls` [EXTRACTED]
- [[run_due]] - `indirect_call` [INFERRED]

#graphify/code #graphify/EXTRACTED #community/Scheduler_Loop