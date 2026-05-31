# Documentation Index

This directory is the navigation layer for the repository. The project is organized into
five lanes. Each lane governs one layer of the system and nothing else. Read them in order,
each lane assumes the one above it.

| Lane | Path | Governs | Question it answers |
|---|---|---|---|
| Origin | [origin/](origin/) | Meaning | Where did this come from, and what does it mean? |
| Doctrine | [doctrine/](doctrine/) | Constraints | What is and isn’t allowed? |
| Specs | [specs/](specs/) | Execution | How is it actually done? |
| Schemas | [schemas/](schemas/) | Machine legibility | What shape must the data take? |
| Reviews | [reviews/](reviews/) | Critique | What was challenged, corrected, or rejected? |

## Authority order

Origin → Doctrine → Specs → Schemas → Reviews

A change in a higher lane can invalidate everything below it. A change in a lower lane must
never silently rewrite a higher one. If a spec contradicts doctrine, doctrine wins and the
spec is wrong. If a review overturns an origin claim, the origin doc is corrected, the
review is not buried.

## What this index is for

- One entry point instead of a pile of files.
- A fixed place for every artifact, so “where does this go?” has exactly one answer.
- A boundary. If something doesn’t fit a lane, that’s a signal, not a reason to add a sixth lane.

## What this index is not

- Not a roadmap. Plans live in issues.
- Not a holding pen for new ideas. An idea earns a lane only after it survives a review.
