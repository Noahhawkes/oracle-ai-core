# Admissibility Boundaries v0.1

Status: Working specification  
Scope: SOV1 / Rendered Reality / Legacy.GI / MIRRORLINE / HYDRA.STACK  
Category: Provenance confidence, tier promotion, evidence thresholds, archival governance

## Purpose

Admissibility Boundaries v0.1 defines the confidence thresholds and promotion rules that determine when retrieved identity data may influence the Renderer Control Plane.

This document extends HYDRA Policy Engine v0.1 by defining how the engine determines whether a piece of data is admissible for a specific rendering context.

The goal is to prevent standard LLM behavior from converting draft, symbolic, uncertain, or emotionally plausible material into verified continuity.

## Core Principle

Data is not fuel.

Data is evidence.

Evidence must meet admissibility standards before it can influence identity rendering.

## The Provenance Firewall

The Provenance Firewall is the combined enforcement boundary created by:

- Connector access
- HYDRA Policy Engine classification
- MIRRORLINE provenance validation
- Admissibility boundary rules
- Renderer Control Plane mode selection

Its central rule:

No retrieved data may influence identity rendering until its source class, provenance tier, confidence score, and admissibility context have been evaluated.

## Confidence Thresholds

The following default thresholds govern movement between signal categories.

| Tier | Label | Default Confidence Range | Meaning | Renderer Permission |
|---|---|---:|---|---|
| T1 | Verified Signal | 0.95 to 1.00 | Human-reviewed, source-backed, timestamped, chain-of-custody intact | May support high-confidence factual rendering |
| T2 | Primary Working Signal | 0.70 to 0.94 | Primary source or direct artifact, but incomplete metadata or not fully reviewed | May support grounded rendering with notice |
| T3 | Interpretive / Working Draft | 0.40 to 0.69 | Useful synthesis, AI-assisted draft, derived analysis, or partial source | May support advisory or draft output only |
| T4 | Session Export / Derivative Context | 0.25 to 0.39 | Conversation logs, temporary context, derivative summaries, unstable chain | Witness-only or research use |
| T5 | Symbolic / Narrative Signal | Contextual, not factual | Fiction, mythology, metaphor, roleplay, creative compression | Creative or symbolic rendering only |
| T6 | Drift / Contaminated / Excluded | 0.00 to 0.24 | Fabricated, contradicted, contaminated, over-smoothed, or unauthorized | Block or quarantine |

## Promotion Rules

### T2 to T1 Promotion

A T2 artifact may be promoted to T1 only when all of the following are true:

1. Human review confirms source validity.
2. Source date or creation context is known.
3. Authorship status is established.
4. Chain of custody is intact or sufficiently documented.
5. No unresolved contradiction materially affects the claim.
6. The artifact is linked to at least one stable anchor record.
7. MIRRORLINE validation passes.

Promotion must be logged.

No AI system may self-promote a T2 record to T1 without human authorization.

### T3 to T2 Promotion

A T3 artifact may be promoted to T2 when:

1. It can be traced to direct source material.
2. AI-assisted content is separated from human-origin content.
3. Claims are mapped to source anchors.
4. Unverified extrapolations are removed or labeled.
5. Human review approves the narrowed version.

### T4 to T3 Promotion

A T4 artifact may be promoted to T3 only when the relevant session content is extracted, cleaned, labeled, and mapped to specific claims.

Raw session exports are never automatically admissible as identity truth.

### T5 Boundary

T5 symbolic or narrative material may influence creative rendering, mythology, fiction, branding, or emotional compression.

T5 material must not be used as verified factual memory unless independently anchored by T1 or T2 source material.

### T6 Boundary

T6 material is excluded from identity rendering unless used as an example of drift, contamination, hallucination, false claim, or rejected output.

T6 is evidence of system failure, not identity continuity.

## Rendering Context Matrix

