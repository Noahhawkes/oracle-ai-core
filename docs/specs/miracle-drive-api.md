# Miracle Drive API Specification

**Path:** `docs/specs/miracle-drive-api.md`  
**Status:** System-Generated API Draft  
**Canon Gate:** Unverified until Noah review  
**Lane:** Specs

## Purpose

Define the first API surface for Miracle Drive / Eternal Drive.

The API exists to capture lived fragments, tag state context, require OIRV separation, enforce sober review, and prevent high-salience or altered-state material from becoming canon without human approval.

Core rule:

> Capture is allowed. Canon requires review. Work identity is protected.

## Design Principles

1. Origin governs meaning.
2. Doctrine governs constraints.
3. Specs govern execution.
4. Schemas govern machine legibility.
5. Reviews preserve critique.
6. The code serves the room, not the other way around.
7. AI may interpret, but the subject governs meaning.
8. High-state capture is permitted, but promotion is locked until review.

## Core Entities

### Capture

A raw or semi-raw fragment of lived reality, thought, AI output, sleep-state cognition, work insight, or media.

Examples:

- voice note
- text note
- transcript
- photo
- video
- AI chat excerpt
- Gmail excerpt
- Drive document reference
- sleep thought
- waking thought
- work insight

### State Context

The condition around the capture.

Examples:

- sober
- THC
- nicotine_heavy
- sleep_deprived
- pre_sleep
- half_sleep
- waking
- dream_fragment
- high_salience_ai_loop
- workday
- work_trip
- family_time

### OIRV Record

The epistemic labeling layer.

- Observed: directly present in evidence.
- Inferred: reasoned from evidence.
- Recognized: matched to known pattern.
- Verified: checked against source, file, database, record, or human confirmation.

### Review

A human-controlled evaluation event that can approve, reject, archive, correct, or promote a capture.

### Canon Decision

A 51/49 human-controlled promotion event.

AI cannot canonize alone.

## API Version

Base path:

```text
/api/v1
```

## Authentication

MVP assumption:

- Single-user local-first app.
- Auth can be deferred for local prototype.

Future:

- OAuth / Sign in with Apple
- encrypted local storage
- optional cloud sync
- user-owned export keys

## Endpoints

## 1. Create Capture

```http
POST /api/v1/captures
```

Creates a raw capture. All captures default to `capture_only` unless explicitly created as a normal sober/work-safe note.

### Request

```json
{
  "source": "voice",
  "content": "I woke up thinking about the API as a gate between thought and canon.",
  "media_refs": [],
  "state_context": ["waking", "high_salience_ai_loop"],
  "work_context": "off_duty",
  "sleep_context": "waking",
  "tags": ["api", "miracle_drive", "thought_capture"],
  "user_note": "Captured immediately after waking."
}
```

### Response

```json
{
  "id": "cap_20260531_000001",
  "created_at": "2026-05-31T00:00:00Z",
  "source": "voice",
  "canon_status": "capture_only",
  "review_required": true,
  "promotion_locked": true,
  "state_context": ["waking", "high_salience_ai_loop"],
  "work_context": "off_duty",
  "sleep_context": "waking"
}
```

## 2. List Captures

```http
GET /api/v1/captures
```

Optional filters:

```text
?canon_status=capture_only&review_required=true&state_context=thc
```

### Response

```json
{
  "items": [
    {
      "id": "cap_20260531_000001",
      "created_at": "2026-05-31T00:00:00Z",
      "source": "voice",
      "summary": "Waking thought about API as gate between thought and canon.",
      "canon_status": "capture_only",
      "review_required": true,
      "promotion_locked": true
    }
  ]
}
```

## 3. Get Capture

```http
GET /api/v1/captures/{capture_id}
```

Returns the capture, state context, OIRV record, review status, and audit history.

## 4. Add OIRV Analysis

```http
POST /api/v1/captures/{capture_id}/oirv
```

Adds an OIRV analysis record. AI-generated OIRV must be labeled as system-generated.

### Request

```json
{
  "generated_by": "ai",
  "model": "gpt-5.5-thinking",
  "observed": [
    "Noah captured a waking thought about the API."
  ],
  "inferred": [
    "The API is being framed as a canon gate."
  ],
  "recognized": [
    "This matches the Miracle Drive doctrine that capture is allowed but canon requires review."
  ],
  "verified": [],
  "notes": "No external verification performed."
}
```

### Response

```json
{
  "capture_id": "cap_20260531_000001",
  "oirv_id": "oirv_000001",
  "status": "added",
  "canon_status": "capture_only"
}
```

## 5. Submit Human Review

```http
POST /api/v1/captures/{capture_id}/reviews
```

Human review is required before promotion.

### Request

```json
{
  "reviewer": "Noah",
  "decision": "approve_for_archive",
  "corrections": [
    "Keep as research note only. Do not promote to doctrine yet."
  ],
  "review_state": "sober_review",
  "notes": "Reviewed after baseline state returned."
}
```

### Decision Values

- approve_for_archive
- reject
- promote_to_doctrine_candidate
- promote_to_spec_candidate
- mark_private
- needs_more_evidence
- delete

### Response

```json
{
  "capture_id": "cap_20260531_000001",
  "review_id": "rev_000001",
  "decision": "approve_for_archive",
  "canon_status": "archived",
  "promotion_locked": true
}
```

## 6. Promote Capture

```http
POST /api/v1/captures/{capture_id}/promote
```

