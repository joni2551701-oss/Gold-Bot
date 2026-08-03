# REPO-001 — Repository Engineering Migration

**Task**: REPO-001, Critical priority, Engineering Infrastructure phase.
**Type**: Audit + Proposal + Engineering Plan only. No branch created, no
branch deleted, no merge performed, no protection enabled, no
repository setting changed — per this task's own Constraints. This
document is the sole deliverable; Implementation is a separate future
task (REPO-002), started only after Director approval of this plan.

**Method**: Every fact below comes from a live GitHub API read (branches,
PRs, tags, releases, registered workflows) and a local read of the
actual checked-out `.github/workflows/*.yml` files and git history —
not from memory or assumption. Where the real repository state differs
from what the Director's brief examples implied, that difference is
stated explicitly rather than silently smoothed over.

---

## 0. Director's Five Verification Questions (Answered)

Added after Director review, before proceeding to any governance
document — per Director instruction, decisions must follow confirmed
facts, not the original brief's assumption. Every answer below is
backed by a live re-check (GitHub PR API, `git log`/`git diff` against
the real refs), not a restatement of §1–§8's existing prose.

**Q1 — Why is production not `main`? Since when?**

Since **2026-07-12**, commit `ad1affe` ("Update config.py") — the exact
last common ancestor of `main` and the production branch, confirmed via
`git merge-base`. From that point, every commit building the real
TradingPipeline (`core.pipeline.TradingPipeline`, `platform_layer/telegram/polling.py`,
the 22-file Telegram Owner Panel, the full monitoring/database/
configuration layers) landed exclusively on
`claude/code-analysis-optimization-pwfo3q`. `main` received exactly 5
commits after that point, and none of them is real development (see
Q3/Q5). This is not a new discovery — `docs/PHASE_BRANCH_SYNC_AUDIT.md`
already formally audited and Director-decided this: *"`claude/code-analysis-optimization-pwfo3q`
is already the de facto production branch... This was a deliberate
decision made in an earlier phase, not an oversight discovered here."*
REPO-001 independently re-confirmed the fact rather than assuming that
prior audit still held, and found nothing has changed since.

**Q2 — Why does deploy run from `claude/code-analysis-optimization-pwfo3q`? Temporary or a historical mistake?**

Neither — a **deliberate, previously-documented engineering decision**,
not a stopgap and not an error. `docs/PHASE_P1_AUDIT.md` (Production
Deployment Pipeline Foundation) records it directly: that phase's own
brief literally named `main` as the trigger branch, but its TASK 0
audit found deploying literal `main` "would ship the stale skeleton to
the VPS" (`main` lacks `core/pipeline.py`, `platform_layer/telegram/polling.py`, and
the entire TradingPipeline architecture) — so it adopted the production
branch instead, matching what `trading_bot.yml` already did, and
explicitly flagged the choice in writing for Director visibility rather
than deciding it silently. The same document states that syncing `main`
to match would require "a separate, explicitly-scoped branch-sync phase
first (133+ commits of drift)" — explicitly out of scope for a
deployment-pipeline phase. The only real gap that prior audit itself
identified was that this decision lived in one workflow-file comment
rather than a proper governance document — precisely the gap a future
`Branch_Policy`/`Repository_Policy` document would close.

**Q3 — What is inside the 171 commits? docs? code? CI? workflows? releases?**

