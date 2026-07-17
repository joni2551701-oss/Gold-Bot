# Director Policy

How the Director and the Worker operate together on this repository.
This document describes the process this project has actually run
since Phase 59 — it is a description made binding, not an aspiration.

## Roles

**Director** sets intent: what gets built, in what order, and why.
The Director never writes code directly and never bypasses the
Worker's validation sequence to push a change faster.

**Worker** (the Claude/AI agent, or a human following the same
discipline) executes: audits first, implements only genuine gaps,
tests, documents, validates, commits, and reports. The Worker never
invents scope beyond what a brief asks for, and never silently expands
a "minimal" brief into a refactor.

## What makes a brief executable

A Director message is an **executable Worker Brief** only when it
contains:

1. An Objective.
2. A `TASK 0` — the Foundation Reuse Audit (Article 11) plus a
   Constitution compliance check.
3. `TASK 1…N`, each naming a concrete deliverable.
4. Strict Rules — the hard boundaries this specific brief must not
   cross.
5. Acceptance Criteria — the checklist the Worker's own final report
   is measured against.

A Director message **without** this shape — a proposal, a roadmap
sketch, a "men tavsiya qilaman" recommendation, a policy decision, a
piece of praise — is guidance, not a brief. The Worker acknowledges it
(explicitly stating what, if anything, changes as a result) and does
not write code or create files until an executable brief arrives. This
is the pattern already followed for the Phase 62.1 Constitution
Enhancement proposal itself, twice, before this policy existed in
writing.

## Conflict handling

If an executable brief's instruction conflicts with the Constitution,
the Worker does not resolve the conflict itself: **STOP → AUDIT →
Director Decision.** The Worker documents the specific Article and the
specific conflicting instruction, and waits. This is Article 8's
Change Management Law in its operational form.

## Reporting discipline

The Worker never uses "Complete," "Validated," "Production Ready," or
"All checks passed" before GitHub Actions has returned `success` for
the exact commit being reported on (`CLAUDE.md`'s Reporting language
rule). Every commit-producing response ends with the Pre-Commit
Verification checklist and an explicit list of changed files.

## Related

- `docs/constitution/CONSTITUTION.md` Article 8 — Change Management
  Law, the constitutional form of this policy.
- `docs/policies/DEVELOPMENT_POLICY.md` — the Documentation First
  sequence a brief is executed against.
- `docs/policies/RELEASE_POLICY.md` — the Freeze/CI gate a phase must
  clear before the Worker uses "complete" language.
