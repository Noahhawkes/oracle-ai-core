# Contributing to oracle-ai-core

This repository is the canonical source of truth for Continuity Engine work.

The workflow is simple:

1. Explore ideas in chat.
2. Promote only crystallized artifacts into the repo.
3. Keep every committed artifact small, named, testable, and retrievable.

## Core Rule

Nothing is canonical until it exists in this repository.

Chat threads, AI responses, screenshots, and drafts are working memory. The repo is continuity memory.

## Repository Roles

- `/docs` contains CRP specifications and design notes.
- `/schemas` contains machine-readable JSON schemas.
- `/examples` contains small operational JSON examples.
- `/api` contains API contracts and handler stubs.
- `/engine` contains executable enforcement code.
- `/tests` contains fixtures and behavior checks.

## One Concept Per File

Each file should do one thing.

Good:

- `evaluateProtocolState.ts`
- `detectConflicts.ts`
- `continuity-record.schema.json`
- `ok-continuity-view.json`

Bad:

- `continuity-everything.ts`
- `all-governance-notes.md`
- `misc-ai-memory-ideas.md`

Small artifacts are easier for humans and AI systems to retrieve, inspect, copy, test, and extend.

## Stable Naming

Use stable names consistently across docs, schemas, code, examples, and tests.

Preferred terms:

- `ContinuityRecord`
- `ContinuityView`
- `ProtocolState`
- `ValidationStatus`
- `InferenceLevel`
- `BoundedSynthesisResponse`
- `Retrieve before render`
- `Evidence before inference`
- `Absence before invention`

Do not introduce new names for existing concepts unless the schema or protocol is being intentionally revised.

## Code Is Canonical

Prose explains the system. Code enforces the system.

If a behavior matters, it should eventually exist as:

- a schema
- a validator
- a state-machine rule
- an engine function
- a test fixture

## AI-Assisted Workflow

This repo is designed for a multi-AI, copy-paste-friendly workflow.

Recommended loop:

1. Open one file from the repo.
2. Copy that file into an AI assistant.
3. Ask for one bounded change.
4. Review the result.
5. Commit the improved artifact back to the repo.

Do not ask an AI model to remember the entire project. Hand it the exact artifact it needs.

## Prompt Discipline

Use stable references in prompts.

Examples:

- `This is CRP-002: Continuity View Schema. Extend only the Gap object.`
- `Given evaluateProtocolState.ts, add one protocol state and update tests.`
- `Using ContinuityView and BoundedSynthesisResponse, generate one failing test fixture.`

Avoid broad prompts like:

- `Improve the whole system.`
- `Make this more advanced.`
- `Add everything we discussed.`

## Engine Directory Rules

The `/engine` directory must stay implementation-focused.

Do not place long theory dumps in `/engine`.

Each module should be small, readable, and testable.

## Test Discipline

Every governance rule should eventually have a test.

Priority tests:

- hallucinated identity
- gap smoothing
- conflict overwriting
- speculative inference
- cross-subject contamination
- unsupported claims without citations

The purpose of the test suite is to show where standard RAG fails and where continuity governance constrains or refuses.

## Canonical Principle

Retrieve before render.
Evidence before inference.
Absence before invention.

The Continuity Engine exists to enforce those rules in code.
