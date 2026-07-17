# Testing Policy

The operating detail behind Constitution Article 6 (Testing Rule).

## The pipeline

```
Code
  ↓
Test (unit + isolation + regression)
  ↓
Smoke (python main.py)
  ↓
CI (GitHub Actions)
  ↓
Freeze
```

A phase does not reach Freeze without passing every stage above, in
order, for the exact commit being frozen.

## Test categories, per new module (Article 6)

- **Unit tests** — the module's own logic in isolation. Every
  constructor argument is optional with a real, working default (the
  "fake-able by default" convention used everywhere in this codebase),
  so a test can inject a stub without needing a mocking framework.
- **Isolation tests** — proof the module respects Article 2/3's
  dependency and import boundaries: a grep/AST sweep for anything
  under `ai/` (`from decision`, `from risk`, `from execution` must be
  absent), a layering check for anything else.
- **Regression tests** — the full `pytest tests/` run itself. A green
  full suite after a change *is* the regression guarantee; there is no
  separate regression-only test category to author.

## The Commit Protocol as the enforcement mechanism

`CLAUDE.md`'s own Commit Protocol is this policy's concrete
implementation:

```
git add -A → pyflakes → (loop back to git add -A if pyflakes changed
anything) → compileall → pytest tests/ → python main.py smoke →
git status clean → git diff --cached reviewed → commit → push →
confirm GitHub Actions success
```

Every step runs against the exact staged state that will be
committed — not an earlier, pre-fix version of the code. `git status`
must be clean before a commit; if it is not, committing is forbidden
and the Worker returns to `git add -A`.

## Reporting

"Complete," "Validated," or "All checks passed" is never used before
GitHub Actions returns `success` for the exact commit reported on.
Before that: "Local validation passed. Waiting for GitHub Actions
confirmation." After: "GitHub Actions: SUCCESS. Phase complete."

## Related

- `docs/constitution/CONSTITUTION.md` Article 6.
- `CLAUDE.md` — the Commit Protocol this policy expands on.
