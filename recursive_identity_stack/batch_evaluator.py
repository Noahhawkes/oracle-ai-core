from typing import Any, Dict, List

from continuity_engine import ContinuityEngine


class BatchEvaluator:
    def __init__(self, engine: ContinuityEngine):
        self.engine = engine

    def evaluate_batch(
        self,
        events: List[Dict[str, Any]],
        initial_state: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        state = dict(initial_state)
        results = []

        for event in events:
            verdict = self.engine.evaluate(event, state)
            results.append(verdict)

            if verdict["continuity_status"] == "ACCEPTED":
                state = verdict.get("new_state", state)

        return results
