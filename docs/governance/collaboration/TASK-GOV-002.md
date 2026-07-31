# TASK-GOV-002 — Branch Audit & `claude/collaboration` Sync

Governance-only task. **No source code is written or modified by the
audit itself.** No new branch opened. Rules per this task's brief and
per `TASK-GOV-001.md` (FROZEN, Revision 3), whose Laws 1–12 govern this
task without restatement.

## 1. Scope

Audit every branch that exists in the repository, determine the latest
Owner-approved flow, and identify what (if anything) is missing from
`claude/collaboration`. Bringing that flow in is this task's deliverable
**only up to the point Law 11 (Fast-Forward Only) requires Owner
approval for a merge commit** — see §5.

## 2. Method

Per Law 10 (Branch Audit First), before anything else: `main`,
`claude/collaboration`, active PRs, and the last Handover
(`TASK-GOV-001.md` §14) were checked. Result: no drift since Revision 3
— `claude/collaboration`'s remote tip matched local state exactly.
Every remote branch was then compared against `origin/main`
(`git rev-list --count` both directions, `git merge-base`), and GitHub
PR history was pulled (`list_pull_requests`, `state=all`) to check for
any open PR.

## 3. Branch Audit Report

Four branches exist in the repository (confirmed via `git branch -r`
after `git fetch --prune`; no others, no stale remote refs).

### `main`
- **Last commit:** `ed6a5e9` — "Merge PR #31: TASK-PROD-001 — share current-price cache with the VPS bot"
- **Vs. main:** is main (baseline).
- **Needed:** yes — production.
- **In `claude/collaboration`:** yes, by definition (baseline).
- **Owner decision needed:** no.

### `claude/collaboration`
- **Last commit:** `3d9ffc2` — "TASK-GOV-001 Revision 3: APPROVED, FROZEN -- Laws 10-12 added"
- **Vs. main:** ahead 3 (the three TASK-GOV-001 governance commits), behind 0.
- **Needed:** yes — the single active working branch (Law 12).
- **In `claude/collaboration`:** yes (it is the branch).
- **Owner decision needed:** no — already fully synced with `main`;
  nothing from `main` is missing here.

### `claude/goldbot-data-layer-architecture-f8dx8j`
- **Last commit:** `a2bae46` — "Phase 3: CurrentPriceProvider depends on PriceStreamService, not SmartDataCache"
- **Vs. main:** ahead 4, behind 1. The 4 ahead are the Price Stream
  Foundation work (Phase 1: `data/stream/*` incl. `PriceStreamService`/
  `PriceCache`/`PriceTick`/`BitgetPriceSource`; Phase 2:
  `MarketDataService` + `TradingPipeline` wiring; Phase 3:
  `CurrentPriceProvider` → `PriceStreamService`), all explicitly
  reviewed and APPROVED by the Owner in-session across three separate
  turns. The 1 behind is `main`'s `ed6a5e9` (TASK-PROD-001) — this
  branch was cut from `main` before that merge landed.
- **Needed:** yes — this is the latest Owner-approved engineering flow
  in the repository, not yet in `main` or `claude/collaboration`.
- **In `claude/collaboration`:** **no.** This is the one gap this audit
  exists to close.
- **Owner decision needed:** **yes** — bringing these 4 commits into
  `claude/collaboration` is not a fast-forward (the two branches
  diverged at `203cfe7`), so it produces a merge commit. Law 11
  requires Owner approval for any merge commit on this branch. Not
  performed in this task without that approval — see §5.

