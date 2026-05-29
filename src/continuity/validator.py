#!/usr/bin/env python3
"""
Continuity Verification Index Validator.

Resolves canonical continuity terms from data/verification_index.json and fails
visibly when provenance is missing instead of allowing generative interpolation.
"""

import argparse
import json
import os
from typing import Any, Dict


class ContinuityValidator:
    """Resolve identity-specific framework terms against a verification index."""

    def __init__(self, index_path: str):
        self.index_path = index_path
        self.records: Dict[str, Dict[str, Any]] = {}
        self._load_index()

    def _load_index(self) -> None:
        if not os.path.exists(self.index_path):
            raise FileNotFoundError(f"Critical error: verification index missing at {self.index_path}")

        with open(self.index_path, "r", encoding="utf-8") as index_file:
            data = json.load(index_file)

        for record in data.get("verification_records", []):
            canonical_term = record["canonical_term"]
            self.records[self._normalize(canonical_term)] = record

    @staticmethod
    def _normalize(term: str) -> str:
        return term.strip().lower()

    def resolve_term(self, term: str) -> Dict[str, Any]:
        normalized_term = self._normalize(term)

        if normalized_term in self.records:
            record = self.records[normalized_term]
            return {
                "status": "VERIFIED",
                "term": record["canonical_term"],
                "definition": record["canonical_definition"],
                "provenance_tier": record["provenance_tier"],
                "source_paths": record["source_paths"],
                "commit_shas": record["commit_shas"],
                "confidence_policy": record["confidence_policy"],
            }

        return {
            "status": "MISSING_PROVENANCE",
            "term": term,
            "fallback_behavior": "emit_missing_provenance_error",
            "action_required": "Halt inference. Do not allow generative interpolation.",
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve a term against the continuity verification index.")
    parser.add_argument("term", help="Canonical term to resolve, such as WIRT.")
    parser.add_argument("--index", default="data/verification_index.json", help="Path to verification index JSON.")
    args = parser.parse_args()

    validator = ContinuityValidator(args.index)
    result = validator.resolve_term(args.term)
    print(json.dumps(result, indent=2))

    if result["status"] == "MISSING_PROVENANCE":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
