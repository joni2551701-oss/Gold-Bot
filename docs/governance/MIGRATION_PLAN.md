# Repository Recovery & Migration — Control Plan (MIGRATION_PLAN.md)

The single control document for GoldBot's Repository Recovery
(ORDER-020) and the Repository Migration that follows it. It
operationalizes the frozen Engineering Governance v1.1 policies —
`docs/governance/policies/Repository_Policy.md`,
`Branch_Policy.md`, `Branch_Protection_Policy.md`, and
`docs/governance/standards/Git_Workflow_Standard.md` — into a concrete,
checklisted, rollback-anchored execution sequence.

**Execution posture**: this document is Audit + Plan. Per
`Repository_Policy.md` §5 (Audit → Plan → Approval → Execution →
Verification), the **mutating** steps below (fixing `main`, creating
tags, creating `develop`/`feature/*`, deleting branches) are **not
executed until the Director approves this plan** and confirms the
branch-operation authority flagged in §"Director Confirmations Needed."
Phase 1 (read-only audit) is already complete and recorded here.

---

## Phase 1 — Recovery Audit (✅ COMPLETE, read-only)

Run fresh against live refs (`git fetch` + plumbing), not assumed from
the earlier `BRANCH-FORENSICS-001`:

| Check | Result |
|---|---|
| **Repository Health** | Working tree clean; current branch `claude/trading-ai-arch-review-tgszrz`; 3 branches total (`main` @ `5618adec`, production `claude/code-analysis-optimization-pwfo3q` @ `d911b97`, working branch @ `45eee10`). |
| **Branch Integrity** | `main` carries the corrupted path `strategies/strategy_manager.py⟨U+2060⟩`; the production branch and the working branch both carry the clean `strategies/strategy_manager.py`. File **content** is byte-identical on all three (same blob) — path-only defect. |
| **Git History Validation** | Merge-base of `main` and production = `ad1affe` (2026-07-12). `git merge-tree` reports **exactly one** rename/rename conflict (`strategy_manager.py`), for both `main`↔production and `main`↔working — no other conflict anywhere. |
| **Rollback Readiness** | **Zero tags** locally and on the remote. No rollback anchor exists — creating anchors is the mandatory first mutating action of Phase 2. |

**Conclusion**: the audit re-confirms a single-file, single-invisible-
character (U+2060 WORD JOINER) root cause with zero code difference.
The recovery is low-risk and content-neutral, exactly as
`BRANCH-FORENSICS-001` established.

## Phase 2 — Recovery (⏸ pending plan approval)

Executed strictly in this order (rollback anchor **before** any
change, per `Branch_Protection_Policy.md` §7 /
`Git_Workflow_Standard.md` §9):

1. **Create rollback anchors first** — annotated tags on each current
   tip:
   - `pre-recovery-main` → `main` @ `5618adec`
   - `pre-recovery-production` → production @ `d911b97`
   - `pre-recovery-working` → working branch @ `45eee10`
   Pushed to the remote. This closes the zero-anchor gap before
   anything is touched.
2. **Fix the Unicode filename on `main`** — a single content-neutral
   rename removing the trailing U+2060 character:
   `git mv "strategies/strategy_manager.py⟨U+2060⟩" strategies/strategy_manager.py`
   on `main`, committed with a clear message, pushed to `main`. This is
   a normal forward commit — **no history rewrite, no force-push**
   (`Git_Workflow_Standard.md` §8).
3. **Create a post-recovery checkpoint** — annotated tag
   `post-recovery-main` on the fixed `main` tip, pushed. This is the
   named "known-good after recovery" checkpoint Migration branches from.

**Note on where the fix lands**: the corrupted path exists only on
`main`, so the fix must be committed to `main` — not to the current
working branch. This crosses the standing "develop on your designated
branch" rule and requires the explicit Director confirmation flagged
below.

## Phase 3 — Validation (⏸ pending Phase 2)

1. **Git Integrity Check** — `git fsck` clean; the fixed `main` tree
   contains the clean filename and no U+2060 remains anywhere
   (`git ls-tree` sweep).
2. **Merge Readiness Check** — `git merge-tree main <production>` and
   `git merge-tree main <working>` both report **zero conflicts** (the
   single rename/rename conflict is gone). This is the objective proof
   recovery succeeded.
3. **Recovery Report** — a short report recording the anchors created,
   the exact fix commit SHA on `main`, and the clean merge-tree result;
   `Repository Recovery → APPROVED` requested from the Director.

## Migration Phases (after Recovery is APPROVED)

Per `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md` §4 and
`Branch_Policy.md`, executed only under a further Director Order
(REPO-002), never folded into Recovery:

