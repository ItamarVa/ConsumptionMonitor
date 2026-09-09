---
source_file: "consumption/jobs.py"
type: "code"
community: "Refresh Schedule"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/Refresh_Schedule
---

# run_job

## Connections
- [[Connection_1]] - `references` [EXTRACTED]
- [[Fetch and store one job's range for every utility. Returns rows written.]] - `rationale_for` [EXTRACTED]
- [[Idempotent Refresh Jobs Convention]] - `implements` [INFERRED]
- [[JOBS schedule table]] - `references` [EXTRACTED]
- [[POST refresh{job}]] - `calls` [EXTRACTED]
- [[SourceNotReady error]] - `references` [EXTRACTED]
- [[UTILITIES tuple]] - `references` [EXTRACTED]
- [[date_2]] - `references` [EXTRACTED]
- [[fetch_hourly]] - `calls` [EXTRACTED]
- [[jobs.py]] - `contains` [EXTRACTED]
- [[local_today]] - `calls` [EXTRACTED]
- [[record_job]] - `calls` [EXTRACTED]
- [[run_due]] - `calls` [EXTRACTED]
- [[test_missing_source_is_recorded_not_raised]] - `calls` [EXTRACTED]
- [[test_missing_source_is_recorded_not_raised()]] - `calls` [EXTRACTED]
- [[upsert_readings]] - `calls` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/Refresh_Schedule