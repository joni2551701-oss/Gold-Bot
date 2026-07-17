# Commit Standard

The concrete, step-by-step companion to `docs/policies/RELEASE_POLICY.md`
and `CLAUDE.md`'s own mandatory Commit Protocol — restated here as the
Operational Standards layer's version of the same sequence, so it is
reachable from `docs/standards/` too.

## The sequence, in order, never reordered or skipped

```
git add -A
    ↓
pyflakes (on git ls-files, so only tracked/staged files are checked)
    ↓
   [changed anything? → back to git add -A]
    ↓
compileall
    ↓
pytest tests/
    ↓
python main.py (smoke run)
    ↓
git status  (must be clean — hard gate, not a warning)
    ↓
git diff --cached  (final review)
    ↓
commit
    ↓
push
    ↓
confirm GitHub Actions success
```

Running `pytest`/`pyflakes` before `git add -A` is a standard
violation even if the result happens to be the same — `pyflakes`
reads `git ls-files`, which only sees staged/tracked files, so a
check run too early silently skips anything not yet staged.

## Commit message shape

A short summary line (what changed, phrased as the change itself, not
"fixes bug"), a body explaining *why* this shape rather than *what*
(the diff already shows what), and — when the change is a phase's
final commit — an explicit list of what was **not** built, matching
the phase's own Freeze document.

## Never

- `--no-verify`, `--no-gpg-sign`, or any hook-skipping flag, unless a
  human explicitly requests it for that specific commit.
- `git commit --amend` on a commit a hook has already rejected — the
  commit did not happen, so amend would silently target the *previous*
  commit instead (this is `CLAUDE.md`'s own stated reason, not a new
  rule).
- A commit with `git status` showing any unstaged or untracked file
  the commit doesn't intend to include.

## Related

- `/CLAUDE.md` — the canonical Commit Protocol this document restates.
- `docs/policies/RELEASE_POLICY.md`.
- `docs/policies/TESTING_POLICY.md`.
