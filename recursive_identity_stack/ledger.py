import hashlib
import json
from datetime import datetime


class ContinuityLedger:
    def __init__(self):
        self.chain = []

    def _hash(self, payload: dict) -> str:
        encoded = json.dumps(payload, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()

    def append(self, event_type: str, content: dict):
        previous_hash = self.chain[-1]["hash"] if self.chain else "GENESIS"

        block = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "content": content,
            "previous_hash": previous_hash
        }

        block_hash = self._hash(block)
        block["hash"] = block_hash

        self.chain.append(block)
        return block

    def verify_integrity(self) -> bool:
        for i in range(1, len(self.chain)):
            if self.chain[i]["previous_hash"] != self.chain[i - 1]["hash"]:
                return False

        return True
