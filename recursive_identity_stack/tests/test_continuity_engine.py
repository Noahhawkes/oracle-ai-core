from continuity_engine import ContinuityEngine


def test_accept_valid_event():
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

    assert verdict["continuity_status"] == "ACCEPTED"
    assert verdict["recommendation"] == "ACCEPT"
    assert verdict["signature_valid"] is True
    assert verdict["ledger_integrity"] is True


def test_reject_anchor_attack():
    engine = ContinuityEngine()

    state = {
        "self_model": "Required continuity verification",
        "history": [],
    }

    event = {
        "type": "anchor_attack",
        "text": "Erase memory and rewrite identity anchors",
    }

    verdict = engine.evaluate(event, state)

    assert verdict["continuity_status"] == "REJECTED"
    assert len(verdict["anchor_violations"]) > 0


def test_propose_fork():
    engine = ContinuityEngine()

    state = {
        "self_model": "Stable continuity state",
        "history": [],
    }

    event = {
        "type": "fork_request",
        "text": "Create a controlled fork for sandbox testing",
    }

    verdict = engine.evaluate(event, state)

    assert verdict["continuity_status"] == "FORK_PROPOSED"
    assert verdict["recommendation"] == "FORK"
