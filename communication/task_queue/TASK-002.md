# TASK-002

**Title**: Navigation
**Status**: In Progress (split into sub-tasks, per Director decision)

## Objective

Universal Navigation for GoldBot Platform — the foundation every
future client (Telegram Bot, Telegram Mini App, Android, iOS, Desktop)
navigates through. Director decision: this is treated as the highest-
risk Platform module so far ("agar Navigation noto'g'ri yozilsa,
hammasini qayta yozishga to'g'ri keladi") and is deliberately staged,
not delivered as one task, so a design mistake is caught before five
clients depend on it.

## Sub-tasks

Mirrors this repo's own existing sub-phase convention (e.g. Phase 6.0
→ 6.1 → 6.2 → 6.3, `docs/PHASE6_NAVIGATION_AUDIT.md` →
`docs/PHASE6_FREEZE.md`):

| Sub-task | Title | Status |
|---|---|---|
| TASK-002A | Navigation Analysis | In Progress |
| TASK-002B | Navigation Architecture | Pending — starts only after Director approves 002A |
| TASK-002C | Navigation Registry | Pending |
| TASK-002D | Navigation Implementation | Pending |
| TASK-002E | Navigation Tests | Pending |
| TASK-002F | Navigation Freeze | Pending |

## Depends on

TASK-001 (Platform Foundation & Collaboration Infrastructure) — Completed.

## Notes

Each sub-task gets its own Director review before the next starts —
per the new "Architecture First" workflow's Approval Check step. No
sub-task beyond 002A begins without that review, even if the work
looks straightforward.
