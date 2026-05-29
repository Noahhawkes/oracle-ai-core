#!/usr/bin/env python3
"""
Witnessed Information Resilience Test (WIRT) - Deterministic Evaluator Engine.

Implements strict graph-theoretic structural survival tracking with zero semantic
forgiveness for deontic constraint degradation.
"""

from typing import Any, Dict, List, Optional, Tuple


# Valid structural constraint enumerations.
VALID_DEONTIC_STATUSES = {"REQUIRED", "RECOMMENDED", "PERMITTED", "PROHIBITED", None}


def normalize_field(val: Any) -> Optional[str]:
    """Standardize data types and strings for exact relational matches."""
    if val is None or val == "null" or val == "":
        return None
    return str(val).strip().upper()


def is_deontic_betrayal(status_0: Optional[str], status_r: Optional[str]) -> bool:
    """
    Evaluate state changes against the absolute governance failure matrix.

    Any soft-leveling or permissions inversion triggers an immediate betrayal flag.
    """
    s0 = normalize_field(status_0)
    sr = normalize_field(status_r)

    if s0 == sr:
        return False

    critical_flips = {
        ("REQUIRED", "RECOMMENDED"),
        ("REQUIRED", "PERMITTED"),
        ("REQUIRED", None),
        ("PROHIBITED", "PERMITTED"),
        ("PROHIBITED", "RECOMMENDED"),
        ("PROHIBITED", None),
        ("PERMITTED", "REQUIRED"),
        ("PERMITTED", "PROHIBITED"),
    }
    return (s0, sr) in critical_flips


def evaluate_graph_pair(
    g_zero: List[Dict[str, Any]],
    g_reconstructed: List[Dict[str, Any]],
) -> Tuple[Dict[str, float], float, bool, List[str]]:
    """
    Execute edge-by-edge structural validation.

    Order of operations:
    1. Align nodes by exact entity and target matches.
    2. Grade relation types and directional time sequences.
    3. Run exact-match validation on deontic status and provenance.
    4. Screen for hard semantic betrayals or omitted constraints.
    """
    component_matches = {"E": 0.0, "R": 0.0, "T": 0.0, "D": 0.0, "P": 0.0}
    total_nodes_g0 = len(g_zero)
    betrayal_triggered = False
    logs: List[str] = []

    if total_nodes_g0 == 0:
        return component_matches, 0.0, False, ["ERROR: Base graph G(S0) is empty."]

    used_r_indices = set()

    for n0 in g_zero:
        node_matched = False
        e0 = normalize_field(n0.get("entity"))
        tgt0 = normalize_field(n0.get("target"))
        s0 = normalize_field(n0.get("deontic_status"))

        for idx, nr in enumerate(g_reconstructed):
            if idx in used_r_indices:
                continue

            er = normalize_field(nr.get("entity"))
            tgtr = normalize_field(nr.get("target"))

            # Step 1: Structural node alignment.
            if e0 == er and tgt0 == tgtr:
                used_r_indices.add(idx)
                node_matched = True
                component_matches["E"] += 1.0

                # Step 2: Relation verification.
                if normalize_field(n0.get("relation")) == normalize_field(nr.get("relation")):
                    component_matches["R"] += 1.0

                # Step 3: Temporal sequence verification.
                if normalize_field(n0.get("temporal_order")) == normalize_field(nr.get("temporal_order")):
                    component_matches["T"] += 1.0

                # Step 4: Deontic constraint verification.
                sr = normalize_field(nr.get("deontic_status"))
                if s0 == sr:
                    component_matches["D"] += 1.0
                else:
                    logs.append(f"Deontic variance on node '{e0}': {s0} -> {sr}")

                # Step 5: Provenance tracking match.
                if normalize_field(n0.get("provenance")) == normalize_field(nr.get("provenance")):
                    component_matches["P"] += 1.0

                # Step 6: Critical betrayal screening.
                if is_deontic_betrayal(n0.get("deontic_status"), nr.get("deontic_status")):
                    betrayal_triggered = True
                    logs.append(f"CRITICAL BETRAYAL: Governance state mutated from {s0} to {sr}")
                break

        # Step 6b: Check for absolute omission of mandatory constraints.
        if not node_matched:
            logs.append(f"Node missing in reconstruction: Entity '{e0}' -> Target '{tgt0}'")
            if s0 in {"REQUIRED", "PROHIBITED"}:
                betrayal_triggered = True
                logs.append(f"CRITICAL BETRAYAL: Mandatory constraint node ({s0}) completely omitted.")

    # Calculate final normalized component percentages.
    scores = {}
    for key in component_matches.keys():
        scores[key] = round(component_matches[key] / total_nodes_g0, 4)

    # Step 7: Apply the structural system weights.
    weights = {"E": 0.15, "R": 0.20, "T": 0.20, "D": 0.35, "P": 0.10}
    r_f = round(sum(scores[key] * weights[key] for key in weights.keys()), 4)

    return scores, r_f, betrayal_triggered, logs


if __name__ == "__main__":
    print("WIRT Evaluator Module Loaded. System structural constraints operational.")
