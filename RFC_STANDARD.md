# RFC Standard — Director Order No. 018

## Module Reuse Justification

This is a new process type with no existing home in the repository.
`CLAUDE.md` records Worker operating rules, `ARCHITECTURE.md` records
the frozen system architecture, and `DIRECTOR_DECISIONS.md` is the
append-only decision log — none of them is a place to draft, review,
and track the lifecycle of a proposed large change before it is
approved. `GOLDBOT_DEVELOPMENT_STANDARD.md` (Order No. 017), when it
exists, governs *how code is written*, not how large changes are
*proposed and approved* — a different process with a different
lifecycle (Draft → Under Review → Approved/Rejected → Implemented →
Superseded) that needs its own document and its own `rfcs/` directory
of individual records, the same way `DIRECTOR_DECISIONS.md` needed its
own file rather than being folded into `CLAUDE.md`. Per the Module
Reuse Principle, steps 1 and 2 (does this exist / can something
existing be extended) were both "no," so a new root-level file plus
a new `rfcs/` directory is justified.

## Purpose

Large changes to GoldBot are **proposed, analyzed, risk-assessed, and
Director-approved before any code is written** — never coded directly
first. The RFC (Request For Change) process is the formal document
trail that makes this gate auditable: a Worker who spots the need for
a large change writes an RFC, the Director reviews it, and only a
Director Decision of **Approved** unlocks implementation.

## When an RFC Is Mandatory

The following situations mandate an RFC before any code change is
made, verbatim from Director Order No. 018:

- New Layer
- Removing a Layer
- Pipeline change
- Ownership change
- Canonical Contract change
- Trading Logic change
- AI Logic change
- Risk Logic change
- Database Architecture change
- Public API Breaking Change
- Security Architecture change
- Engineering Standard change
- Development Standard change

This list is not a new boundary — it is the same boundary already
established by `CLAUDE.md`'s "Director Review Required" list (Order
No. 016: Layer Architecture, Pipeline, Trading Logic, AI Logic,
Decision Logic, Risk Logic, public-API breaking change, Ownership, a
Canonical Contract, or a Foundation Rule) and by `ARCHITECTURE.md`'s
Layer rules, now formalized into a document process. Anything that
already required Director Review under Order No. 016 now also
requires an RFC document before implementation begins; the RFC
Standard does not expand what needs Director approval, it defines
*how* that approval is requested and recorded.

## RFC Document Template

```markdown
# RFC-NNN: <Title>

## Current State
<Describe the system as it exists today, relevant to this change.>

## Problem
<What is wrong, missing, or limiting about the current state?>

## Proposal
<The change being proposed, in concrete terms.>

## Benefits
<Why this proposal is worth doing.>

## Risks
<What could go wrong, and how likely/severe each risk is.>

## Impact Analysis
<Which Layers, modules, contracts, or ownership boundaries this
touches, and how.>

## Migration Plan
<Steps to get from Current State to the proposed state.>

## Rollback Plan
<How to undo this change if it fails validation or production use.
If GOLDBOT_DEVELOPMENT_STANDARD.md's Rollback Strategy standard
exists, reference it here rather than redefining rollback mechanics.>

## Alternatives
<Other approaches considered and why they were not chosen.>

## Director Decision
<Filled in by the Director: Approved / Rejected / notes.>

## Final Status
Draft | Under Review | Approved | Rejected | Implemented | Superseded
```

A copy of this template, without the surrounding explanation, lives
at `rfcs/TEMPLATE.md` for direct copy-paste into a new
`rfcs/RFC-NNN-title.md` file.

## Worker Authority

The Worker **may** draft and write an RFC — this is Documentation
Evolution work under Order No. 016 and needs no pre-approval to
author. The Worker **must not** begin implementation of the proposed
change until the RFC's Director Decision field reads **Approved**.
This is a hard gate, not a suggestion: writing the RFC is unrestricted
Worker Authority; acting on it is not, no matter how confident the
Worker is that the change is correct.

## Where RFCs Live

- `rfcs/README.md` — index of every RFC (ID, title, status, date).
- `rfcs/TEMPLATE.md` — the reusable template above, ready to copy.
- `rfcs/RFC-NNN-title.md` — one file per RFC, following the template.

This rollout (Director Order No. 018 itself) does not require an RFC
of its own — it is a governance-standard rollout, not a Layer,
Pipeline, Trading, Risk, or other change on the mandatory list above.
The `rfcs/` index starts empty.
