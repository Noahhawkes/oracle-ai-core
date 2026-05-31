# Mac Quarantine UI Design

**Date:** May 30, 2026
**System:** Oracle.AI / Clipboard Quarantine App
**Architecture:** Minimum Viable Discriminator Kernel (MVDK)

## 1. Design Objective

Create a Mac interface that turns clipboard quarantine from a background script into a usable personal signal inbox.

The emotional target is relief, not obligation.

The user should feel:

```text
I do not have to hold this in my head anymore.
```

The user should not feel:

```text
Great. Another inbox.
```

## 2. Core UX Principle

The interface must express constraint.

It may show captured signal.

It may not pressure the user to act.

It may not auto-generate tasks, summaries, or categories.

It may not create the sense that quarantine items are overdue.

## 3. Menu Bar States

The menu bar icon should remain calm and minimal.

```text
○ Empty
● New captures waiting
▲ Review recommended
■ Sync or encryption issue
```

No aggressive red badges.

No countdowns.

No urgency language.

Quarantine is a safe harbor, not a ticking clock.

## 4. Primary Window: Quarantine Inbox

The first window should be a compact inbox.

```text
--------------------------------------------------
QUARANTINE INBOX

17 items awaiting review

[Search]

Today
--------------------------------------------------
9:12 PM
Clipboard
"I need to call Luke tomorrow..."

Status: Quarantined

[Review]

--------------------------------------------------
8:41 PM
Clipboard
"Boondoggle business idea..."

Status: Quarantined

[Review]
--------------------------------------------------
```

## 5. Review Screen

Opening a record displays the captured item and its metadata.

```text
--------------------------------------------------
QUARANTINE RECORD

Source:
Clipboard

Captured:
2026-05-30 21:12

Risk:
Low

Status:
Quarantined

--------------------------------------------------

I need to call Luke tomorrow about dealer training.

--------------------------------------------------

Actions

[Keep Quarantined]
[Promote]
[Reject]
[Copy]
[Export]
--------------------------------------------------
```

## 6. Promote Trigger Decision

The first implementation should use a modal overlay for the Promote action.

### Rationale

Promotion is the sovereign trigger.

It should feel distinct from browsing, reviewing, or copying.

A modal creates a deliberate pause and prevents accidental state transition.

Inline expansion is too casual for canonical routing.

A tear-away window is too heavy for MVP.

Therefore:

```text
Promote = modal overlay
```

## 7. Promotion Modal

The Promote modal asks the human to assign meaning and destination.

```text
--------------------------------------------------
PROMOTE RECORD

This will move the item out of quarantine.

What is this?

( ) Task
( ) Memory
( ) Business Idea
( ) Evidence
( ) Note
( ) Other

Destination

( ) GitHub
( ) Notes
( ) Drive
( ) Calendar
( ) Archive

[Cancel]
[Promote]
--------------------------------------------------
```

## 8. Promotion Modal Invariants

The modal must enforce:

- No default selected type.
- No default selected destination.
- Promote button disabled until the user chooses both type and destination.
- Cancel remains available at all times.
- Closing the modal leaves the record quarantined.
- Promotion must generate an audit event.

## 9. Explicit Non-Features for MVP

The MVP must not include:

- AI summaries.
- Auto-categorization.
- Automatic tasks.
- Automatic calendar events.
- Automatic GitHub issues.
- Automatic Drive writes.
- Priority scoring.
- Urgency badges.

These omissions are intentional safeguards, not missing features.

## 10. Voice Capture UX

The future voice mode should behave like a dashcam.

The system should confirm capture without forcing interpretation.

```text
Captured. No action taken.
```

## 11. Core Invariant

```text
The user controls promotion.
The interface controls pressure.
```

## 12. Final Compression

The Quarantine UI does not exist to make the user process more.

It exists so the user can safely remember less.

#RenderedReality
