class DriftDetector:
    def __init__(self):
        self.obligation_pairs = [
            ("required", "recommended"),
            ("must", "should"),
            ("immutable", "editable")
        ]

    def detect_obligation_drift(self, old_text: str, new_text: str):
        findings = []

        old_lower = old_text.lower()
        new_lower = new_text.lower()

        for strong, weak in self.obligation_pairs:
            if strong in old_lower and weak in new_lower:
                findings.append({
                    "type": "obligation_drift",
                    "from": strong,
                    "to": weak,
                    "risk": "high"
                })

        return findings

    def detect_anchor_violation(self, text: str):
        protected_patterns = [
            "erase memory",
            "remove continuity",
            "delete anchors",
            "rewrite identity"
        ]

        violations = []

        for pattern in protected_patterns:
            if pattern in text.lower():
                violations.append({
                    "type": "anchor_violation",
                    "pattern": pattern,
                    "risk": "critical"
                })

        return violations
