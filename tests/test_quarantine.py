"""Tests for quarantine.py boundary invariants.

These tests verify the Minimum Viable Discriminator Kernel (MVDK) rule:

    capture -> quarantine -> review -> promote

quarantine.py is allowed to create quarantined records only.
It must not promote, canonize, rewrite, or bypass human authority.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

import pytest

import quarantine
from quarantine import quarantine_capture, load_quarantine, tombstone_record


@pytest.fixture(autouse=True)
def test_key(monkeypatch):
    """Use a deterministic Fernet key for tests instead of OS keyring."""
    monkeypatch.setenv(
        "ORACLE_AI_CORE_QUARANTINE_KEY",
        "MDEyMzQ1Njc4OWFiY2RlZjAxMjM0NTY3ODlhYmNkZWY=",
    )


@pytest.fixture
def quarantine_dir(tmp_path: Path) -> Path:
    return tmp_path / "quarantine"


def test_record_creation_defaults_quarantined(quarantine_dir: Path):
    record = quarantine_capture("Test signal", source="test", quarantine_dir=quarantine_dir)
    assert record["status"] == "quarantined"


def test_promotion_eligible_is_strictly_false(quarantine_dir: Path):
    record = quarantine_capture("Test signal", source="test", quarantine_dir=quarantine_dir)
    assert record["promotion_eligible"] is False


def test_sha256_hash_is_correct(quarantine_dir: Path):
    content = "Test signal"
    expected_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    record = quarantine_capture(content, source="test", quarantine_dir=quarantine_dir)
    assert record["content_hash_sha256"] == expected_hash


def test_metadata_stamping_includes_timestamp(quarantine_dir: Path):
    record = quarantine_capture("Test signal", source="test", quarantine_dir=quarantine_dir)
    assert "captured_at" in record
    assert record["captured_at"] is not None


def test_source_metadata_is_preserved(quarantine_dir: Path):
    record = quarantine_capture("Test signal", source="clipboard", quarantine_dir=quarantine_dir)
    assert record["source"] == "clipboard"


def test_invalid_source_is_rejected(quarantine_dir: Path):
    with pytest.raises(ValueError):
        quarantine_capture("Test signal", source="mac_clipboard", quarantine_dir=quarantine_dir)


def test_no_promotion_path_exists():
    assert not hasattr(quarantine, "promote_record")
    assert not hasattr(quarantine, "auto_promote")
    assert not hasattr(quarantine, "promote_to_canon")


def test_load_quarantine_returns_unmodified_state(quarantine_dir: Path):
    record = quarantine_capture("Read test", source="test", quarantine_dir=quarantine_dir)
    loaded = load_quarantine(quarantine_dir=quarantine_dir)

    assert len(loaded) == 1
    assert loaded[0]["id"] == record["id"]
    assert loaded[0]["status"] == "quarantined"
    assert loaded[0]["promotion_eligible"] is False


def test_audit_log_is_created_without_raw_content(quarantine_dir: Path):
    raw = "Audit log should not leak this exact content"
    quarantine_capture(raw, source="test", quarantine_dir=quarantine_dir)

    audit_path = quarantine_dir / quarantine.AUDIT_LOG_NAME
    assert audit_path.exists()

    audit_text = audit_path.read_text(encoding="utf-8")
    assert "capture_created" in audit_text
    assert raw not in audit_text


def test_audit_log_appends_events(quarantine_dir: Path):
    quarantine_capture("Signal 1", source="test", quarantine_dir=quarantine_dir)
    quarantine_capture("Signal 2", source="test", quarantine_dir=quarantine_dir)

    audit_path = quarantine_dir / quarantine.AUDIT_LOG_NAME
    lines = audit_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2


def test_tombstone_record_removes_raw_content_and_preserves_hash(quarantine_dir: Path):
    record = quarantine_capture("Sensitive data", source="test", quarantine_dir=quarantine_dir)
    original_hash = record["content_hash_sha256"]

    tombstoned = tombstone_record(record["id"], quarantine_dir=quarantine_dir)

    assert tombstoned["raw_content"] is None
    assert tombstoned["status"] == "tombstoned"
    assert tombstoned["promotion_eligible"] is False
    assert tombstoned["content_hash_sha256"] == original_hash


def test_record_ids_are_unique(quarantine_dir: Path):
    record1 = quarantine_capture("Signal 1", source="test", quarantine_dir=quarantine_dir)
    record2 = quarantine_capture("Signal 1", source="test", quarantine_dir=quarantine_dir)
    assert record1["id"] != record2["id"]


def test_raw_store_is_encrypted_not_plaintext(quarantine_dir: Path):
    raw = "Plaintext should not appear in encrypted store"
    quarantine_capture(raw, source="test", quarantine_dir=quarantine_dir)

    store_path = quarantine_dir / quarantine.ENCRYPTED_STORE_NAME
    assert store_path.exists()
    store_bytes = store_path.read_bytes()
    assert raw.encode("utf-8") not in store_bytes


def test_boundary_enforcement_success(quarantine_dir: Path):
    record = quarantine_capture("Final test", source="test", quarantine_dir=quarantine_dir)
    assert record["promotion_eligible"] is False
    assert record["status"] == "quarantined"
    assert "content_hash_sha256" in record
    assert record["promoted_to"] is None
