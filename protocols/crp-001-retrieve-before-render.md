# CRP-001: Retrieve Before Render

**Status:** Public canon — v0.1

## Purpose

Prevent reconstruction failure by requiring retrieval before synthesis.

## Procedure

1. Retrieve highest-authority canon.
2. Check authority hierarchy.
3. Check exclusion ledger.
4. Identify contradictions.
5. Mark unresolved gaps.
6. Separate fact, inference, and speculation.
7. Generate only inside verified boundaries.
8. Log divergence when detected.

## Output Requirements

Every reconstruction should distinguish:

- Verified canon
- Verified exclusion
- Inference
- Speculation
- Unresolved conflict

## Failure Condition

If synthesis occurs before retrieval when canon is available, the output is non-compliant with CRP-001.

## One-line definition

> Retrieve first. Render second. Guess last.
