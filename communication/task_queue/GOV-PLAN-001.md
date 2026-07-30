# GOV-PLAN-001

**Order**: ORDER-013
**Title**: Engineering Governance v1.1 Master Plan
**Track**: Governance (same track as `GOVERNANCE-REVIEW-XXX` — see
`communication/task_queue/QUEUE.md`)
**Priority**: Critical
**Status**: ✅ DELIVERED — awaiting Director review before GOV-001
through GOV-009 are individually issued.

## Objective

Produce a single Master Plan covering all 9 Governance v1.1 documents
(Director.md, Core_Worker.md, Platform_Worker.md, Collaboration_Rules.md,
Repository_Policy.md, Branch_Policy.md, Branch_Protection_Policy.md,
Engineering_Language_Policy.md, Git_Workflow_Standard.md) — Purpose,
Scope, Dependencies, Required Sections, Out of Scope, Acceptance
Criteria, Review Checklist, Freeze Criteria for each — so the Director
can issue each as its own separate, executable task without further
clarification. Planning only; no document itself written.

## Constraints (respected)

- No new governance document created (beyond this Master Plan itself).
- No existing Constitution, Law, Policy, ADR, or Standard modified.
- No repository implementation performed.
- No branch operation performed.
- No GitHub settings changed.

## Delivered

`docs/GOVERNANCE_V1_1_MASTER_PLAN.md` — Writing Order, Cross-Document
Dependency Map, and a full sub-plan (all 8 required fields) for each of
GOV-001 through GOV-009, plus a shared Review Checklist pattern and the
Freeze Sequencing rule (Governance v1.1 as a whole Freezes only once
all 9 individually Freeze).

**Naming flag raised**: the Director's own note referred to launching
"TASK-001 through TASK-009" for the 9 documents; `TASK-XXX` is already
a reserved prefix (Platform Tasks track, `TASK-001`–`TASK-005`
allocated). Proposed `GOV-001` through `GOV-009` instead, mapping 1:1
onto the Director's own ordering, flagged explicitly rather than
silently substituted.

**Key cross-references identified for each future task's own TASK 0**:
`GOV-001` must reconcile with `docs/policies/DIRECTOR_POLICY.md`;
`GOV-002`/`GOV-003` with `docs/HANDOFF.md` and `docs/CURRENT_PHASE.md`;
`GOV-004` with `communication/README.md`'s 9-folder index; `GOV-005`
with `docs/PHASE_BRANCH_SYNC_AUDIT.md`/`PHASE_P1_AUDIT.md`/`DEPLOYMENT.md`;
`GOV-006`/`GOV-007` directly promote `REPO-001` §3/§5's proposals;
`GOV-008` has no existing overlap (confirmed via `GOVERNANCE-REVIEW-001`'s
full policy read); `GOV-009` must reconcile with `docs/standards/COMMIT_STANDARD.md`.

## Depends on

`docs/GOVERNANCE_REVIEW_001.md` (Part B's gap findings inform several of
the 9 documents' scope), `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md`
and `docs/BRANCH_FORENSICS_001.md` (direct source material for
GOV-005/006/007/009).

## Notes

Planning only — no code, no branch, no settings action taken. Each of
GOV-001 through GOV-009 remains a future, separately-issued task; none
is started by this plan.
