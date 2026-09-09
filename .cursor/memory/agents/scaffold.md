Task: Build the initial project scaffold for ConsumptionMonitor - a local API serving electricity and water consumption scraped from www.mycitygrid.com (no public API).
Status: active
Updated: 2026-09-09T13:50Z
Files: requirements.txt, .env.example, .gitignore, README.md, run.bat, scripts/launch.ps1, consumption/*.py, tests/test_aggregation.py, .cursor/memory/INDEX.md, .cursor/rules/*.mdc
Next step: Scaffold is complete and self-checks pass. When the user supplies mycitygrid credentials, implement `fetch_hourly` in `consumption/source.py` (currently raises NotImplementedError) and flip `SOURCE_READY`; nothing else should need to change.
