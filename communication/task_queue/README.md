# task_queue/

The Platform Worker's own task chain. Per the Director's explicit
instruction, the Platform Worker no longer asks "what's next?" after
finishing a task — it maintains this queue and pulls the next item
itself.

## Two independent tracks

Per Director decision: **Platform Tasks** (`TASK-XXX`) and
**Engineering** (`DEVOPS-XXX`) are two separate roadmaps that never
interrupt each other — an Engineering item is never inserted into the
Platform Tasks numbering (it does not, for example, take a reserved
`TASK-003` slot). Both live in this same folder; `QUEUE.md` lists them
in two separate sections.

## Files

- `QUEUE.md` — the live chain for both tracks (this is the file to
  check first): each task with its current status, in order.
- `TASK-XXX.md` — one file per Platform task, `TASK-001`, `TASK-002`,
  ... — **3-digit**, matching the Director's own worked example
  exactly (`TASK-001 / Completed / TASK-002 / In Progress / ...`) —
  the only ticket type in `communication/` (besides `DEVOPS-XXX`) that
  uses 3 digits instead of 4, deliberately, to match that example
  rather than force a different convention onto it.
- `DEVOPS-XXX.md` — one file per Engineering task, same 3-digit
  convention, kept in its own numbering sequence so it's never
  confused with a Platform Task.

## Status values

`Pending` → `In Progress` → `Completed` (or `Blocked`, with a pointer
to the `requests/REQ-XXXX.md` blocking it, or to the Platform Tasks
milestone it's waiting on — e.g. DEVOPS-001 is `Blocked` on Navigation
Foundation Complete).

## Rule

Exactly one Platform Task is `In Progress` at a time. When it
completes, its `TASK-XXX.md` is updated to `Completed`, `QUEUE.md` is
updated, and the next `Pending` task becomes `In Progress` — without
asking the Director first, unless the next task itself requires a
Director decision (per `docs/CURRENT_PHASE.md`'s own role-boundary
rule: Core is off-limits without an explicit Director task). The
Engineering track follows the same rule independently — an
Engineering task becoming `In Progress` never pauses or reorders the
Platform Tasks chain, and vice versa.

## Related

- `docs/CURRENT_PHASE.md` — the phase this queue operates inside.
