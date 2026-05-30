from fastapi import FastAPI
from .models import MemoryItem, Claim, AttentionRequest

app = FastAPI(title='Continuity Layer 2082')

memory_store = []

@app.get('/')
def root():
    return {
        'system': 'Continuity Layer 2082',
        'principle': 'AI learns the interface, not the soul.'
    }

@app.post('/memory')
def add_memory(item: MemoryItem):
    memory_store.append(item)
    return {'status': 'stored', 'id': item.id}

@app.get('/memory')
def list_memory():
    return memory_store

@app.post('/claims/evaluate')
def evaluate_claim(claim: Claim):
    return {
        'claim': claim.claim,
        'oirv_mode': claim.oirv_mode,
        'confidence': claim.confidence,
        'basis': claim.basis
    }

@app.post('/attention/next')
def next_attention(req: AttentionRequest):
    return {
        'prompt': req.prompt,
        'message': 'Attention engine placeholder',
        'recommended_action': 'Review active memory anchors'
    }
