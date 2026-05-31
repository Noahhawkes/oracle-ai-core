# Review Artifact: Meta Quarantine Critique

**Path:** `docs/reviews/2026-05-30-meta-quarantine-critique.md`  
**Status:** Review Artifact  
**Source:** Meta.AI response relayed by Noah  
**Canon Gate:** Not canon unless promoted by Noah  
**Lane:** Reviews

## Purpose

Preserve the Meta.AI critique of the Miracle Drive / Eternal Drive quarantine model as a review artifact without promoting its proposed schema fields into the source of truth.

This file belongs in Reviews, not Specs and not Schemas.

## Observed

Meta identified four useful pieces of value:

1. **Capture asserts occurrence, not truth.**
2. **Default-quarantine over default-allow.**
3. **Git / evidence / OS analogies as builder language.**
4. **Hazmat container as product framing.**

Meta also suggested fields such as:

- `altered: bool`
- `sleep_drift: bool`
- `voice: bool`
- `confidence: 0-1`

These fields are not currently in `docs/specs/miracle-drive-api.md` and should not be treated as schema truth.

## Inferred

The critique reinforces the rule of Name After Witness.

The analogies and field names are useful lenses, but they are not canon until they pass review against the committed spec.

Miracle Drive exists to prevent exactly this failure mode: AI inventing schema during capture.

## Recognized

This maps back to Issue #11 and the five-lane model:

- Origin holds meaning.
- Specs hold execution.
- Schemas hold machine legibility.
- Reviews hold critique.

Meta's output belongs in Reviews until promoted.

## Verified

Current source of truth at the time of this review:

- `docs/specs/miracle-drive-api.md` at commit `2cf318a4668f0be86ea1e91278b595d2720bbc6c`
- `docs/README.md` at commit `9d31cba891b063ffe9dc7c8d7c1c0a0678296a13`
- Human safety protocol: Issue #9
- Quarantine-first architecture: Issue #11

Meta's proposed fields are not in those artifacts.

## Clean Separation

Plain English:

Meta threw ideas at the quarantine wall. Some stuck as useful analogies. None get to touch canon until Noah says so.

That is the system working.

## Candidate Lines

The following lines may be considered later as doctrine candidates or product language:

- Capture asserts occurrence, not truth.
- Capture is not canon.
- Quarantine is not philosophy. It is the first gate.
- You do not start by building a notepad. You start by building a hazmat container.
- Default-quarantine, then promote.

## Review Guidance

When drafting `miracle-drive-capture.schema.json`:

1. Pull from `docs/specs/miracle-drive-api.md` first.
2. Use the committed spec vocabulary before considering review suggestions.
3. Treat Meta field names as notes, not schema.
4. Promote only after explicit review.
5. Preserve the invariant that capture, review, and promotion are separate states.

## Core Line

**Capture is not canon. Quarantine is not philosophy. It is the first gate.**
