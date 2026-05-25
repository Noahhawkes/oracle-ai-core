from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class ContinuityEvent:
    event_type: str
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AttestationRecord:
    signer_id: str
    payload_hash: str
    signature: str


@dataclass
class SnapshotRecord:
    snapshot_hash: str
    timestamp: str


@dataclass
class ForkRecordSchema:
    fork_id: str
    parent_identity_id: str
    parent_hash: str
    divergence_timestamp: str
    declared_reason: str


@dataclass
class ContinuityVerdictSchema:
    continuity_status: str
    recommendation: str
    drift_score: float
    anchor_violations: List[Dict[str, Any]]
    obligation_drift: List[Dict[str, Any]]
    fork_detected: bool
    reasoning: List[str]


@dataclass
class GovernanceReportSchema:
    report_id: str
    timestamp: str
    event_hash: str
    continuity_verdict: Dict[str, Any]
    ledger_summary: Dict[str, Any]
    attestation: Optional[Dict[str, Any]]
    reasoning: List[str]
    governance_metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
