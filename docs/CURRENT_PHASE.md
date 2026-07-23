# GoldBot — Current Phase

Living pointer to whatever phase is presently open. Updated at the
close of each phase to reflect the phase that just froze and, where
known, what's authorized to start next. `docs/changelog/CHANGELOG.md`
and `docs/changelog/PHASE_HISTORY.md` are the permanent record; this
document is only ever the current tip.

## Phase: TASK-002D — Navigation Implementation

**Status: DELIVERED, AWAITING DIRECTOR REVIEW.** Type: Real
implementation, wiring TASK-002C's Registry into an actual Navigation
Core — Director-authorized under an explicit permitted/forbidden
list. 12 new tests (51 total in `tests/platforms/`), full suite 4660
passing, zero diff to Trading Core or `telegram/`.

**Permitted**: Navigation Registry integration, Navigation State
connection (Platform Layer only — Business Layer has zero awareness),
Permission Flow integration (`Request → Permission → Navigation →
Screen`), Event Interface connection (real operations produce
`NavigationEvent`s, still no dispatcher), Platform Layer's own
internal adapter interface (abstract only, no concrete per-platform
implementation).

**Forbidden**: Any Trading Core change, touching Signal/Decision
Engine, any database schema change, breaking any Telegram public
API/contract, hardcoded platform-specific logic.

Full detail: `communication/task_queue/TASK-002D.md`.

## Frozen / closed phases

- **PLATFORM-001** — ✅ **FROZEN**, never reopened.
- **TASK-002A (Navigation Analysis)** — ✅ **CLOSED**.
- **TASK-002B (Navigation Architecture)** — ✅ **APPROVED**.
- **TASK-002C (Navigation Registry)** — ✅ **FROZEN** — full Freeze
  Checklist complete (`communication/task_queue/TASK-002C.md`). No
  refactoring or new capability added to it except a critical bug, a
  security issue, a Director-approved ADR, or a future Migration Task.

## Governance added this round

- **ADR-005** (`communication/decisions/ADR-005.md`) — Universal
  Screen Identity Migration is its own, separately-scoped Migration
  Task: no silent migration, frozen tasks not modified, mandatory
  Backward Compatibility and Rollback plans.
- **Freeze Checklist** (`docs/PLATFORM_WORKFLOW.md`) — the formal
  definition of step 9 ("Freeze"): 10 mandatory boxes (CI Passed,
  Tests Passed, Documentation Updated, ADR Updated, Constitution
  Impact Reviewed, Public Contracts Reviewed, Backward Compatibility
  Checked, No Silent Decisions, Director Approval, Freeze Applied) —
  a task is not "Completed" until every box is checked.
- **PR #2** (base `main`, this branch's head) — Director order: no
  action. Not merged, not closed, not reviewed. Its own, separate
  review process, gated by a future Director + Founder decision.

## Role boundary (unchanged)

**Core** (Trading Engine & AI) remains untouched. **Platform** (Product
Experience & Platform Foundation) is where all activity happens.

## Next

TASK-002D's own deliverable (Navigation Core + Platform Adapter
interface, tests, documentation, CI), then Director review before
TASK-002E (Navigation Tests) / TASK-002F (Navigation Freeze). See
`communication/task_queue/QUEUE.md` for the full chain.

## Related

- `docs/NAVIGATION_ARCHITECTURE.md` — the approved architecture this
  Implementation follows.
- `communication/decisions/ADR-001.md` through `ADR-005.md`.
- `docs/PLATFORM_WORKFLOW.md` — "Architecture First," Universal UI
  Abstraction, Future Expansion, Director Questions, Freeze Checklist.
- `communication/task_queue/QUEUE.md` — the live task chain.
- `docs/HANDOFF.md` — the Core/Platform role split and how to pick up
  Platform work.
- `docs/TECHNICAL_DEBT.md` — the one open item from an earlier phase,
  still unresolved (out of scope for this one too).
