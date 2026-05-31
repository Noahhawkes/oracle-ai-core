"""derivative_metadata_ledger.py

Derivative Metadata Ledger (DML) for Oracle.AI / RECURSIONSTACK.

Purpose:
    Store generated metadata as testimony that points to raw evidence,
    without mutating the raw quarantine record.

Core invariant:
    Raw signal is evidence.
    Generated metadata is testimony.
    They must not be stored as the same thing.

This module creates derivative records only. It does not modify quarantine.enc.json,
promote records, or write canonical memory.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


DEFAULT_DML_DIR = Path.home() / "Quarantine" / "metadata"
DML_FILE_NAME = "derivative_metadata.jsonl"
DML_AUDIT_FILE_NAME = "derivative_metadata.audit.jsonl"
SCHEMA_VERSION = "0.1.0"
APP_VERSION = "0.1.0"

DERIVATIVE_STATUS = "quarantined_derivative"
ALLOWED_METADATA_TYPES = {
    "classification",
    "tag",
    "priority_signal",
    "summary_candidate",
    "risk_flag",
    "possible_task",
    "possible_memory",
    "possible_business_signal",
    "note",
}


@dataclass
class DerivativeMetadataRecord:
    metadata_id: str
    source_record_id: str
    source_hash_sha256: str
    generated_at: str
    generator: str
    metadata_type: str
    value: str
    confidence: str
    status: str
    promotion_eligible: bool
    schema_version: str = SCHEMA_VERSION
    app_version: str = APP_VERSION


class DerivativeMetadataError(RuntimeError):
    """Raised when DML operations fail."""


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _get_dml_dir(dml_dir: Optional[Path | str] = None) -> Path:
    if dml_dir is None:
        return DEFAULT_DML_DIR
    return Path(dml_dir).expanduser().resolve()


def _ledger_path(dml_dir: Optional[Path | str] = None) -> Path:
    return _get_dml_dir(dml_dir) / DML_FILE_NAME


def _audit_path(dml_dir: Optional[Path | str] = None) -> Path:
    return _get_dml_dir(dml_dir) / DML_AUDIT_FILE_NAME


def _ensure_dir(dml_dir: Optional[Path | str] = None) -> Path:
    directory = _get_dml_dir(dml_dir)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def _hash_event(event: Dict[str, Any]) -> str:
    canonical = json.dumps(event, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _append_jsonl(path: Path, payload: Dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def _append_audit_event(event: Dict[str, Any], dml_dir: Optional[Path | str] = None) -> None:
    _ensure_dir(dml_dir)
    event = dict(event)
    event["integrity_hash_sha256"] = _hash_event(event)
    _append_jsonl(_audit_path(dml_dir), event)


def create_derivative_metadata(
    *,
    source_record_id: str,
    source_hash_sha256: str,
    generator: str,
    metadata_type: str,
    value: str,
    confidence: str = "unknown",
    dml_dir: Optional[Path | str] = None,
) -> Dict[str, Any]:
    """Create a quarantined derivative metadata record.

    The source quarantine record is referenced by ID and hash only.
    This function never mutates the source record.
    """
    if not source_record_id:
        raise ValueError("source_record_id is required")
    if not source_hash_sha256:
        raise ValueError("source_hash_sha256 is required")
    if metadata_type not in ALLOWED_METADATA_TYPES:
        raise ValueError(f"metadata_type must be one of: {sorted(ALLOWED_METADATA_TYPES)}")

    _ensure_dir(dml_dir)

    record = DerivativeMetadataRecord(
        metadata_id=f"meta_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}",
        source_record_id=source_record_id,
        source_hash_sha256=source_hash_sha256,
        generated_at=_utc_now_iso(),
        generator=generator,
        metadata_type=metadata_type,
        value=value,
        confidence=confidence,
        status=DERIVATIVE_STATUS,
        promotion_eligible=False,
    )

    record_dict = asdict(record)
    _append_jsonl(_ledger_path(dml_dir), record_dict)

    _append_audit_event(
        {
            "audit_event_id": f"dml_audit_{uuid.uuid4().hex}",
            "event_type": "derivative_metadata_created",
            "event_timestamp": _utc_now_iso(),
            "metadata_id": record.metadata_id,
            "source_record_id": source_record_id,
            "source_hash_sha256": source_hash_sha256,
            "metadata_type": metadata_type,
            "status_after": DERIVATIVE_STATUS,
            "promotion_eligible": False,
            "module": "derivative_metadata_ledger.py",
            "schema_version": SCHEMA_VERSION,
            "app_version": APP_VERSION,
        },
        dml_dir,
    )

    return record_dict


def load_derivative_metadata(*, dml_dir: Optional[Path | str] = None) -> List[Dict[str, Any]]:
    """Load derivative metadata records from the JSONL ledger."""
    path = _ledger_path(dml_dir)
    if not path.exists():
        return []

    records: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def get_metadata_for_source(
    source_record_id: str,
    *,
    dml_dir: Optional[Path | str] = None,
) -> List[Dict[str, Any]]:
    """Return derivative metadata records pointing to a source record."""
    return [
        record
        for record in load_derivative_metadata(dml_dir=dml_dir)
        if record.get("source_record_id") == source_record_id
    ]


if __name__ == "__main__":
    sample = create_derivative_metadata(
        source_record_id="clip_example",
        source_hash_sha256="sha256_example",
        generator="manual_test",
        metadata_type="classification",
        value="possible_task",
        confidence="low",
    )
    print(json.dumps(sample, indent=2))
