# Succession Authority Constitution

**Status:** Draft research specification
**Date:** 2026-05-31
**Layer:** Succession governance / post-sovereign authority boundary
**Depends on:** Evidence/Testimony separation, Read-Path Authority Firewall, Portable Custody Capsule, Quorum Authenticity Boundary

## Core Thesis

Continuity after sovereign absence is not the persistence of active will.

It is the governed separation of sovereign evidence from successor testimony.

## Corrected Anchor

Absence does not create new sovereign authority.

It creates successor authority, which must be marked as the successor's and may never contaminate the sovereign's signal.

This replaces the earlier, weaker anchor:

```text
Absence does not create new authority.
```

That earlier formulation fails under novel cases. A fixed constitution cannot anticipate every future circumstance. When the rule-set is silent, some living agent or institution must interpret, defer, or refuse. The system must therefore govern attribution rather than pretend new authority can be eliminated.

## Primary Boundary

The system may allow successors to act.

The system may not allow successor action to impersonate sovereign intent.

```text
Sovereign evidence remains sovereign evidence.
Successor interpretation remains successor testimony.
```

## Authority Classes

### 1. Sovereign-Authored Rule

Direct evidence created or explicitly authorized by the sovereign before absence.

Properties:

- highest authority
- immutable after sovereign absence
- may be referenced
- may not be rewritten
- may not be extended under the sovereign's name

### 2. Successor Interpretation

A bounded act by a named successor applying sovereign-authored evidence to a future case.

Properties:

- attributed to the successor
- linked to the sovereign evidence reviewed
- bound to a clause, rule, or domain of authority
- subject to evidence-distance decay
- never merged into sovereign-origin evidence

Required attribution format:

```text
[Successor Name], under [Succession Clause], interpreted this record as [decision].
Source evidence reviewed: [record ids + hashes].
Testimony visible: [yes/no + source ids].
Uncertainty or dissent: [noted explicitly].
```

### 3. Forbidden Impersonation

Any output that claims new sovereign intent after sovereign absence.

Forbidden forms:

- "Noah decided" when the decision occurred after Noah's absence.
- "Noah would have wanted" presented as verified sovereign intent.
- Model-generated stance presented as sovereign-authored stance.
- Successor interpretation merged into the sovereign evidence ledger.

## Pillar 1: The Interface Is Governance

The distinction between process and evidence is not clean enough.

If a successor modifies the algorithm that surfaces records, changes default views, lowers quorum requirements, or alters archive navigation, that successor is exercising interpretive authority over the sovereign signal.

Control over the read path is control over the legacy.

Therefore, any modification to:

- archive interface
- default views
- ranking mechanics
- suppression mechanics
- quorum rules
- review burdens
- promotion workflow
- successor role permissions

must be logged as a bounded, attributed successor act.

It is never merely administrative.

## Pillar 2: Evidence-Distance Decay

Attribution prevents immediate impersonation, but it does not prevent cumulative drift.

Each interpretive layer stacked on prior interpretation moves further from sovereign evidence.

The system therefore applies evidence-distance decay to succession testimony.

Let direct sovereign evidence be:

```text
E_0
```

Let interpretation depth be:

```text
n
```

Let the decay factor be:

```text
lambda = 0.8
```

Then successor interpretation weight is bounded by:

```text
E_n = lambda^n E_0
```

This prevents deeply nested interpretations from mathematically overpowering direct sovereign evidence.

Rules:

- direct sovereign evidence has distance 0
- first-generation successor testimony has distance 1
- testimony based on testimony increases distance
- distance must be visible in review
- distance greater than a defined threshold must be marked speculative
- high-distance testimony cannot override direct sovereign evidence

## Pillar 3: The Lived-Memory Limit

The system can preserve attribution indefinitely.

It cannot preserve living recognition indefinitely.

Ashley, Elijah, Ethan, Ender, Titus, and other living witnesses may hold a form of fidelity that no archive can fully automate: the ability to say, "That is not what he meant."

When living memory expires, the system loses its organic error-correction layer.

From that point forward, the archive can still preserve:

- provenance
- attribution
- hash integrity
- clause references
- testimony distance
- decision logs
- dissent records

But it cannot guarantee human fidelity to the remembered person.

The system guarantees attribution in perpetuity.

It guarantees detection of bad-faith distortion only as long as living memory or a trusted witness tradition remains able to contest the render.

This is not a defect to hide.

It is a system boundary to declare.

## Amendment Dilemma

Successors may amend successor governance.

They may not amend sovereign-origin evidence.

Permitted amendments:

- review process changes
- interface improvements
- quorum mechanics for successor acts
- archive access policies
- tooling updates
- visibility controls, if logged and reversible

Forbidden amendments:

- rewriting sovereign evidence
- reattributing successor testimony as sovereign intent
- deleting dissent to make a successor interpretation appear unanimous
- lowering attribution requirements retroactively
- removing evidence-distance markers

## Novel Case Handling

When no sovereign-authored rule directly governs a case, the system must not fabricate sovereign intent.

Allowed outcomes:

1. keep quarantined
2. mark unresolved
3. record successor interpretation
4. record dissent
5. request additional quorum
6. seal the record pending future review

Forbidden outcome:

```text
New sovereign intent generated after sovereign absence.
```

## Successor Decision Object

A successor decision must include:

```json
{
  "decision_id": "succession_decision_001",
  "successor": "name_or_role",
  "decision_type": "promote | reject | seal | keep_quarantined | amend_process",
  "sovereign_absence_state": true,
  "clause_invoked": "succession_clause_7",
  "source_evidence": [
    {
      "record_id": "clip_001",
      "source_hash_sha256": "...",
      "evidence_distance": 0
    }
  ],
  "successor_testimony_used": [
    {
      "metadata_id": "meta_001",
      "source_hash_sha256": "...",
      "evidence_distance": 1
    }
  ],
  "decision_statement": "Elijah interpreted this as promotable under clause 7.",
  "uncertainty": "noted explicitly",
  "dissent": "recorded or null",
  "promotion_claim": "successor_attributed",
  "forbidden_claim": "sovereign_decided"
}
```

## Hard Invariants

```text
Successors may execute bounded authority.
They may not manufacture sovereign will.
```

```text
The system may preserve the record.
It may not automate wisdom.
```

```text
Technology can preserve attribution.
Living memory carries the fire.
```

## Final Compression

Absence does not create new sovereign authority.

It creates successor authority.

Successor authority must be attributed, bounded, decay-aware, and forbidden from contaminating the sovereign signal.

#RenderedReality
