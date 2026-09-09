Task: Get real consumption numbers out of the mycitygrid portal and start collecting history.
Status: blocked
Updated: 2026-09-09T18:30Z
Files: consumption/readings.py, consumption/source.py, scripts/connection_report.py, run.bat, set-credentials.bat, test-connection.bat, scripts/*.ps1
Waiting for: the user. They asked to stop all work on 2026-09-09 and will say when to resume.

What is already proven, on 2026-09-09 against the live portal:
- Login works. The reverse-engineered OAuth password grant is correct.
- `user/info` returns both meters: electricity meterId 30400 (multiplier 0.01), water meterId 30399.
- `meterdata/consumption?period=hourly` returns the hypothesised ngx-charts shape and the parser reads it.
- Full evidence in the git-ignored `data/connection-report.txt` (contains the household address and
  coordinates - do not commit it, do not paste it anywhere).

Two open problems, in priority order:

1. Every value came back 0.0 for local day 2026-09-08, on both meters, 24 buckets each. The portal
   returned the zeros, so this is not a parsing bug. Unknown whether that day simply has no data, whether
   hourly data lags, or whether the request needs a different range. Try several older days before
   concluding anything.
2. The `series` array carries four entries per bucket - "Import Consumption 2026" and
   "Export Consumption 2026", each appearing twice. Confirm how `consumption/readings.py` treats them.
   Summing all four would double-count, and export is generation, not consumption. The all-zero sample
   made this impossible to verify.

Known but deliberately unfixed: the `.bat` safety net is broken. `if errorlevel 1 pause` misses negative
exit codes (`powershell -File` returns -196608 when it rejects the script file) and misses failures that
exit 0, so a launcher can still close without a message. Proven, not yet fixed.

Next step: do nothing until the user asks. When they do, start with problem 1 above - fetch several past
days through `consumption/source.py` and find one that returns non-zero values, then resolve problem 2.
