"""Interactive first-time setup: ask for the portal credentials and store them encrypted.

Started by set-credentials.bat. It lives outside the package because it is an operator
tool, not part of the API; consumption/secrets.py does the encryption and stays the only
module that touches the blob. The password is read with getpass, so it is never echoed to
the console, never printed back and never written anywhere except the encrypted file.
"""

from __future__ import annotations

import getpass
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from consumption import secrets  # noqa: E402


def main() -> int:
    # The project path may contain non-Latin characters that a cp1252 console cannot print.
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")

    print("ConsumptionMonitor - mycitygrid credentials")
    print("They are encrypted for this Windows user on this PC and are never shown again.")
    print()
    username = input("Username: ").strip()
    password = getpass.getpass("Password (nothing appears while you type): ")
    if not username or not password:
        print("\nNothing was saved: both the username and the password are required.")
        return 1

    try:
        secrets.save(username, password)
    except secrets.SecretsError as exc:
        print(f"\nNothing was saved. {exc}")
        return 1

    print(f"\nSaved for {username}. The password is encrypted and was not displayed.")
    print(f"Stored at: {secrets.CREDENTIALS_FILE}")
    print("You can now start the API by double-clicking run.bat.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
