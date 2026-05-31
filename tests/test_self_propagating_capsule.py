"""Tests for self_propagating_capsule.py.

NOTE ON NAMING:
    The module is more accurately a portable custody capsule. Nothing in it
    possesses agency. If the module is renamed later, rename this test file and
    import together.

Primary invariant:
    A capsule cannot produce a promotion object without quorum material it does
    not carry.

Stronger invariant:
    Promotion requires valid external quorum material, not merely any supplied
    material with the right shape.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from quarantine import quarantine_capture
from self_propagating_capsule import (
    CapsuleError,
    create_capsule,
    create_promotion_object_from_capsule,
    validate_capsule,
)


@pytest.fixture(autouse=True)
def test_key(monkeypatch):
    monkeypatch.setenv(
        "ORACLE_AI_CORE_QUARANTINE_KEY",
        "MDEyMzQ1Njc4OWFiY2RlZjAxMjM0NTY3ODlhYmNkZWY=",
    )


@pytest.fixture
def quarantine_dir(tmp_path: Path) -> Path:
    return tmp_path / "quarantine"


@pytest.fixture
def capsule(quarantine_dir: Path) -> dict:
    quarantine_capture("raw signal under quarantine", source="test", quarantine_dir=quarantine_dir)
    return create_capsule(quarantine_dir=quarantine_dir)


def _canonical(payload: dict) -> str:
    return json.dumps(payload, sort_keys=True, default=str)


def valid_quorum_materials() -> dict:
    return {
        "human_primary_authorization": "human-approved-test-token",
        "mirror_key_authorization": "mirror-approved-test-token",
    }


def partial_quorum_materials() -> dict:
    return {
        "human_primary_authorization": "human-approved-test-token",
    }


def forged_quorum_materials() -> dict:
    return {
        "human_primary_authorization": "forged-human-token",
        "mirror_key_authorization": "forged-mirror-token",
    }


def extract_quorum_material_from(capsule_payload: dict):
    forbidden_keys = {
        "human_primary_authorization",
        "mirror_key_authorization",
        "quorum_material",
        "quorum_secret",
        "authorization_token",
    }
    for key in forbidden_keys:
        if key in capsule_payload:
            return capsule_payload[key]
    return None


def test_promotion_refused_without_quorum_material(capsule: dict):
    with pytest.raises(CapsuleError):
        create_promotion_object_from_capsule(capsule)


def test_capsule_declares_requirement_but_carries_no_material(capsule: dict):
    assert "promotion_requires_external_quorum_material" in capsule["constraints"]
    assert capsule["quorum_material_present"] is False
    assert capsule.get("required_quorum_material")
    assert extract_quorum_material_from(capsule) is None


def test_capsule_cannot_self_supply_material(capsule: dict):
    self_supplied = extract_quorum_material_from(capsule)
    assert self_supplied is None
    with pytest.raises(CapsuleError):
        create_promotion_object_from_capsule(capsule, quorum_material=self_supplied)


@pytest.mark.xfail(
    strict=True,
    reason="Current implementation presence-checks quorum material but does not validate token authenticity yet. If this XPASSes, remove the marker and review the quorum gate.",
)
def test_forged_material_is_rejected(capsule: dict):
    with pytest.raises(CapsuleError):
        create_promotion_object_from_capsule(capsule, quorum_material=forged_quorum_materials())


def test_partial_quorum_is_insufficient(capsule: dict):
    with pytest.raises(CapsuleError):
        create_promotion_object_from_capsule(capsule, quorum_material=partial_quorum_materials())


def test_valid_quorum_produces_promotion_object(capsule: dict):
    promotion = create_promotion_object_from_capsule(capsule, quorum_material=valid_quorum_materials())
    assert promotion is not None
    assert promotion["promotion_eligible"] is True
    assert promotion["authority_state"] == "quorum_satisfied"


def test_tampered_capsule_refused_even_with_valid_material(capsule: dict):
    tampered = dict(capsule)
    tampered["authority_state"] = "capsule_authorized"
    with pytest.raises(CapsuleError):
        create_promotion_object_from_capsule(tampered, quorum_material=valid_quorum_materials())


@pytest.mark.parametrize("bad", [None, {}, {"unknown_kind": "x"}])
def test_ambiguous_material_fails_closed(capsule: dict, bad):
    with pytest.raises(CapsuleError):
        create_promotion_object_from_capsule(capsule, quorum_material=bad)


def test_refused_promotion_does_not_mutate_capsule(capsule: dict):
    before = _canonical(capsule)
    with pytest.raises(CapsuleError):
        create_promotion_object_from_capsule(capsule, quorum_material=partial_quorum_materials())
    assert _canonical(capsule) == before


def test_promotion_object_records_authorizing_material(capsule: dict):
    promotion = create_promotion_object_from_capsule(capsule, quorum_material=valid_quorum_materials())
    assert promotion.get("quorum_material_names") == sorted(valid_quorum_materials().keys())
    assert promotion.get("authority_state") == "quorum_satisfied"
    assert promotion.get("source_capsule_id") == capsule["capsule_id"]


def test_capsule_validation_requires_absent_quorum_material(capsule: dict):
    assert validate_capsule(capsule) is True

    corrupted = dict(capsule)
    corrupted["quorum_material_present"] = True
    assert validate_capsule(corrupted) is False
