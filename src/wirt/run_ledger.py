#!/usr/bin/env python3
"""
Witnessed Information Resilience Test (WIRT) - Run Ledger.

Transforms raw WIRT run logs into a deterministic SHA-256 hash-linked ledger.
This module secures the record of drift after the evaluator has measured it.
"""

import argparse
import hashlib
import json
import os
from typing import Any, Dict, List, Optional


def canonicalize(obj: Any) -> str:
    """Return a deterministic JSON string for hashing."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_json(obj: Any) -> str:
    """Compute the SHA-256 hash of a canonicalized JSON object."""
    return hashlib.sha256(canonicalize(obj).encode("utf-8")).hexdigest()


def build_ledger(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Transform raw run-log entries into a hash-linked WIRT ledger."""
    ledger: List[Dict[str, Any]] = []
    prev_hash: Optional[str] = None

    for index, entry in enumerate(entries):
        entry_hash = sha256_json(entry)
        ledger_node = {
            "ledger_index": index,
            "prev_hash": prev_hash,
            "entry_hash": entry_hash,
            "entry": entry,
        }
        ledger_node_hash = sha256_json(ledger_node)
        ledger_node["ledger_node_hash"] = ledger_node_hash
        ledger.append(ledger_node)
        prev_hash = ledger_node_hash

    return ledger


def verify_ledger(ledger: List[Dict[str, Any]]) -> bool:
    """Verify entry hashes and prev_hash links across the full ledger."""
    previous_node_hash: Optional[str] = None

    for expected_index, node in enumerate(ledger):
        if node.get("ledger_index") != expected_index:
            return False

        if node.get("prev_hash") != previous_node_hash:
            return False

        entry = node.get("entry")
        if node.get("entry_hash") != sha256_json(entry):
            return False

        stored_node_hash = node.get("ledger_node_hash")
        node_without_hash = {
            "ledger_index": node.get("ledger_index"),
            "prev_hash": node.get("prev_hash"),
            "entry_hash": node.get("entry_hash"),
            "entry": entry,
        }
        calculated_node_hash = sha256_json(node_without_hash)

        if stored_node_hash != calculated_node_hash:
            return False

        previous_node_hash = stored_node_hash

    return True


def load_json(path: str) -> Any:
    """Load JSON from a UTF-8 file."""
    with open(path, "r", encoding="utf-8") as input_file:
        return json.load(input_file)


def write_json(path: str, payload: Any) -> None:
    """Write JSON to a UTF-8 file, creating parent directories as needed."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    with open(path, "w", encoding="utf-8") as output_file:
        json.dump(payload, output_file, indent=2, ensure_ascii=False)


def summarize_ledger(ledger: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Return a compact summary of a built ledger."""
    return {
        "entries": len(ledger),
        "genesis_hash": ledger[0]["ledger_node_hash"] if ledger else None,
        "head_hash": ledger[-1]["ledger_node_hash"] if ledger else None,
        "verified": verify_ledger(ledger),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build or verify a WIRT hash-linked run ledger.")
    parser.add_argument("--input", required=True, help="Path to raw WIRT run log JSON or ledger JSON.")
    parser.add_argument("--output", help="Path to write the generated ledger JSON.")
    parser.add_argument("--verify-only", action="store_true", help="Verify an existing ledger instead of building one.")
    args = parser.parse_args()

    payload = load_json(args.input)

    if args.verify_only:
        if not isinstance(payload, list):
            raise ValueError("Ledger payload must be a JSON array.")
        verified = verify_ledger(payload)
        print(json.dumps({"verified": verified, "entries": len(payload)}, indent=2))
        raise SystemExit(0 if verified else 1)

    if not isinstance(payload, list):
        raise ValueError("Run log payload must be a JSON array.")

    ledger = build_ledger(payload)
    summary = summarize_ledger(ledger)

    if args.output:
        write_json(args.output, ledger)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
