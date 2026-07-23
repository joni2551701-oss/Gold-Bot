# task_queue/

The Platform Worker's own task chain. Per the Director's explicit
instruction, the Platform Worker no longer asks "what's next?" after
finishing a task — it maintains this queue and pulls the next item
itself.

## Files

- `QUEUE.md` — the live chain (this is the file to check first): each
  task with its current status, in order.
- `TASK-XXX.md` — one file per task, `TASK-001`, `TASK-002`, ... —
  **3-digit**, matching the Director's own worked example exactly
  (`TASK-001 / Completed / TASK-002 / In Progress / ...`) — the only
  ticket type in `communication/` that uses 3 digits instead of 4,
  deliberately, to match that example rather than force a different
  convention onto it.

## Status values

`Pending` → `In Progress` → `Completed` (or `Blocked`, with a pointer
to the `requests/REQ-XXXX.md` blocking it).

## Rule

Exactly one task is `In Progress` at a time. When it completes, its
`TASK-XXX.md` is updated to `Completed`, `QUEUE.md` is updated, and
the next `Pending` task becomes `In Progress` — without asking the
Director first, unless the next task itself requires a Director
decision (per `docs/CURRENT_PHASE.md`'s own role-boundary rule: Core
is off-limits without an explicit Director task).

## Related

- `docs/CURRENT_PHASE.md` — the phase this queue operates inside.
