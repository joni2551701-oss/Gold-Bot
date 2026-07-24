# BRANCH-FORENSICS-001 — Repository History Forensics

**Task**: BRANCH-FORENSICS-001, issued as ORDER-003 following ORDER-002
(all Repository Migration work paused: no merge, rebase, branch
rename, branch delete, or default-branch change performed or proposed
as an action in this document).
**Type**: Forensic investigation only. Every fact below is backed by a
git plumbing command run directly against the real repository history
— `git merge-base`, `git log --follow`, `git merge-tree` — not
inference or restatement of REPO-001's earlier findings. Where this
investigation sharpens or corrects an earlier approximate finding, that
correction is stated explicitly.

**Headline result**: the entire `mergeable_state: "dirty"` conflict
blocking both PR #1 and PR #2 traces to **exactly one file** and
**exactly one invisible character**. `git merge-tree` (a safe,
side-effect-free git plumbing command) reports precisely one conflict
in each case, on `strategies/strategy_manager.py` — and the underlying
file content is byte-identical on every side (same blob SHA,
`89a66416a8...`, confirmed via `git ls-tree` and `git cat-file`/`md5sum`).
This is a path-only collision, not a content conflict.

---

## Timeline

All timestamps converted to UTC for a single consistent ordering
(source commits carry `+03:00` or `+00:00`, noted per entry).