1. **Backup / anchor** — `pre-migration-*` tags on the post-recovery
   tips (a second anchor set, distinct from Recovery's).
2. **Create `develop`** from the production branch's post-recovery tip
   (the real, current codebase).
3. **Create `feature/core`** from the same point.
4. **Create `feature/platform`** from the working branch's tip
   (carrying the Platform/Governance work).
5. **Merge verification** — confirm `develop`/`feature/*` bases are
   consistent; run the full Commit Protocol on `develop`; confirm CI on
   `develop` (add `ci.yml` to `develop` — a `.github/workflows/` change
   that is itself separately authorized).
6. **Branch cleanup** — resolve PR #1/#2 and retire the session-named
   branches, **only** after Phase 5 confirms every commit is captured
   (`Branch_Policy.md` §8); never before, never as a side effect.
7. **Branch protection** — apply `Branch_Protection_Policy.md`'s rules
   to `main` and `develop`, last, once the branches hold everything.

**Critical migration constraint** (from `REPO-001` §8): `trading_bot.yml`
and `production_deploy.yml` pin the production branch by name. Any
rename/delete of that branch updates those workflow files' refs in the
**same** phase, before or atomically with the branch operation — never
after — or the live scheduled trading pipeline breaks immediately.

## Rollback Plan

- **Every mutating step is preceded by an annotated tag** (Phase 2.1,
  Migration Phase 1), so a named known-good state always exists — the
  gap that did not exist before this plan.
- **Recovery rollback**: if the `main` fix goes wrong, `git reset --hard
  pre-recovery-main` restores `main` exactly; the anchor tag makes this
  a named, safe operation, not a scramble for a SHA.
- **Migration rollback**: `develop`/`feature/*` are new branches — a
  failed migration is rolled back by deleting the new branches (they
  hold nothing not already on the source branches by construction) and,
  if a source branch was altered, resetting it to its `pre-migration-*`
  anchor.
- **No rollback uses force-push on a protected branch**; recovery
  rollback of `main` (unprotected until Migration Phase 7) is a
  Director-authorized reset to a named anchor.
- **Deployment rollback** (`docs/deployment/ROLLBACK.md`) is a separate
  VPS mechanism, unaffected by and not used for git-level rollback.

## Risk Analysis

| Risk | Severity | Mitigation |
|---|---|---|
| Fix applied to wrong branch / working branch instead of `main` | Medium | Fix is scoped to `main` explicitly (Phase 2.2); Director confirms the `main`-operation authority first. |
| Losing a known-good state during a mutating step | High → Low | Rollback anchors created **first** (Phase 2.1, Migration Phase 1) — this plan's core safeguard. |
| Breaking the live trading/deploy pipeline during Migration | Critical | Update `trading_bot.yml`/`production_deploy.yml` pinned refs in the same phase as any production-branch rename/delete (Migration constraint above). |
| A second invisible-character defect elsewhere | Low | `git ls-tree` sweep for non-ASCII/invisible chars in filenames during Phase 3.1; `merge-tree` already shows only one conflict. |
| Force-push / history rewrite | Eliminated by design | Recovery is a forward `git mv` commit; no rebase, no force-push (`Git_Workflow_Standard.md` §8). |
| PR #1/#2 disruption | Low | PRs resolved only in Migration Phase 6, after verification, under explicit Order; PR #2 untouched until then. |

## Success Criteria (Director-updated, this decision)

- Rollback anchors exist for every branch before any change (closes the
  zero-anchor gap).
- The `strategy_manager.py` **rename/rename conflict is resolved** —
  `main`'s filename byte-identical to production's/working's (blob
  `89a66416` preserved).
- `git merge-tree main <production>` and `main <working>` report zero
  conflicts.
- `git fsck` clean.
- A Recovery Report is delivered and the Director returns `Repository
  Recovery → APPROVED`.

**Explicitly NOT a success criterion**: eliminating all Unicode
filenames from `main`. A fresh sweep found 9 U+2060 filenames on `main`;
testing proved fixing only `strategy_manager.py` yields 0 conflicts
while fixing all 9 introduces 4. Per Director decision, the other 8 are
**stale artifacts left to Migration** (superseded when `main` is
reconciled from production) and are **not** renamed inside Recovery.

## Exit Criteria

- **Recovery** exits when all Success Criteria above are met and the
  Director approves the Recovery Report.
- **Migration** (a later Order) exits when the four-branch model is live,
  protected, verified, the workflow files' refs are correct, PRs are
  resolved, and the Director declares the branch strategy in force.
- This control document remains the single reference throughout; it is
  updated (not replaced) as each phase completes.

## Recovery Checklist

