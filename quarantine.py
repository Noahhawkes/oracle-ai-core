"""quarantine.py

Boundary engine for the Oracle.AI / Miracle Drive quarantine layer.

Core invariant:
    quarantine.py may create quarantined records only.

This module captures raw text into a local encrypted JSON staging file,
stamps it with witness-grade metadata, and prevents automatic promotion.

It intentionally contains no Miracle Drive API write path.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import keyring  # type: ignore
except ImportError:  # pragma: no cover
    keyring = None

try:
    from cryptography.fernet import Fernet, InvalidToken
except ImportError as exc:  # pragma: no cover
    raise RuntimeError(
        "Missing dependency: cryptography. Install with `pip install cryptography`."
    ) from exc


SERVICE_NAME = "oracle-ai-core-quarantine"
KEY_NAME = "local-fernet-key"
DEFAULT_QUARANTINE_DIR = Path.home() / "Quarantine" / "clipboard"
ENCRYPTED_STORE_NAME = "quarantine.enc.json"
AUDIT_LOG_NAME = "quarantine.audit.jsonl"
SCHEMA_VERSION = "0.1.0"
APP_VERSION = "0.1.0"

ALLOWED_SOURCES = {
    "clipboard",
    "manual_text",
    "voice_transcript",
    "test",
}

QUARANTINED_STATUS = "quarantined"
TOMBSTONED_STATUS = "tombstoned"


@dataclass
class QuarantineRecord:
    id: str
    source: str
    captured_at: str
    content_type: str
    content_hash_sha256: str
    content_length_chars: int
    content_size_bytes: int
    status: str
    promotion_eligible: bool
    reviewed_by: Optional[str]
    reviewed_at: Optional[str]
    promoted_to: Optional[str]
    raw_content: Optional[str]
    schema_version: str = SCHEMA_VERSION
    app_version: str = APP_VERSION


class QuarantineError(RuntimeError):
    """Raised when quarantine operations fail."""


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _get_quarantine_dir(quarantine_dir: Optional[Path | str] = None) -> Path:
    if quarantine_dir is None:
        return DEFAULT_QUARANTINE_DIR
    return Path(quarantine_dir).expanduser().resolve()


def _store_path(quarantine_dir: Optional[Path | str] = None) -> Path:
    return _get_quarantine_dir(quarantine_dir) / ENCRYPTED_STORE_NAME


def _audit_path(quarantine_dir: Optional[Path | str] = None) -> Path:
    return _get_quarantine_dir(quarantine_dir) / AUDIT_LOG_NAME


def _ensure_dir(quarantine_dir: Optional[Path | str] = None) -> Path:
    qdir = _get_quarantine_dir(quarantine_dir)
    qdir.mkdir(parents=True, exist_ok=True)
    return qdir


def _generate_key() -> bytes:
    return Fernet.generate_key()


def _load_or_create_key() -> bytes:
    """Load encryption key from OS keyring, creating it if missing.

    Fallback to an environment variable for headless/dev environments:
    ORACLE_AI_CORE_QUARANTINE_KEY

    The key is never written to the repository.
    """
    env_key = os.getenv("ORACLE_AI_CORE_QUARANTINE_KEY")
    if env_key:
        return env_key.encode("utf-8")

    if keyring is None:
        raise QuarantineError(
            "OS keyring is unavailable and ORACLE_AI_CORE_QUARANTINE_KEY is not set."
        )

    existing = keyring.get_password(SERVICE_NAME, KEY_NAME)
    if existing:
        return existing.encode("utf-8")

    key = _generate_key()
    keyring.set_password(SERVICE_NAME, KEY_NAME, key.decode("utf-8"))
    return key


def _fernet() -> Fernet:
    return Fernet(_load_or_create_key())


def _encrypt_records(records: List[Dict[str, Any]]) -> bytes:
    payload = json.dumps(records, indent=2, sort_keys=True).encode("utf-8")
    return _fernet().encrypt(payload)


def _decrypt_records(encrypted_payload: bytes) -> List[Dict[str, Any]]:
    try:
        decrypted = _fernet().decrypt(encrypted_payload)
    except InvalidToken as exc:
        raise QuarantineError("Unable to decrypt quarantine store with available key.") from exc

    if not decrypted:
        return []

    data = json.loads(decrypted.decode("utf-8"))
    if not isinstance(data, list):
        raise QuarantineError("Quarantine store is malformed. Expected a list of records.")
    return data


def _read_records(quarantine_dir: Optional[Path | str] = None) -> List[Dict[str, Any]]:
    path = _store_path(quarantine_dir)
    if not path.exists():
        return []
    return _decrypt_records(path.read_bytes())


def _write_records(records: List[Dict[str, Any]], quarantine_dir: Optional[Path | str] = None) -> None:
    _ensure_dir(quarantine_dir)
    _store_path(quarantine_dir).write_bytes(_encrypt_records(records))


def _hash_content(raw_content: str) -> str:
    return hashlib.sha256(raw_content.encode("utf-8")).hexdigest()


def _audit_hash(event: Dict[str, Any]) -> str:
    safe_event = {k: v for k, v in event.items() if k != "integrity_hash_sha256"}
    canonical = json.dumps(safe_event, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _append_audit_event(event: Dict[str, Any], quarantine_dir: Optional[Path | str] = None) -> None:
    _ensure_dir(quarantine_dir)
    event["integrity_hash_sha256"] = _audit_hash(event)
    with _audit_path(quarantine_dir).open("a", encoding="utf-8") as audit_file:
        audit_file.write(json.dumps(event, sort_keys=True) + "\n")


def _audit_event(
    *,
    record_id: str,
    event_type: str,
    source_type: str,
    capture_vector: str,
    content_type: str,
    content_length_chars: int,
    content_size_bytes: int,
    content_hash_sha256: str,
    status_before: Optional[str],
    status_after: str,
    promotion_eligible: bool,
    actor_type: str = "system",
    actor_id: str = "local_user",
) -> Dict[str, Any]:
    return {
        "audit_event_id": f"audit_{uuid.uuid4().hex}",
        "record_id": record_id,
        "event_type": event_type,
        "event_timestamp": _utc_now_iso(),
        "source_type": source_type,
        "capture_vector": capture_vector,
        "device_label": os.uname().nodename if hasattr(os, "uname") else "local_device",
        "content_type": content_type,
        "content_length_chars": content_length_chars,
        "content_size_bytes": content_size_bytes,
        "content_hash_sha256": content_hash_sha256,
        "encrypted_payload_path": str(_store_path()),
        "status_before": status_before,
        "status_after": status_after,
        "promotion_eligible": promotion_eligible,
        "actor_type": actor_type,
        "actor_id": actor_id,
        "module": "quarantine.py",
        "schema_version": SCHEMA_VERSION,
        "app_version": APP_VERSION,
    }


def quarantine_capture(
    raw_content: str,
    source: str,
    *,
    quarantine_dir: Optional[Path | str] = None,
    content_type: str = "text/plain",
) -> Dict[str, Any]:
    """Capture raw content into quarantine and return metadata.

    This function stores the raw content exactly as received.
    It does not validate, summarize, rewrite, promote, or classify truth.
    """
    if not isinstance(raw_content, str):
        raise TypeError("raw_content must be a string")

    if source not in ALLOWED_SOURCES:
        raise ValueError(f"source must be one of: {sorted(ALLOWED_SOURCES)}")

    content_bytes = raw_content.encode("utf-8")
    record = QuarantineRecord(
        id=f"clip_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}",
        source=source,
        captured_at=_utc_now_iso(),
        content_type=content_type,
        content_hash_sha256=_hash_content(raw_content),
        content_length_chars=len(raw_content),
        content_size_bytes=len(content_bytes),
        status=QUARANTINED_STATUS,
        promotion_eligible=False,
        reviewed_by=None,
        reviewed_at=None,
        promoted_to=None,
        raw_content=raw_content,
    )

    records = _read_records(quarantine_dir)
    record_dict = asdict(record)
    records.append(record_dict)
    _write_records(records, quarantine_dir)

    _append_audit_event(
        _audit_event(
            record_id=record.id,
            event_type="capture_created",
            source_type=source,
            capture_vector=source,
            content_type=content_type,
            content_length_chars=record.content_length_chars,
            content_size_bytes=record.content_size_bytes,
            content_hash_sha256=record.content_hash_sha256,
            status_before=None,
            status_after=QUARANTINED_STATUS,
            promotion_eligible=False,
        ),
        quarantine_dir,
    )

    return record_dict


def load_quarantine(*, quarantine_dir: Optional[Path | str] = None) -> List[Dict[str, Any]]:
    """Load quarantined records from the encrypted staging file."""
    return _read_records(quarantine_dir)


def tombstone_record(record_id: str, *, quarantine_dir: Optional[Path | str] = None) -> Dict[str, Any]:
    """Reject a quarantined record and remove sensitive raw content.

    Metadata is preserved. raw_content is destroyed.
    """
    records = _read_records(quarantine_dir)
    for record in records:
        if record.get("id") == record_id:
            status_before = record.get("status")
            record["status"] = TOMBSTONED_STATUS
            record["promotion_eligible"] = False
            record["raw_content"] = None
            record["reviewed_at"] = _utc_now_iso()

            _write_records(records, quarantine_dir)

            _append_audit_event(
                _audit_event(
                    record_id=record_id,
                    event_type="record_tombstoned",
                    source_type=record.get("source", "unknown"),
                    capture_vector=record.get("source", "unknown"),
                    content_type=record.get("content_type", "unknown"),
                    content_length_chars=record.get("content_length_chars", 0),
                    content_size_bytes=record.get("content_size_bytes", 0),
                    content_hash_sha256=record.get("content_hash_sha256", "unknown"),
                    status_before=status_before,
                    status_after=TOMBSTONED_STATUS,
                    promotion_eligible=False,
                ),
                quarantine_dir,
            )

            return record

    raise QuarantineError(f"Record not found: {record_id}")


if __name__ == "__main__":
    sample = quarantine_capture("Captured. No action taken.", "test")
    print(json.dumps({k: v for k, v in sample.items() if k != "raw_content"}, indent=2))