| UTC time | Event |
|---|---|
| 2026-07-11 10:01:08 | **Repository's very first commits** (`a8c345e4` "Create decision_engine.py", `ab85640c` "Delete decision_engine.py⁠", `fd9e1e69` "Update decision_engine.py") — the corrupted-filename pattern is present from the first commits that create strategy files, not something that started later. |
| 2026-07-11 10:01:08 | `fd9e1e69` adds `"signal/strategy_manager.py⁠"` — **the origin commit**: singular, typo'd `signal/` directory, plus a trailing invisible Unicode character already present. |
| 2026-07-11 10:18:23 | `e1fa1291` renames `signal/` → `signals/` (directory typo partially fixed); invisible character still present. |
| 2026-07-12 11:22:29 | `30eaf766` renames `signals/` → `strategies/` (directory typo fully fixed) but introduces a stray **leading space** before the filename; invisible character still present. **This commit is shared history — it predates the branch split and both branches inherit it.** |
| **2026-07-12 13:10:54** | **`ad1affe` "Update config.py" — the last commit both branches share.** Confirmed via `git merge-base` and `git merge-base --is-ancestor` (true for both `main` and the production branch). |
| 2026-07-12 13:46:38 | `e67e5e4` (main-only) — repairs `ai/ai_analyzer.py⁠`'s own corrupted name. |
| 2026-07-12 13:48:34 | `acc844a` (main-only) — renames `"strategies/ liquidity_strategy.py⁠"` → `"strategie/lsiquidity_strategy.py⁠"`. **This is where the `strategie/` (missing "s") directory typo is introduced** — a regression relative to the already-correct `strategies/` spelling one commit earlier. |
| 2026-07-12 13:48:59 | `8c69ae77` (main-only) — renames `"strategies/ strategy_manager.py⁠"` → `"strategies/strategy_manager.py⁠"`: **removes the leading space but does not remove the trailing invisible character.** This is `main`'s own final, incomplete fix for this file — no later commit touches it, so this exact (still-corrupted) name persists to `main`'s current tip. |
| 2026-07-12 14:04:41 | `f78461b` (production branch's **first** post-divergence commit, "fix: stabilize imports and config path") — renames `"strategies/ strategy_manager.py⁠"` → `strategies/strategy_manager.py`, cleanly, in one step: removes both the leading space and the trailing invisible character. Production's copy is fully clean from this point on. |
| 2026-07-12 14:05:26 | **PR #1 opened** — 45 seconds after `f78461b` was pushed; head = production branch, base = `main` @ `8c69ae77` (itself one of the mid-repair commits above, not `main`'s later tip). Timing is consistent with an auto-created PR on first push of a new session branch, not a hand-authored change proposal. |
| 2026-07-12 16:45:34 | `7af7ddc5` (main-only) — renames `"strategie/lsiquidity_strategy.py⁠"` → `strategies/liquidity_strategy.py`: fixes the directory typo, the "lsiquidity" typo, and removes the invisible character, all in one commit. This file fully converges with production's clean version — no conflict remains for `liquidity_strategy.py`. |
| 2026-07-20 17:40:23 | `5618adec` (main-only) — "Add owner_snapshot.yml to main" — `main`'s current tip. |
| 2026-07-23 12:41:49 | `d911b97` "V2 Phase 6 Freeze" — production branch's current tip. |
| 2026-07-23 20:25:22 | **PR #2 opened** — head = current Platform Worker branch (production branch + 18 Platform/Governance commits, none touching `strategies/`). |

## Root Cause Analysis

**Q: When did the repository split from the production branch?**
2026-07-12 13:10:54 UTC, commit `ad1affe` ("Update config.py") — the
exact, confirmed last common ancestor (`git merge-base`, cross-checked
with `--is-ancestor` against both branch tips).

**Q: Why did `claude/*` become the production branch?**
Already answered with full evidence in REPO-001 §0/Q2: a deliberate,
Director-visible decision recorded in `docs/PHASE_P1_AUDIT.md`, because
`main` lacked the entire TradingPipeline architecture. Nothing in this
deeper forensic pass changes that answer.

**Q: Why did `main` fall behind?**
Because after `ad1affe`, `main` received exactly 5 more commits ever —
4 same-day filename-repair commits (13:46–16:45 UTC, 2026-07-12) and
one workflow-registration commit 8 days later (`owner_snapshot.yml`,
2026-07-20) — while all real architecture work (171 commits, 1,208
files, +137,391 lines per REPO-001 §0/Q3) happened exclusively on the
production line. `main` was never actively developed after the split;
it was only lightly, sporadically touched for unrelated
housekeeping.

**Q: What is the exact conflict origin?**
A **rename/rename conflict on a single file**, `strategies/strategy_manager.py`,
caused by two *independent* cleanup attempts on the same
originally-corrupted filename (`"signal/strategy_manager.py⁠"`,
created 2026-07-11 with a directory typo and a trailing U+2060 WORD
JOINER character already embedded). `main`'s cleanup (`8c69ae77`,
13:48:59 UTC) fixed the directory and the leading-space issue but
missed the trailing invisible character; the production branch's
cleanup (`f78461b`, 14:04:41 UTC, ~16 minutes later, done independently
without knowledge of `main`'s parallel fix) fixed everything in one
pass. Both branches believe they hold the "correct," clean name — and
both render visually identical in any normal terminal or editor — but
they differ by one invisible codepoint, which is exactly the kind of
difference a byte-exact rename-detection algorithm cannot silently
reconcile.

**How the corruption itself originated** (not just how it was
fixed): every `git log --follow` trace on this file (and the parallel
trace on `ai/ai_analyzer.py`, `strategies/liquidity_strategy.py`)
begins with the *very first* commits that created these files, on
2026-07-11 — the invisible-character pattern is not something either
branch introduced; it was present in this repository from its
earliest history, most consistent with files having been created or
renamed through a web-based editor/upload flow that silently inserted
a zero-width Unicode character (a known, common failure mode of
copy-paste or drag-and-drop file operations in browser-based editors).
Both branches inherited this pre-existing corruption and each
independently tried to clean it up — `main` incompletely, production
completely — which is the actual mechanism that produced two divergent
"clean" states for the same file.

## Commit Chain

Full chain for the one file that actually conflicts,
`strategies/strategy_manager.py`, oldest to newest:

```
fd9e1e69 (2026-07-11 10:01:08 UTC, shared)
    "signal/strategy_manager.py⁠"                     [created — typo'd dir + invisible char]
        ↓
e1fa1291 (2026-07-11 10:18:23 UTC, shared)
    "signals/strategy_manager.py⁠"                    [dir typo fixed; invisible char remains]
        ↓
30eaf766 (2026-07-12 11:22:29 UTC, shared — last common history before split)
    "strategies/ strategy_manager.py⁠"                [dir fixed; leading space added; invisible char remains]
        ↓
   ═══════════════ ad1affe (2026-07-12 13:10:54 UTC) — BRANCH SPLIT ═══════════════
        ↓                                                    ↓
   [main line]                                          [production line]
        ↓                                                    ↓
8c69ae77 (13:48:59 UTC)                              f78461b (14:04:41 UTC)
    "strategies/strategy_manager.py⁠"                  strategies/strategy_manager.py
    [leading space removed;                            [leading space AND invisible
     invisible char NOT removed —                        char both removed — fully
     main's final, incomplete fix]                       clean, production's final state]
        ↓                                                    ↓
   (no further commits touch                          (171 more commits of real
    this file on main)                                  architecture work, unrelated
        ↓                                                to this file)
   main's current tip (5618adec)                       production's current tip (d911b97)
    still carries the invisible                         clean, matches PR #2's head
    character in this filename                          (current working branch) too
```

Companion file `strategies/liquidity_strategy.py` went through a
similar but ultimately **non-conflicting** chain: `main`'s `acc844a`
(13:48:34 UTC) introduced a *worse* intermediate state
(`"strategie/lsiquidity_strategy.py⁠"` — directory typo regression plus
a second filename typo), but `main`'s own later commit `7af7ddc5`
(16:45:34 UTC, same day) fully cleaned it — directory, filename typo,
and invisible character all fixed in one step — converging exactly with
production's already-clean version. This is why `git merge-tree`
reports **zero** conflict for this file, only for `strategy_manager.py`.

## Conflict Origin

Confirmed directly via `git merge-tree --write-tree` (a git plumbing
command that computes a merge without touching the working tree, index,
or any branch ref — fully safe, no side effects, consistent with
ORDER-002's constraints):

```
$ git merge-tree --write-tree origin/main origin/claude/code-analysis-optimization-pwfo3q
CONFLICT (rename/rename): strategies/ strategy_manager.py⁠ renamed to
strategies/strategy_manager.py⁠ in origin/main and to
strategies/strategy_manager.py in origin/claude/code-analysis-optimization-pwfo3q.
```

Re-run against PR #2's actual head (the current Platform Worker
branch) produces the **identical single conflict** — confirming PR #2
is blocked by the exact same one-file issue as PR #1, not a separate
problem introduced by this session's 18 Platform/Governance commits
(which never touch `strategies/`).

**Content is identical on every side.** `git ls-tree` shows all three
paths — `main`'s corrupted name, the production branch's clean name,
and the intermediate shared-history name — point to the **same blob
SHA** (`89a66416a8f53672ceb12312760188fedd1b4bd8`); `git cat-file -p
<blob> | md5sum` confirms byte-for-byte identical content
(`c0cd59ba6090a20639dabead3187421f`) from both retrieval paths. **This
is a path-only conflict. Not one line of actual code differs.**

## Recovery Strategy

Not executed — proposed only, per ORDER-002/ORDER-003's constraints.

1. **The fix, once authorized, is a single-file, content-neutral
   rename on `main`**: `git mv "strategies/strategy_manager.py⁠"
   strategies/strategy_manager.py` (removing the one trailing U+2060
   character) — this makes `main`'s path byte-identical to the
   production branch's, at which point `git merge-tree` would report
   zero conflicts for this file, and (based on this investigation
   finding no other conflict anywhere in the full diff) very likely
   zero conflicts overall. This should be re-verified with a fresh
   `git merge-tree` run once the rename is proposed, not assumed.
2. **This does not need to happen before understanding is complete** —
   ORDER-002's pause stands; this is the recommended shape of the fix
   *when* migration resumes, not an action taken now.
3. **Recovery does not require deleting or rewriting any branch
   history.** The one-file rename above is a normal, forward commit —
   no force-push, no history rewrite, no risk to either branch's
   existing commits.
4. **Independent of this specific fix, REPO-001's Phase 1 (tag today's
   tips of both `main` and the production branch) remains the correct
   first action whenever migration resumes** — it costs nothing, and
   gives a named rollback point before any rename, merge, or
   protection change is made, including the `strategy_manager.py` fix
   itself.
