import hashlib
import hmac
import json
from dataclasses import dataclass
from typing import Dict


@dataclass
class AttestationResult:
    payload_hash: str
    signature: str
    signer_id: str


class HMACAttestationService:
    """Lightweight signing layer for prototype continuity events.

    This intentionally uses HMAC from the Python standard library so the prototype
    has no external dependency. Production versions should replace this with
    Ed25519 signing and DID-bound public key verification.
    """

    def __init__(self, signer_id: str, secret: str):
        self.signer_id = signer_id
        self.secret = secret.encode("utf-8")

    def _canonicalize(self, payload: Dict) -> bytes:
        return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")

    def sign(self, payload: Dict) -> AttestationResult:
        canonical_payload = self._canonicalize(payload)
        payload_hash = hashlib.sha256(canonical_payload).hexdigest()
        signature = hmac.new(self.secret, canonical_payload, hashlib.sha256).hexdigest()

        return AttestationResult(
            payload_hash=payload_hash,
            signature=signature,
            signer_id=self.signer_id,
        )

    def verify(self, payload: Dict, signature: str) -> bool:
        expected = self.sign(payload).signature
        return hmac.compare_digest(expected, signature)
