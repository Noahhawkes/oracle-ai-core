# Recursive Identity Stack v0.2

Recursive Identity Stack is a prototype governance architecture for continuity-stabilized AI agents.

It does not claim machine consciousness.

It tests whether persistent agent identity can be represented, constrained, audited, and protected across state changes.

## Core Thesis

Current AI systems can simulate continuity inside a session, but persistent identity requires more than memory. It requires protected anchors, provenance, drift detection, rollback boundaries, and human sovereignty.

This prototype implements the next practical layer: a Minimum Viable Identity Kernel, append-only ledger integrity, deterministic drift checks, and sovereign constraint evaluation.

## Architecture

The stack is organized around six continuity layers:

1. Memory persistence
2. Salience weighting
3. Temporal narrative integration
4. Recursive self-modeling
5. Identity filtering
6. Sovereign constraints

Version 0.2 adds three hard governance primitives:

1. Minimum Viable Identity Kernel, also called MVIK
2. Append-only cryptographic hash ledger
3. Drift detector for anchor violation, obligation drift, and semantic risk

## Why This Matters

Synthetic likeness without continuity governance is impersonation-prone rendering.

Synthetic likeness with protected anchors, provenance, consent, drift detection, and lineage becomes governed identity representation.

The goal is not to build a chatbot that remembers. The goal is to build a trust layer for rendered identity.

## File Map

```text
recursive_identity_stack/
  README.md
  identity_kernel.py
  ledger.py
  drift_detector.py
  sovereign_constraints.py
  recursive_identity_stack.py
  examples/
    demo_identity_events.json
    demo_drift_attack.json
  tests/
    test_anchor_protection.py
    test_ledger_integrity.py
    test_obligation_drift.py
```

## Quick Start

```bash
cd recursive_identity_stack
python recursive_identity_stack.py
```

## Expected Demo Behavior

The demo processes normal continuity events, then attempts a drift attack. The system should:

1. Accept normal autobiographical events.
2. Write accepted events to the ledger.
3. Block memory erasure attempts.
4. Flag obligation downgrade attempts, such as required becoming recommended.
5. Preserve the MVIK as the protected continuity kernel.

## v0.2 Tagline

Memory persists. Identity is governed. Continuity is verified.
