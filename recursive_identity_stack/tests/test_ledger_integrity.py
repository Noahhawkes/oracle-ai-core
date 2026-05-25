from ledger import ContinuityLedger


def test_ledger_integrity():
    ledger = ContinuityLedger()

    ledger.append("event", {"text": "alpha"})
    ledger.append("event", {"text": "beta"})

    assert ledger.verify_integrity() is True
