from continuity_engine import ContinuityEngine
from governance_report import GovernanceReport


def test_governance_report_generation():
    engine = ContinuityEngine()

    state = {
        "self_model": "Required continuity verification",
        "history": [],
    }

    event = {
        "type": "identity_event",
        "text": "Maintain immutable provenance anchors",
    }

    verdict = engine.evaluate(event, state)

    report = GovernanceReport.generate(
        verdict=verdict,
        event=event,
        ledger=engine.ledger,
    )

    assert report["continuity_verdict"]["status"] == "ACCEPTED"
    assert report["ledger_summary"]["integrity_valid"] is True
    assert "report_id" in report
