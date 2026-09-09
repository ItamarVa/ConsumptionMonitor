"""Runtime configuration, read once at import from the environment and an optional .env file.

Credentials come from the encrypted store in secrets.py, with environment variables as a
fallback when nothing is stored. They surface only here, so no other module reads them
directly, and nothing in this file may be logged or returned by the API.
Depended on by: db.py (DB_PATH), jobs.py (LOCAL_TZ), api.py (HOST/PORT, credentials check).
"""

from __future__ import annotations

import os
from pathlib import Path
from zoneinfo import ZoneInfo

from . import secrets

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


def _credentials() -> tuple[str, str, str | None]:
    """Encrypted store first; the environment stays available as a manual override."""
    try:
        stored = secrets.load()
    except secrets.SecretsError as exc:
        # A damaged or foreign blob must not stop the API from serving stored history;
        # the reason travels to /health so the user is told to re-run setup.
        return "", "", str(exc)
    if stored:
        return stored[0], stored[1], None
    return (
        os.environ.get("MYCITYGRID_USERNAME", "").strip(),
        os.environ.get("MYCITYGRID_PASSWORD", ""),
        None,
    )


MYCITYGRID_USERNAME, MYCITYGRID_PASSWORD, CREDENTIALS_ERROR = _credentials()
MYCITYGRID_BASE_URL = _env("MYCITYGRID_BASE_URL", "https://www.mycitygrid.com")

DB_PATH = Path(_env("DB_PATH", str(ROOT / "data" / "consumption.sqlite")))

# The portal reports consumption in local wall-clock hours, so every UTC timestamp is
# converted with this zone. Requires the `tzdata` package on Windows.
LOCAL_TZ = ZoneInfo(_env("LOCAL_TZ", "Asia/Jerusalem"))

HOST = _env("HOST", "127.0.0.1")
PORT = int(_env("PORT", "8123"))

# Comma-separated Host header values accepted by TrustedHostMiddleware (port stripped).
ALLOWED_HOSTS = [h.strip() for h in _env("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if h.strip()]

# How often the scheduler loop wakes up to check whether any job is due.
TICK_SECONDS = int(_env("TICK_SECONDS", "300"))

UTILITIES = ("electricity", "water")


def credentials_present() -> bool:
    return bool(MYCITYGRID_USERNAME and MYCITYGRID_PASSWORD)
