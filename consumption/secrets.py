"""Encrypted local storage for the portal credentials - the only module that touches the blob.

Encryption is the Windows Data Protection API (CryptProtectData / CryptUnprotectData in
crypt32.dll) reached through ctypes, so there is no dependency and no master password:
the ciphertext is decryptable only by the same Windows user on the same machine, which is
exactly the "enter it once per machine at setup" model the user asked for.
Invariant: nothing here is ever logged, printed or returned by the API. Must not import
config - config imports this. Depended on by: config.py, scripts/set_credentials.py.
"""

from __future__ import annotations

import ctypes
import json
import os
from pathlib import Path

# ponytail: Windows only. Ceiling: DPAPI ties the blob to one Windows user on one machine,
# so this project cannot move to Linux or be copied to a second PC without re-entering the
# credentials. Upgrade path: the `keyring` package, which fronts DPAPI, macOS Keychain and
# Secret Service with one API - only _protect/_unprotect below would change.
CREDENTIALS_FILE = Path(__file__).resolve().parent.parent / "data" / "credentials.dpapi"

# Application-specific entropy, passed to both calls. Without it any DPAPI blob this
# Windows user can decrypt - including one written by another program - would be accepted.
_ENTROPY = b"ConsumptionMonitor:mycitygrid:v1"

_RESET_HINT = "Double-click set-credentials.bat to enter your credentials again."

_CRYPTPROTECT_UI_FORBIDDEN = 0x1


class SecretsError(RuntimeError):
    """The credential store could not be read or written. Never carries a Windows code."""


class _Blob(ctypes.Structure):
    """The DATA_BLOB struct DPAPI passes in both directions. DWORD is an unsigned 32-bit."""

    _fields_ = [("cbData", ctypes.c_uint32), ("pbData", ctypes.POINTER(ctypes.c_char))]


def _crypt32():
    if os.name != "nt":
        raise SecretsError("Encrypted credential storage needs Windows.")
    return ctypes.WinDLL("crypt32.dll")


def _input_blob(data: bytes) -> tuple[_Blob, ctypes.Array]:
    """Returns the blob and its buffer - the caller must hold the buffer during the call."""
    buf = ctypes.create_string_buffer(data, len(data))
    return _Blob(len(data), ctypes.cast(buf, ctypes.POINTER(ctypes.c_char))), buf


def _dpapi(func_name: str, data: bytes, failure: str) -> bytes:
    crypt32 = _crypt32()
    func = getattr(crypt32, func_name)
    func.restype = ctypes.c_int
    func.argtypes = [
        ctypes.POINTER(_Blob),  # data in
        ctypes.c_void_p,  # description, unused in both directions
        ctypes.POINTER(_Blob),  # entropy
        ctypes.c_void_p,  # reserved
        ctypes.c_void_p,  # prompt struct
        ctypes.c_uint32,  # flags
        ctypes.POINTER(_Blob),  # data out
    ]

    payload, payload_buf = _input_blob(data)
    entropy, entropy_buf = _input_blob(_ENTROPY)
    out = _Blob()
    ok = func(
        ctypes.byref(payload),
        None,
        ctypes.byref(entropy),
        None,
        None,
        _CRYPTPROTECT_UI_FORBIDDEN,
        ctypes.byref(out),
    )
    del payload_buf, entropy_buf  # only held so Python could not free them mid-call
    if not ok:
        # The Windows error code says nothing a non-technical user can act on.
        raise SecretsError(f"{failure} {_RESET_HINT}")
    try:
        return ctypes.string_at(out.pbData, out.cbData)
    finally:
        ctypes.WinDLL("kernel32.dll").LocalFree(out.pbData)


def save(username: str, password: str, path: Path | None = None) -> None:
    """Encrypt and store the credentials, replacing anything already stored."""
    target = path or CREDENTIALS_FILE
    payload = json.dumps({"username": username, "password": password}).encode("utf-8")
    blob = _dpapi("CryptProtectData", payload, "Windows could not encrypt the credentials.")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(blob)


def load(path: Path | None = None) -> tuple[str, str] | None:
    """Return (username, password), or None when nothing has been stored yet."""
    target = path or CREDENTIALS_FILE
    if not target.is_file():
        return None
    decrypted = _dpapi(
        "CryptUnprotectData",
        target.read_bytes(),
        "The stored credentials cannot be read on this Windows account.",
    )
    try:
        payload = json.loads(decrypted.decode("utf-8"))
        return str(payload["username"]), str(payload["password"])
    except (ValueError, KeyError, TypeError) as exc:
        raise SecretsError(f"The stored credentials are damaged. {_RESET_HINT}") from exc


def clear(path: Path | None = None) -> None:
    (path or CREDENTIALS_FILE).unlink(missing_ok=True)
