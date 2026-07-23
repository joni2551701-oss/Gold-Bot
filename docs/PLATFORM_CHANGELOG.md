# Platform Changelog

Per-commit record for Platform-role changes, introduced by
PLATFORM-001. Different granularity from `docs/changelog/CHANGELOG.md`
(phase-level: Version/Changes/Architecture Impact) — this document is
commit-level and Platform-scoped, per the Director's explicit
six-field format. It complements, not replaces, the phase-level
changelog: a Platform phase still gets its own `CHANGELOG.md` entry at
freeze time; each commit inside that phase gets its own entry here.

## Format

Each entry:

- **Changed** — exactly what changed (files, behavior).
- **Reason** — why, in one or two sentences.
- **Impact** — what this affects (which platforms, which modules,
  whether it's foundation-only or live).
- **Migration** — what a consumer of the changed code needs to do
  differently, if anything ("None — new module, nothing depended on
  it yet" is a valid, honest answer).
- **Rollback** — how to undo this commit if needed (usually `git
  revert <sha>` for a foundation-only change with no data migration).
- **Compatibility** — whether this is backward compatible, and with
  what (existing Telegram commands, existing tests, existing DB
  schema).

## Entries

### Commit — PLATFORM-001: Platform Foundation & Collaboration Infrastructure

**Changed**: New `platforms/` package (`platform_model.py`,
`platform_registry.py`, `capability_model.py`, `capability_registry.py`,
`cross_platform_checker.py`, `navigation_model.py`, `menu_registry.py`)
+ `tests/platforms/` (unit tests for all seven). New `communication/`
folder tree (nine subfolders + `task_queue/QUEUE.md` and five seeded
`TASK-XXX.md` tickets). New `docs/PLATFORM_DOCUMENTATION_POLICY.md`,
`docs/PLATFORM_BUG_REPORT_STANDARD.md`, `docs/PLATFORM_CHANGELOG.md`
(this document), `docs/PLATFORM_FOUNDATION.md`.

**Reason**: Director's PLATFORM-001 brief — the foundation every
future client platform (Telegram Bot, Telegram Mini App, Android,
iOS, Desktop) shares, plus the process infrastructure so the Platform
Worker maintains its own task queue instead of asking "what's next?"
after each task.

**Impact**: Foundation only — no live wiring into `telegram/`'s
existing commands, keyboards, or handlers. Zero Trading Core diff.
Registers Telegram Bot as the only `LIVE` platform (honest — matches
reality); the other four platforms are `NOT_STARTED`.

**Migration**: None — every new module is unimported by any existing
file in this phase; nothing depended on it before, so nothing needs
to change to accommodate it.

**Rollback**: `git revert` the commit — no database migration, no
schema change, no existing file modified outside `docs/CURRENT_PHASE.md`/
`docs/changelog/CHANGELOG.md` (both additive entries).

**Compatibility**: Fully backward compatible — every existing test,
command, and keyboard behaves identically; `python -m pytest tests/`
passes unchanged plus the new `tests/platforms/` suite.

## Related

- `docs/changelog/CHANGELOG.md` — the phase-level companion record.
- `docs/PLATFORM_FOUNDATION.md` — the architecture this first entry
  introduces.
