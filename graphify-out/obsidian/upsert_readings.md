---
source_file: "consumption/db.py"
type: "code"
community: "Self-Check Suite"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/Self-Check_Suite
---

# upsert_readings

## Connections
- [[Connection]] - `references` [EXTRACTED]
- [[LOCAL_TZ setting]] - `references` [EXTRACTED]
- [[One Row Per Utility, Meter, Hour]] - `implements` [INFERRED]
- [[Reading dataclass]] - `shares_data_with` [EXTRACTED]
- [[_utc_now()]] - `calls` [EXTRACTED]
- [[db.py]] - `contains` [EXTRACTED]
- [[reading table]] - `shares_data_with` [EXTRACTED]
- [[run_job]] - `calls` [EXTRACTED]
- [[test_local_day_mapping]] - `calls` [EXTRACTED]
- [[test_local_day_mapping()]] - `calls` [EXTRACTED]
- [[test_naive_timestamp_rejected]] - `calls` [EXTRACTED]
- [[test_naive_timestamp_rejected()]] - `calls` [EXTRACTED]
- [[test_refetch_overwrites_and_daily_sums]] - `calls` [EXTRACTED]
- [[test_refetch_overwrites_and_daily_sums()]] - `calls` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/Self-Check_Suite