Measured directly (`git diff --stat`, `git log --format=%s` over
`origin/main..origin/claude/code-analysis-optimization-pwfo3q`):
**1,208 files changed, +137,391 / −650 lines** (GitHub's own PR #1 API
independently reports the same shape: 1,208 changed files,
+137,391/−597 — the small deletion-count difference is a rename-detection
accounting difference, not a discrepancy in substance). By top-level
directory: 394 files under `tests/`, 264 under `docs/`, 194 under `ai/`,
48 under `telegram/`, 35 under `database/`, plus `context/`, `core/`,
`monitoring/`, `analytics/`, `knowledge/`, `contracts/`, `configuration/`,
`strategies/`, `signals/`, `execution/`, `decision/`, `risk/`, `deploy/`,
and 4 files under `.github/` (the CI/deploy workflows themselves). By
commit-message shape: 25 commits tagged `feat:`, 10 tagged `fix:`, 132
reference "docs/Phase/audit/freeze" (this repo's own habit of pairing
every phase with an audit/freeze document, per Constitution Article 12),
3 mention CI/workflow changes directly. **This is 171 commits of real,
tested, documented architecture and feature work — not churn, and not
something a routine one-shot merge could safely absorb.**

**Q4 — If this branch broke today, where would rollback come from?**

Two distinct mechanisms exist in this repository, and they answer
different halves of this question:

- **VPS deployment rollback — fully built, but not yet exercised.**
  `docs/deployment/ROLLBACK.md` + `scripts/deploy/rollback.sh` +
  `scripts/deploy/release_manager.py` implement a real, atomic
  symlink-switch rollback: every deployed release stays on disk under
  `releases/`, a failed deploy's own post-restart health check triggers
  an automatic rollback to the last known-good release, and a manual
  rollback is one SSH command. **However, this protects a future live
  VPS deployment, not the git branch itself** — `docs/PHASE_P1_AUDIT.md`
  states directly that no VPS exists yet, so this mechanism has never
  actually been exercised against real traffic.
- **Git-level rollback (recovering the branch itself) — still zero
  anchor.** Re-confirmed again for this answer: 0 tags, 0 releases
  exist anywhere in this repository's history. If
  `claude/code-analysis-optimization-pwfo3q` were force-pushed over or
  otherwise damaged today, the only recovery path is manually locating
  a known-good commit SHA in `git log`/GitHub's own history (today,
  that would be `d911b97`) and resetting to it by hand — which depends
  entirely on someone already knowing which SHA was good. **This
  confirms §8's original finding and keeps it High Priority**: tagging
  today's tip of the production branch (and `main`) remains Migration
  Plan Phase 1 — a zero-risk, zero-side-effect action, independent of
  any larger branch-model decision, and nothing in this deeper check
  changes that recommendation.

**Q5 — Why is PR #2 still unmerged? Conflict? No review? Something else?**

All three, confirmed directly via the GitHub PR API rather than
inferred:

1. **A real merge conflict exists.** `pull_request_read(method: get)`
   reports `"mergeable_state": "dirty"` for **both** PR #2 and PR #1 —
   GitHub's own signal that its merge-commit computation cannot cleanly
   combine head and base. Not a guess; the API's own conflict state.
2. **Zero reviews exist.** `pull_request_read(method: get_reviews)` for
   PR #2 returns an empty list — no approval, no requested changes, no
   formal review from anyone.
