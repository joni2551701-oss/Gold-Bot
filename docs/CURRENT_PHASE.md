# GoldBot — Current Phase

Living pointer to whatever phase is presently open. Updated at the
close of each phase to reflect the phase that just froze and, where
known, what's authorized to start next. `docs/changelog/CHANGELOG.md`
and `docs/changelog/PHASE_HISTORY.md` are the permanent record; this
document is only ever the current tip.

## Phase: TASK-002E — Navigation Tests (Validation)

**Status: IN PROGRESS.** Director-authorized: Navigation Validation,
Edge Cases, Stack Consistency, Multi-session Validation, Permission
Validation, Event Validation, Recovery Scenarios, Integration
Validation — all against the existing, frozen TASK-002D contracts.

**Forbidden**: redesigning the Navigation architecture, changing any
existing public contract, touching Trading Core, or turning
`PlatformAdapterBase` into a concrete per-platform implementation.

## New governance this round

- **ADR-009 (CI Supersession Rule)** — a CI run cancelled only by a
  superseding push (never a real failure) is resolved by that later
  run's `success`, which becomes the official validation. Recorded in
  `docs/PLATFORM_WORKFLOW.md`'s Freeze Checklist section and
  `docs/changelog/DECISION_LOG.md`. Applies to every future task.

## Frozen / closed phases

- **PLATFORM-001** — ✅ **FROZEN**, never reopened.
- **TASK-002A (Navigation Analysis)** — ✅ **CLOSED**.
- **TASK-002B (Navigation Architecture)** — ✅ **APPROVED**.
- **TASK-002C (Navigation Registry)** — ✅ **FROZEN**.
- **TASK-002D (Navigation Implementation)** — ✅ **FROZEN** — CI
  validated via ADR-009's Supersession Rule (run #159 success covers
  run #158's cancelled-by-supersession content). Full Freeze Checklist:
  `communication/task_queue/TASK-002D.md`.

## Engineering track (unchanged, still parked)

**DEVOPS-001 (Smart CI Routing)** remains recorded and ⏳ **Blocked**
until Navigation Foundation (TASK-002E + TASK-002F) is fully complete
— the pause on Navigation itself has been lifted (this phase), but
DEVOPS-001's own block stands independently, per Director order.
DEVOPS-002/003/004 remain unscoped.

## Role boundary (unchanged)

**Core** (Trading Engine & AI) remains untouched. **Platform** (Product
Experience & Platform Foundation) is where all activity happens.

## Next

TASK-002E's own deliverable (deeper Navigation test coverage), then
Director review before TASK-002F (Navigation Freeze) — which closes
Navigation Foundation and unblocks DEVOPS-001.

## Related

- `docs/NAVIGATION_ARCHITECTURE.md` — the approved architecture.
- `communication/decisions/ADR-001.md` through `ADR-009.md`.
- `docs/PLATFORM_WORKFLOW.md` — "Architecture First," Freeze Checklist,
  CI Supersession Rule.
- `communication/task_queue/QUEUE.md` — the live task chain (both
  Platform Tasks and Engineering tracks).
- `docs/HANDOFF.md` — the Core/Platform role split and how to pick up
  Platform work.
- `docs/TECHNICAL_DEBT.md` — the one open item from an earlier phase,
  still unresolved (out of scope for this one too).
