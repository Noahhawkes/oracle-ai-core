import hashlib
import json
from datetime import datetime
from typing import Any, Dict, Optional


class GovernanceReport:
    REPORT_VERSION = "1.0"

    @staticmethod
    def generate(
        verdict: Dict[str, Any],
        event: Dict[str, Any],
        ledger: Optional[Any] = None,
        subject_did: Optional[str] = None,
        mvik_version: str = "v0.2",
    ) -> Dict[str, Any]:
        report_core = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "subject_did": subject_did or "did:example:pending-subject-binding",
            "event_hash": "sha256:" + GovernanceReport._hash(event),
            "continuity_verdict": {
                "status": verdict.get("continuity_status"),
                "recommendation": verdict.get("recommendation"),
                "drift_score": verdict.get("drift_score", 0.0),
                "anchor_violations": verdict.get("anchor_violations", []),
                "obligation_drift": verdict.get("obligation_drift", []),
                "fork_detected": verdict.get("fork_detected", False),
            },
            "ledger_summary": GovernanceReport._ledger_summary(ledger),
            "attestation": verdict.get("attestation"),
            "snapshot_reference": verdict.get("snapshot_hash"),
            "reasoning": verdict.get("reasoning", []),
            "governance_metadata": {
                "sovereignty_rule": "51/49",
                "mvik_version": mvik_version,
                "report_version": GovernanceReport.REPORT_VERSION,
            },
        }

        report_id = "govrep_" + GovernanceReport._hash(report_core)[:24]
        return {"report_id": report_id, **report_core}

    @staticmethod
    def to_json(report: Dict[str, Any]) -> str:
        return json.dumps(report, sort_keys=True, indent=2)

    @staticmethod
    def _ledger_summary(ledger: Optional[Any]) -> Dict[str, Any]:
        if ledger is None:
            return {
                "chain_head": None,
                "integrity_valid": None,
                "event_count": 0,
            }

        chain = getattr(ledger, "chain", [])
        chain_head = chain[-1]["hash"] if chain else None
        integrity_valid = ledger.verify_integrity() if hasattr(ledger, "verify_integrity") else None

        return {
            "chain_head": "ledger_hash:" + chain_head if chain_head else None,
            "integrity_valid": integrity_valid,
            "event_count": len(chain),
        }

    @staticmethod
    def _hash(payload: Dict[str, Any]) -> str:
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()
