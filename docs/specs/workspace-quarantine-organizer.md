# Workspace Quarantine Organizer: System Specification

**Date:** May 30, 2026
**Architecture:** Minimum Viable Discriminator Kernel (MVDK)
**System:** Oracle.AI / Workspace Organizer

## 1. System Objective

To automatically sort Gmail and Google Drive into a clean, searchable structure while strictly preventing AI or automation from deleting, moving, or misfiling important records without explicit human approval. This system applies the 51/49 Human Sovereignty Rule directly to personal and professional data management.

## 2. Core Workflow and Invariants

The system deprecates blind automation in favor of the Continuity Intelligence pipeline:

```text
Scan -> Classify -> Quarantine -> Review -> Apply
```

## 3. Absolute Rules of Engagement

- Automation may label.
- Automation may recommend.
- Automation may quarantine.
- Automation may NOT delete or permanently move without approval.

## 4. Proposed Taxonomy

The baseline classification engine will operate on a rules-first architecture before invoking AI heuristics. The initial taxonomy is structured to manage the high-velocity data influx from immediate operational demands.

### Professional / Work

- EcoWater
  - Onboarding
  - Communications
- Travel
  - Flights
  - Hotels
  - Rentals
- Receipts and Expenses
- Benefits / HR and Training
- Recruiters and Career
- Noah AI Technologies / Oracle AI Core
- GitHub and AI Projects

### Personal / Infrastructure

- Family
- Finance and Banking
- Home and Medical
- Archive
- Quarantine / Needs Review

## 5. MVP Implementation Steps

### 5.1 Read Metadata

Scan-only mode for Gmail and Drive metadata.

### 5.2 Classify

Filter items into recommended buckets through a deterministic rules engine.

Example:

```text
from:(ecowater.com) -> Work/EcoWater
```

### 5.3 Apply Safe Labels

Execute non-destructive Gmail labeling only.

### 5.4 Suggest Moves

Queue Google Drive folder moves as proposals into the review state. Initial implementation should prefer suggestions, shortcuts, or copy proposals before any permanent move behavior.

### 5.5 Audit and Rollback

Maintain a strict log of every action to ensure reversibility, accountability, and provenance preservation.

## 6. Gmail Label Taxonomy

Initial Gmail labels should include:

- Work/EcoWater
- Work/EcoWater/Onboarding
- Work/EcoWater/Training
- Work/EcoWater/Benefits-HR
- Work/Travel
- Work/Travel/Flights
- Work/Travel/Hotels
- Work/Travel/Rentals
- Work/Receipts-Expenses
- Career/Recruiters
- Tech/GitHub
- Tech/AI-Projects
- Noah-AI-Technologies/Oracle-AI-Core
- Personal/Family
- Personal/Finance-Banking
- Personal/Home-Medical
- Quarantine/Needs-Review
- Archive/Low-Priority

## 7. Google Drive Folder Taxonomy

Initial Drive folder structure should include:

```text
/Workspace Organizer
  /Work
    /EcoWater
      /Onboarding
      /Training
      /Benefits-HR
      /Travel
        /Flights
        /Hotels
        /Rentals
      /Receipts-Expenses
    /Career-Recruiters
  /Noah AI Technologies
    /Oracle AI Core
    /GitHub and AI Projects
  /Personal
    /Family
    /Finance-Banking
    /Home-Medical
  /Quarantine
    /Needs Review
  /Archive
```

## 8. Rules-First Classification Examples

```text
from:(ecowater.com) -> Gmail label: Work/EcoWater
from:(training.knowbe4.com) -> Gmail label: Work/EcoWater/Training
from:(github.com) -> Gmail label: Tech/GitHub
subject:(flight OR hotel OR itinerary OR rental car) -> Gmail label: Work/Travel
has:attachment (receipt OR invoice) -> Gmail label: Work/Receipts-Expenses
from:(linkedin.com OR indeed.com OR greenhouse.io OR lever.co) -> Gmail label: Career/Recruiters
```

## 9. Review and Apply Model

Gmail labels may be applied automatically when a deterministic rule reaches high confidence and the action is non-destructive.

Google Drive changes must begin in review mode. The app may recommend folder placement, shortcuts, or copy proposals, but permanent moves require explicit human approval.

## 10. Audit Requirements

Every scan, classification, label application, recommendation, approval, rejection, or rollback must generate an audit event.

Audit events must capture metadata only. They must not store private email body text, Drive document contents, passwords, tokens, financial details, medical details, or legal content.

Minimum audit fields:

- audit_event_id
- event_timestamp
- item_source
- item_id_hash
- action_type
- recommended_category
- applied_category
- actor_type
- actor_id
- confidence_type
- status_before
- status_after
- rollback_available

## 11. Rollback Requirements

The system must preserve enough metadata to reverse every applied label or Drive change where the underlying platform permits reversal.

No destructive action may execute in the MVP.

## 12. Core Invariant

```text
Automation may organize access.
Automation may not erase memory.
```
