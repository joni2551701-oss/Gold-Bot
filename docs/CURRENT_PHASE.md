# GoldBot — Current Phase

Living pointer to whatever phase is presently open. Updated at the
close of each phase to reflect the phase that just froze and, where
known, what's authorized to start next. `docs/changelog/CHANGELOG.md`
and `docs/changelog/PHASE_HISTORY.md` are the permanent record; this
document is only ever the current tip.

## Phase: Repository Recovery (ORDER-020) — Phase 1 done, Phase 2/3 gated

**Status: 🟡 IN PROGRESS.** Engineering Governance v1.1 is **FROZEN**
(all 9 GOV documents approved). The project has returned to Engineering
Implementation, starting with Repository Recovery — fixing the single
invisible U+2060 character in `strategy_layer/strategy_manager/strategy_manager.py` on `main`
(diagnosed by `BRANCH-FORENSICS-001`) and creating the repository's
first rollback anchors.

- **Phase 1 — Recovery Audit**: ✅ complete (read-only) — re-confirmed
  fresh against live refs: single-file/single-character root cause,
  zero code diff, zero existing tags.
- **Phase 2 — Recovery** (rollback anchors → Unicode fix on `main` →
  checkpoint tag) and **Phase 3 — Validation**: ⏸ **mutating**, gated on
  Director approval of `docs/governance/MIGRATION_PLAN.md` (the single
  Recovery+Migration control document) and confirmation of the
  branch-operation authority (commit to `main`, push tags), per the
  frozen `Repository_Policy.md` §5 Audit → Plan → **Approval** →
  Execution discipline.

**Next after Recovery is APPROVED**: Repository Migration (REPO-002) —
the four-branch model (`main`/`develop`/`feature/core`/`feature/platform`),
per `MIGRATION_PLAN.md`.

## Superseded pointer (historical)

The prior tip (TASK-002F — Navigation Foundation Final Audit) was
paused when the Director redirected the project into the Governance
v1.0 → Governance v1.1 → Repository Recovery/Migration sequence.
Navigation Foundation (TASK-001…002E) remains Frozen; TASK-002F is
still Pending and resumes when the Director returns to the Platform
Tasks track.

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
