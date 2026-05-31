# Read-Path Authority Firewall

**Status:** Draft research note, design only. Nothing here is implemented. Do not cite as an existing system component.
**Date:** 2026-05-31
**Layer:** Governance / consumption boundary
**Depends on:** `quarantine.py` (evidence boundary), `derivative_metadata_ledger.py` (testimony boundary)
**Relates to:** 51/49 anchor (T-03), confidence decay (lambda=0.8), Drift Log 2026-05-14 (recursive reversion)

## Core Thesis

A metadata system can preserve evidence at rest while still exercising authority through retrieval, ranking, and promotion influence. Therefore, governance must constrain not only writes to the source ledger, but also reads from the derivative ledger.

The DML closed write-side contamination: generated metadata cannot mutate the raw record. It did not close decision influence. Metadata can leave the source byte-identical while still controlling which evidence gets seen, prioritized, promoted, or ignored.

## The Distinction This Layer Rests On

**Evidence integrity is a storage property. Authority is a workflow property.**

These are enforced in different places. The DML enforces the first at the storage layer. The Read-Path Authority Firewall enforces the second at the consumption layer.

**The 51/49 boundary is enforced where metadata is consumed, not only where metadata is created.**

This relocates the load-bearing constraint. The DML lets the AI interpret freely at write time. `possible_task`, `summary_candidate`, and `classification` are all permitted because they carry no authority as stored. Authority is acquired, or not, on the read path. T-03's Renderer-not-Interpreter line is therefore a property of this layer, not the DML.

## Threat Model

Authority leaks while evidence stays byte-identical through two channel families.

### Surfacing Channels

Testimony shapes what the human attends to:

- ranking
- summarizing
- grouping
- default views
- promotion prompts
- review order

### Suppression Channels

Testimony shapes what the human never attends to:

- filtering
- demotion
- exclusion from default view
- fold placement

Suppression is higher risk because its effect is invisible to the decision-maker. A disclosed ranking still lets a human see and reweigh a record. A record filtered out by a derivative `risk_flag` is never seen and never reweighed. The human cannot correct an exclusion they do not know occurred. Any governance that only controls surfacing leaves the larger hole open.

## Two Consumers, Two Regimes

### Read Path to Human Decision

Risk: anchoring and suppression.

Controls:

- raw-first ordering
- disclosure of testimony status
- disclosure of ranking basis
- recoverability of suppressed records
- capture of decision sequence

### Read Path to Machine Derivation

Risk: recursive drift. The May 14 reversion vector reappears one layer up. Every node can pass the DML invariant individually while the chain drifts off evidence.

Controls:

- provenance-chain preservation
- evidence-distance tracking
- distance-based attenuation

## Control Classes

1. **Disclosure:** make influence visible through status labels, ranking basis, and recursion flags.
2. **Ordering:** bound when testimony enters the decision so an uninfluenced prior exists.
3. **Measurement:** quantify influence after the fact through decision logs and ablation.
4. **Recoverability:** make suppression auditable. The hidden set must be enumerable.

## Rules

Each rule states its enforcement type: **structural** (impossible to violate by construction) or **audited** (violation detectable after the fact). The DML worked because it was structural. This layer should reach for structural wherever possible.

### 1. Raw-First Review Mode Must Exist

Raw-first review mode must exist and be the default for canonical promotion.

Enforcement: Ordering. Structural for mode availability, audited for default usage.

Failure signature: a promotion event with no recorded pre-testimony state.

### 2. Testimony Is Never Returned Bare

The read API yields derivative metadata only inside a non-strippable provenance envelope:

```json
{
  "kind": "classification",
  "source_id": "clip_001",
  "source_sha256": "...",
  "evidence_distance": 1,
  "recursion_flag": false,
  "ranking_basis": "raw_first"
}
```

Enforcement: Disclosure. Structural.

Failure signature: any read path that produces testimony without its envelope.

### 3. AI-Ranked Views Must Disclose Ranking Basis

The ranking key is part of the envelope and visible at the point of consumption.

Enforcement: Disclosure. Structural.

Failure signature: a ranked view whose ordering key is null or unrecorded.

### 4. Promotion Decisions Record Testimony Visibility and Order

