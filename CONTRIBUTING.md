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

## Multi-Model iOS Workflow

This repository is designed to work as the shared brain for a phone-based AI workflow.

The repo is the source of truth. AI models are bounded workers.

Use different model roles for different tasks:

- generalist chat models for specs, CRP docs, explanations, and naming
- code-centric models for TypeScript, Python, validators, tests, and refactors
- web-aware models for prior art, standards language, terminology, and positioning
- file-aware or snippet-friendly models for schemas, examples, and fixture generation
- mobile-integrated tools for share-sheet, clipboard, and shortcut workflows

Do not depend on any model to remember the whole project. Give each model one artifact and one job.

## AI-Assisted Workflow

Recommended loop:

1. Choose one unit of work.
2. Open the relevant file in GitHub.
3. Copy that file or snippet into an AI assistant.
4. Ask for one bounded transformation.
5. Review the output.
6. Commit the improved artifact back to the repo.
7. Use the committed repo artifact as the input for the next model if needed.

Examples of bounded transformations:

- extend one schema object
- add one ProtocolState
- write one test fixture
- refactor one function
- generate one additional example
- tighten one CRP section without changing semantics

Avoid unbounded transformations:

- improve everything
- rewrite the whole system
- add all missing features
- make this more advanced

## Prompt Discipline

Use stable references in prompts.

Examples:

- `This is CRP-002: Continuity View Schema. Extend only the Gap object.`
- `Given evaluateProtocolState.ts, add one protocol state and update tests.`
- `Using ContinuityView and BoundedSynthesisResponse, generate one failing test fixture.`
- `Using boundedSynthesis.ts, add enforcement for unsupported claims without changing policy derivation.`

Avoid broad prompts like:

- `Improve the whole system.`
- `Make this more advanced.`
- `Add everything we discussed.`

## Integration Rule

AI output is not canonical until reviewed and committed.

A model may draft, refactor, summarize, or test. The repository decides what persists.

The correct integration loop is:

```text
GitHub artifact → AI worker → human review → GitHub commit
```

Do not integrate directly from a model response into another model as if it were canonical. Pass through the repo whenever possible.

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
