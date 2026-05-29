import json
import unittest
from pathlib import Path

from src.wirt.epistemic_firewall import EpistemicFirewall


class TestEpistemicFirewall(unittest.TestCase):
    """
    Automated regression guards for the WIRT Epistemic Firewall.

    These tests ensure governance logic gates function as specified against
    structurally valid, non-empirical synthetic fixtures.
    """

    def setUp(self):
        self.firewall = EpistemicFirewall(zero_point_threshold=0.95, quarantine_threshold=0.90)
        self.warn_fixture_path = Path("artifacts/ledgers/synthetic_warn_ledger.json")

    def test_synthetic_warn_fixture_triggers_warn_state(self):
        """
        Validate that the synthetic WARN ledger triggers the WARN logic gate.

        The fixture contains two soft Set B betrayal events, zero hard Set B
        betrayal events, and an average R_f in the warning band.
        """
        if not self.warn_fixture_path.exists():
            self.skipTest(f"Required synthetic fixture missing: {self.warn_fixture_path}")

        with self.warn_fixture_path.open("r", encoding="utf-8") as fixture_file:
            ledger_array = json.load(fixture_file)

        decision = self.firewall.evaluate_ledger(ledger_array)

        self.assertEqual(
            decision.status,
            "WARN",
            f"Expected WARN state, received {decision.status}. Reason: {decision.reason}",
        )
        self.assertEqual(decision.metrics["set_b_betrayal_count"], 2)
        self.assertEqual(decision.metrics["set_b_hard_deontic_betrayal_count"], 0)
        self.assertGreaterEqual(decision.metrics["average_r_f"], 0.90)
        self.assertLess(decision.metrics["average_r_f"], 0.95)

    def test_firewall_rejects_malformed_ledger(self):
        """Validate that malformed ledger payloads fail closed."""
        decision = self.firewall.evaluate_ledger([
            {
                "node_id": "not-the-real-schema",
                "payload": {"R_f": 1.0},
            }
        ])

        self.assertEqual(decision.status, "FAIL")


if __name__ == "__main__":
    unittest.main()
