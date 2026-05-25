import copy
import hashlib
import json
from datetime import datetime


class SnapshotManager:
    def __init__(self):
        self.snapshots = []

    def create_snapshot(self, identity_state: dict):
        frozen_state = copy.deepcopy(identity_state)

        snapshot_hash = hashlib.sha256(
            json.dumps(frozen_state, sort_keys=True).encode()
        ).hexdigest()

        snapshot = {
            "timestamp": datetime.utcnow().isoformat(),
            "snapshot_hash": snapshot_hash,
            "state": frozen_state,
        }

        self.snapshots.append(snapshot)
        return snapshot

    def latest(self):
        if not self.snapshots:
            return None

        return self.snapshots[-1]
