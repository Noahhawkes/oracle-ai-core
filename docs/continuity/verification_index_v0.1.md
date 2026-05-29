# Verification Index v0.1

## Purpose

The Verification Index reframes continuity preservation as a routing, discovery, and verification problem rather than a simple storage problem.

The core observation is that identity-relevant artifacts may already exist across many surfaces: GitHub commits, patents, public posts, manuscripts, websites, notes, chats, and recorded media. The risk is not only loss. The risk is incorrect assembly.

A future model parsing scattered fragments may use semantic interpolation to fill gaps, producing plausible but false reconstructions. The Verification Index exists to prevent that by giving future systems a cryptographic and semantic compass.

## Core Finding

The airplane-mode Gemini Nano experiment exposed the boundary between conversation persistence and continuity persistence.

- Conversation persistence: an active thread can continue using local context or cached state.
- Continuity persistence: a fresh session can recover identity-specific frameworks across sessions, devices, and models.

The fresh offline thread failed to recover the actual WIRT definition and instead synthesized a generic public-governance meaning. This suggests the artifacts existed elsewhere, but the local model lacked the routing layer required to discover and verify them.

## Fragment Spectrum

### Tier 1: Witness-Grade Evidence

Examples:

- GitHub commits
- Cryptographically signed logs
- Ledgered run artifacts
- Filed patent documents
- Primary source records

Interpretation:

The system may treat this as directly preserved evidence, subject to verification of path, hash, signature, or other provenance marker.

### Tier 2: Corroborated Context

Examples:

- Public posts
- Books
- Interviews
- Recorded lectures
- Website pages
- Repeated consistent claims across sources

Interpretation:

The system may treat this as high-probability context, but not as absolute proof unless linked to Tier 1 evidence.

### Tier 3: Generative Interpolation

Examples:

- AI-generated summaries
- Unverified notes
- Reconstructed memories without source anchors
- Plausible expansions of undefined acronyms

Interpretation:

The system must mark this as synthetic or inferred. It may be useful for hypothesis generation, but it must not overwrite Tier 1 or Tier 2 records.

## Required Bridges

### 1. Provenance Anchor

Each foundational framework definition should include a stable file path, commit hash, signature, or ledger reference.

When a model encounters a fragment, its first step should be verification, not semantic completion.

### 2. Deontic Guardrail

The system must be trained or prompted to say:

"I can find fragments of this concept, but I lack Witness-Grade routing to verify its exact parameters."

This is preferred over a smooth hallucination.

### 3. Local Cross-Artifact Index

The identity layer should include a lightweight offline index mapping key terms to their verified definitions and source anchors.

Example:

```json
{
  "term": "WIRT",
  "canonical_definition": "Witnessed Information Resilience Test",
  "category": "continuity governance evaluation framework",
  "tier": "TIER_1_WITNESS_GRADE",
  "source_paths": [
    "docs/resilience_tests/WIRT_v0.1_spec.md",
    "data/corpus/sov1_10_pair_corpus.json",
    "src/wirt/evaluator.py"
  ]
}
```

## Design Principle

The Verification Index should not be a massive vault. It should be a routing layer.

It does not need to contain every source artifact. It needs to point future systems toward the correct artifacts, rank their provenance, and prevent semantic interpolation from replacing verified definitions.

## Strategic Boundary

If continuity depends on public training data alone, unique identity constructs will be averaged into generic concepts. This is how a model can transform WIRT into a plausible but false backronym like Wisdom, Information, Relationships, and Tactics.

The Verification Index exists to stop that failure mode.

## Initial Canonical Terms

The first index should include at minimum:

- WIRT
- Continuity Intelligence
- The Perpetual Consult
- Witness Grade
- 51/49 Governance
- Legacy.GI
- HYDRA.STACK
- SOV1
- Epistemic Firewall
- Run Ledger

## Status

Design artifact only. Not yet implemented as code.
