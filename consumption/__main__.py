"""Entry point: `python -m consumption` serves the API and runs the refresh scheduler."""

from __future__ import annotations

import sys

import uvicorn

from . import config


def main() -> None:
    # The project path may contain non-Latin characters, and a Windows console defaults
    # to cp1252, which cannot encode them - printing the DB path would crash on startup.
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")

    print(f"ConsumptionMonitor listening on http://{config.HOST}:{config.PORT}  (docs at /docs)")
    print(f"Database: {config.DB_PATH}", flush=True)
    uvicorn.run("consumption.api:app", host=config.HOST, port=config.PORT, log_level="info")


if __name__ == "__main__":
    main()
