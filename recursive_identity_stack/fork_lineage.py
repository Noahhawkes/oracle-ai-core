from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class ForkRecord:
    fork_id: str
    parent_identity_id: str
    parent_hash: str
    divergence_timestamp: str
    declared_reason: str


class ForkManager:
    def create_fork(
        self,
        parent_identity_id: str,
        parent_hash: str,
        declared_reason: str,
    ) -> ForkRecord:
        return ForkRecord(
            fork_id=str(uuid.uuid4()),
            parent_identity_id=parent_identity_id,
            parent_hash=parent_hash,
            divergence_timestamp=datetime.utcnow().isoformat(),
            declared_reason=declared_reason,
        )
