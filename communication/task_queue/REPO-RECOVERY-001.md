# REPO-RECOVERY-001 (Repository Recovery)

**Order**: ORDER-020
**Title**: Repository Recovery — Unicode filename fix + rollback anchors
**Track**: Repository Engineering (`REPO-XXX` family)
**Priority**: Critical
**Status**: ⛔ BLOCKED (Phase 2) — Director approval + authority granted
(MIGRATION_PLAN.md APPROVED, ORDER-020 Phase 2 AUTHORIZED), but the
execution is blocked by an **environment egress-policy denial**: the
session's git proxy permits pushes to the designated working branch
only and returns **HTTP 403** for pushing tags (and, by inference, for
pushing to `main`). Phase 1 remains complete; Phase 2 cannot proceed
from this session until the push scope is widened or the recovery is
performed by a differently-scoped actor. **Escalated to Director.**

## Phase 2 execution attempt — blocker record (STOP → AUDIT → Director Decision)

The Director authorized Phase 2 (ORDER-020) with an explicit 5-step
order. Execution began and stopped at the first push:

- **Step 1 (rollback anchors)** — the three annotated tags
  (`pre-recovery-main` @ `5618adec`, `pre-recovery-production` @
  `d911b97`, `pre-recovery-working` @ `04b9223`) were created **locally**
  and verified to point at the correct SHAs. Pushing them returned
  **`HTTP 403` from the egress proxy** (`send-pack: unexpected
  disconnect`).
- **Diagnosis**: branch commits to `claude/trading-ai-arch-review-tgszrz`
  have succeeded throughout this session; only the *tag* push is denied.
  The agent proxy README maps 403 to "destination not allowed by your
  organization's egress policy for this session — do not retry or route
  around it, report it." Combined with the working-branch pushes
  succeeding, the policy is **ref-scoped**: pushes are permitted to the
  designated working branch ref only, and denied for `refs/tags/*` (and
  therefore, by strong inference, for `refs/heads/main` — the Step 2
  target). Not retried, not routed around (per proxy policy and per this
  session's own governance).
- **Remote state after the failure**: completely untouched — 0 tags on
  the remote, `main` still `5618adec`, working branch still `04b9223`,
  local working tree clean. Nothing partial reached the remote.
- **Local state**: the three anchor tags exist locally-only (unpushed);
  they are valid and ready to push if/when the policy is widened. No
  mutating operation touched `main` (Step 2 was never reached).

This constraint also coincides with this session's own standing rule
("never push to a different branch without explicit permission") being
enforced at the infrastructure level: even with the Director's explicit
authorization, the environment's proxy will not permit a push to `main`
or to tag refs from this session.

## ORDER-021 — Operator handoff prepared + a scope finding (Worker preparation, no push)

Per ORDER-021 (Director chose Option 2), the Worker prepared and
**locally tested** the full recovery (throwaway branch, zero push):

- `docs/governance/RECOVERY_OPERATOR_RUNBOOK.md` — exact, tested
  commands for the Authorized Operator (anchor tags → single `git mv`
  fix on `main` → checkpoint tag → validation), with verified expected
  results (blob `89a66416` preserved; merge-tree `main`↔production and
  `main`↔working both 0 conflicts; fsck clean).

**Scope finding (No Silent Decisions — Director confirmation requested)**:
a fresh full-tree sweep found **9** U+2060-corrupted filenames on `main`
(the conflicting `strategy_manager.py` + 8 more: `ai/ai_prompt.py`,
`ai/confidence_model.py`, `context/market_structure.py`,
`database/signal_repository.py`, `signals/models.py`,
`signals/signal_engine.py`, `strategies/amd_strategy.py`,
`strategies/fvg_strategy.py`). Both scopes were tested locally:

- Fix **only** `strategy_manager.py` → **0** merge conflicts (correct).
- Fix **all 9** → **4** merge conflicts introduced (harmful).

The 8 extra files have different content on `main` vs. production (171
commits of divergence); renaming `main`'s stale copies to the clean
names collides them with production's evolved versions. They are stale
artifacts that Migration supersedes when `main` is reconciled from
production. **Recommendation: fix only `strategy_manager.py`** (confirms
the original scope) and leave the 8 to Migration. Requesting Director
confirmation that the Exit Criterion "Unicode filename problem resolved"
= the conflicting file fixed + 0 merge conflicts, with the 8 documented
as superseded-by-Migration.

## Resolution options (for the earlier push blocker — Director chose Option 2)

1. **Widen this session's git push scope** (an environment/admin
   configuration change) to permit `refs/tags/*` and `refs/heads/main`,
   then re-run Phase 2 from here — the local anchor tags are already
   staged and ready.
2. **Perform the recovery from a differently-scoped actor** — a session
   or operator whose egress policy allows pushing tags and to `main`
   (the fix itself is a single, content-neutral `git mv` on `main` plus
   4 tags, fully specified in `docs/governance/MIGRATION_PLAN.md`).
3. **Defer** Repository Recovery until the push-scope question is
   resolved; Governance v1.1 remains FROZEN and the plan remains ready.
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
