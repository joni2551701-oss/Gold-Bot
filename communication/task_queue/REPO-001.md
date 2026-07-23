# REPO-001

**Title**: Repository Engineering Migration
**Track**: Repository Engineering (separate from Platform Tasks,
Engineering/`DEVOPS-XXX`, and Governance/`GOVERNANCE-REVIEW-XXX` — see
`communication/task_queue/QUEUE.md`)
**Priority**: Critical
**Status**: ✅ DELIVERED — awaiting Director approval before REPO-002
(Implementation) may start.
**Phase**: Engineering Infrastructure — first task after Governance v1.0
Freeze.

## Objective

Audit the repository's real branch/PR/CI/protection state, audit the
two existing `claude/*` branches, and produce a complete branch
strategy, migration plan, branch protection proposal, collaboration
model, cleanup proposal, and risk analysis — so the Director can decide
whether and how to proceed with REPO-002 (Implementation). Audit +
Proposal + Plan only.

## Constraints (respected)

- No branch created.
- No feature branch created.
- No branch deleted.
- No protection enabled.
- No merge performed.
- No repository setting changed.

Only: Audit, Proposal, Engineering Plan.

## Delivered

`docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md` — the single
report, covering all 8 requested deliverables plus Director
Recommendations and Final Recommendation:

1. Repository Audit Report
2. Claude Branch Audit
3. Branch Strategy
4. Migration Plan (7 phases)
5. Branch Protection Proposal
6. Collaboration Model
7. Cleanup Proposal
8. Risk Analysis

**Key findings**: only 3 branches exist total (`main`, and 2 `claude/*`
branches) — no stale/orphaned branch cleanup is actually needed, since
both `claude/*` branches are currently load-bearing (one is the real,
undocumented-by-name production branch per `production_deploy.yml`'s
own header comment and `trading_bot.yml`'s pinned checkout ref; the
other is the current active Platform Worker line, a strict superset of
the first). `main` is the configured default branch but has no CI, no
deploy pipeline, and is 171 commits behind the real production content.
Zero branch protection exists anywhere. Zero tags/releases exist
anywhere — no rollback anchor. 2 PRs are open (11+ days and same-day),
neither merged; PR #2 untouched per standing Director order.

**Final Recommendation**: Migration Plan is complete and ready for
Director decision; recommend approving it and authorizing REPO-002 to
execute Phases 1–7 in sequence, starting with Phase 1 (rollback-anchor
tags — zero risk, closes the one true present-tense gap regardless of
what else is decided).

**Addendum (Director follow-up)**: Director requested direct, evidenced
answers to 5 verification questions before any governance document is
written, so future policy is based on confirmed fact rather than the
original brief's assumption. Added as new §0 in the report: (Q1) since
which exact commit/date `main` and production diverged (2026-07-12,
`ad1affe`); (Q2) confirmation the deploy-branch choice was a deliberate,
already-documented decision (`docs/PHASE_P1_AUDIT.md`), not a temporary
fix or historical mistake; (Q3) a full files/lines/directory/commit-type
breakdown of the 171-commit gap; (Q4) the VPS rollback mechanism
(`docs/deployment/ROLLBACK.md`) is real but unexercised (no VPS yet) and
is distinct from the still-zero git-level rollback anchor; (Q5) both PR
#1 and PR #2 report GitHub's own `mergeable_state: "dirty"` (a real
conflict) plus zero reviews, traced to `main`'s own post-divergence
filename-repair commits (fixing invisible Unicode characters and a
typo'd directory name) colliding with the production branch's
independent history of the same files.

## Depends on

GOVERNANCE-REVIEW-001 — per Director instruction, this is the first
Engineering task after Governance v1.0 is frozen.

## Notes

This task does not touch PR #2, per the standing Director instruction
recorded earlier in this session ("Worker: merge qilmaydi; close
qilmaydi; review qilmaydi") — that instruction is treated as still in
force and was not reinterpreted or narrowed for this task.
