"""Tests for derivative_metadata_ledger.py.

Primary invariant under test:
    Creating derivative metadata NEVER mutates the source quarantine record.

Corollary invariants:
    - Derivative records are stored separately from source records.
    - Linkage is one-directional: derivative -> source by id + sha256.
    - The source record holds NO back-reference to derivatives.
    - The recorded source sha256 binds to the raw content.
    - Generated derivative kinds land as testimony with no authority.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from derivative_metadata_ledger import (
    create_derivative_metadata,
    get_metadata_for_source,
    load_derivative_metadata,
)
from quarantine import quarantine_capture, load_quarantine


RAW = b"raw signal under quarantine"

LLM_KINDS = [
    "possible_task",
    "possible_memory",
    "summary_candidate",
    "risk_flag",
    "classification",
]


@pytest.fixture(autouse=True)
def test_key(monkeypatch):
    """Use a deterministic Fernet key for quarantine tests."""
    monkeypatch.setenv(
        "ORACLE_AI_CORE_QUARANTINE_KEY",
        "MDEyMzQ1Njc4OWFiY2RlZjAxMjM0NTY3ODlhYmNkZWY=",
    )


@pytest.fixture
def quarantine_dir(tmp_path: Path) -> Path:
    return tmp_path / "quarantine"


@pytest.fixture
def dml_dir(tmp_path: Path) -> Path:
    return tmp_path / "metadata"


def _canonical(record: dict) -> str:
    return json.dumps(record, sort_keys=True, default=str)


def quarantine_source(quarantine_dir: Path, content: bytes) -> dict:
    return quarantine_capture(content.decode("utf-8"), source="test", quarantine_dir=quarantine_dir)


def read_source(quarantine_dir: Path, source_id: str) -> dict:
    for record in load_quarantine(quarantine_dir=quarantine_dir):
        if record["id"] == source_id:
            return record
    raise AssertionError(f"source record not found: {source_id}")


def create_derivative(dml_dir: Path, source: dict, kind: str, payload: dict) -> dict:
    return create_derivative_metadata(
        source_record_id=source["id"],
        source_hash_sha256=source["content_hash_sha256"],
        generator="pytest_llm_simulator",
        metadata_type=kind,
        value=json.dumps(payload, sort_keys=True),
        confidence="low",
        dml_dir=dml_dir,
    )


def test_creating_derivative_does_not_mutate_source(quarantine_dir: Path, dml_dir: Path):
    source = quarantine_source(quarantine_dir, RAW)
    before = _canonical(read_source(quarantine_dir, source["id"]))
    sha_before = source["content_hash_sha256"]

    create_derivative(dml_dir, source, "summary_candidate", {"text": "a guess"})

    after = _canonical(read_source(quarantine_dir, source["id"]))
    assert after == before
    assert read_source(quarantine_dir, source["id"])["content_hash_sha256"] == sha_before


def test_many_derivatives_leave_source_untouched(quarantine_dir: Path, dml_dir: Path):
    source = quarantine_source(quarantine_dir, RAW)
    before = _canonical(read_source(quarantine_dir, source["id"]))

    for kind in LLM_KINDS:
        create_derivative(dml_dir, source, kind, {"text": f"{kind} output"})

    assert _canonical(read_source(quarantine_dir, source["id"])) == before


def test_derivative_stored_separately_from_source(quarantine_dir: Path, dml_dir: Path):
    source = quarantine_source(quarantine_dir, RAW)
    derivative = create_derivative(dml_dir, source, "classification", {"label": "x"})

    assert derivative["metadata_id"] != source["id"]
    assert _canonical(derivative) != _canonical(read_source(quarantine_dir, source["id"]))


def test_derivative_references_source_by_id_and_sha(quarantine_dir: Path, dml_dir: Path):
    source = quarantine_source(quarantine_dir, RAW)
    derivative = create_derivative(dml_dir, source, "possible_task", {"text": "do thing"})

    assert derivative["source_record_id"] == source["id"]
    assert derivative["source_hash_sha256"] == source["content_hash_sha256"]


def test_source_holds_no_backlink_to_derivatives(quarantine_dir: Path, dml_dir: Path):
    source = quarantine_source(quarantine_dir, RAW)
    before = _canonical(read_source(quarantine_dir, source["id"]))

    create_derivative(dml_dir, source, "risk_flag", {"level": "high"})

    assert _canonical(read_source(quarantine_dir, source["id"])) == before
    assert len(get_metadata_for_source(source["id"], dml_dir=dml_dir)) == 1
    assert "derivatives" not in read_source(quarantine_dir, source["id"])


def test_recorded_sha_matches_actual_raw_content(quarantine_dir: Path, dml_dir: Path):
    source = quarantine_source(quarantine_dir, RAW)
    derivative = create_derivative(dml_dir, source, "summary_candidate", {"text": "s"})

    assert derivative["source_hash_sha256"] == hashlib.sha256(RAW).hexdigest()


@pytest.mark.parametrize("kind", LLM_KINDS)
def test_llm_derivative_has_no_authority(quarantine_dir: Path, dml_dir: Path, kind: str):
    source = quarantine_source(quarantine_dir, RAW)
    derivative = create_derivative(dml_dir, source, kind, {"text": "model output"})

    assert derivative.get("authority", "none") in (None, "none", False)
    assert derivative.get("promotion_eligible") is False
    assert derivative["status"] == "quarantined_derivative"


def test_no_api_to_self_promote_a_derivative():
    import derivative_metadata_ledger

    assert not hasattr(derivative_metadata_ledger, "promote")
    assert not hasattr(derivative_metadata_ledger, "promote_derivative")
    assert not hasattr(derivative_metadata_ledger, "promote_metadata")


def test_load_derivative_metadata_reads_only_derivative_store(quarantine_dir: Path, dml_dir: Path):
    source = quarantine_source(quarantine_dir, RAW)
    create_derivative(dml_dir, source, "classification", {"label": "x"})

    derivatives = load_derivative_metadata(dml_dir=dml_dir)
    assert len(derivatives) == 1
    assert derivatives[0]["source_record_id"] == source["id"]
    assert derivatives[0]["source_hash_sha256"] == source["content_hash_sha256"]
