"""instant_capture.py

Experimental near-instant capture queue for Oracle.AI quarantine.

Goal:
    Make capture feel instant by splitting the act of noticing a signal from the
    heavier act of encryption, audit logging, and compilation.

This does not literally achieve 0.05 ms end-to-end persistence. That is not a
realistic guarantee for clipboard polling, disk I/O, encryption, and audit logs.
Instead, it invents a practical architecture for perceived-instant capture:

    Clipboard change -> memory queue acknowledgement -> background quarantine write

Core invariants:
    - Capture should feel instant.
    - Promotion should feel intentional.
    - Compilation should feel invisible.
    - Queueing is not promotion.
    - Background persistence may quarantine only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import queue
import subprocess
import sys
import threading
import time
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from quarantine import quarantine_capture, QuarantineError


DEFAULT_POLL_SECONDS = 0.05
DEFAULT_SOURCE = "clipboard"
QUEUE_ACK_TARGET_SECONDS = 0.001


@dataclass
class CaptureEnvelope:
    queue_id: str
    source: str
    received_at: str
    content_hash_sha256: str
    content_length_chars: int
    raw_content: str


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_macos_clipboard() -> str:
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


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def build_envelope(raw_content: str, source: str = DEFAULT_SOURCE) -> CaptureEnvelope:
    return CaptureEnvelope(
        queue_id=f"queue_{uuid.uuid4().hex}",
        source=source,
        received_at=utc_now_iso(),
        content_hash_sha256=sha256_text(raw_content),
        content_length_chars=len(raw_content),
        raw_content=raw_content,
    )


class InstantCaptureQueue:
    """Memory-first capture queue with background quarantine persistence."""

    def __init__(self, *, quarantine_dir: Optional[Path] = None) -> None:
        self.quarantine_dir = quarantine_dir
        self._queue: queue.Queue[CaptureEnvelope] = queue.Queue()
        self._stop_event = threading.Event()
        self._worker = threading.Thread(target=self._persist_loop, daemon=True)
        self._started = False

    def start(self) -> None:
        if not self._started:
            self._worker.start()
            self._started = True

    def stop(self) -> None:
        self._stop_event.set()
        self._worker.join(timeout=5)

    def capture_now(self, raw_content: str, source: str = DEFAULT_SOURCE) -> dict:
        """Acknowledge capture into memory immediately.

        This returns before encryption and disk persistence complete.
        """
        if not raw_content:
            raise ValueError("raw_content cannot be empty")

        envelope = build_envelope(raw_content, source)
        start = time.perf_counter()
        self._queue.put(envelope)
        elapsed = time.perf_counter() - start

        return {
            "queue_id": envelope.queue_id,
            "received_at": envelope.received_at,
            "content_hash_sha256": envelope.content_hash_sha256,
            "content_length_chars": envelope.content_length_chars,
            "queued": True,
            "queue_ack_seconds": elapsed,
            "status": "queued_for_quarantine",
            "promotion_eligible": False,
        }

    def _persist_loop(self) -> None:
        while not self._stop_event.is_set():
            try:
                envelope = self._queue.get(timeout=0.1)
            except queue.Empty:
                continue

            try:
                record = quarantine_capture(
                    envelope.raw_content,
                    envelope.source,
                    quarantine_dir=self.quarantine_dir,
                    content_type="text/plain",
                )
            except QuarantineError as exc:
                print(f"Quarantine persistence failed for {envelope.queue_id}: {exc}", file=sys.stderr)
            else:
                safe_event = {
                    "queue_id": envelope.queue_id,
                    "record_id": record["id"],
                    "status": record["status"],
                    "promotion_eligible": record["promotion_eligible"],
                    "content_hash_sha256": record["content_hash_sha256"],
                }
                print(json.dumps(safe_event, sort_keys=True))
            finally:
                self._queue.task_done()


def watch_instant_clipboard(
    *,
    poll_seconds: float = DEFAULT_POLL_SECONDS,
    quarantine_dir: Optional[Path] = None,
) -> None:
    capture_queue = InstantCaptureQueue(quarantine_dir=quarantine_dir)
    capture_queue.start()
    last_hash: Optional[str] = None

    print("Instant clipboard capture running.")
    print("Copy text to queue it immediately, then persist to quarantine in the background.")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            content = read_macos_clipboard()
            current_hash = sha256_text(content) if content else None

            if content and current_hash != last_hash:
                ack = capture_queue.capture_now(content, DEFAULT_SOURCE)
                print(json.dumps(ack, sort_keys=True))
                print("Captured into queue. No action taken.")
                last_hash = current_hash

            time.sleep(poll_seconds)
    except KeyboardInterrupt:
        print("\nStopping instant capture queue.")
    finally:
        capture_queue.stop()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Near-instant macOS clipboard capture using an in-memory queue and background quarantine persistence."
    )
    parser.add_argument(
        "--poll-seconds",
        type=float,
        default=DEFAULT_POLL_SECONDS,
        help="Clipboard polling interval in seconds. Default is 0.05 seconds.",
    )
    parser.add_argument(
        "--quarantine-dir",
        type=Path,
        default=None,
        help="Optional quarantine directory override.",
    )

    args = parser.parse_args()
    watch_instant_clipboard(
        poll_seconds=args.poll_seconds,
        quarantine_dir=args.quarantine_dir,
    )


if __name__ == "__main__":
    main()
