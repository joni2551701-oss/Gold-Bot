# REPO-RECOVERY-001 (Repository Recovery)

**Order**: ORDER-020
**Title**: Repository Recovery — Unicode filename fix + rollback anchors
**Track**: Repository Engineering (`REPO-XXX` family)
**Priority**: Critical
**Status**: 🟢 READY FOR AUTHORIZED OPERATOR — Worker side complete.
Director confirmed the one-file scope, updated the Exit Criteria, and
**APPROVED** `docs/governance/RECOVERY_OPERATOR_RUNBOOK.md`. The
Authorized Operator (Option 2, ORDER-021) executes the approved runbook;
the Worker then verifies the returned results against the tested
expected values and writes the Recovery Report for the Director's
`APPROVED` / `CHANGES REQUIRED` verdict.

**Push blocker (resolved by routing, not bypassed)**: the Claude Code
git-proxy returns HTTP 403 for pushing **tags** (any ref outside
`refs/heads/*`); a `refs/heads/main` push from this session was **not
tested**. Never retried or routed around; the Director chose Option 2
(a differently-scoped Authorized Operator) rather than weaken the
policy. HTTP-trace-confirmed details below (ORDER-022 correction).

**Director-updated Exit Criteria** (ORDER-020, this decision): Recovery
succeeds when — `strategy_manager.py` rename/rename conflict resolved;
`main`↔production merge conflict = 0; `main`↔working merge conflict = 0;
rollback tags created; `git fsck` passes. The other 8 Unicode filenames
are out of scope (superseded by Migration; not renamed in Recovery).

## Phase 2 execution attempt — blocker record (STOP → AUDIT → Director Decision)

The Director authorized Phase 2 (ORDER-020) with an explicit 5-step
order. Execution began and stopped at the first push:

- **Step 1 (rollback anchors)** — the three annotated tags
  (`pre-recovery-main` @ `5618adec`, `pre-recovery-production` @
  `d911b97`, `pre-recovery-working` @ `04b9223`) were created **locally**
  and verified to point at the correct SHAs. Pushing them returned
  **`HTTP 403`** (`send-pack: unexpected disconnect`).
- **Remote state after the failure**: completely untouched — 0 tags on
  the remote, `main` still `5618adec`, working branch still `04b9223`,
  local working tree clean. Nothing partial reached the remote.
- **Local state**: the three anchor tags exist locally-only (unpushed).
  No mutating operation touched `main` (Step 2 was never reached).

## Diagnostic Evidence — HTTP-trace confirmed (ORDER-022 / DOC-CORRECTION-001 → ✅ APPROVED)

*DOC-CORRECTION-001 (ORDER-022) was reviewed and **APPROVED** by the
Director: root-cause attribution corrected to the Claude Code git-proxy,
evidence/assumption separation confirmed, the `main`-blocked claim
withdrawn (Not Tested), and Recovery/Migration logic verified unchanged.
The recovery documentation is in its final, evidence-based state.*


The push-source of the 403 was investigated with `GIT_TRACE_CURL` /
`GIT_CURL_VERBOSE`. Facts are labelled **Confirmed** (HTTP evidence) or
**Not Tested**; no assumption is labelled Confirmed.

**Confirmed (by HTTP trace):**
- The git remote is a **Claude Code local git-proxy** at
  `http://local_proxy@127.0.0.1:41729/...`, not github.com directly —
  its auth challenge self-identifies: `HTTP/1.1 401 Unauthorized`,
  `Www-Authenticate: Basic realm="Git Proxy"`.
- **GitHub accepted the receive-pack advertisement**: after auth,
  `GET /info/refs?service=git-receive-pack` → **200 OK**,
  `agent=github/spokes-receive-pack…`. GitHub advertised push capability.
- **The 403 is returned on the ref-update `POST /git-receive-pack`**,
  body: `ERR push contains a ref outside refs/heads/*; only branch
  updates are permitted.` The `Request-Id: req_011Cd…` header is the
  Claude Code/Anthropic format (not GitHub's `X-GitHub-Request-Id`).
- **The 403 originates from the Claude Code git-proxy policy layer, not
  from GitHub repository permissions.** No evidence indicates GitHub
  repository permissions caused the rejection.
- **Tag pushes are therefore blocked** — `refs/tags/*` is outside
  `refs/heads/*`. Confirmed by the HTTP 403 response body.

**Not Tested (assumption withdrawn):**
- Whether a `refs/heads/main` push is rejected from this session is
  **not known** — no standalone push to `refs/heads/main` was executed
  (it would be a real mutating commit; the session is in WAIT STATE).
  The earlier "by inference, `main` is blocked" claim is **withdrawn**.
  The policy message states branch updates *are* permitted, so **no
  evidence currently exists that a `main` push itself is rejected**.
  Status: **Not Tested**.

**Why the Authorized Operator is still required** (unchanged): the
safety sequence needs the rollback **anchor tags first**, and tag
pushes are confirmed blocked from this session — so a plan-compliant
recovery cannot be performed here regardless of the `main` question. The
repeated push requests during diagnosis were read-only (all denied;
zero mutation), never retried to route around the policy.

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
(the conflicting `strategy_manager.py` + 8 more: `ai_layer/ai_engine/ai_prompt.py`,
`ai_layer/confidence_ai/confidence_model.py`, `context_layer/market_structure/market_structure.py`,
`database_layer/trade_repository/signal_repository.py`, `signal_layer/signal_builder/models.py`,
`signal_layer/signal_engine/signal_engine.py`, `strategy_layer/strategy_library/amd_strategy.py`,
`strategy_layer/strategy_library/fvg_strategy.py`). Both scopes were tested locally:

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
   configuration change) to permit `refs/tags/*` (confirmed blocked)
   — and `refs/heads/main` if not already permitted (untested) — then
   re-run Phase 2 from here.
2. **Perform the recovery from a differently-scoped actor** — a session
   or operator whose git push scope allows tag pushes and a `main`
   commit (the fix itself is a single, content-neutral `git mv` on
   `main` plus 4 tags, fully specified in
   `docs/governance/MIGRATION_PLAN.md`). **← Director chose this
   (Option 2, ORDER-021).**
3. **Defer** Repository Recovery until the push-scope question is
   resolved; Governance v1.1 remains FROZEN and the plan remains ready.
**Context**: First implementation task after Engineering Governance v1.1
was declared FROZEN. Executes the recovery diagnosed by
`BRANCH-FORENSICS-001`, under the frozen v1.1 repository policies.

## Objective

Restore repository merge-integrity by removing the single invisible
U+2060 character from `strategy_layer/strategy_manager/strategy_manager.py` on `main`, after
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
