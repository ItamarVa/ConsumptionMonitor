---
source_file: "consumption/jobs.py"
type: "code"
community: "Refresh Schedule"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/Refresh_Schedule
---

# _last_full_week range

## Connections
- [[GET summary]] - `calls` [EXTRACTED]
- [[JOBS schedule table]] - `references` [EXTRACTED]
- [[_DAYS_SINCE_SUNDAY helper]] - `calls` [EXTRACTED]
- [[date_2]] - `references` [EXTRACTED]
- [[jobs.py]] - `indirect_call` [INFERRED]
- [[test_job_ranges]] - `calls` [EXTRACTED]
- [[timedelta]] - `calls` [INFERRED]

#graphify/code #graphify/EXTRACTED #community/Refresh_Schedule