```
Recovery Checklist
☑ Phase 1 audit complete (health / integrity / history / rollback readiness)   [done]
☑ Director approval of this plan + branch-operation authority confirmed          [MIGRATION_PLAN APPROVED; ORDER-020 Phase 2 AUTHORIZED]
◐ Rollback anchors created ... and pushed   [created LOCALLY; tag push CONFIRMED blocked by the Claude Code git-proxy — see Diagnostic Evidence below]
□ Unicode filename fixed on main (single git mv, forward commit, pushed)          [not attempted from this session; main-push scope NOT independently tested]
□ post-recovery-main checkpoint tag created and pushed                            [tag push CONFIRMED blocked]
□ git fsck clean; no U+2060 remains (ls-tree sweep)
□ merge-tree main↔production = zero conflicts
□ merge-tree main↔working = zero conflicts
□ Recovery Report delivered
□ Director verdict: Repository Recovery APPROVED
```

### Phase 2 execution blocker — Diagnostic Evidence (HTTP-trace confirmed, ORDER-022)

Phase 2 began under ORDER-020 and stopped at the first push. The
push-source of the block was investigated with `GIT_TRACE_CURL`/
`GIT_CURL_VERBOSE`; the following are **confirmed by HTTP trace**, and
each earlier assumption is corrected below.

**CONFIRMED (by HTTP trace):**
- The git remote is a **Claude Code local git-proxy** at
  `http://local_proxy@127.0.0.1:41729/...` (auth challenge:
  `Www-Authenticate: Basic realm="Git Proxy"`), not github.com directly.
- **GitHub accepted the receive-pack advertisement**: after auth,
  `GET /info/refs?service=git-receive-pack` returns **200 OK**
  (`agent=github/spokes-receive-pack…`). GitHub grants push capability.
- **The 403 is returned on the ref-update `POST /git-receive-pack`**,
  with body: `ERR push contains a ref outside refs/heads/*; only branch
  updates are permitted.` The `Request-Id: req_011Cd…` header is the
  Claude Code/Anthropic request-id format (not GitHub's
  `X-GitHub-Request-Id`).
- **Therefore: the 403 originates from the Claude Code git-proxy policy
  layer, not from GitHub repository permissions.** The policy rejects
  any push containing a ref **outside `refs/heads/*`** — so **tag pushes
  are blocked** (`refs/tags/*` is outside `refs/heads/*`).

**NOT TESTED / assumption withdrawn:**
- A previous note said `refs/heads/main` was blocked "by inference."
  **That inference is withdrawn.** No standalone push to
  `refs/heads/main` was executed (it would be a real mutating commit,
  and the session is in WAIT STATE). The policy message says branch
  updates *are* permitted, so **no evidence currently exists that a
  `main` push is itself rejected** — it is simply untested. Treat
  "`main` push from this session" as **Not Tested**, neither confirmed
  allowed nor confirmed blocked.

**Impact on the plan (unchanged):** the safety sequence requires the
rollback **anchor tags first**, and tag pushes are confirmed blocked
from this session — so a plan-compliant recovery still requires the
Authorized Operator (Option 2). Remote is untouched (0 tags, `main`
unchanged). Per policy, the 403 was never retried-to-route-around; the
repeated requests here were read-only diagnostics that mutated nothing.
Full record: `communication/task_queue/REPO-RECOVERY-001.md`. This is an
environment/authorization boundary, not a defect in the recovery plan.

## Migration Checklist

```
Migration Checklist (executed only under a later Director Order, REPO-002)
□ Recovery APPROVED (prerequisite)
□ pre-migration-* anchors created
□ develop created from production post-recovery tip
□ feature/core created
□ feature/platform created
□ merge verification + CI green on develop
□ trading_bot.yml / production_deploy.yml refs updated in lockstep with any production-branch change
□ PR #1 / PR #2 resolved (after verification, under explicit Order)
□ session-named branches retired (only after every commit confirmed captured)
□ branch protection applied to main + develop (last)
□ Director declares the new branch strategy in force
```

## Director Confirmations Needed (before Phase 2 executes)

1. **Approve this MIGRATION_PLAN.md** as the control document.
2. **Confirm branch-operation authority for Recovery** — specifically
   that ORDER-020 authorizes: (a) pushing annotated tags to the remote,
   and (b) committing the single content-neutral filename fix directly
   to `main` (which the standing "develop on your designated branch"
   rule otherwise reserves). The fix cannot land anywhere but `main`,
   since that is the only branch carrying the corrupted path.

## References

- `docs/governance/policies/Repository_Policy.md` (§5–§10),
  `Branch_Policy.md`, `Branch_Protection_Policy.md`;
  `docs/governance/standards/Git_Workflow_Standard.md` — the frozen
  v1.1 policies this plan executes.
- `docs/BRANCH_FORENSICS_001.md` — the root-cause audit this recovery
  acts on.
- `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md` — the migration
  audit/plan this document operationalizes.
- `docs/deployment/ROLLBACK.md` — the separate deployment-rollback
  mechanism.
- `communication/task_queue/REPO-002.md` — the Migration task this plan
  feeds (issued separately after Recovery).
