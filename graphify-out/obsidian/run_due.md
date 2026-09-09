---
source_file: "consumption/jobs.py"
type: "code"
community: "Refresh Schedule"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/Refresh_Schedule
---

# run_due

## Connections
- [[Run every job whose interval has elapsed. Safe to call as often as you like.]] - `rationale_for` [EXTRACTED]
- [[connect (SQLite connection)]] - `calls` [EXTRACTED]
- [[datetime_1]] - `references` [EXTRACTED]
- [[due (interval check)]] - `calls` [EXTRACTED]
- [[job_states]] - `calls` [EXTRACTED]
- [[jobs.py]] - `contains` [EXTRACTED]
- [[local_today]] - `calls` [EXTRACTED]
- [[loop (scheduler tick)]] - `indirect_call` [INFERRED]
- [[run_job]] - `calls` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/Refresh_Schedule