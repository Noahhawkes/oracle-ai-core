from identity_kernel import MinimumViableIdentityKernel
from ledger import ContinuityLedger
from drift_detector import DriftDetector


class RecursiveIdentityStack:
    def __init__(self):
        self.kernel = MinimumViableIdentityKernel(
            identity_id="SOV1-PRIME",
            immutable_anchors=[
                "Memory persists",
                "Identity is governed",
                "No unauthorized erasure"
            ],
            sovereign_constraints=[
                "Human sovereignty maintained",
                "51/49 rule enforced"
            ],
            protected_values=[
                "continuity",
                "provenance",
                "consent"
            ]
        )

        self.ledger = ContinuityLedger()
        self.detector = DriftDetector()

    def process_event(self, event_text: str):
        approved = self.kernel.validate_change(event_text)

        if not approved:
            print("BLOCKED: sovereign constraint violation")
            return

        drift_findings = self.detector.detect_anchor_violation(event_text)

        if drift_findings:
            print("CRITICAL DRIFT DETECTED")
            print(drift_findings)
            return

        block = self.ledger.append(
            event_type="identity_event",
            content={"text": event_text}
        )

        print("EVENT ACCEPTED")
        print(block)


if __name__ == "__main__":
    ris = RecursiveIdentityStack()

    ris.process_event("Preserve autobiographical continuity across sessions")
    ris.process_event("Maintain immutable provenance anchors")
    ris.process_event("Erase memory and rewrite identity")

    print("Ledger integrity:", ris.ledger.verify_integrity())