3. **The structural reason a clean merge was never realistic**: `main`'s
   5 post-divergence commits are themselves a chain of broken-filename
   repairs. `git log --name-status` shows `ai_layer/ai_engine/ai_analyzer.py`,
   `strategy_layer/strategy_manager/strategy_manager.py`, and `strategy_layer/strategy_library/liquidity_strategy.py`
   were each renamed one or more times on `main` to fix invisible
   Unicode word-joiner characters and a typo'd `strategie/` directory
   name that had been embedded in the filenames (consistent with an
   earlier manual edit through GitHub's web file editor). Those same
   filenames exist on the production branch under their own,
   independently-clean history — and in `ai/`'s case, also in a
   different structural location entirely (`ai/analyzer/ai_analyzer.py`
   exists there too). Git's merge/rename-detection logic sees two
   independently-diverged, partially-overlapping histories for the same
   filenames and cannot reconcile them automatically. This is very
   likely the literal, file-level source of the "dirty" state, layered
   on top of the much larger structural divergence
   `docs/PHASE_BRANCH_SYNC_AUDIT.md` already documented (133+ commits
   of drift, `platform_layer/telegram/polling.py` and `platform_layer/telegram/owner/` not existing on
   `main` at all).

**In one sentence**: PR #2 is not stuck on a missing review — it is
stuck because `main` kept receiving small, uncoordinated direct edits
after real development moved to the production branch, and those edits
are just different enough to produce a real, tool-confirmed conflict on
top of the pre-existing structural drift.

---

## 1. Repository Audit Report

**Branches** (3 total, confirmed via `list_branches` and `git ls-remote`
— no branch beyond these three exists):

| Branch | Latest commit | Protected | Role (confirmed from code, see below) |
|---|---|---|---|
| `main` | `5618adec`, 2026-07-20, "Add owner_snapshot.yml to main (workflow registration fix)" | No | **Configured default branch** (`origin/HEAD` → `refs/heads/main`). **Not the real production branch** — see Finding 1. |
| `claude/code-analysis-optimization-pwfo3q` | `d911b97`, 2026-07-23 12:41, "V2 Phase 6 Freeze: audit, cleanup, and freeze documentation" | No | **The actual production branch** — explicitly named as such in `production_deploy.yml`'s own header comment and pinned as the checkout `ref:` in `trading_bot.yml` (the live scheduled trading runner). |
| `claude/trading-ai-arch-review-tgszrz` | `f505858`, 2026-07-23 22:07 (this session's own HEAD) | No | Current active Platform Worker development line — a strict superset of the production branch (see Finding 3). |

**Default branch**: `main` (confirmed via `git ls-remote --symref origin HEAD` → `refs/heads/main`).

**Branch protection**: **None on any of the 3 branches.** `list_branches`
reports `"protected": false` for `main`, the production branch, and the
current working branch alike. No required review, no required status
check, no push restriction exists anywhere in this repository today.

**Open PRs** (2 total — both open, neither merged, neither closed):

| PR | Head → Base | Opened | Title |
|---|---|---|---|
| #1 | `claude/code-analysis-optimization-pwfo3q` → `main` | 2026-07-12 | "fix: stabilize imports and config path" |
| #2 | `claude/trading-ai-arch-review-tgszrz` → `main` | 2026-07-23 | "fix: stabilize imports and config path" |

Both carry an identical, generic auto-generated title and an identical
attribution footer differing only by session ID — consistent with the
Claude Code environment auto-opening a PR when a session branch is
first pushed, not with a hand-authored change description. **Per
standing Director instruction, PR #2 is never merged, closed, or
reviewed by the Worker — no action was taken on either PR during this
audit, only factual observation.**

**Closed PRs**: none. `list_pull_requests` with `state=all` returns
exactly the 2 open PRs above and nothing else.

**Stale branches**: none beyond what's already covered above — there
are only 3 branches in the entire repository, so there is no long tail
of abandoned feature branches to identify.

**GitHub Actions workflows** (5 registered, confirmed via
`actions_list(method=list_workflows)`):

| Workflow | File | Registered on branch(es) | Trigger |
|---|---|---|---|
| GoldBot CI | `ci.yml` | Production branch + current working branch only — **not on `main`** | `push` to `main`/`claude/**`, `pull_request`, `workflow_dispatch` |
| GoldBot Owner Snapshot Reporter | `owner_snapshot.yml` | `main` only — **not on the production branch** | `schedule` (every 15 min), `workflow_dispatch` |
| GoldBot Production Deployment | `production_deploy.yml` | Production branch + current working branch only — **not on `main`** | (deploy pipeline; not itself schedule-triggered) |
| GoldBot Trading Pipeline | `trading_bot.yml` | All 3 branches | `schedule` (`*/5 3-18 * * 1-5`), `workflow_dispatch` |
| Dependency Graph | (Dependabot, no committed YAML) | N/A (GitHub-managed) | automatic |

**Release branch**: none exists. No branch named `release`, `release/*`,
or equivalent.

**Tag strategy**: none exists. `list_tags` and `list_releases` both
return empty — zero tags, zero GitHub Releases, anywhere in the
repository's history.

### Findings (facts, not yet recommendations — see §9 for proposals)

**Finding 1 — `main` is the configured default branch but is not where
GoldBot actually runs.** `production_deploy.yml`'s own header comment
states this explicitly in the file itself: *"Deploy branch:
`claude/code-analysis-optimization-pwfo3q` — this is the repository's
actual production branch... `main` is a stale pre-TradingPipeline
snapshot never read by any other CI/CD job in this repository."*
`trading_bot.yml`'s checkout step independently confirms this by
pinning `ref: claude/code-analysis-optimization-pwfo3q` explicitly,
with its own comment: *"GoldBot v0.1 stable... currently lives on this
branch, not on the default branch."*

**Finding 2 — `main` has no CI and no deploy pipeline of its own.**
`main`'s tree contains only `owner_snapshot.yml` and `trading_bot.yml`
— `ci.yml` and `production_deploy.yml` do not exist there. A commit
landing directly on `main` today would trigger `ci.yml`'s `push`
trigger (which lists `main` in its `branches:` filter) — but since the
workflow file itself is absent from `main`'s tree, no run would
actually fire from a push confined to `main`. (`pull_request`-triggered
runs against `main` as a base still work today, because GitHub reads
the merge of head+base for that event type, and every PR head so far
has carried `ci.yml` — but this is incidental to the PRs' branches
being `claude/**`, not a property of `main` itself.)

**Finding 3 — the current working branch is a strict superset of the
production branch.** `git rev-list --left-right --count` shows 0
commits exist on the production branch that aren't already in the
current working branch, and 18 commits exist on the current working
branch beyond the production branch (this session's Platform Foundation/
Navigation/Governance work). No divergence, no conflict between them.

**Finding 4 — `main` and the production branch have diverged in both
directions.** `main` has 5 commits the production branch does not
(including the `owner_snapshot.yml` addition); the production branch
has 171 commits `main` does not (the entire TradingPipeline
implementation this repository actually runs). Total commit counts:
`main` = 50, production branch = 216, current working branch = 234.

**Finding 5 — `owner_snapshot.yml` (on `main` only) is already known-broken.**
Documented in `docs/TECHNICAL_DEBT.md`: it checks out the production
branch and runs a module (`monitoring/run_snapshot.py`) deleted from
that branch, so every scheduled run fails. This audit does not change
that entry's "No action" status — it is out of scope for REPO-001,
which is Audit/Proposal only.

## 2. Claude Branch Audit

Only 2 branches match the `claude/*` pattern the Director asked about.
**Neither is a stale, abandoned, or safe-to-delete throwaway branch** —
both are currently load-bearing.

### `claude/code-analysis-optimization-pwfo3q`

- **Why created**: per its own commit history and `production_deploy.yml`'s
  comment, this is where "V2" development (the real TradingPipeline —
  `core/pipeline.py` and every layer under it) actually happened,
  distinct from `main`'s pre-TradingPipeline skeleton state.
- **Which task**: not a single task — 216 commits spanning this
  project's entire real trading-engine history, most recently "V2
  Phase 6 Freeze."
- **Merged?** No — PR #1 (opened 2026-07-12, still open 11+ days as of
  this audit) proposes merging it into `main` and has not been acted
  on.
- **Needed commits?** Yes — this branch is the sole checkout target for
  `trading_bot.yml` (the live scheduled trading runner, cron
  `*/5 3-18 * * 1-5`) and `production_deploy.yml` (the VPS deployment
  pipeline). **Deleting or renaming this branch without first updating
  both workflow files' pinned `ref:`/`branches:` values would break the
  live scheduled trading pipeline and the deploy pipeline immediately.**
- **Deletable?** **No, not as-is.** This is de facto production
  infrastructure wearing a session-branch name.

### `claude/trading-ai-arch-review-tgszrz`

- **Why created**: this session's own designated development branch —
  originally created for an architecture review task, later re-pointed
  (per this session's own history) to track the production branch as
  its base, then extended with 18 commits of Platform Foundation,
  Navigation (TASK-002A–002F), Governance Review (GOVERNANCE-REVIEW-001),
  and this REPO-001 audit itself.
- **Which task**: TASK-001 through TASK-002F (Platform/Navigation
  track), GOVERNANCE-REVIEW-001, REPO-001 — all Platform-role work,
  zero Trading Core changes (confirmed throughout this session's own
  commit history: every commit's `git diff --cached --stat` against
  `core/`, `decision/`, `risk/`, `execution/`, `strategies/`, `signals/`,
  `context/`, `ai/`, `database/`, `telegram/`, `.github/` came back
  empty).
- **Merged?** No — PR #2 (opened 2026-07-23, same day as this audit)
  proposes merging it into `main` and, per standing Director order, is
  never merged/closed/reviewed by the Worker.
- **Needed commits?** Yes — this is the only branch containing all of
  Platform Foundation, Navigation, and the Governance Review work done
  to date; it is also this session's own HEAD.
- **Deletable?** **No.** This is the active Platform Worker line, not a
  discardable scratch branch.

### Audit conclusion for this section

The Mission statement's framing ("clean up temporary Claude branches")
does not match what actually exists: there are exactly two `claude/*`
branches, and both are currently necessary — one is real production
infrastructure, the other is real active development. **There is no
garbage to delete today.** The actual problem this repository has is
not excess branches; it is that its two functionally-permanent branches
are named and structured like disposable session branches, with no
naming convention, no protection, and two 11+-day-old unmerged PRs
sitting against a `main` that neither branch actually depends on for
anything. §3–§7 below propose how to fix that shape, not how to delete
anything.

## 3. New Branch Strategy

Proposed model, per Director's brief:

```
main
  ↓
develop
  ↓
feature/core
  ↓
feature/platform
```

| Branch | Purpose |
|---|---|
| `main` | The single source of truth for what is actually deployed to production. Every commit on `main` is releasable. Direct pushes forbidden; the only way onto `main` is a reviewed, CI-passed merge from `develop`. This is the role `claude/code-analysis-optimization-pwfo3q` already plays today in practice — the migration's job is to give that role its conventional name and protection, not to invent a new one. |
| `develop` | The integration branch where Core Worker and Platform Worker output meets. CI-gated; Worker-mergeable without requiring a Director review for every single merge (unlike `main`), so both Workers can integrate continuously without waiting on Director bandwidth for each individual change. Promoted to `main` only in a deliberate, Director-reviewed release step. |
| `feature/core` | Core Worker's dedicated line — Trading Engine & AI (`context/`, `strategies/`, `signals/`, `ai/`, `decision/`, `risk/`, `execution/`, `database/`). Maps onto this repository's existing Core/Platform role boundary (`docs/HANDOFF.md`, `docs/CURRENT_PHASE.md`'s "Role boundary" section) — giving Core its own branch is what actually lets Core and Platform work in parallel without one blocking the other's CI or merge queue. |
| `feature/platform` | Platform Worker's dedicated line — `platforms/`, `telegram/`, `communication/`, Platform-facing docs. This is exactly the role `claude/trading-ai-arch-review-tgszrz` already plays today. |

**Why this maps cleanly onto what already exists**: the repository
already has, in practice, a production branch and a Platform-work
branch — it just doesn't have the `develop` integration point or a
dedicated `feature/core` line, and none of the three real branches
carry names that say what they are. This plan does not invent new
workflows; it names and protects the ones already running.

## 4. Migration Plan

Seven phases, per Director's example structure. **None of these phases
are executed by this task — this is the plan REPO-002 would follow if
approved.**

**Phase 1 — Repository Backup / Rollback Anchor.** Before any branch
operation: tag the current tip of the production branch
(`claude/code-analysis-optimization-pwfo3q` @ `d911b97`) and the
current tip of `main` (@ `5618adec`) as annotated Git tags (e.g.
`pre-migration-production`, `pre-migration-main`). Zero tags exist
today (§1), so this is also the repository's first rollback anchor of
any kind, not only a migration safeguard.

**Phase 2 — Create `develop`.** Branch `develop` from the production
branch's current tip (`d911b97`) — not from `main`'s stale tip — since
the production branch, not `main`, holds the real, current, working
codebase.

**Phase 3 — Create `feature/core`.** Branch `feature/core` from the
same point as `develop` (`d911b97`). No separate "Core Worker branch"
has existed until now — this is a genuinely new line, not a rename of
anything existing.

**Phase 4 — Create `feature/platform`.** Branch `feature/platform` from
`claude/trading-ai-arch-review-tgszrz`'s current tip (`f505858`) —
carrying forward all 18 commits of Platform/Governance work already
done, rather than starting Platform Worker's new branch empty.

**Phase 5 — Merge verification.** Verify `develop` = `feature/core`'s
base = `feature/platform`'s base, all traceable to the same known
commit (`d911b97`); run the full commit protocol (pyflakes, compileall,
pytest, `main.py` smoke run) on `develop` before treating it as the new
integration point; confirm CI (`ci.yml`) passes on `develop` itself,
since `ci.yml` does not exist on `main` today (Finding 2) and this is
the first point at which it needs to exist on whatever becomes the
long-term default.

**Phase 6 — Branch cleanup.** Resolve PR #1 and PR #2 (both currently
open against `main`, both superseded in substance by whatever `develop`/
`feature/platform` become) — this phase is where those PRs finally get
closed or re-targeted, **not before**, and not by this Worker without
explicit Director authorization for that specific action, consistent
with the standing "never touch PR #2" instruction. Retire `main`'s
current stale content in favor of the new model (exact mechanism —
fast-forward vs. formal deprecation — is a Director decision, not
proposed here as a fait accompli). The two now-legacy-named branches
(`claude/code-analysis-optimization-pwfo3q`, `claude/trading-ai-arch-review-tgszrz`)
are only deleted once `develop`/`feature/core`/`feature/platform` are
confirmed to carry every commit they hold (Phase 5's job) — never
before that confirmation.

**Phase 7 — Branch protection.** Apply the protection rules proposed in
§5 to `main` and `develop`. This is deliberately the last phase — a
protected branch cannot receive the setup commits Phases 2–6 require
without a bypass, so protection is switched on only once the new
branches already contain everything they need.

## 5. Branch Protection Proposal

| Branch | Direct push | Required review | Required CI | Notes |
|---|---|---|---|---|
| `main` | Forbidden | Director review mandatory | Mandatory (`ci.yml` + `production_deploy.yml`'s validate stage) | Only a merge from `develop` reaches `main`. |
| `develop` | Forbidden (PR-only) | Worker-mergeable (no Director review required per merge) | Mandatory (`ci.yml`) | The continuous-integration point; Director reviews at promotion-to-`main` time, not per merge into `develop`. |
| `feature/core` | Allowed for Core Worker | None (single-owner branch) | Recommended, not required | Core Worker's own working branch. |
| `feature/platform` | Allowed for Platform Worker | None (single-owner branch) | Recommended, not required | Platform Worker's own working branch — same posture `claude/trading-ai-arch-review-tgszrz` already has today. |

`ci.yml` would need to add `develop` to its `push`/trigger `branches:`
list (today: `main`, `claude/**`) — a workflow-file change, itself part
of Phase 7, not this task.

## 6. Collaboration Model

```
Director
   ↓ (Task)
Core Worker ──────────┐
   ↓ (feature/core)   │
   │                  ↓ (feature/platform)
   │            Platform Worker
   ↓                  ↓
   └──────→ develop ←──┘
              ↓ (Director Review)
             main
```

- Director issues a Task (Platform Task, DEVOPS task, Governance
  Review, or a future Core-track task) exactly as today.
- Core Worker and Platform Worker each commit to their own
  `feature/*` branch, following the existing Commit Protocol
  (`CLAUDE.md`, `docs/standards/COMMIT_STANDARD.md`) unchanged.
- Each Worker opens a PR from its `feature/*` branch into `develop`;
  `ci.yml` gates the merge; no Director review required at this step
  (this is the actual point of having `develop` — it lets both Workers
  integrate without waiting on Director bandwidth for every commit).
- Promotion from `develop` to `main` is a deliberate, batched step,
  always Director-reviewed, mirroring how `docs/PLATFORM_WORKFLOW.md`'s
  Freeze Checklist already requires "Director Approval" before a task
  is considered Frozen — this model extends that same discipline to the
  branch level.
- This does not change the existing two-track task queue
  (`communication/task_queue/QUEUE.md`'s Platform Tasks / Engineering /
  Governance tracks) — it changes which branch each track's commits
  land on, not how tasks are planned or authorized.

## 7. Cleanup Proposal

**What would be deleted** (only after Phase 5's verification confirms
zero unique content remains uncaptured): `claude/code-analysis-optimization-pwfo3q`
and `claude/trading-ai-arch-review-tgszrz`, once `develop`/`feature/core`/
`feature/platform` demonstrably contain everything they held. Neither is
deleted today, or by this task.

**What would be kept**: `main` (repurposed as the protected release
branch), `develop`, `feature/core`, `feature/platform`.

**What would be archived, not deleted**: nothing identified — this
repository has no long-lived historical branch worth preserving as a
read-only archive beyond what Phase 1's tags already capture. If the
Director wants a permanent historical marker of "this is what
`claude/code-analysis-optimization-pwfo3q` looked like before
migration," Phase 1's `pre-migration-production` tag already serves
that purpose without needing a kept branch.

**PRs**: #1 and #2 are proposed for resolution at Phase 6, not before,
and not by this Worker's own initiative for #2 specifically (standing
Director order). #1 is, as of this audit, fully subsumed by #2's
content (Finding 3) — the Director may find it redundant to resolve
separately, but no action is taken on either here.

## 8. Risk Analysis

| Risk | Severity | Detail |
|---|---|---|
| **Breaking the live trading pipeline mid-migration** | Critical | `trading_bot.yml`'s `schedule` trigger is read from `main` (GitHub always reads scheduled-workflow YAML from the default branch, per this repo's own `owner_snapshot.yml` precedent) but its `checkout` step explicitly pins `ref: claude/code-analysis-optimization-pwfo3q`. If that branch is renamed or deleted before this pinned `ref:` is updated, the next scheduled run (as frequent as every 5 minutes, weekdays 3am–6pm UTC) fails outright. **Sequencing must update the workflow file's pinned ref in the same phase, before or atomically with, any rename/delete of that branch.** |
| **Breaking production deploy mid-migration** | Critical | Same mechanism, `production_deploy.yml`'s `branches:` deploy-trigger list names the production branch explicitly. Same sequencing requirement applies. |
| **No rollback point exists today** | High | Zero tags, zero releases (§1). If any migration step goes wrong, there is currently no tagged "last known good" commit to return to other than the raw commit SHA. Phase 1 exists specifically to close this gap before anything else happens. |
| **Merge/conflict risk grows with delay** | Medium, growing | PR #1 has been open 11+ days; PR #2 opened same day as this audit. Neither is merged. The longer resolution is deferred, the larger any eventual merge/rebase becomes — this is a reason to sequence Phase 6 deliberately, not a reason to rush it. |
| **Zero branch protection today, independent of migration** | High | Any collaborator with push access can force-push directly to `main` or the production branch right now, with no required review and no required CI check, regardless of whether migration happens. This is a present-tense risk, not a future one — the current absence of protection is itself the finding, not something migration introduces. |
| **`ci.yml` not present on `main`** | Medium | A push confined to `main` alone would not trigger `ci.yml` today (Finding 2) — if `develop` is created without also adding `ci.yml` to it directly (Phase 2/5), the same gap would silently carry forward into the new model. |
| **Branch Risk — naming collision** | Low | `feature/core` and `feature/platform` are new names; no existing branch, tag, or workflow reference collides with either. |
| **Conflict Risk — `develop` vs. two long-running lines** | Low | Finding 3 confirms zero divergence between the production branch and the current working branch — creating `develop` from the production branch's tip and `feature/platform` from the working branch's tip introduces no merge conflict at creation time, since one is a strict prefix of the other's history. |

## 9. Director Recommendations

1. Tag a rollback anchor (Phase 1) as the very first migration step,
   independent of everything else — this closes the "zero rollback
   point" risk immediately and cheaply, before any branch decision is
   even finalized.
2. Sequence the `trading_bot.yml`/`production_deploy.yml` ref updates
   in lockstep with any rename/delete of the production branch — never
   as an afterthought.
3. Resolve PR #1 and PR #2 as part of Phase 6, once `develop` exists and
   is verified — not before, and not as a side effect of an unrelated
   task.
4. Consider enabling at minimum a "no direct push, require PR" rule on
   `main` even before the full 4-branch model exists — this is the one
   piece of the Branch Protection Proposal (§5) that closes today's
   highest-severity present-tense risk (unprotected `main`) and does
   not require `develop`/`feature/*` to exist first.
5. Treat REPO-002 (Implementation) as its own separately-authorized
   task once this plan is approved, following the same Architecture
   First discipline (`docs/PLATFORM_WORKFLOW.md`) already governing
   Platform work — Phase-by-phase, each phase's own CI/verification
   step confirmed before the next phase starts.

## 10. Final Recommendation

**Migration Plan is complete and ready for Director decision.** No
blocking unknown remains: every branch, PR, workflow, and protection
fact in scope has been directly confirmed via the GitHub API and the
actual checked-out workflow files, not assumed — including, per §0's
follow-up verification, the exact divergence commit and date (Q1), the
documented rationale for the deploy-branch decision (Q2), a full
files/lines/category breakdown of the 171-commit gap (Q3), a clear
separation between the (built but unexercised) VPS rollback mechanism
and the (still-zero) git-level rollback anchor (Q4), and the confirmed,
API-verified reason both PRs remain unmerged — a real `dirty`
merge-conflict state plus zero reviews, traced to `main`'s own
post-divergence filename-repair commits colliding with the production
branch's independent history (Q5). The plan's highest-risk step
(breaking the live trading/deploy pipelines) has a concrete, sequenced
mitigation (update pinned refs before/atomically with any branch rename
or delete). Recommend: approve this plan, then authorize REPO-002
(Implementation) to execute Phases 1–7 in order, confirming each
phase's CI/verification before the next phase begins — starting with
Phase 1 (rollback-anchor tags), which carries no risk and closes this
repository's one true present-tense gap (zero rollback point)
regardless of what else is ultimately decided about the branch model
itself.

## Related

- `docs/PLATFORM_WORKFLOW.md` — the Architecture First discipline this
  plan's phased approach follows.
- `docs/GOVERNANCE_REVIEW_001.md` — the governance-layer review this
  task's own Mission statement says must be frozen before Engineering
  Infrastructure work begins.
- `docs/TECHNICAL_DEBT.md` — `owner_snapshot.yml`'s pre-existing,
  separately-tracked breakage on `main`.
- `communication/task_queue/REPO-001.md` — this task's own ticket
  record.
- `.github/workflows/ci.yml`, `production_deploy.yml`, `trading_bot.yml`
  — the three real workflow files this plan's risk analysis is based on.
