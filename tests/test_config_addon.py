"""Config portability for the Home Assistant add-on (track A)."""

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from consumption import config, secrets  # noqa: E402


def test_credentials_skip_dpapi_off_windows() -> None:
    with (
        patch.object(os, "name", "posix"),
        patch.dict(
            os.environ,
            {"MYCITYGRID_USERNAME": "addon-user", "MYCITYGRID_PASSWORD": "addon-pass"},
            clear=False,
        ),
        patch.object(secrets, "load", side_effect=AssertionError("DPAPI must not run")),
    ):
        user, password, error = config._credentials()
    assert user == "addon-user"
    assert password == "addon-pass"
    assert error is None


def test_credentials_dpapi_error_on_windows() -> None:
    with (
        patch.object(os, "name", "nt"),
        patch.object(secrets, "load", side_effect=secrets.SecretsError("damaged blob")),
    ):
        user, password, error = config._credentials()
    assert user == ""
    assert password == ""
    assert error == "damaged blob"


def test_ha_bridge_env_vars() -> None:
    with patch.dict(
        os.environ,
        {
            "HA_BRIDGE": "1",
            "SUPERVISOR_TOKEN": "tok123",
            "ADDON_VERSION": "1.0.0",
        },
        clear=False,
    ):
        importlib.reload(config)
    assert config.HA_BRIDGE is True
    assert config.SUPERVISOR_TOKEN == "tok123"
    assert config.ADDON_VERSION == "1.0.0"
    importlib.reload(config)


def test_allowed_client_ips_parsed() -> None:
    with patch.dict(os.environ, {"ALLOWED_CLIENT_IPS": "172.30.32.2, 10.0.0.1"}, clear=False):
        importlib.reload(config)
    assert config.ALLOWED_CLIENT_IPS == ["172.30.32.2", "10.0.0.1"]
    importlib.reload(config)


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
        print(f"  ok  {test.__name__}")
    print(f"{len(tests)} config add-on checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
