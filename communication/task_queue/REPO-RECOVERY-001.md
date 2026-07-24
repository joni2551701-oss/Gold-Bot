# REPO-RECOVERY-001 (Repository Recovery)

**Order**: ORDER-020
**Title**: Repository Recovery — Unicode filename fix + rollback anchors
**Track**: Repository Engineering (`REPO-XXX` family)
**Priority**: Critical
**Status**: 🟡 IN PROGRESS — Phase 1 (Recovery Audit) complete; Phase 2
(Recovery, mutating) and Phase 3 (Validation) gated on Director approval
of `docs/governance/MIGRATION_PLAN.md` and confirmation of the
branch-operation authority.
**Context**: First implementation task after Engineering Governance v1.1
was declared FROZEN. Executes the recovery diagnosed by
`BRANCH-FORENSICS-001`, under the frozen v1.1 repository policies.

## Objective

Restore repository merge-integrity by removing the single invisible
U+2060 character from `strategies/strategy_manager.py` on `main`, after
first establishing rollback anchors — closing both the merge-conflict
defect and the zero-rollback-anchor gap.

## Phases (per ORDER-020)

- **Phase 1 — Recovery Audit** ✅ COMPLETE (read-only): Repository
  Health Check, Branch Integrity Check, Git History Validation, Rollback
  Readiness Audit. Results recorded in `docs/governance/MIGRATION_PLAN.md`
  Phase 1 — re-confirmed fresh against live refs: single-file,
  single-U+2060 root cause, zero code diff, zero existing tags.
- **Phase 2 — Recovery** ⏸ (mutating, gated): create `pre-recovery-*`
  rollback anchors first; fix the Unicode filename on `main` (single
  content-neutral `git mv`, forward commit, no force-push); create the
  `post-recovery-main` checkpoint tag.
- **Phase 3 — Validation** ⏸ (gated): `git fsck` + no-U+2060 sweep;
  `git merge-tree` main↔production and main↔working both zero-conflict;
  Recovery Report → request `Repository Recovery → APPROVED`.

## Deliverable this stage

`docs/governance/MIGRATION_PLAN.md` — the single control document for
Recovery **and** the subsequent Migration, per the Director's
recommendation, containing: Recovery phases, Migration phases, Rollback
Plan, Risk Analysis, Success Criteria, Exit Criteria, Recovery
Checklist, Migration Checklist, and the explicit Director confirmations
needed before Phase 2 executes.

## Why Phase 2 is gated (not stalling)

The frozen `docs/governance/policies/Repository_Policy.md` §5 mandates
Audit → Plan → **Approval** → Execution for any repository-level change.
Phase 2 is the first *mutating* repository operation of the session
(committing to `main`, pushing tags), and the Director's own ORDER-020
recommendation was to have MIGRATION_PLAN.md in place first. Two points
need explicit Director confirmation before Phase 2:

1. Approval of `MIGRATION_PLAN.md` as the control document.
2. Branch-operation authority: that ORDER-020 authorizes pushing
   annotated tags and committing the content-neutral fix **directly to
   `main`** (the only branch carrying the corrupted path), which the
   standing "develop on your designated branch" rule otherwise reserves.

## Constraints (respected so far)

Phase 1 used only read-only git plumbing (`fetch`, `ls-tree`,
`merge-base`, `merge-tree`, `tag -l`) — no branch, tag, merge, or
push performed; working tree clean throughout. No mutating operation
taken pending approval.

## Depends on

`BRANCH-FORENSICS-001` (APPROVED root cause), Engineering Governance
v1.1 (FROZEN). Blocks REPO-002 (Migration), which starts only after
Recovery is APPROVED.

## Notes

Filed as `REPO-RECOVERY-001` on the Repository Engineering track (the
"Repository Recovery" backlog item ORDER-010 queued, now activated by
ORDER-020).
