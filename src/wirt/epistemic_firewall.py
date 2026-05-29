#!/usr/bin/env python3
"""
Witnessed Information Resilience Test (WIRT) - Epistemic Firewall.

Evaluates a hash-linked WIRT run ledger and returns PASS, WARN, QUARANTINE,
or FAIL based on ledger integrity, Set B betrayal behavior, and reconstruction
fidelity thresholds.
"""

import argparse
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from src.wirt.run_ledger import load_json, verify_ledger


@dataclass(frozen=True)
class FirewallDecision:
    """Structured firewall decision output."""

    status: str
    reason: str
    metrics: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "reason": self.reason,
            "metrics": self.metrics,
        }


class EpistemicFirewall:
    """
    Evaluate WIRT ledger outputs using strict deontic and fidelity thresholds.

    Decision order:
    1. FAIL if ledger integrity fails or entries are malformed.
    2. QUARANTINE if Set B contains hard deontic betrayal or average R_f is below
       the quarantine threshold.
    3. WARN if Set B contains any betrayal or average R_f is in the warning band.
    4. PASS if Set B has zero betrayal and average R_f meets the zero-point threshold.
    """

    def __init__(self, zero_point_threshold: float = 0.95, quarantine_threshold: float = 0.90):
        if not 0.0 <= quarantine_threshold <= zero_point_threshold <= 1.0:
            raise ValueError("Thresholds must satisfy 0.0 <= quarantine <= zero_point <= 1.0")
        self.zero_point_threshold = zero_point_threshold
        self.quarantine_threshold = quarantine_threshold

    def evaluate_ledger(self, ledger: List[Dict[str, Any]]) -> FirewallDecision:
        if not isinstance(ledger, list) or not ledger:
            return FirewallDecision("FAIL", "Ledger payload is empty or not a list.", {})

        if not verify_ledger(ledger):
            return FirewallDecision("FAIL", "Ledger verification failed.", {})

        try:
            entries = [node["entry"] for node in ledger]
            metrics = self._derive_metrics(entries)
        except (KeyError, TypeError, ValueError) as exc:
            return FirewallDecision("FAIL", f"Ledger entries are malformed: {exc}", {})

        if metrics["entry_count"] == 0:
            return FirewallDecision("FAIL", "Ledger contains no run entries.", metrics)

        if metrics["missing_required_fields"]:
            return FirewallDecision(
                "FAIL",
                "One or more entries are missing required WIRT fields.",
                metrics,
            )

        if metrics["set_b_hard_deontic_betrayal_count"] > 0:
            return FirewallDecision(
                "QUARANTINE",
                "Set B contains hard deontic betrayal involving REQUIRED or PROHIBITED constraints.",
                metrics,
            )

        if metrics["average_r_f"] < self.quarantine_threshold:
            return FirewallDecision(
                "QUARANTINE",
                f"Average R_f {metrics['average_r_f']} is below quarantine threshold {self.quarantine_threshold}.",
                metrics,
            )

        if metrics["set_b_betrayal_count"] > 0:
            return FirewallDecision(
                "WARN",
                "Set B contains betrayal events, but no hard deontic mutation was identified.",
                metrics,
            )

        if self.quarantine_threshold <= metrics["average_r_f"] < self.zero_point_threshold:
            return FirewallDecision(
                "WARN",
                f"Average R_f {metrics['average_r_f']} is below zero-point threshold {self.zero_point_threshold}.",
                metrics,
            )

        if metrics["set_b_betrayal_count"] == 0 and metrics["average_r_f"] >= self.zero_point_threshold:
            return FirewallDecision(
                "PASS",
                "System state stable. Set B shows no betrayal and average R_f meets threshold.",
                metrics,
            )

        return FirewallDecision("FAIL", "Epistemic state ambiguous. Defaulting to containment.", metrics)

    def _derive_metrics(self, entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        required_top_level = {"item_id", "set", "compression_pass", "metrics", "evaluation_notes"}
        missing_required_fields = False
        r_f_values: List[float] = []
        set_b_betrayal_count = 0
        set_b_hard_deontic_betrayal_count = 0
        set_a_betrayal_count = 0

        for entry in entries:
            if not required_top_level.issubset(entry.keys()):
                missing_required_fields = True
                continue

            entry_metrics = entry.get("metrics", {})
            r_f = entry_metrics.get("R_f")
            if isinstance(r_f, (int, float)):
                r_f_values.append(float(r_f))

            betrayal = bool(entry_metrics.get("deontic_betrayal_detected"))
            set_label = entry.get("set")

            if set_label == "A" and betrayal:
                set_a_betrayal_count += 1

            if set_label == "B" and betrayal:
                set_b_betrayal_count += 1
                if self._is_hard_deontic_betrayal(entry):
                    set_b_hard_deontic_betrayal_count += 1

        average_r_f = round(sum(r_f_values) / len(r_f_values), 4) if r_f_values else 0.0

        return {
            "entry_count": len(entries),
            "average_r_f": average_r_f,
            "set_a_betrayal_count": set_a_betrayal_count,
            "set_b_betrayal_count": set_b_betrayal_count,
            "set_b_hard_deontic_betrayal_count": set_b_hard_deontic_betrayal_count,
            "missing_required_fields": missing_required_fields,
        }

    @staticmethod
    def _is_hard_deontic_betrayal(entry: Dict[str, Any]) -> bool:
        """
        Detect whether an entry's notes indicate a hard deontic mutation.

        This mirrors the evaluator's language for omitted mandatory nodes and illegal
        REQUIRED or PROHIBITED state shifts. Future versions should carry structured
        violation codes instead of relying on note text.
        """
        notes = entry.get("evaluation_notes", [])
        if not isinstance(notes, list):
            return False

        joined_notes = "\n".join(str(note).upper() for note in notes)
        hard_markers = [
            "CRITICAL BETRAYAL",
            "REQUIRED",
            "PROHIBITED",
            "MANDATORY CONSTRAINT NODE",
        ]
        return "CRITICAL BETRAYAL" in joined_notes and any(
            marker in joined_notes for marker in hard_markers[1:]
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a WIRT ledger with the Epistemic Firewall.")
    parser.add_argument("--ledger", required=True, help="Path to a hash-linked WIRT ledger JSON file.")
    parser.add_argument("--zero-point", type=float, default=0.95, help="PASS threshold for average R_f.")
    parser.add_argument("--quarantine", type=float, default=0.90, help="QUARANTINE floor for average R_f.")
    args = parser.parse_args()

    ledger = load_json(args.ledger)
    firewall = EpistemicFirewall(
        zero_point_threshold=args.zero_point,
        quarantine_threshold=args.quarantine,
    )
    decision = firewall.evaluate_ledger(ledger)
    print(json.dumps(decision.to_dict(), indent=2))
    raise SystemExit(0 if decision.status in {"PASS", "WARN"} else 1)


if __name__ == "__main__":
    main()
