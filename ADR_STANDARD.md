# ADR Standard — Director Order No. 019

## Module Reuse Justification

WAR/WDR entries already exist in `Architecture_Audit_Plan.md` and
`DIRECTOR_DECISIONS.md`, but those are short decision records — a
paragraph stating what was decided and where the full text lives.
Neither file has a slot for the detailed technical record of *why* a
significant architecture decision was made: the options considered,
the trade-offs, the consequences — kept as permanent history rather
than a summary line. Extending `DIRECTOR_DECISIONS.md`'s short-entry
format to carry this level of detail would break its existing
contract (append-only, short-paragraph entries), and `ARCHITECTURE.md`
is the frozen *current* architecture, not a historical decision log.
Per the Module Reuse Principle, steps 1 and 2 were both "no," so a new
root-level file plus a new `adrs/` directory of individual records is
justified — the same reasoning `RFC_STANDARD.md` (Order No. 018)
already applied to `rfcs/`.

## Purpose

WAR/WDR entries in `DIRECTOR_DECISIONS.md` record *that* a decision
was made. The ADR (Architecture Decision Record) is the detailed
technical record of *why* a significant architecture decision was
made — the context, the options weighed, and the consequences — kept
as permanent history so a future Worker or Director can understand
the reasoning behind today's architecture without having to
reconstruct it.

## When an ADR Is Mandatory

The following situations mandate an ADR, verbatim from Director Order
No. 019:

- New Layer
- Layer merge
- Event Bus change
- Pipeline change
- Database Architecture
- AI Architecture
- Execution Flow
- Security Architecture
- Performance Architecture
- Canonical Rule
- Engineering Rule
- Development Rule

## ADR Document Template

```markdown
# ADR-NNN: <Title>

## Context
<The situation and forces at play that make this decision necessary.>

## Problem
<The specific question this decision answers.>

## Options Considered
<Every option that was weighed, briefly.>

## Selected Solution
<The option that was chosen.>

## Why This Solution
<The reasoning that led to this choice over the alternatives.>

## Consequences
<What this decision changes going forward, positive and negative.>

## Risks
<Known risks accepted by making this decision.>

## Alternatives
<Options not chosen, and why — may overlap with Options Considered
but focused on rejection reasons.>

## References
<Related docs, code, discussions.>

## Related RFC
<RFC-NNN, if this decision followed an RFC approval, or "None".>

## Related Director Orders
<Director Order numbers this decision stems from or relates to.>

## Final Status
Draft | Proposed | Approved | Superseded | Deprecated
```

A copy of this template, without the surrounding explanation, lives
at `adrs/TEMPLATE.md` for direct copy-paste into a new
`adrs/ADR-NNN-title.md` file.

## Worker Authority

The Worker may prepare an ADR draft — this is Documentation Evolution
work under Order No. 016 and needs no pre-approval to author. A draft
ADR only becomes **Approved** after explicit Director sign-off; until
then it is not binding and does not itself justify implementation.

## Relationship to RFC

An RFC is the proposal-and-approval gate for a change; an ADR is the
permanent record of the resulting architecture decision — a single
major change often has both: an RFC to get Director approval to make
the change, and an ADR written afterward to record, for history, why
that specific solution was selected over its alternatives. For
example, a Pipeline change would go through `RFC-014` to get approval
to proceed, and once implemented, `ADR-014` would record why that
particular pipeline redesign was chosen over the alternatives
considered.

## Where ADRs Live

- `adrs/README.md` — index of every ADR (ID, title, status, date).
- `adrs/TEMPLATE.md` — the reusable template above, ready to copy.
- `adrs/ADR-NNN-title.md` — one file per ADR, following the template.

The `adrs/` index starts empty; this rollout does not itself require
an ADR (it is a governance-standard rollout, not one of the
ADR-mandatory situations above).

The full Governance Chain (Architecture Standard through Release
Management Standard) is recorded in `CLAUDE.md`'s Worker Authority
section, per Director Order No. 018/019/020.
