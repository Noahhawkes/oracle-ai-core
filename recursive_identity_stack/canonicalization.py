import hashlib
import json
from typing import Any, Dict


def canonical_json(payload: Dict[str, Any]) -> str:
    """Return deterministic JSON for hashing, signing, and interoperability."""
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    )


def sha256_digest(payload: Dict[str, Any], prefix: bool = False) -> str:
    digest = hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()
    return f"sha256:{digest}" if prefix else digest
