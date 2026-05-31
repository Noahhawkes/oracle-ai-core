"""mac_clipboard_watcher.py

Minimum viable Mac clipboard interface for the Oracle.AI quarantine layer.

Behavior:
    Copy text -> watcher detects clipboard change -> quarantine.py captures it

This is intentionally not a full menu bar app yet. It is the first working
bridge between real clipboard behavior and the quarantine boundary engine.

Core invariant:
    The watcher may capture.
    The watcher may not promote.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

from quarantine import quarantine_capture, QuarantineError


DEFAULT_POLL_SECONDS = 1.0
DEFAULT_SOURCE = "clipboard"


def read_macos_clipboard() -> str:
    """Read the macOS clipboard using pbpaste.

    pbpaste is available by default on macOS and avoids requiring an early GUI
    dependency for the first prototype.
    """
    try:
        result = subprocess.run(
            ["pbpaste"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("pbpaste not found. This prototype currently requires macOS.") from exc

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Unable to read macOS clipboard.")

    return result.stdout


def content_fingerprint(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def should_capture(content: str, last_hash: Optional[str]) -> bool:
    if not content:
        return False

    current_hash = content_fingerprint(content)
    return current_hash != last_hash


def watch_clipboard(
    *,
    poll_seconds: float = DEFAULT_POLL_SECONDS,
    quarantine_dir: Optional[Path] = None,
    once: bool = False,
) -> None:
    """Watch clipboard changes and route new text into quarantine."""
    last_hash: Optional[str] = None

    print("Clipboard watcher running.")
    print("Copy text to capture it into quarantine.")
    print("Press Ctrl+C to stop.")

    while True:
        content = read_macos_clipboard()
        current_hash = content_fingerprint(content) if content else None

        if content and should_capture(content, last_hash):
            try:
                record = quarantine_capture(
                    content,
                    DEFAULT_SOURCE,
                    quarantine_dir=quarantine_dir,
                    content_type="text/plain",
                )
            except QuarantineError as exc:
                print(f"Quarantine error: {exc}", file=sys.stderr)
            else:
                safe_preview = {
                    "id": record["id"],
                    "source": record["source"],
                    "captured_at": record["captured_at"],
                    "content_hash_sha256": record["content_hash_sha256"],
                    "content_length_chars": record["content_length_chars"],
                    "status": record["status"],
                    "promotion_eligible": record["promotion_eligible"],
                }
                print(json.dumps(safe_preview, indent=2))
                print("Captured. No action taken.")

            last_hash = current_hash

            if once:
                return

        if once:
            print("No new clipboard text captured.")
            return

        time.sleep(poll_seconds)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Watch the macOS clipboard and send new text to quarantine."
    )
    parser.add_argument(
        "--poll-seconds",
        type=float,
        default=DEFAULT_POLL_SECONDS,
        help="Clipboard polling interval in seconds.",
    )
    parser.add_argument(
        "--quarantine-dir",
        type=Path,
        default=None,
        help="Optional quarantine directory override for testing or local routing.",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Capture the current clipboard once and exit.",
    )

    args = parser.parse_args()

    try:
        watch_clipboard(
            poll_seconds=args.poll_seconds,
            quarantine_dir=args.quarantine_dir,
            once=args.once,
        )
    except KeyboardInterrupt:
        print("\nClipboard watcher stopped.")


if __name__ == "__main__":
    main()
