# Continuity Layer 2082 MVP

A local-first prototype for a governed personal continuity layer.

## What this MVP does

- Stores user-approved memory items with provenance.
- Tags claims using OIRV: Observed, Inferred, Recognized, Verified.
- Keeps sources, corrections, artifacts, and attention events auditable.
- Provides basic API endpoints for memory, claim evaluation, attention, and audit trail.
- Refuses to pretend that inferred content is verified.

## What this MVP does not do yet

- It does not claim consciousness.
- It does not autonomously crawl private data.
- It does not replace user judgment.
- It does not simulate identity.
- It does not make irreversible memory changes without an API call.

## Quickstart

```bash
cd continuity_layer_2082
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Core principle

AI learns the interface, not the soul.
