# Judgment Drift

**Status:** Public canon — v0.1

**Scope:** Extension of the discriminator layer from fact drift into decision and judgment drift.

## Definition

Judgment drift occurs when a reconstruction produces a decision, recommendation, interpretation, or priority that diverges from documented human judgment while remaining factually plausible and stylistically convincing.

Judgment drift is more dangerous than simple factual error because it may break no explicit exclusion. The output may sound right, cite real facts, and match the author's cadence, while still reaching a decision the author would not have made from the same context.

## Why this matters

A future system may learn to mimic voice, cadence, humor, slogans, values, and surface preferences. Those are easy to imitate.

Live judgment is harder. Judgment is not a static content object. It is a function applied to a context.

A style-complete, judgment-empty reconstruction is one of the highest-risk failure modes. It can sound like continuity while making non-continuous decisions.

Therefore, the next target is not generator capture.

The target is judgment-drift detection.

## Generator trap

A naive identity generator tries to recreate the author directly.

That is unsafe.

The easily captured layers are often the least identity-bearing:

- voice
- cadence
- humor
- slogans
- repeated phrases
- stated values

The hardest layers are the most identity-bearing:

- live judgment
- case-specific discernment
- moral weighting
- contradiction handling
- priority under pressure
- refusal boundaries
- what the author would not do even when plausible

If a system captures the easy layers and misses the hard layers, it creates a fluent impersonation surface.

That is reconstruction failure with the author's face on it.

## Discriminator extension

The safe near-term goal is not to generate Noah's judgment.

The safe near-term goal is to detect when a generated decision diverges from documented Noah judgment.

This requires a corpus of documented decisions, not merely summaries.

Each decision record should include:

- context
- available options
- chosen action
- rejected alternatives
- reason for choice
- constraints in force
- emotional or ethical friction, if explicitly documented
- outcome, if known
- provenance and date

The system then checks a new reconstruction against documented decision patterns.

## Required distinction

Do not confuse:

- factual consistency
- stylistic similarity
- value quotation
- judgment continuity

A reconstruction can be factually consistent, stylistically similar, and value-aligned in language while still drifting in judgment.

## Judgment Drift Test

A reconstruction should be flagged if it:

1. Makes a decision opposite to documented prior choices under similar constraints.
2. Treats a rejected alternative as preferred without new evidence.
3. Collapses a known tradeoff into a clean answer.
4. Quotes values while violating the documented priority order.
5. Sounds like the author but chooses unlike the author.
6. Uses emotional coherence to override documented refusal boundaries.
7. Generates a recommendation without retrieving relevant decision records.

## Success condition

The discriminator succeeds when it can say:

- This decision is consistent with documented judgment.
- This decision is unsupported by documented judgment.
- This decision conflicts with documented judgment.
- This case is novel and cannot be resolved from the record.

The fourth outcome is essential. Novel cases must not be filled with invented certainty.

## Boundary

Judgment-drift detection is not identity generation.

It does not claim to know what the person would do in every future case.

It only compares a reconstruction against documented cases and flags divergence.

This preserves the human as the live integrator while externalizing part of the witness function.

## One-line definition

> Judgment drift is the failure mode where a reconstruction sounds like the author and uses real facts, but makes a decision that diverges from documented human judgment.

---

*The goal is recognition and drift detection, not regeneration. A system that cannot admit novelty cannot preserve judgment faithfully.*