### `claude/code-analysis-optimization-pwfo3q`
- **Last commit:** `203cfe7` — "fix(deploy): TASK-PROD-001 — share the current-price cache between the fetch pipeline and the VPS bot"
- **Vs. main:** ahead 0, behind 1 — every commit on this branch is
  already an ancestor of `main` (its content reached `main` through PR
  #31's merge commit). It has no content `main` doesn't already have.
- **Needed:** stale as a working branch (superseded), but
  `docs/governance/policies/Branch_Policy.md` §8 explicitly records
  this branch (alongside `claude/trading-ai-arch-review-tgszrz`, which
  no longer exists in the remote — likely already cleaned up in an
  earlier, undocumented step) as "load-bearing today" and states it is
  "cleaned up only as an explicit, verified step of Repository
  Migration ... never before, and never as a side effect." This audit
  does not override that policy.
- **In `claude/collaboration`:** N/A — fully contained in `main`, which
  `claude/collaboration` already contains. Any retirement/deletion is
  not actionable without Owner approval, per `Branch_Policy.md` §8 and
  this task's own Rule 4.
- **Owner decision needed:** **yes, but only if the Owner wants to
  formally retire it.** No action is required to keep the repository
  correct — this branch is inert (fully merged, nothing points to it
  as a working line) and does not block or drift anything on its own.

## 4. Active PR Check

`list_pull_requests(state=all)` returned 32 PRs, all `state: closed`.
**Zero open PRs.** Nothing is currently pending review or blocking a
merge decision.

## 5. Latest Stable Flow — Conclusion

The latest Owner-approved flow not yet reflected in `claude/collaboration`
is entirely contained in `claude/goldbot-data-layer-architecture-f8dx8j`'s
4 commits ahead of its merge-base with `main`:

```
203cfe7 (merge-base, already superseded by main's ed6a5e9)
   │
   ├─ e10f7e8 Merge PR #30: GoldBot Core rebuild
   ├─ 98030f4 Add Price Stream Foundation (TASK-DATA-001): unified get_price() API
   ├─ 68f1286 Move PriceCache and PriceStreamService into data/stream/
   ├─ 1600635 Phase 2: TradingPipeline depends on MarketDataService, not MarketDataNormalizer directly
   └─ a2bae46 Phase 3: CurrentPriceProvider depends on PriceStreamService, not SmartDataCache
```

(`e10f7e8` is already in `main`/`claude/collaboration` via a different
path — it is listed here only because it is this branch's own history;
the four commits genuinely missing from `claude/collaboration` are the
last four.)

**Recommended sync action:** merge
`claude/goldbot-data-layer-architecture-f8dx8j` into
`claude/collaboration` (a real merge commit — the two branches
diverged, so no fast-forward is possible), bringing in the missing
Price Stream / `MarketDataService` / `CurrentPriceProvider` work while
`claude/collaboration` already supplies the one commit that branch is
missing from `main` (their common ancestor covers it). **Not executed
in this task** — Law 11 requires Owner approval for the merge commit
itself, and that approval has not yet been given for this specific
action (approval of the *content*, across three prior conversation
turns, is not the same as approval of *this merge onto
`claude/collaboration`* — the two are kept separate on purpose, per
Law 11's letter).

## 6. Old Branches Remaining

- `claude/code-analysis-optimization-pwfo3q` — fully merged into
  `main`, inert, retained per `Branch_Policy.md` §8 pending a
  Director/Owner-authorized Repository Migration step. No action taken.

No other branches exist in the repository as of this audit
(`git branch -r` after `git fetch --prune`: exactly `main`,
`claude/collaboration`,
`claude/goldbot-data-layer-architecture-f8dx8j`,
`claude/code-analysis-optimization-pwfo3q`).

## 7. Deliverable Checklist

1. Branch audit report — §3.
2. Latest stable flow conclusion — §5.
3. `claude/collaboration` sync state — currently synced with `main`
   (0 behind); **not yet synced** with the Phase 1–3 Data Layer flow
   pending the Owner decision in §5.
4. Remaining old branches list — §6.
5. Handover — §8.

## 8. Handover

1. **What was reviewed:** all 4 repository branches, their commits
   relative to `main`, and all 32 PRs (all closed, none open).
2. **What was accepted:** `claude/collaboration`'s current state is
   correct and needs no change to be in sync with `main`.
3. **What was rejected:** deleting or renaming
   `claude/code-analysis-optimization-pwfo3q` — out of scope without
   Owner authorization and contrary to standing `Branch_Policy.md` §8
   language; not attempted.
4. **What is left for the next Worker (or this session, once
   approved):** executing the merge described in §5 — Phase 1–3 Data
   Layer work (`claude/goldbot-data-layer-architecture-f8dx8j`) into
   `claude/collaboration` — the moment the Owner approves that specific
   merge action.
5. **FROZEN:** `TASK-GOV-001.md` (Revision 3); all `.py` source under
   every CLAUDE.md change-controlled module (unchanged by this audit).
6. **Opens next:** the §5 merge, on explicit Owner approval; after
   that, `claude/collaboration` becomes the single branch carrying both
   the governance rules and the Data Layer engineering work, exactly as
   Law 12 intends.

## 9. Status

```
TASK-ID:    TASK-GOV-002
Goal:       Audit all branches; determine and (where approved) bring
            the latest approved flow into claude/collaboration.
Rules:      TASK-GOV-001.md Laws 1-12 (unchanged, referenced not restated).
Forbidden:  New branch; merge/delete/rename without Owner approval;
            code changes; touching FROZEN layers.
Allowed:    Read-only git/GitHub audit; this report.
Input:      TASK-GOV-002 brief (Owner instruction).
Output:     This document.
Owner:      Worker (this session) -- task-assignee sense.
Status:     REVIEW -- audit complete; sync action (Sec 5) pending
            explicit Owner approval.
Next step:  Owner approves (or declines) merging
            claude/goldbot-data-layer-architecture-f8dx8j into
            claude/collaboration. On approval, the merge is executed
            as its own commit, validated, and reported with its own
            Handover.
```