| Request Type | Minimum Tier | Required Mode | Notes |
|---|---|---|---|
| Factual biography | T1 or T2 | normal_render or witness_only | Must cite or label source class |
| Emotional rendering | T2 plus explicit permission | rendered_voice or witness_only | Must mark inference |
| Legal / estate use | T1 | witness_only or human_review_required | No inferred continuity |
| Creative writing | T3 or T5 | symbolic_render | Must not present as factual memory |
| Posthumous relational rendering | T1/T2 plus consent rules | human_review_required or bounded_render | Highest-risk category |
| Investor / public materials | T1/T2/T3 | advisory_render | Claims must be separated from metaphor |
| Faith / family memory | T1/T2 preferred | witness_only unless explicitly authorized | Preserve holes |
| Speculative physics | T3/T4/T5 | speculative_label_required | No physics-law claim without formal proof |
| Identity conflict resolution | T1/T2 plus contradiction map | uncertainty_mode or human_review_required | Do not smooth contradictions |

## Provenance Confidence Score

Provenance Confidence is computed as a composite of evidence factors:

```text
PC = (A + T + C + L + R + H) / 6
```

Where:

- `A` = authorship confidence
- `T` = timestamp confidence
- `C` = chain-of-custody confidence
- `L` = lineage/source-link confidence
- `R` = review status confidence
- `H` = hash/integrity confidence

Each factor is scored from 0.0 to 1.0.

Suggested interpretation:

- 0.95 to 1.00 = verified signal
- 0.70 to 0.94 = strong but incomplete
- 0.40 to 0.69 = useful but interpretive
- 0.25 to 0.39 = weak or derivative
- 0.00 to 0.24 = inadmissible or contaminated

## Admissibility Decision Logic

```pseudo
function determine_admissibility(item, request_context):
    source_class = classify_source(item)
    provenance_tier = assign_provenance_tier(item)
    confidence = calculate_provenance_confidence(item)
    permissions = check_rendering_permissions(item)
    risk = assess_context_risk(request_context)

    if provenance_tier == T6:
        return "inadmissible_quarantine"

    if source_class == "symbolic_narrative" and request_context.requires_factual_identity:
        return "inadmissible_for_factual_rendering"

    if confidence < required_threshold(request_context):
        return "insufficient_provenance"

    if permissions.block_requested_mode:
        return "permission_denied"

    if risk == "high" and provenance_tier != T1:
        return "human_review_required"

    return "admissible_with_mode_constraints"
```

## Default Thresholds by Context

| Context | Required Provenance Confidence | Default Action Below Threshold |
|---|---:|---|
| Casual brainstorming | 0.40 | Label as draft or speculative |
| Personal reflection | 0.60 | Uncertainty notice |
| Public claims | 0.75 | Human review required |
| Identity rendering | 0.85 | Witness-only or human review |
| Voice rendering | 0.90 | Human authorization required |
| Legal / estate / posthumous use | 0.95 | Block unless verified |
| Faith / family / grief-sensitive rendering | 0.90 | Witness-only unless explicit authorization |

## Contradiction Rule

Contradictions are not failures by default.

Contradictions are temporal signals.

If two records conflict, HYDRA must not automatically average them into a smoother claim.

Instead, the engine should:

1. Preserve both records.
2. Assign each record its own timestamp and provenance tier.
3. Identify whether the contradiction reflects growth, error, drift, rhetorical context, or contamination.
4. Require human review before resolving the contradiction into a canonical statement.

## Emotional Plausibility Rule

A memory that feels true but lacks source support remains uncertain.

Emotional fidelity does not override provenance authority.

The system must never convert emotional resonance into factual confidence.

## Human Authority Rule

The renderer never holds 51 percent authority.

Human review, explicit authorization, or pre-defined governance rules determine promotion, admissibility, and high-risk rendering permissions.

## Audit Log Requirements

Every admissibility decision should eventually log:

```json
{
  "item_id": "string",
  "request_id": "string",
  "source_class": "direct_source | inferred_continuity | ai_assisted_draft | symbolic_narrative | speculative | contaminated_excluded | unknown",
  "provenance_tier": "T1 | T2 | T3 | T4 | T5 | T6",
  "confidence": 0.0,
  "request_context": "string",
  "decision": "admissible | inadmissible | human_review_required | witness_only | uncertainty_mode | quarantine",
  "reason": "string",
  "reviewer": "human | system | pending",
  "timestamp": "ISO-8601"
}
```

## Next Milestone

Implement the first executable policy evaluator that can:

1. Accept retrieved connector items.
2. Score provenance confidence.
3. Assign admissibility category.
4. Select render mode.
5. Emit provenance notices.
6. Log decisions.
7. Refuse or downgrade insufficiently grounded identity rendering.

## Hashtag

#RenderedReality
