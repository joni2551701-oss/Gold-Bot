# GoldBot — Current Phase

Living pointer to whatever phase is presently open. Updated at the
close of each phase to reflect the phase that just froze and, where
known, what's authorized to start next. `docs/changelog/CHANGELOG.md`
and `docs/changelog/PHASE_HISTORY.md` are the permanent record; this
document is only ever the current tip.

## Phase: TASK-002F — Navigation Foundation Final Audit

**Status: 🟢 AUTHORIZED TO START.** Scope expanded by Director order
beyond the original "Navigation Freeze": Architecture Audit (Constitution/
ADR/Workflow compliance), Code Audit (Frozen Contracts, Public
Interfaces, Dependency review), Documentation Audit, Test Audit,
Future Audit (Telegram Mini App/Android/iOS/Desktop readiness), and a
Security Audit built on ADR-011. Full scope:
`communication/task_queue/TASK-002F.md`.

**If successful**: Director will declare Platform Foundation — Phase 1
(Navigation System) — **COMPLETE, Production Ready: YES** — the first
major Platform Foundation milestone, and DEVOPS-001 unblocks.

## New governance this round

- **ADR-009 (CI Supersession Rule)** — a CI run cancelled only by a
  superseding push (never a real failure) is resolved by that later
  run's `success`, which becomes the official validation.
- **ADR-010 (Fail Closed Permission Policy)** — any permission check,
  present or future, must fail closed: an unknown/invalid/missing/
  malformed value on either side of the comparison never grants
  access. Prompted by TASK-002E's `has_sufficient_permission()`
  finding (tracked, not yet fixed, in `docs/TECHNICAL_DEBT.md`'s
  Security Backlog — the module is Frozen and the fix is deferred to
  a dedicated future Security Task).
- **ADR-011 (Security Review Layer)** — every task touching Permission/
  Authentication/Authorization/Session/Navigation code must include a
  Security Review section (Attack Surface, Failure Modes, Fail Open/
  Fail Closed, Abuse Scenarios, Recommendations) in its report.
  Applies starting with TASK-002F.

## Frozen / closed phases

- **PLATFORM-001** — ✅ **FROZEN**, never reopened.
- **TASK-002A (Navigation Analysis)** — ✅ **CLOSED**.
- **TASK-002B (Navigation Architecture)** — ✅ **APPROVED**.
- **TASK-002C (Navigation Registry)** — ✅ **FROZEN**.
- **TASK-002D (Navigation Implementation)** — ✅ **FROZEN** — CI
  validated via ADR-009's Supersession Rule (run #159 success covers
  run #158's cancelled-by-supersession content). Full Freeze Checklist:
  `communication/task_queue/TASK-002D.md`.
- **TASK-002E (Navigation Tests / Validation)** — ✅ **FROZEN** — 80
  tests passing (29 new), full suite 4689/4689, CI #163 `success`.
  Surfaced the `has_sufficient_permission()` finding resolved into
  ADR-010/ADR-011 rather than a silent fix. Full Freeze Checklist:
  `communication/task_queue/TASK-002E.md`.

## Engineering track (unchanged, still parked)

**DEVOPS-001 (Smart CI Routing)** remains recorded and ⏳ **Blocked**
until Navigation Foundation (TASK-002E + TASK-002F) is fully complete
— TASK-002E is now Frozen; DEVOPS-001 unblocks once TASK-002F also
closes successfully. DEVOPS-002/003/004 remain unscoped.

## Role boundary (unchanged)

**Core** (Trading Engine & AI) remains untouched. **Platform** (Product
Experience & Platform Foundation) is where all activity happens.

## Next

TASK-002F's own deliverable (the Navigation Foundation Final Audit,
including its mandatory Security Audit section per ADR-011), then
Director review — which, if successful, declares Navigation
Foundation COMPLETE and unblocks DEVOPS-001.

## Related

- `docs/NAVIGATION_ARCHITECTURE.md` — the approved architecture.
- `communication/decisions/ADR-001.md` through `ADR-011.md`.
- `docs/PLATFORM_WORKFLOW.md` — "Architecture First," Freeze Checklist,
  CI Supersession Rule, Fail Closed Permission Policy, Security Review
  Layer.
- `communication/task_queue/QUEUE.md` — the live task chain (both
  Platform Tasks and Engineering tracks).
- `docs/HANDOFF.md` — the Core/Platform role split and how to pick up
  Platform work.
- `docs/TECHNICAL_DEBT.md` — the earlier open item plus this phase's
  new Security Backlog entry (`has_sufficient_permission()`), both
  unresolved and out of scope for TASK-002F itself.
