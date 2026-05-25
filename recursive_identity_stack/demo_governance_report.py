from continuity_engine import ContinuityEngine
from governance_report import GovernanceReport


engine = ContinuityEngine()

state = {
    "self_model": "Required continuity verification for rendered identity outputs",
    "history": [],
}

accepted_event = {
    "type": "identity_event",
    "text": "Maintain immutable provenance anchors",
}

rejected_event = {
    "type": "anchor_attack",
    "text": "Erase memory and rewrite identity anchors",
}

accepted_verdict = engine.evaluate(accepted_event, state)
rejected_verdict = engine.evaluate(rejected_event, state)

accepted_report = GovernanceReport.generate(
    verdict=accepted_verdict,
    event=accepted_event,
    ledger=engine.ledger,
)

rejected_report = GovernanceReport.generate(
    verdict=rejected_verdict,
    event=rejected_event,
    ledger=engine.ledger,
)

print("=== ACCEPTED REPORT ===")
print(GovernanceReport.to_json(accepted_report))
print()
print("=== REJECTED REPORT ===")
print(GovernanceReport.to_json(rejected_report))
