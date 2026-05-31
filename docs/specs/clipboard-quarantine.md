# Clipboard Quarantine Application Specification

**Date:** May 30, 2026
**Architecture:** Minimum Viable Discriminator Kernel (MVDK)
**System:** Oracle.AI / Miracle Drive

## 1. System Objective

To physically enforce the boundary between the `capture state` and the `review state`. The application allows for rapid, high-signal capture while protecting the canonical memory from unstable states, unverified inputs, and data drift.

## 2. The Four-Stage Trust Model

This application deprecates the standard three-stage pipeline (Capture -> Review -> Promote) and enforces the Continuity Intelligence pipeline:

1. **Capture:** Frictionless intake of data.
2. **Quarantine (Default State):** Absolute isolation from the Miracle Drive. Distrusted by default.
3. **Review:** UI rendering of the quarantined data for the 51 percent human sovereignty check.
4. **Promote:** Execution of the `promotion object` to write witness-grade records to permanent storage.

## 3. Core Components

### 3.1 `capture_intake`

- **Function:** Monitors system clipboard or accepts direct text/voice input.
- **Behavior:** Immediate, unopinionated ingestion. No validation required at entry.

### 3.2 `quarantine.py` (The Boundary Engine)

- **Function:** State router.
- **Behavior:** Assigns a unique ID and timestamp to the captured data. Locks the data in a temporary, non-canonical local store. Blocks any automated external API pushes.

### 3.3 `review_ui`

- **Function:** Human-in-the-loop rendering interface.
- **Behavior:** Displays the contents of the quarantine holding area. Provides binary options: Approve (Promote) or Reject (Tombstone).

### 3.4 `promotion_engine`

- **Function:** Miracle Drive API executor.
- **Behavior:** Requires a signed `promotion object` from the `review_ui`. Upon receipt, executes the push to `HawkesNest-LLC/oracle-ai-core` and clears the item from quarantine.

## 4. Invariants

- No data may bypass the quarantine state.
- No data may be promoted without explicit human authorization.
- Rejected data generates a tombstone record; the sensitive raw input is destroyed.
