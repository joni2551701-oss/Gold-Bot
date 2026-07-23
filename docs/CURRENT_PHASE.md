# GoldBot — Current Phase

Living pointer to whatever phase is presently open. Updated at the
close of each phase to reflect the phase that just froze and, where
known, what's authorized to start next. `docs/changelog/CHANGELOG.md`
and `docs/changelog/PHASE_HISTORY.md` are the permanent record; this
document is only ever the current tip.

## Phase: TASK-002D — Navigation Implementation (governance review)

**Status: 🟡 CONDITIONALLY APPROVED.** Architecture (Navigation Core,
Platform Adapter, Tests) reviewed and approved by the Director. Freeze
pending final CI confirmation — see the CI note below.

**CI note**: `ci.yml` run #158 (commit `b366971`, TASK-002D's own
content) shows `cancelled`, not `success` — GitHub's own
`concurrency: cancel-in-progress: true` killed it when the next commit
(`8adf53b`, a 1-line changelog fix, no code) was pushed before #158
finished. Run #159 (`8adf53b`) — the exact same code as #158 plus that
one non-code line — completed with `success`. Flagged for Director
confirmation that this satisfies the "CI #158 Success" condition.

## New governance from this review

- **ADR-006 (Navigation Transaction)**, **ADR-007 (Navigation
  Context)**, **ADR-008 (Navigation Result)** — all recorded
  (`communication/decisions/ADR-006.md` through `ADR-008.md`, folded
  into `docs/changelog/DECISION_LOG.md`). All three explicitly govern
  **future** Navigation work — none is applied retroactively to
  TASK-002D's own already-approved code in this cycle (No Silent
  Decisions Policy: rewriting a same-cycle contract is its own task).
- **TASK-002E (Navigation Tests / Validation)** scoped
  (`communication/task_queue/TASK-002E.md`): stress tests, edge cases,
  session recovery, stack consistency, invalid route handling,
  permission failures, event validation, multi-session isolation.
  Pending — starts only after TASK-002D's freeze is confirmed.

## Frozen / closed phases

- **PLATFORM-001** — ✅ **FROZEN**, never reopened.
- **TASK-002A (Navigation Analysis)** — ✅ **CLOSED**.
- **TASK-002B (Navigation Architecture)** — ✅ **APPROVED**.
- **TASK-002C (Navigation Registry)** — ✅ **FROZEN**.

## Role boundary (unchanged)

**Core** (Trading Engine & AI) remains untouched. **Platform** (Product
Experience & Platform Foundation) is where all activity happens.

## Engineering track established (separate from Platform Tasks)

Director decision: DevOps/CI-infrastructure work is its own roadmap
(`DEVOPS-XXX`), sequenced independently so it never interrupts or
reorders the Platform Tasks chain (`TASK-XXX`) — Architecture First
discipline applied to roadmap sequencing itself. **DEVOPS-001 (Smart
CI Routing)** is recorded (`communication/task_queue/DEVOPS-001.md`)
but explicitly **Blocked** until Navigation Foundation (TASK-002E +
TASK-002F) is fully complete; DEVOPS-002/003/004 (Release Pipeline,
Branch Protection, Build Optimization) are named but not yet scoped.
No `.github/workflows/*.yml` file is touched — design first,
implementation second, and only once DEVOPS-001's five mandatory
pre-start deliverables are reviewed and approved.

## Next

Awaiting Director confirmation on the CI note above before TASK-002D
is marked ✅ APPROVED / Frozen and TASK-002E starts.

## Related

- `docs/NAVIGATION_ARCHITECTURE.md` — the approved architecture.
- `communication/decisions/ADR-001.md` through `ADR-008.md`.
- `docs/PLATFORM_WORKFLOW.md` — "Architecture First," Freeze Checklist.
- `communication/task_queue/QUEUE.md` — the live task chain.
- `docs/HANDOFF.md` — the Core/Platform role split and how to pick up
  Platform work.
- `docs/TECHNICAL_DEBT.md` — the one open item from an earlier phase,
  still unresolved (out of scope for this one too).
