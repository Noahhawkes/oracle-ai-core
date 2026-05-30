from pydantic import BaseModel
from typing import Optional, List

class Source(BaseModel):
    source_type: str
    source_id: str
    timestamp: str

class MemoryItem(BaseModel):
    id: str
    content: str
    type: str
    oirv_mode: str
    source: Source
    confidence: float
    user_approved: bool = True

class Claim(BaseModel):
    claim: str
    oirv_mode: str
    confidence: float
    basis: List[str] = []

class AttentionRequest(BaseModel):
    prompt: str
