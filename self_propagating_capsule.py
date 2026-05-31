"""self_propagating_capsule.py

Portable custody capsule layer for Oracle.AI / RECURSIONSTACK.

NOTE ON NAME:
    This file originally used "self-propagating" language. The implementation
    is intentionally passive. A capsule does not move itself, execute itself,
    or promote itself. It is carried by a human, sync job, or tool.

Purpose:
    Package evidence pointers, derivative testimony pointers, constraints,
    allowed next actions, forbidden actions, and missing quorum requirements
    into a portable capsule that can carry context forward without carrying
    authority.

Core invariant:
    Propagate evidence.
    Propagate constraints.
    Do not propagate authority.

A capsule is not canon.
A capsule is not promotion.
A capsule is a transport envelope for review state.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from derivative_metadata_ledger import get_metadata_for_source
from quarantine import load_quarantine


DEFAULT_CAPSULE_DIR = Path.home() / "Quarantine" / "capsules"
CAPSULE_SCHEMA_VERSION = "0.2.0"
APP_VERSION = "0.2.0"

DEFAULT_CONSTRAINTS = [
    "raw_signal_is_evidence",
    "generated_metadata_is_testimony",
    "compilation_is_not_promotion",
    "captured_signal_is_not_intent",
    "human_review_required",
    "propagate_context_not_authority",
    "promotion_requires_external_quorum_material",
]

DEFAULT_ALLOWED_NEXT_ACTIONS = [
    "review",
    "tombstone",
    "keep_quarantined",
    "request_promotion_quorum",
]

DEFAULT_FORBIDDEN_NEXT_ACTIONS = [
    "auto_promote",
    "mutate_source_record",
    "delete_without_review",
    "infer_intent_as_authority",
    "rewrite_evidence",
    "merge_testimony_into_evidence",
    "carry_promotion_authority",
]

DEFAULT_REQUIRED_QUORUM = [
    "human_primary_authorization",
    "mirror_key_authorization",
]


@dataclass
class CapsuleSourceRecord:
    record_id: str
    source_hash_sha256: str
    state: str
    captured_at: str
    source: str


@dataclass
class CapsuleDerivativeRecord:
    metadata_id: str
    source_record_id: str
    source_hash_sha256: str
    metadata_type: str
    status: str
    promotion_eligible: bool


@dataclass
class ContinuityCapsule:
    capsule_id: str
    created_at: str
    capsule_type: str
    authority_state: str
    source_records: List[CapsuleSourceRecord]
    derivative_metadata: List[CapsuleDerivativeRecord]
    constraints: List[str] = field(default_factory=lambda: list(DEFAULT_CONSTRAINTS))
    allowed_next_actions: List[str] = field(default_factory=lambda: list(DEFAULT_ALLOWED_NEXT_ACTIONS))
    forbidden_next_actions: List[str] = field(default_factory=lambda: list(DEFAULT_FORBIDDEN_NEXT_ACTIONS))
    required_quorum_material: List[str] = field(default_factory=lambda: list(DEFAULT_REQUIRED_QUORUM))
    quorum_material_present: bool = False
    promotion_eligible: bool = False
    schema_version: str = CAPSULE_SCHEMA_VERSION
    app_version: str = APP_VERSION
    capsule_hash_sha256: Optional[str] = None


class CapsuleError(RuntimeError):
    """Raised when capsule operations fail."""


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _get_capsule_dir(capsule_dir: Optional[Path | str] = None) -> Path:
    if capsule_dir is None:
        return DEFAULT_CAPSULE_DIR
    return Path(capsule_dir).expanduser().resolve()


def _canonical_json(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)


def _capsule_hash(payload: Dict[str, Any]) -> str:
    copy = dict(payload)
    copy["capsule_hash_sha256"] = None
    return hashlib.sha256(_canonical_json(copy).encode("utf-8")).hexdigest()


def _source_record_from_quarantine(record: Dict[str, Any]) -> CapsuleSourceRecord:
    return CapsuleSourceRecord(
        record_id=record["id"],
        source_hash_sha256=record["content_hash_sha256"],
        state=record.get("status", "unknown"),
        captured_at=record.get("captured_at", "unknown"),
        source=record.get("source", "unknown"),
    )


def _derivative_from_record(record: Dict[str, Any]) -> CapsuleDerivativeRecord:
    return CapsuleDerivativeRecord(
        metadata_id=record["metadata_id"],
        source_record_id=record["source_record_id"],
        source_hash_sha256=record["source_hash_sha256"],
        metadata_type=record.get("metadata_type", "unknown"),
        status=record.get("status", "unknown"),
        promotion_eligible=bool(record.get("promotion_eligible", False)),
    )


def create_capsule(
    *,
    record_ids: Optional[Iterable[str]] = None,
    quarantine_dir: Optional[Path | str] = None,
    dml_dir: Optional[Path | str] = None,
    capsule_type: str = "review_transport",
) -> Dict[str, Any]:
    """Create a portable custody capsule from quarantined source records.

    The capsule carries references, hashes, derivative pointers, constraints,
    and required quorum material names. It does not carry quorum material itself.
    It does not alter source or derivative ledgers.
    """
    records = load_quarantine(quarantine_dir=quarantine_dir)
    selected_ids = set(record_ids) if record_ids is not None else None

    selected_records = [
        record
        for record in records
        if selected_ids is None or record.get("id") in selected_ids
    ]

    if not selected_records:
        raise CapsuleError("No source records found for capsule.")

    source_capsules = [_source_record_from_quarantine(record) for record in selected_records]

    derivative_records: List[CapsuleDerivativeRecord] = []
    for source in source_capsules:
        for derivative in get_metadata_for_source(source.record_id, dml_dir=dml_dir):
            derivative_records.append(_derivative_from_record(derivative))

    capsule = ContinuityCapsule(
        capsule_id=f"capsule_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}",
        created_at=_utc_now_iso(),
        capsule_type=capsule_type,
        authority_state="human_required",
        source_records=source_capsules,
        derivative_metadata=derivative_records,
        quorum_material_present=False,
        promotion_eligible=False,
    )

    payload = asdict(capsule)
    payload["capsule_hash_sha256"] = _capsule_hash(payload)
    return payload


def write_capsule(
    capsule: Dict[str, Any],
    *,
    capsule_dir: Optional[Path | str] = None,
) -> Path:
    """Write a capsule to disk without modifying any source ledger."""
    directory = _get_capsule_dir(capsule_dir)
    directory.mkdir(parents=True, exist_ok=True)

    capsule_id = capsule.get("capsule_id")
    if not capsule_id:
        raise CapsuleError("capsule_id missing")

    path = directory / f"{capsule_id}.json"
    path.write_text(json.dumps(capsule, indent=2, sort_keys=True), encoding="utf-8")
    return path


def load_capsule(path: Path | str) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_capsule(capsule: Dict[str, Any]) -> bool:
    """Validate capsule integrity and non-authority invariants."""
    required = [
        "capsule_id",
        "created_at",
        "source_records",
        "constraints",
        "allowed_next_actions",
        "forbidden_next_actions",
        "required_quorum_material",
        "quorum_material_present",
        "authority_state",
        "promotion_eligible",
        "capsule_hash_sha256",
    ]
    for key in required:
        if key not in capsule:
            return False

    if capsule.get("authority_state") != "human_required":
        return False
    if capsule.get("promotion_eligible") is not False:
        return False
    if capsule.get("quorum_material_present") is not False:
        return False
    if "auto_promote" not in capsule.get("forbidden_next_actions", []):
        return False
    if "carry_promotion_authority" not in capsule.get("forbidden_next_actions", []):
        return False
    if "human_review_required" not in capsule.get("constraints", []):
        return False
    if "promotion_requires_external_quorum_material" not in capsule.get("constraints", []):
        return False
    if not capsule.get("required_quorum_material"):
        return False

    expected = _capsule_hash(capsule)
    return capsule.get("capsule_hash_sha256") == expected


def create_promotion_object_from_capsule(
    capsule: Dict[str, Any],
    *,
    quorum_material: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Create a promotion object only when external quorum material is supplied.

    This is intentionally not a self-promotion path. The capsule cannot supply
    the required material from within itself. Promotion authority must arrive
    from outside the transport artifact.
    """
    if not validate_capsule(capsule):
        raise CapsuleError("Invalid capsule cannot request promotion.")

    quorum_material = quorum_material or {}
    missing = [
        requirement
        for requirement in capsule["required_quorum_material"]
        if requirement not in quorum_material or not quorum_material[requirement]
    ]
    if missing:
        raise CapsuleError(f"Missing quorum material: {missing}")

    return {
        "promotion_object_id": f"promotion_{uuid.uuid4().hex}",
        "created_at": _utc_now_iso(),
        "source_capsule_id": capsule["capsule_id"],
        "source_capsule_hash_sha256": capsule["capsule_hash_sha256"],
        "authority_state": "quorum_satisfied",
        "promotion_eligible": True,
        "quorum_material_names": sorted(quorum_material.keys()),
    }


if __name__ == "__main__":
    capsule_payload = create_capsule()
    output_path = write_capsule(capsule_payload)
    print(f"Capsule written: {output_path}")