Promotion requires human review and cannot occur if state policy blocks promotion.

### Request

```json
{
  "target_lane": "doctrine",
  "target_path": "docs/doctrine/miracle-drive/state-sleep-career-continuity.md",
  "promotion_reason": "Reviewed sober and accepted as doctrine candidate.",
  "human_confirmation": true
}
```

### Response

```json
{
  "capture_id": "cap_20260531_000001",
  "promoted": false,
  "reason": "Promotion locked. Capture requires additional review or explicit Noah confirmation."
}
```

## 7. Check Boundary Status

```http
POST /api/v1/boundary/check
```

Checks whether a proposed action violates state, work, or family boundaries.

### Request

```json
{
  "action": "promote_capture",
  "state_context": ["thc", "nicotine_heavy", "high_salience_ai_loop"],
  "work_context": "work_trip",
  "target_lane": "doctrine"
}
```

### Response

```json
{
  "allowed": false,
  "severity": "critical",
  "reason": "No THC on work trips. No doctrine promotion during altered or work-risk state.",
  "required_action": "capture_only_and_sober_review"
}
```

## 8. Create AI Session Log

```http
POST /api/v1/ai-sessions
```

Logs an AI interaction session.

### Request

```json
{
  "start_time": "2026-05-31T00:00:00Z",
  "end_time": "2026-05-31T01:30:00Z",
  "purpose": "research",
  "state_context": ["sober"],
  "work_context": "off_duty",
  "summary": "Worked on Miracle Drive API spec."
}
```

### Response

```json
{
  "id": "ais_000001",
  "canon_status": "capture_only",
  "review_required": false
}
```

## 9. Create Boundary Rule

```http
POST /api/v1/boundary/rules
```

Creates a boundary rule.

### Request

```json
{
  "name": "No THC on work trips",
  "condition": {
    "state_context_contains": "thc",
    "work_context_equals": "work_trip"
  },
  "action": "block_promotion_and_alert",
  "severity": "critical",
  "source": "Ashley boundary + Noah confirmation"
}
```

### Response

```json
{
  "id": "rule_000001",
  "status": "active"
}
```

## 10. Export Capture

```http
POST /api/v1/captures/{capture_id}/export
```

Exports a capture to a destination after review.

### Request

```json
{
  "destination": "github_issue",
  "target": "Noahhawkes/oracle-ai-core",
  "include_raw": false,
  "include_oirv": true,
  "include_review_history": true
}
```

### Response

```json
{
  "exported": true,
  "destination": "github_issue",
  "external_ref": "issue_000"
}
```

## Canon Status Values

```text
capture_only
pending_sober_review
archived
approved
rejected
doctrine_candidate
spec_candidate
canon
private
deleted
```

## Work Context Values

```text
off_duty
workday
work_trip
customer_facing
driving
meeting
family_time
unknown
```

## Sleep Context Values

```text
none
pre_sleep
half_sleep
waking
dream_fragment
post_sleep
sleep_interruption
unknown
```

## State Context Values

```text
sober
thc
nicotine_light
nicotine_moderate
nicotine_heavy
sleep_deprived
pre_sleep
half_sleep
waking
dream_fragment
high_salience_ai_loop
agitated
calm
focused
scattered
family_time
work_risk
unknown
```

## Default Policy Rules

1. All captures default to `capture_only`.
2. THC captures require sober review.
3. Nicotine-heavy plus high-salience AI loop requires review before promotion.
4. Sleep-state captures require review before promotion.
5. Work-trip plus THC blocks promotion and triggers critical alert.
6. Workday plus THC blocks promotion and triggers critical alert.
7. Family claims require human confirmation before canon.
8. AI-generated analysis can never become Noah-primary without re-authoring or explicit promotion.
9. Deletion must remain available unless legal hold or explicit archive lock is applied.
10. Export to GitHub requires review unless the target is clearly marked system-generated.

## MVP Storage Model

Recommended local-first tables:

- captures
- media_refs
- oirv_records
- reviews
- promotions
- boundary_rules
- ai_sessions
- audit_events

## Audit Event Examples

```json
{
  "id": "audit_000001",
  "timestamp": "2026-05-31T00:00:00Z",
  "actor": "system",
  "event": "capture_created",
  "capture_id": "cap_20260531_000001",
  "details": {
    "canon_status": "capture_only",
    "promotion_locked": true
  }
}
```

## Security and Privacy Requirements

- Local-first storage preferred.
- Health and state data should be encrypted at rest.
- No employer reporting.
- No automatic third-party export.
- User controls deletion.
- Family-related records should default to private.
- Altered-state records should default to private and review-locked.

## Non-Goals for MVP

- No automatic medical diagnosis.
- No addiction scoring.
- No employer compliance reporting.
- No automated canonization.
- No continuous surveillance.
- No forced social posting.

## Acceptance Criteria

The API is acceptable when:

- A raw thought can be captured safely.
- State context can be tagged.
- OIRV can be added without promoting the capture.
- Human review can approve, reject, archive, or escalate.
- High-state material is blocked from automatic canonization.
- Work-trip and workday THC boundaries are enforced.
- Export is controlled and auditable.
- The user retains 51/49 authority over meaning.

## Core Lines

Capture is allowed. Canon requires review. Work identity is protected.

The API is not a memory machine. It is a boundary machine for memory.

AI may interpret, but the subject governs meaning.

The code serves the room, not the other way around.
