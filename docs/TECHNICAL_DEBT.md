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
  16 related files once `platform_layer/telegram/polling.py`'s own live heartbeat
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

## Security Backlog: `has_sufficient_permission()` fails open for an unrecognized required tier

- **Where**: `platform_layer/platform_service/navigation_core.py` (Frozen since TASK-002D),
  `has_sufficient_permission(user_tier, required_tier)`.
- **What**: `_TIER_RANK.get(required_tier, -1)` ranks any unrecognized
  `required_tier` value at `-1`. Since every real user tier
  (`USER`/`ADMIN`/`OWNER`) ranks at 0 or above, `rank(user) >= -1` is
  always true — an empty, malformed, or unrecognized *required* tier
  is treated as "no restriction" instead of "no access." The *user*-tier
  side of the same function correctly fails closed (an unrecognized
  user tier ranks at `-1`, which never satisfies a real required tier's
  rank ≥0).
- **Why it's not exploitable today**: every `DEFAULT_MENUS` entry's
  `permission` field is independently validated (by test) to be
  exactly one of `USER`/`ADMIN`/`OWNER` — no live code path can supply
  an unrecognized `required_tier` to this function today.
- **Discovery**: surfaced by TASK-002E's validation test suite
  (`tests/platforms/test_navigation_validation.py`), not fixed at the
  time, since `navigation_core.py` was already Frozen.
- **Director decision**: classified as a **Potential Security
  Weakness**, not a routine bug — see `communication/decisions/ADR-010.md`
  (Fail Closed Permission Policy, the standing rule this violates) and
  `communication/decisions/ADR-011.md` (Security Review Layer, the
  reporting practice that will re-check this class of issue going
  forward). No code change made yet — a dedicated future Security Task,
  authorized separately after Navigation Foundation (TASK-002E +
  TASK-002F) closes, will fix `_TIER_RANK.get(required_tier, -1)`'s
  handling explicitly (e.g. treating an unrecognized required tier as
  "deny," not "no restriction").
- **Resolution path, if/when authorized**: change
  `has_sufficient_permission()` so an unrecognized `required_tier`
  returns `False` rather than being satisfied by any real user rank —
  requires reopening the Frozen `navigation_core.py` module under
  ADR-010's own authorization, plus a regression test confirming the
  fix doesn't change behavior for any of the three real tier values.

## Related documents

- `docs/PHASE_BRANCH_SYNC_AUDIT.md` — the branch-of-record decision
  this debt item depends on.
- `docs/PHASE_OWNER_SNAPSHOT_REMOVAL.md` — the removal phase that
  created this gap on `main`.
