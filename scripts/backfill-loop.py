"""Run backfill jobs until BACKFILL_DONE or no progress. Logs to data/backfill.log.

Invoked by Wave 3 verification or manually: python scripts/backfill-loop.py [--max N]
Respects source.REQUEST_DELAY_SECONDS between portal pages. Safe to stop and resume.
"""

from __future__ import annotations

import argparse
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from consumption import db, jobs  # noqa: E402
from consumption.jobs import BACKFILL_DONE, BACKFILL_KEY  # noqa: E402

LOG_PATH = ROOT / "data" / "backfill.log"


def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Run backfill until done or max iterations.")
    parser.add_argument(
        "--max",
        type=int,
        default=0,
        help="Stop after N successful months (0 = until BACKFILL_DONE)",
    )
    args = parser.parse_args()

    conn = db.connect()
    try:
        progress = db.get_state(conn, BACKFILL_KEY)
        if progress == BACKFILL_DONE:
            log(f"already {BACKFILL_DONE}; coverage={db.coverage(conn)}")
            return 0

        log(f"loop start progress={progress!r} coverage={db.coverage(conn)}")
        ran = 0
        while True:
            progress = db.get_state(conn, BACKFILL_KEY)
            if progress == BACKFILL_DONE:
                log(f"finished {BACKFILL_DONE}; coverage={db.coverage(conn)}")
                break
            before = db.coverage(conn)
            try:
                written = jobs.run_job(conn, "backfill")
            except Exception as exc:  # noqa: BLE001
                log(f"ERROR {type(exc).__name__}: {exc}\n{traceback.format_exc(limit=2)}")
                return 1
            after = db.coverage(conn)
            progress = db.get_state(conn, BACKFILL_KEY)
            log(
                f"month rows={written} progress={progress!r} "
                f"elec={after['electricity']} water={after['water']}"
            )
            if written == 0 and after == before:
                log("no progress; stopping")
                break
            ran += 1
            if args.max and ran >= args.max:
                log(f"reached --max {args.max}; resume with run.bat or this script")
                break
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
