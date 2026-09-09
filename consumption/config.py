"""Runtime configuration, read once at import from the environment and an optional .env file.

Credentials live only here so no other module reads os.environ directly. Nothing in this
file may be logged or returned by the API - `MYCITYGRID_PASSWORD` is a secret.
Depended on by: db.py (DB_PATH), jobs.py (LOCAL_TZ, credentials check), api.py (HOST/PORT).
"""

from __future__ import annotations

import os
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env"


def _load_env_file(path: Path) -> None:
    """Populate os.environ from a KEY=VALUE file. Real environment variables always win."""
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


_load_env_file(ENV_FILE)


def _env(key: str, default: str) -> str:
    value = os.environ.get(key, "").strip()
    return value or default


MYCITYGRID_USERNAME = os.environ.get("MYCITYGRID_USERNAME", "").strip()
MYCITYGRID_PASSWORD = os.environ.get("MYCITYGRID_PASSWORD", "")
MYCITYGRID_BASE_URL = _env("MYCITYGRID_BASE_URL", "https://www.mycitygrid.com")

DB_PATH = Path(_env("DB_PATH", str(ROOT / "data" / "consumption.sqlite")))

# The portal reports consumption in local wall-clock hours, so every UTC timestamp is
# converted with this zone. Requires the `tzdata` package on Windows.
LOCAL_TZ = ZoneInfo(_env("LOCAL_TZ", "Asia/Jerusalem"))

HOST = _env("HOST", "127.0.0.1")
PORT = int(_env("PORT", "8123"))

# How often the scheduler loop wakes up to check whether any job is due.
TICK_SECONDS = int(_env("TICK_SECONDS", "300"))

UTILITIES = ("electricity", "water")


def credentials_present() -> bool:
    return bool(MYCITYGRID_USERNAME and MYCITYGRID_PASSWORD)
