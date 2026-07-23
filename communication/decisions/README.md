# decisions/

Two distinct ticket types live here — do not conflate them:

## `DEC-XXXX.md` — recorded decisions

A cross-role decision ticket for a specific Core↔Platform boundary
question that has already been resolved (jointly, or by the Director).
Working record; once load-bearing, it is also folded into
`docs/changelog/DECISION_LOG.md` (Constitution Article 8's permanent
ledger) — this folder does not replace that ledger.

## `PROPOSED-DECISION-XXXX.md` — the No Silent Decisions Policy

**Director rule, effective immediately.** The Platform Worker does not
decide the following on its own — it opens a
`PROPOSED-DECISION-XXXX.md` ticket and waits for Director approval
before Implementation (step 5 of `docs/PLATFORM_WORKFLOW.md`) begins:

- Changing a folder structure (new top-level package, renamed/moved
  package).
- Creating a new public API.
- Breaking an existing API contract.
- Changing a database schema.
- Changing the Core↔Platform interface.

**Exempt** (no ticket required): internal refactoring, bug fixes, and
documentation — these proceed without a decision ticket, per the
Director's explicit carve-out.

If a task's Analysis or Architecture step (`docs/PLATFORM_WORKFLOW.md`
steps 1–2) surfaces one of the five trigger conditions above, the
worker stops, files `PROPOSED-DECISION-XXXX.md`, and does not proceed
to Implementation until it is approved — matching the Approval Check
gate the whole workflow is built around.

## Naming

`DEC-XXXX.md` and `PROPOSED-DECISION-XXXX.md` share the same
`decisions/` folder but are two different, independently-numbered
sequences (a `PROPOSED-DECISION` that gets approved does not become a
`DEC` — it stays `PROPOSED-DECISION-XXXX.md` with its status field
updated to `Approved`, since it already carries the full record).

## Template

See `TEMPLATE.md` (recorded decisions) and `PROPOSED_DECISION_TEMPLATE.md`
(pending-approval decisions) in this folder.

## Related

- `docs/changelog/DECISION_LOG.md` — the permanent ledger a load-bearing
  `DEC-XXXX` decision graduates into.
- `docs/PLATFORM_WORKFLOW.md` — the Approval Check step this ticket
  type gates.
