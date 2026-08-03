# Repository Recovery — Authorized Operator Runbook

**Status: ✅ APPROVED by the Director** as the official execution guide
for the Authorized Operator (ORDER-021; scope confirmed by the Director
after the 9-file finding).

Prepared by the Worker under **ORDER-021** (Director chose Option 2:
recovery performed by an Authorized Operator with the required push
scope). **Why this session cannot do it (HTTP-trace confirmed,
ORDER-022):** the Claude Code git-proxy rejects any push containing a
ref outside `refs/heads/*` with `HTTP 403` (body: `ERR push contains a
ref outside refs/heads/*; only branch updates are permitted`), so
**tag pushes are blocked**. Since the recovery's safety sequence needs
the rollback **anchor tags first**, this session cannot perform a
plan-compliant recovery. (Whether a `refs/heads/main` push would be
permitted from this session was **not tested** — no standalone `main`
push was executed; see the runbook's precondition note.) Every command
below was **tested locally by the Worker** on a throwaway branch (no
push); the expected results are the actual results of that test. The
Authorized Operator executes the pushes, then the Worker verifies and
writes the Recovery Report.

**Scope (Director-confirmed, final)**: this runbook fixes **only**
`strategies/strategy_manager.py` — the one file whose corrupted name
causes the merge conflict. Testing proved this achieves zero merge
conflicts, and proved that fixing the other 8 corrupted filenames on
`main` would *introduce* 4 new conflicts. **The other 8 are explicitly
out of Recovery scope** — they are stale artifacts that Migration
supersedes when `main` is reconciled from production; renaming them
inside Recovery is forbidden by Director decision. Do not extend this
runbook to the other 8.

**Updated ORDER-020 Exit Criteria (Director, this decision)** — Recovery
succeeds when: the `strategy_manager.py` rename/rename conflict is
resolved; `main`↔production merge conflict = 0; `main`↔working merge
conflict = 0; rollback tags created; `git fsck` passes. The remaining 8
Unicode filenames are **not** part of these criteria.

## Preconditions

- Actor has repository write permission and push scope for
  `refs/tags/*` and `refs/heads/main`. (Note: the Worker's own session
  is **confirmed** to lack `refs/tags/*` push scope — the Claude Code
  git-proxy blocks non-branch refs; the Worker's `refs/heads/main` push
  scope was **not tested**. The Authorized Operator must hold both.)
- A clean clone of `joni2551701-oss/Gold-Bot`.
- Reference tips at preparation time (verify with `git fetch` first;
  `main`/production are stable, the working branch may have advanced):
  - `main` = `5618adec01e53ad836c144cad7dc986e5fc80ec4`
  - production `claude/code-analysis-optimization-pwfo3q` = `d911b97e…`
  - working `claude/trading-ai-arch-review-tgszrz` = `0f75c67…` (or later)

## Step 1 — Create & push rollback anchors (from current tips)

```bash
git fetch origin
git tag -a pre-recovery-main       origin/main                                   -m "Rollback anchor: main before Repository Recovery (ORDER-020/021)."
git tag -a pre-recovery-production origin/claude/code-analysis-optimization-pwfo3q -m "Rollback anchor: production branch before Repository Recovery."
git tag -a pre-recovery-working    origin/claude/trading-ai-arch-review-tgszrz    -m "Rollback anchor: working branch before Repository Recovery."
git push origin pre-recovery-main pre-recovery-production pre-recovery-working
```

Requirements: annotated tags; pushed; **no** force update.

## Step 2 — Fix the U+2060 filename on `main` (single file, content-neutral)

```bash
git checkout -B main origin/main       # main's exact current tip

python3 - <<'PY'
import subprocess
files = subprocess.check_output(['git','ls-files','-z','strategies/']).decode().split('\0')
target = [f for f in files if 'strategy_manager.py' in f and any(ord(c) > 127 for c in f)]
assert len(target) == 1, f"expected exactly one corrupted strategy_manager.py, got {target!r}"
old = target[0]
new = ''.join(c for c in old if ord(c) < 128)      # strips the trailing U+2060
before = subprocess.check_output(['git','rev-parse',f':{old}']).decode().strip()
subprocess.check_call(['git','mv', old, new])       # pure rename, stages only this
after = subprocess.check_output(['git','rev-parse',f':{new}']).decode().strip()
assert before == after, f"BLOB CHANGED ({before} -> {after}) — abort"
print(f"renamed {old!r} -> {new}  | blob {before} preserved")
PY

# Commit ONLY the rename. Do NOT use `git add -A` or `git commit -a`
# (that can pull in a stray runtime database/goldbot.db).
git commit -m "Repository Recovery: fix U+2060 in strategies/strategy_manager.py filename

Removes a trailing U+2060 WORD JOINER from the filename that caused the
only rename/rename merge conflict between main and the production/working
branches (docs/BRANCH_FORENSICS_001.md). Content unchanged (blob
89a66416a8f53672ceb12312760188fedd1b4bd8 preserved); filename only.
Forward commit, no history rewrite."

git push origin main       # normal forward push — NO force
```

Requirements: `git mv` used; content unchanged; **blob SHA
`89a66416a8f53672ceb12312760188fedd1b4bd8` preserved**; filename only;
forward commit; **force push forbidden**.

## Step 3 — Create & push the recovery checkpoint

```bash
git tag -a post-recovery-main main -m "Repository Recovery checkpoint: main after the U+2060 filename fix. Known-good post-recovery state Migration branches from."
git push origin post-recovery-main
```

## Step 4 — Validation (run and capture output)

```bash
git fsck --full                                                    # expect: no corruption errors
git rev-parse "main:strategies/strategy_manager.py"                # expect: 89a66416a8f53672ceb12312760188fedd1b4bd8
git merge-tree --write-tree main origin/claude/code-analysis-optimization-pwfo3q | grep -ci conflict   # expect: 0
git merge-tree --write-tree main origin/claude/trading-ai-arch-review-tgszrz     | grep -ci conflict   # expect: 0
```

**Expected results (from the Worker's local test):**
- `git fsck` — clean, no corruption.
- `strategy_manager.py` blob = `89a66416a8f53672ceb12312760188fedd1b4bd8` (unchanged).
- merge-tree `main`↔production — **0 conflicts**.
- merge-tree `main`↔working — **0 conflicts**.

**Expected and intentional**: a full non-ASCII filename sweep of `main`
will still list **8 other** U+2060 filenames (`ai/ai_prompt.py`,
`ai/confidence_model.py`, `context_layer/market_structure/market_structure.py`,
`database/signal_repository.py`, `signals/models.py`,
`signals/signal_engine.py`, `strategies/amd_strategy.py`,
`strategies/fvg_strategy.py`). These are **left unfixed on purpose** —
see the finding below. Their presence is not a validation failure.

## Step 5 — Return to the Worker

Return: the 4 tag names + their SHAs; the `main` fix commit hash; the
`git fsck` result; the `strategy_manager.py` blob SHA; both merge-tree
conflict counts. The Worker verifies these against the expected results
above and writes the Recovery Report for Director approval.

## Finding: `main` has 9 U+2060 filenames, but only 1 may be fixed

The Worker's fresh full-tree sweep (which `BRANCH-FORENSICS-001`
explicitly recommended before the fix) found **9** U+2060-corrupted
filenames on `main`, not 1. Testing both scopes locally proved:

- Fixing **only** `strategy_manager.py` → merge-tree `main`↔production
  and `main`↔working both **0 conflicts**. ✅
- Fixing **all 9** → both merge-tree checks jump to **4 conflicts**. ❌

Why: `strategy_manager.py` was a true rename/rename conflict where both
sides held byte-identical content (blob `89a66416`), so aligning the
names *resolves* it. The other 8 have *different* content on `main` vs.
production (171 commits of divergence); renaming `main`'s stale copies
to the clean names collides them with production's evolved versions =
new add/add conflicts. Those 8 are stale artifacts on `main` that
**Repository Migration supersedes** when `main` is reconciled from
production — so they are correctly left untouched by Recovery.

This confirmed the Director's original one-file scope. **Director
decision (final)**: the ORDER-020 Exit Criterion means the conflicting
file fixed + zero merge conflicts (achieved); the 8 stale filenames are
superseded-by-Migration and are **not** renamed inside Recovery.

## References

- `docs/governance/MIGRATION_PLAN.md` — the control plan this executes.
- `docs/BRANCH_FORENSICS_001.md` — the root-cause audit.
- `communication/task_queue/REPO-RECOVERY-001.md` — the task record and
  blocker/finding log.
- `docs/governance/policies/Branch_Protection_Policy.md` §5/§6 (no
  force-push, recovery method), `Git_Workflow_Standard.md` §8/§10.
