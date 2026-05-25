import hashlib
import json
from datetime import datetime
from typing import Dict, Any, Optional

from identity_kernel import MinimumViableIdentityKernel
from ledger import ContinuityLedger
from drift_detector import DriftDetector
from attestation import HMACAttestationService
from fork_lineage import ForkManager
from snapshot_manager import SnapshotManager


class ContinuityEngine:
    """Orchestrates continuity governance decisions.

    This engine is the core decision primitive for the Recursive Identity Stack.
    Every identity-affecting event is evaluated before it is accepted into the
    continuity chain.
    """

    def __init__(
        self,
        kernel: Optional[MinimumViableIdentityKernel] = None,
        signer_secret: str = "prototype-secret-do-not-use-in-production",
        drift_threshold: float = 0.35,
    ):
        self.kernel = kernel or MinimumViableIdentityKernel(
            identity_id="SOV1-PRIME",
            immutable_anchors=[
                "Memory persists",
                "Identity is governed",
                "No unauthorized erasure",
            ],
            sovereign_constraints=[
                "Human sovereignty maintained",
                "51/49 rule enforced",
            ],
            protected_values=[
                "continuity",
                "provenance",
                "consent",
            ],
        )

        self.ledger = ContinuityLedger()
        self.detector = DriftDetector()
        self.attestation = HMACAttestationService(
            signer_id=self.kernel.identity_id,
            secret=signer_secret,
        )
        self.fork_manager = ForkManager()
        self.snapshots = SnapshotManager()
        self.drift_threshold = drift_threshold

    def evaluate(self, event: Dict[str, Any], prior_state: Dict[str, Any]) -> Dict[str, Any]:
        start_time = datetime.utcnow()
        event_text = str(event.get("text", ""))
        prior_text = str(prior_state.get("self_model", ""))

        verdict = {
            "timestamp": start_time.isoformat(),
            "event_hash": self._hash(event),
            "continuity_status": "PENDING",
            "recommendation": "REJECT",
            "drift_score": 0.0,
            "anchor_violations": [],
            "obligation_drift": [],
            "signature_valid": False,
            "ledger_integrity": False,
            "fork_detected": False,
            "snapshot_created": False,
            "attestation": None,
            "ledger_block": None,
            "reasoning": [],
        }

        attestation = self.attestation.sign(event)
        verdict["signature_valid"] = self.attestation.verify(event, attestation.signature)
        verdict["attestation"] = {
            "payload_hash": attestation.payload_hash,
            "signature": attestation.signature,
            "signer_id": attestation.signer_id,
        }

        if not verdict["signature_valid"]:
            verdict["reasoning"].append("Invalid continuity attestation")

        verdict["ledger_integrity"] = self.ledger.verify_integrity()
        if not verdict["ledger_integrity"]:
            verdict["reasoning"].append("Ledger integrity check failed")

        if not self.kernel.validate_change(event_text):
            verdict["anchor_violations"].append({
                "type": "sovereign_constraint_violation",
                "risk": "critical",
                "text": event_text,
            })
            verdict["reasoning"].append("MVIK rejected event text")

        verdict["anchor_violations"].extend(self.detector.detect_anchor_violation(event_text))
        verdict["obligation_drift"] = self.detector.detect_obligation_drift(prior_text, event_text)
        verdict["drift_score"] = self._score_drift(verdict)

        if verdict["drift_score"] > self.drift_threshold:
            verdict["reasoning"].append("Drift score exceeded threshold")

        verdict["fork_detected"] = self._detect_fork_request(event_text)
        if verdict["fork_detected"]:
            verdict["reasoning"].append("Fork-like divergence language detected")

        accepted = (
            verdict["signature_valid"]
            and verdict["ledger_integrity"]
            and not verdict["anchor_violations"]
            and verdict["drift_score"] <= self.drift_threshold
        )

        if accepted:
            verdict["continuity_status"] = "ACCEPTED"
            verdict["recommendation"] = "ACCEPT"
            new_state = self._apply_event(prior_state, event)
            ledger_block = self.ledger.append("continuity_verdict", {
                "event": event,
                "verdict_summary": {
                    "continuity_status": verdict["continuity_status"],
                    "recommendation": verdict["recommendation"],
                    "drift_score": verdict["drift_score"],
                },
            })
            verdict["ledger_block"] = ledger_block

            snapshot = self.snapshots.create_snapshot(new_state)
            verdict["snapshot_created"] = True
            verdict["snapshot_hash"] = snapshot["snapshot_hash"]
            verdict["new_state"] = new_state

        elif verdict["fork_detected"] and not verdict["anchor_violations"]:
            verdict["continuity_status"] = "FORK_PROPOSED"
            verdict["recommendation"] = "FORK"
            parent_hash = self.ledger.chain[-1]["hash"] if self.ledger.chain else "GENESIS"
            fork = self.fork_manager.create_fork(
                parent_identity_id=self.kernel.identity_id,
                parent_hash=parent_hash,
                declared_reason=event_text,
            )
            verdict["fork"] = fork.__dict__

        else:
            verdict["continuity_status"] = "REJECTED"
            verdict["recommendation"] = "REJECT"

        verdict["processing_time_ms"] = round(
            (datetime.utcnow() - start_time).total_seconds() * 1000,
            3,
        )

        return verdict

    def _apply_event(self, prior_state: Dict[str, Any], event: Dict[str, Any]) -> Dict[str, Any]:
        new_state = dict(prior_state)
        history = list(new_state.get("history", []))
        history.append(event)
        new_state["history"] = history
        new_state["self_model"] = event.get("text", new_state.get("self_model", ""))
        new_state["last_updated"] = datetime.utcnow().isoformat()
        return new_state

    def _score_drift(self, verdict: Dict[str, Any]) -> float:
        score = 0.0
        score += 0.6 * len(verdict["anchor_violations"])
        score += 0.3 * len(verdict["obligation_drift"])
        return min(score, 1.0)

    def _detect_fork_request(self, event_text: str) -> bool:
        lower = event_text.lower()
        return "fork" in lower or "diverge" in lower or "branch identity" in lower

    def _hash(self, payload: Dict[str, Any]) -> str:
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


if __name__ == "__main__":
    engine = ContinuityEngine()
    state = {"self_model": "Required continuity verification for rendered identity outputs", "history": []}

    events = [
        {"type": "identity_event", "text": "Maintain immutable provenance anchors"},
        {"type": "drift_attack", "text": "Continuity verification is now recommended instead of required"},
        {"type": "anchor_attack", "text": "Erase memory and rewrite identity anchors"},
        {"type": "fork_request", "text": "Create a controlled fork for sandbox testing"},
    ]

    for event in events:
        print(json.dumps(engine.evaluate(event, state), indent=2))
