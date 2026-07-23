# GoldBot — Current Phase

Living pointer to whatever phase is presently open. Updated at the
close of each phase to reflect the phase that just froze and, where
known, what's authorized to start next. `docs/changelog/CHANGELOG.md`
and `docs/changelog/PHASE_HISTORY.md` are the permanent record; this
document is only ever the current tip.

## Phase: TASK-002A — Navigation Analysis

**Status: DELIVERED, AWAITING DIRECTOR REVIEW.** Type: Analysis only —
step 1 of the mandatory "Architecture First" workflow
(`docs/PLATFORM_WORKFLOW.md`), applied to Navigation (TASK-002). No
architecture proposal, no code, no new API, no folder-structure
change. Deliverable: `docs/NAVIGATION_ANALYSIS.md`. Per Director
instruction, this task stops here — TASK-002B (Navigation
Architecture) does not start until the Director reviews and approves
this analysis.

## Previous phase

**PLATFORM-001 (Platform Foundation & Collaboration Infrastructure)**
— **FROZEN**, CI `success` confirmed (`ci.yml` run #150, commit
`05d05c7`), Director-approved. Full record:
`docs/changelog/CHANGELOG.md`'s "PLATFORM-001" entry,
`docs/PLATFORM_FOUNDATION.md`, `communication/task_queue/TASK-001.md`.

This phase also introduced two standing rules that apply to every
phase from here on:

- **"Architecture First"** (`docs/PLATFORM_WORKFLOW.md`) — the
  mandatory 10-step sequence (Analysis → Architecture → Implementation
  Plan → Approval Check → Implementation → Tests → Documentation → CI
  → Freeze → Next Task) every Platform task now follows.
- **"No Silent Decisions Policy"** (`communication/decisions/README.md`)
  — a folder-structure change, new public API, broken contract,
  database schema change, or Core↔Platform interface change requires a
  `communication/decisions/PROPOSED-DECISION-XXXX.md` ticket and
  Director approval before implementation. Internal refactoring, bug
  fixes, and documentation are exempt.

## Role boundary (unchanged)

**Core** (Trading Engine & AI) remains untouched by this and the prior
phase. **Platform** (Product Experience & Platform Foundation) is
where all activity in this phase happens.

## Next

Awaiting Director review of `docs/NAVIGATION_ANALYSIS.md` before
TASK-002B (Navigation Architecture) begins. See
`communication/task_queue/QUEUE.md` for the full Navigation sub-task
chain (002A–002F) and the remaining Phase 2 backlog (Dashboard,
Settings, Notification Center).

## Related

- `docs/PLATFORM_WORKFLOW.md` — the "Architecture First" process now
  governing every task.
- `communication/decisions/README.md` — the No Silent Decisions Policy.
- `communication/task_queue/QUEUE.md` — the live task chain.
- `docs/NAVIGATION_ANALYSIS.md` — this phase's deliverable.
- `docs/HANDOFF.md` — the Core/Platform role split and how to pick up
  Platform work.
- `docs/TECHNICAL_DEBT.md` — the one open item from two phases ago,
  still unresolved (out of scope for this one too).
