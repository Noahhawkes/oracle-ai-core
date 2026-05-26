# CRP-002 — Continuity View Schema

**Status:** Minimal viable schema  
**Scope:** Data contract between the Continuity Engine and downstream LLMs or agents  
**Serialization:** JSON-compatible objects

CRP-002 defines the minimal schema surface for continuity-preserving retrieval and bounded synthesis.

It covers:

- `ContinuityRecord`
- `ContinuityView`
- `Gap`
- `Conflict`
- `ValidationStatus`
- `ProtocolState`
- `InferenceLevel`
- `BoundedSynthesisResponse`

## 1. ContinuityRecord

```json
{
  "artifact_id": "string",
  "subject_id": "string",
  "artifact_type": "string",
  "content_pointer": "string",
  "timestamp": "string",
  "continuity_scope": "string",
  "provenance": {
    "issuer": "string",
    "method": "string",
    "captured_at": "string",
    "chain_of_custody": ["string"]
  },
  "integrity_hash": "string",
  "validation_status": "VALID_PRIMARY | VALID_DERIVED | PROVENANCE_UNVERIFIED | REJECTED",
  "lineage": ["string"],
  "uncertainty": {
    "confidence_score": "number"
  }
}
```

## 2. Gap

```json
{
  "start": "string",
  "end": "string",
  "reason": "NO_PRIMARY_ARTIFACTS | OUT_OF_SCOPE | FILTERED_BY_POLICY"
}
```

## 3. Conflict

```json
{
  "field": "string",
  "records": ["artifact_id_1", "artifact_id_2"],
  "description": "string"
}
```

## 4. ValidationStatus

```json
[
  "VALID_PRIMARY",
  "VALID_DERIVED",
  "PROVENANCE_UNVERIFIED",
  "REJECTED"
]
```

## 5. ProtocolState

```json
[
  "OK_CONTINUITY_VIEW",
  "PARTIAL_CONTINUITY",
  "NO_PRIMARY_ARTIFACTS",
  "IDENTITY_AMBIGUOUS",
  "CONTINUITY_BREAK"
]
```

## 6. InferenceLevel

```json
[
  "DIRECT",
  "WEAK_INFERENCE",
  "SPECULATIVE_FORBIDDEN"
]
```

## 7. ContinuityView

The Continuity View is the core object. It is the only identity-bound context downstream LLMs or agents are allowed to consume.

```json
{
  "subject_id": "string",
  "requested_scope": "string",
  "protocol_state": "ProtocolState",
  "artifacts": ["ContinuityRecord"],
  "gaps": ["Gap"],
  "conflicts": ["Conflict"],
  "constraints": {
    "allow_inference": true,
    "forbid_speculation": true,
    "require_citations": true
  }
}
```

## 8. BoundedSynthesisResponse

The BoundedSynthesisResponse is the only allowed generative output from a continuity-bound synthesis layer.

```json
{
  "content": "string",
  "source_refs": [
    {
      "artifact_id": "string",
      "inference_level": "InferenceLevel"
    }
  ],
  "surfaced_gaps": ["Gap"],
  "surfaced_conflicts": ["Conflict"],
  "protocol_state": "ProtocolState"
}
```

## Design Requirements

CRP-002 must remain:

- implementable
- testable
- serializable
- enforceable
- auditable
- safe for LLM boundary control

## Core Rule

Continuity Engine → Continuity View → Bounded Synthesis → Auditable Output

Downstream systems must not bypass the Continuity View boundary for identity-bound generation.
