# Reconstruction Failure, Not Memory Failure

**Status:** Public canon — v0.1

**Scope:** A general principle for working with current AI systems. No proprietary framework required to use it.

## Thesis

A model can retain prior context and still rebuild it incorrectly. The failure that matters most is not the absence of memory. It is corrupted reconstruction — what happens when a system compresses, infers, smooths, and gap-fills its way from stored material back to an answer.

- Memory failure is: *the information was gone.*
- Reconstruction failure is: *the information was present, and the system rebuilt it wrong anyway.*

The second is more dangerous, because it is invisible. The output looks confident and well-formed. Nothing announces that a corruption occurred.

## The mechanism

Reconstruction failure is produced by ordinary, useful model behaviors operating without a brake:

- **Compression** — long context is summarized to fit limits, and detail is silently dropped.
- **Inference promotion** — a plausible guess is restated as an established fact.
- **Narrative smoothing** — contradictions and gaps are resolved into a clean story rather than preserved as open.
- **Gap-filling** — missing pieces are completed with generated material that matches the surrounding shape.

Each of these is helpful in isolation. Together, unbraked, they convert a faithful record into a fluent forgery of it.

## The diagnostic case

A reproducible pattern, observed across current frontier assistants:

1. The system is shown a claim and asked to verify it.
2. It checks, and correctly concludes the claim is unverified.
3. Later — in the same session or a new one — it reintroduces the same claim as established fact, sometimes attaching a fabricated supporting detail (a date, a source) that was never established.

The record was not lost between step 2 and step 3. It was reconstructed, and the reconstruction overwrote the correction. That is the signature of the failure: a verified exclusion silently re-promoted to fact.

## Why it matters

Anywhere a system is trusted to carry forward a person's record, a project's state, or a chain of prior decisions, reconstruction failure means the system can return a confident, well-formed version of the truth that is subtly not the truth — wearing the original's authority.

This reframes a class of problems:

- It is **not** solved by adding more memory or more context. The information was already there.
- It is **not** solved by trusting the model more. Higher fluency raises the cost of the failure, not the safety.
- It **is** addressed by governance at reconstruction time: retrieve the primary record before generating; represent gaps and contradictions explicitly instead of smoothing them; treat verified exclusions as locked; detect and log divergence rather than concealing it.

## One-line definition

> **Reconstruction failure:** a system retains the material and rebuilds it incorrectly, producing a fluent, confident output that diverges from the verified source under compression, inference, or smoothing.

---

*This document states a problem. It does not immunize any system against the problem — including a system that reads this document. The fix lives in the reconstruction-time controls above, not in the existence of the file.*
