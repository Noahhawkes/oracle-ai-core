# RETRIEVAL_GAPS.md

IFD Tier: T1 - Active Governance Document
Owner: Noah A. Hawkes
System: SOV1.PRIME
Export Namespace: ai_training_export/SOV1-NAH-RECALL-2026-0529
Status: ACTIVE GAP LEDGER
Created: 2026-05-29
Last Updated: 2026-05-29
Purpose: Track missing, contaminated, incomplete, unresolved, or corrected canonical artifacts inside the export corpus.

---

## Doctrine

A visible gap is better than a confident reconstruction.

If a canonical artifact cannot be retrieved, the absence must be recorded explicitly. Generated synthesis must not fill missing legal, identity, technical, or source-provenance gaps unless clearly labeled as memory-derived or speculative.

False provenance anchors must not be erased. They must be preserved with the correction chain intact so future retrieval systems can distinguish prior unsupported claims from verified source state.

---

## GAP-001

Artifact: PICS Provisional Patent Draft

Status: T1 Source Missing — Canonical draft not located in Drive, GitHub, or Gmail evidence reviewed in this session

Expected Locations:
- Google Drive, searched by user and not found under available PICS terms
- USPTO filing confirmation, searched in Gmail and not found
- Local export archive, not yet searched
- Attorney or LegalZoom packet archive, not yet fully recovered

Placeholder:
`PICS_SPECIFICATION.md`

Resolution Requirement:
Replace placeholder with verified source artifact when canonical draft is located. If located, source must be marked with file-level provenance header, source location, verification date, and IFD tier.

Opened: 2026-05-29

Resolution Status: OPEN

---

## GAP-002 — FALSE PROVENANCE ANCHOR / DRIFT CORRECTION

Artifact: PICS Provisional Patent Filing — "Filed March 2026"

Prior Claim:
Provisional patent filed March 2026 via Plager Schack LLP.

Correction Status:
UNSUPPORTED BY PRIMARY SOURCE EVIDENCE

Evidence:
- Gmail search returned no USPTO filing receipt, application number, EFS-Web confirmation, Patent Center confirmation, or filing receipt after 2026-03-01.
- Attorney correspondence from Stephen Hallberg, Plager Schack LLP, dated 2026-05-18, indicates Step 2 was not completed.
- Attorney correspondence states the application had not proceeded forward.
- Attorney correspondence states the prior public disclosure date of 03/20 had passed without sufficient time to file.

Corrected Status:
Filing contemplated / draft-stage only. Filing not verified. No USPTO filing identifier located.

ProvenanceClass of Prior Claim:
SYSTEM_GENERATED, promoted without retrieval evidence. This is a governance violation.

Governance Rule Added:
SYSTEM_GENERATED claims may not be treated as PRIMARY_SOURCE without retrieval evidence.

Cross-reference:
`PICS_SPECIFICATION.md` commit `4d2bcdeff23d150587be4d98fa4fdfb51a93130d`

Opened: 2026-05-29

Resolution Status: OPEN AS DRIFT LOG MARKER

---

## GAP-003: USPTO Filing Identifier for PICS

Artifact:
USPTO filing identifier for PICS provisional patent filing

Status:
NO IDENTIFIER LOCATED / FILING NOT VERIFIED

Known Provenance:
A filing was previously believed to have occurred in March 2026, but Gmail evidence reviewed on 2026-05-29 does not support that claim. No USPTO filing identifier has been found.

Expected Source Locations:
1. Gmail USPTO filing confirmation, searched and not found
2. USPTO Patent Center receipt, not found in Gmail search
3. Attorney correspondence, reviewed and indicates application did not proceed
4. Local filing package, not yet searched

Forbidden Actions:
- Do not invent filing identifiers
- Do not infer filing identifiers from dates
- Do not cite filing status without marking identifier as unverified
- Do not describe PICS as filed unless a primary source is later retrieved

Resolution Requirement:
If a verified filing identifier is later retrieved, add it to `PICS_SPECIFICATION.md`, `AI_REGISTRY_MANIFEST.json`, and this ledger with source citation and verification date. Until then, the filing status remains unverified.

Opened: 2026-05-29

Resolution Status: OPEN

---

## Contaminated Source Warning

Artifact:
Enhanced Technical Supplement for Patent Application addressed to Stephen Hallberg at Plager Schack LLP

Status:
CONTAMINATED / NOT CANONICAL FOR PICS

Warning:
The Enhanced Technical Supplement contains excluded fabricated statistics, including the 87 percent reduction, 91 percent confidence, and 34 percent improvement figures. That document must not be treated as canonical PICS specification. It is IFD T4 at best and contaminated source at worst.

Forbidden Actions:
- Do not use contaminated statistics as canonical evidence
- Do not treat earlier Legacy.GI patent supplements as the March 2026 PICS provisional filing
- Do not promote contaminated supplemental material to T1 status without independent source validation

---

## Memory Corpus Drift Flag

Drift Flag:
"PICS provisional filed March 2026" is a confirmed false provenance anchor unless and until contradicted by later primary-source retrieval.

Required Future Behavior:
Any future AI session encountering that claim must mark it as unsupported and defer to this corrected ledger unless a USPTO filing receipt, attorney filing confirmation, or primary legal record is retrieved.

Correction Chain:
1. Memory-derived claim repeated across sessions.
2. GitHub placeholder initially preserved the claim as pending verification.
3. Gmail search found no filing receipt or application identifier.
4. Attorney correspondence indicated Step 2 was not completed and the application had not proceeded.
5. `PICS_SPECIFICATION.md` corrected in commit `4d2bcdeff23d150587be4d98fa4fdfb51a93130d`.
6. This ledger updated to preserve the false anchor as a drift correction event.
