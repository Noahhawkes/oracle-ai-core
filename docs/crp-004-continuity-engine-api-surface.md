# CRP-004 — Continuity Engine API Surface

**Status:** Minimal viable API surface  
**Scope:** Contract for Continuity Engine services  
**Serialization:** JSON-compatible request and response bodies

CRP-004 defines the smallest API surface required to support:

- identity binding
- artifact retrieval
- provenance validation
- continuity analysis
- continuity view generation
- bounded synthesis
- audit logging

It maps to the reference implementation layout:

```text
/schemas
/api
/engine
/examples
/tests
```

## 1. Identity Binding API

```http
POST /identity/resolve
```

Resolves a human subject into a stable `subject_id`.

### Request

```json
{
  "input": {
    "name": "string",
    "email": "string",
    "handles": ["string"]
  }
}
```

### Response

```json
{
  "output": {
    "subject_id": "string",
    "candidates": ["string"],
    "protocol_state": "OK | IDENTITY_AMBIGUOUS | SUBJECT_NOT_FOUND"
  }
}
```

## 2. Artifact Retrieval API

```http
GET /artifacts/{subject_id}
```

Returns raw ContinuityRecords before validation.

### Query Parameters

- `scope`
- `start`
- `end`
- `types`

### Response

```json
{
  "artifacts": ["ContinuityRecord"]
}
```

## 3. Provenance Validation API

```http
POST /validation/validate-records
```

Validates provenance, integrity, and lineage.

### Request

```json
{
  "input": {
    "records": ["ContinuityRecord"]
  }
}
```

### Response

```json
{
  "output": {
    "validated_records": ["ContinuityRecord"]
  }
}
```

## 4. Continuity Analysis API

```http
POST /continuity/analyze
```

Builds the continuity graph, detects gaps and conflicts, and sets protocol state.

### Request

```json
{
  "input": {
    "subject_id": "string",
    "records": ["ContinuityRecord"],
    "requested_scope": "string"
  }
}
```

### Response

```json
{
  "output": {
    "protocol_state": "ProtocolState",
    "gaps": ["Gap"],
    "conflicts": ["Conflict"]
  }
}
```

## 5. Continuity View API

```http
POST /continuity/view
```

Generates the ContinuityView object. This is the only identity-bound object downstream LLMs or agents are allowed to consume.

### Request

```json
{
  "input": {
    "subject_id": "string",
    "requested_scope": "string"
  }
}
```

### Response

```json
{
  "output": {
    "continuity_view": "ContinuityView"
  }
}
```

## 6. Bounded Synthesis API

```http
POST /synthesis/bounded
```

Consumes a ContinuityView and a task, then enforces inference and citation rules.

### Request

```json
{
  "input": {
    "continuity_view": "ContinuityView",
    "task": "string"
  }
}
```

### Response

```json
{
  "output": {
    "response": "BoundedSynthesisResponse"
  }
}
```

## 7. Audit Logging API

```http
POST /audit/log
```

Writes a continuity-bound audit event.

### Request

```json
{
  "input": {
    "event_type": "string",
    "subject_id": "string",
    "continuity_view": "ContinuityView",
    "response": "BoundedSynthesisResponse"
  }
}
```

### Response

```json
{
  "output": {
    "status": "OK"
  }
}
```

## 8. Reference Implementation Layout

```text
/schemas
  crp-002-continuity-view-schema.json
/api
  identity.ts
  artifacts.ts
  validation.ts
  continuity.ts
  synthesis.ts
  audit.ts
/engine
  identity-binding/
  provenance-validator/
  continuity-analyzer/
  view-generator/
  bounded-synthesis/
  audit-logger/
/examples
/tests
```

## Core API Rule

Downstream systems must never bypass the Continuity View boundary for identity-bound generation.

```text
Raw Archive → Continuity Engine → Continuity View → Bounded Synthesis → Auditable Output
```
