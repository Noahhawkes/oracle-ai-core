# Continuity Protocol API Surface Draft

Status: Experimental

## Purpose

This document defines a minimal API surface for continuity governance systems.

The goal is interoperability between:

- AI agents
- synthetic media systems
- renderers
- governance engines
- provenance validators
- continuity-aware orchestration layers

## Core Endpoints

### POST /evaluate

Evaluate an identity-affecting event.

Input:

```json
{
  "event": {
    "event_type": "identity_event",
    "text": "Maintain immutable provenance anchors"
  },
  "prior_state": {
    "self_model": "Required continuity verification"
  }
}
```

Output:

```json
{
  "continuity_status": "ACCEPTED",
  "recommendation": "ACCEPT",
  "drift_score": 0.0,
  "ledger_integrity": true
}
```

### POST /report

Generate a governance report from a continuity verdict.

### POST /fork

Request a governed continuity fork.

### GET /ledger/head

Return current continuity ledger head.

### GET /snapshot/latest

Return latest identity snapshot metadata.

## Security Guidance

Production deployments should:

- use deterministic canonical serialization
- replace prototype HMAC signing with Ed25519
- validate provenance before rendering
- preserve append-only ledger integrity
- maintain auditable fork lineage

## Non-Goals

This API surface does not define:

- consciousness
- legal identity
- metaphysical personhood
- biometric authentication