5. **No evidence found of any other corrupted file beyond the three
   already identified** (`ai_analyzer.py`, `liquidity_strategy.py`,
   `strategy_manager.py`) — `git merge-tree`'s single reported conflict
   is the complete list for a `main`-vs-production merge; a full repo
   scan for other zero-width/invisible Unicode characters in filenames
   was not run as part of this task (out of the 8 questions ORDER-003
   named) and would be a reasonable, cheap addition if the Director
   wants full certainty before the fix is applied.

## Director Recommendation

The repository's history and the conflict's root cause are now fully
understood, down to the single character responsible. This was never
a deep architectural incompatibility requiring a complex resolution —
it is one file whose two independent cleanup attempts each removed a
different subset of accumulated corruption, leaving one branch's
"fixed" name one invisible character short of matching the other's.

Recommend: once the Director is satisfied this investigation is
complete, authorize a narrowly-scoped follow-up (not a routine part of
REPO-002's broader migration) to (a) tag both branches' current tips
first (zero risk), (b) apply the single-file rename fix on `main`
described above, (c) re-run `git merge-tree` to confirm zero conflicts
remain, and only then (d) resume the paused Repository Migration
(REPO-001/REPO-002) exactly as previously planned. This keeps the
"fix the actual cause, not the symptom" principle ORDER-002 was issued
under: the fix is the one-character rename, not a broad merge or a
branch-model change performed without understanding why the conflict
existed.

## Related

- `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md` — the audit this
  forensics task follows up on, especially §0/Q5.
- `communication/task_queue/BRANCH-FORENSICS-001.md` — this task's own
  ticket record.
- `docs/PHASE_BRANCH_SYNC_AUDIT.md`, `docs/PHASE_P1_AUDIT.md` — the
  prior, independently-confirmed audits this investigation cross-checks
  against.
