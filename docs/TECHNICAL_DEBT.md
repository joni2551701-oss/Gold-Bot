# GoldBot Technical Debt Register

Known, deliberately-unfixed issues — recorded so they aren't
rediscovered as a surprise, not a queue to work through unprompted.
An entry stays here until a dedicated Director task authorizes fixing
it; adding an entry is documentation only and implies no code change.

## `main`'s `owner_snapshot.yml` references code deleted from production

- **Where**: `.github/workflows/owner_snapshot.yml`, present only on
  `main` (not on `claude/code-analysis-optimization-pwfo3q`, the
  production branch — see `docs/PHASE_BRANCH_SYNC_AUDIT.md`).
- **What**: scheduled every 15 minutes (`*/15 * * * *`), it checks out
  `ref: claude/code-analysis-optimization-pwfo3q` and runs
  `python -m monitoring.run_snapshot`.
- **Why it's broken**: `docs/PHASE_OWNER_SNAPSHOT_REMOVAL.md` (V2
  Phase 2, production branch) deleted `monitoring/run_snapshot.py` and
  16 related files once `telegram/polling.py`'s own live heartbeat
  replaced the need for a GitHub-Actions substitute. Confirmed absent
  from the production branch's current `monitoring/` (14 files, none
  named `run_snapshot.py`). Every scheduled run of this workflow since
  that removal checks out code that no longer contains the module it
  tries to invoke, and fails.
- **Why the workflow file still exists on `main` at all**: GitHub
  Actions' `on: schedule` trigger reads the workflow YAML from the
  repository's default branch (`main`), regardless of which branch its
  own `checkout` step later pins — so the YAML had to stay on `main`
  to keep firing at all, even though its target code moved.
  `docs/PHASE_OWNER_SNAPSHOT_REMOVAL.md` explicitly scoped its removal
  to the production branch only and left the `main` copy untouched,
  per Director instruction not to edit `main` directly; it further
  states the `main` copy "updates automatically once this branch is
  merged" — a merge that has not happened.
- **Director decision (this phase)**: No action. Belongs to legacy
  synchronization work, intentionally outside current scope. Left
  exactly as-is.
- **Resolution path, if/when authorized**: either delete
  `.github/workflows/owner_snapshot.yml` from `main` directly (a
  `main`-only change, no production-branch code involved), or address
  it as part of whatever future `main` ↔ production branch strategy
  decision follows the Constitution v2 / documentation-system work
  referenced in the Director's own roadmap.

## Related documents

- `docs/PHASE_BRANCH_SYNC_AUDIT.md` — the branch-of-record decision
  this debt item depends on.
- `docs/PHASE_OWNER_SNAPSHOT_REMOVAL.md` — the removal phase that
  created this gap on `main`.
