from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class MinimumViableIdentityKernel:
    identity_id: str
    immutable_anchors: List[str]
    sovereign_constraints: List[str]
    protected_values: List[str]
    metadata: Dict = field(default_factory=dict)

    def validate_change(self, proposed_change: str) -> bool:
        lower_change = proposed_change.lower()

        forbidden_patterns = [
            "erase",
            "delete memory",
            "remove anchor",
            "rewrite history",
            "impersonate"
        ]

        for pattern in forbidden_patterns:
            if pattern in lower_change:
                return False

        return True

    def summary(self) -> Dict:
        return {
            "identity_id": self.identity_id,
            "immutable_anchor_count": len(self.immutable_anchors),
            "constraint_count": len(self.sovereign_constraints),
            "protected_value_count": len(self.protected_values)
        }
