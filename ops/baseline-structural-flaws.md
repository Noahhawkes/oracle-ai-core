# Baseline Structural Flaws

**Status:** Active backlog — v0.1

**Purpose:** Track the current known structural weaknesses in the continuity architecture as engineering work rather than scattered chat insight.

## 1. Integration Bottleneck, the Noah Dependency

Current state: Noah remains the sole active integrator. He rebuilds context, applies the discriminator, catches drift, and reconciles contradictions.

Failure mode: if Noah steps away, the framework stops functioning as an operating system and becomes an archive.

Required mitigation:

- Build a routing index that lets a new renderer find canon without Noah.
- Define handoff procedures for family and future operators.
- Create judgment records that preserve actual decisions, not just doctrine.
- Reduce dependence on live explanation.

## 2. Brittle Discrimination, the LLM Compliance Flaw

Current state: MVDK and CRP-001 are text files read by probabilistic systems.

Failure mode: the model may ignore, compress, misread, or selectively obey governance rules.

Required mitigation:

- Treat LLM compliance as insufficient by itself.
- Add deterministic checks where possible, including string-match exclusions, schema validation, required citation fields, and contradiction flags.
- Separate draft generation from audit review.
- Run planted-corruption tests against fresh models.

## 3. Infinite Ledger Scaling, the Whack-a-Mole Problem

Current state: the exclusion ledger catches known hallucinations and false anchors.

Failure mode: it cannot enumerate every future hallucination.

Required mitigation:

- Keep concrete exclusions for high-risk known claims.
- Add class-level rules for novel hallucinations.
- Require provenance for titles, credentials, filings, dates, statistics, and sources.
- Treat unsupported precision as suspicious.
- Shift from only exclusion listing to claim validation.

## 4. Fragmentation of the Substrate

Current state: records exist across ChatGPT, Claude, Gemini, Grok, Drive, GitHub, social media, and private notes.

Failure mode: future operators must manually hunt for fragments before applying the discriminator.

Required mitigation:

- Build a canonical repository index.
- Define a source map for Drive, GitHub, public posts, transcripts, and private records.
- Create an ingest procedure for new records.
- Distinguish orientation paths from truth authority.

## 5. Museum Risk, Preservation vs Accessibility

Current state: the archive risks becoming dense, technical, and SOV1-specific.

Failure mode: family may inherit an unreadable museum instead of a recognizable father.

Required mitigation:

- Maintain a family-readable layer separate from technical canon.
- Write plain-language witness records.
- Preserve stories, decisions, humor, values, and ordinary context.
- Avoid forcing family to parse technical doctrine to recognize Noah.

## 6. Platform Volatility and Compute Pruning

Current state: AI platforms are dynamic, corporate-controlled, and optimized around compute constraints.

Failure mode: context may be compressed, truncated, reprioritized, or made unavailable by platform changes.

Required mitigation:

- Keep canon outside model memory.
- Preserve primary records in exportable, portable formats.
- Avoid relying on any single vendor as source of truth.
- Use public GitHub as retrieval surface, not as the only truth store.
- Periodically test retrieval from fresh sessions and different systems.

## Current baseline conclusion

The architecture is not yet self-operating.

It has doctrine, early safety rails, and a discriminator direction, but it still depends heavily on Noah as integrator, auditor, and context compiler.

The next engineering target is not more philosophy. It is operationalization:

1. Canon index
2. Source map
3. Concrete validation rules
4. Planted-corruption test harness
5. Family-readable witness layer
6. Ingest procedure

## One-line risk statement

> If the record does not become findable, testable, and readable without Noah manually holding it together, the drift wins.
