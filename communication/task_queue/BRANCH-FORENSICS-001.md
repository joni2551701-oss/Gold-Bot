# BRANCH-FORENSICS-001

**Title**: Repository History Forensics
**Track**: Repository Engineering (`REPO-XXX` family — see
`communication/task_queue/QUEUE.md`)
**Priority**: Critical
**Status**: ✅ APPROVED — Director review complete (F-008 through F-013
confirmed: root cause is a single file, `strategies/strategy_manager.py`,
zero code difference, caused by one invisible Unicode U+2060 character;
the `strategie/` typo was a separate, already self-corrected historical
event, not the conflict cause).

**Follow-on orders** (this review): ORDER-008 — Repository Recovery
Strategy not yet authorized (Engineering Governance v1.1 must complete
first). ORDER-009 — Repository Migration stays PAUSED. ORDER-010 —
Repository Recovery moves to QUEUED (backlog), first implementation
item after Governance v1.1 Freeze.
**Issued as**: ORDER-003, immediately following ORDER-002 (Repository
Migration halted — no merge, rebase, branch rename, branch delete, or
default-branch change).

## Objective

Fully reconstruct repository history to determine: when the repository
diverged from the production branch; why `claude/*` became production;
why `main` fell behind; PR #1/#2's historical sequence; the exact
commit(s) that caused the merge conflict; which commit introduced the
Unicode filename problem; which commit introduced the `strategie/` →
`strategies/` change; and a safe recovery strategy.

## Constraints (respected)

Forensic investigation only — no merge, rebase, branch rename, branch
delete, or default-branch change performed.

## Delivered

`docs/BRANCH_FORENSICS_001.md` — Timeline, Root Cause Analysis, Commit
Chain, Conflict Origin, Recovery Strategy, Director Recommendation.

**Headline finding**: `git merge-tree` (safe, side-effect-free) proves
the entire `mergeable_state: dirty` conflict blocking both PR #1 and PR
#2 traces to exactly one file (`strategies/strategy_manager.py`) and
exactly one invisible Unicode character (U+2060 WORD JOINER) left over
from an incomplete cleanup on `main`, while the production branch's
independent cleanup removed it fully. The file's content is
byte-identical on every side (same blob SHA) — this is a path-only
conflict, not a content conflict. The corruption itself traces back to
the repository's very first commits (2026-07-11), before either branch
existed, consistent with a browser-based file editor silently inserting
a zero-width character.

All 8 questions from ORDER-003 answered with commit-level evidence:
divergence point (`ad1affe`, 2026-07-12 13:10:54 UTC), why `claude/*`
became production (cross-references REPO-001 §0/Q2), why `main` fell
behind (5 post-divergence commits, only 4 of them touching code at
all), PR #1/#2's exact historical sequence (PR #1 opened 45 seconds
after the production branch's first post-divergence commit), the exact
conflicting commit pair (`8c69ae77` on `main` vs. `f78461b` on
production), the Unicode corruption's origin commit (`fd9e1e69`,
2026-07-11, the repository's first commits), the `strategie/` typo's
introduction (`acc844a`, 2026-07-12) and its own same-day fix
(`7af7ddc5`), and a proposed (not executed) single-file, content-neutral
rename as the recovery strategy.

## Depends on

REPO-001 (Repository Engineering Migration) — this task is a direct
follow-up to REPO-001 §0/Q5, ordered before REPO-001's paused Migration
Plan may resume.

## Notes

No branch, PR, protection, or repository setting was touched. `git
merge-tree` is a read-only plumbing command — confirmed to make no
working-tree, index, or ref changes; `git status` remained clean of any
unintended change throughout this investigation.