The log must capture whether the reviewer saw raw or testimony first, and what was visible when the decision was made. A simple boolean is not enough.

Enforcement: Measurement. Structural, via log-write gating.

Failure signature: a promotion event with a null visibility or sequence field.

### 5. Derivative Chains Preserve and Attenuate Distance from Source

`evidence_distance` equals interpretation hops back to raw. Distance is recorded and reduces the derivative's standing in any ranked view, bound to the existing lambda=0.8 decay. Beyond a depth threshold, testimony is hard-labeled speculative or blocked from default views.

Enforcement: Measurement plus Ordering. Structural.

Failure signature: a derivative with undefined `evidence_distance`.

### 6. Summaries of Summaries Are Marked Recursive Testimony

Any derivative at depth greater than 1 carries `recursion_flag = true`.

Enforcement: Disclosure. Structural.

Failure signature: a depth greater than 1 derivative with no recursion flag.

### 7. Suppression Must Be Recoverable

Any derivative-driven exclusion from a default view must be enumerable on demand: "show me what the interpretation hid." A filtered view is permitted only if its complement, the suppressed set, is one query away.

Enforcement: Recoverability. Structural.

Failure signature: a default view that filters by metadata with no path to the suppressed set.

### 8. Authority Is Measured by Ablation

For machine consumers, run the pipeline with testimony present versus hidden and compare outputs. This is a clean A/B.

For human consumers, clean ablation is impossible because a reviewer cannot unsee testimony. Use cohort ablation (raw-first versus assisted reviewers, compare promoted-set distributions) or sequential-prior capture (record the reviewer's lean before testimony, compare to the final decision).

Enforcement: Measurement. Audited.

Failure signature: an automated consumer with no ablation baseline, or a human review surface with no cohort or sequential baseline.

## Enforcement Model: Structural vs. Audited

The firewall's strength is the share of rules that are structural rather than aspirational. The mechanism that makes most of them structural is the **non-strippable provenance envelope**: testimony cannot leave the derivative store except wrapped, and the wrapper carries everything disclosure, ordering, and recursion rules need.

If the read API physically cannot return bare testimony, rules 2, 3, 5, and 6 hold by construction rather than by reviewer discipline.

The genuinely audited rules, raw-first default usage, promotion sequence logging, and ablation, cannot be made fully structural because they concern human behavior and post-hoc analysis. For those, governance is detectability: the failure signature must be a queryable absence.

## Measuring Authority: The Counterfactual and Its Limit

If the promoted set changes when AI testimony is hidden, the AI had decision influence.

This is the operational definition of authority for this layer. A changed promoted-set is not a failure. It means authority was exercised, and the requirement is that the exercise be measured, disclosed, and bounded, not eliminated.

The counterfactual runs clean only against machine consumers. Against humans it degrades to statistical proxies, such as cohort or sequential-prior tests, which detect aggregate influence but cannot prove a single decision was uninfluenced. This is an honest limit of the doctrine, not a defect to paper over: a human who has read the summary holds it whether or not the log says so.

## Success Criterion

**Useful-and-zero-authority is probably impossible. Useful-and-governed-authority is the real target.**

The firewall does not aim to drive influence to zero. It aims for **reconstructable authority**. Given the logs, the system can answer "would this record have been promoted without AI testimony?" for machine consumers, and "was this decision raw-first or testimony-anchored, and what was hidden at the time?" for human consumers.

The DML provides the hard floor: evidence integrity. This layer governs the slope above the floor and keeps it inspectable, so the human stays at 51%.

## Open Questions

- **`evidence_distance` definition:** Hops to raw is the obvious metric; derivatives drawing on multiple sources at different depths need a precise rule: max, mean, weighted, or another model.
- **Attenuation curve:** lambda=0.8 is the write-side decay. Read-side standing may require the same curve or a steeper drop.
- **Envelope schema as formal contract:** Specify and test this like the DML invariant. A future `test_read_path_firewall.py` should assert that the read API cannot return bare testimony.
- **Cohort design for human ablation:** Split reviewers without starving the raw-first cohort of assistance that makes the queue tractable.
- **Suppression-set cost:** Rule 7 implies the suppressed complement is always materializable. At corpus scale this may be expensive. Bound or index it.

#RenderedReality
