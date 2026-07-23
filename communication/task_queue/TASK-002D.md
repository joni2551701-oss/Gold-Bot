# TASK-002D

**Title**: Navigation Implementation
**Status**: 🟡 Conditionally Approved — architecture (Navigation Core,
Platform Adapter, Tests) reviewed and approved. Freeze pending final
CI confirmation.

**CI note**: `ci.yml` run #158 (commit `b366971`, this task's own
content) shows `cancelled`, not `success` — GitHub's own
`concurrency: cancel-in-progress: true` on `ci.yml` killed it when the
very next commit (`8adf53b`, a 1-line changelog fix, no code) was
pushed before #158 finished. Run #159 (`8adf53b`) — which contains the
exact same code as #158 plus that one non-code line — completed with
`success`. Flagged for Director confirmation that #159's success
satisfies the "CI #158 Success" condition, since #158 itself never
reached a conclusion of `success` or `failure`.

## Objective

Wire the pieces TASK-002C built into an actual Navigation Core, within
strict Director-set boundaries.

**Permitted**:
- Navigation Registry integration (consume `platforms/menu_registry.py`'s
  `MenuRegistry`, don't duplicate it).
- Navigation State connection (a real per-session stack, living only
  in the Platform Layer — Business Layer has zero awareness of it,
  per Director's Q6 answer at TASK-002B).
- Permission Flow integration (`Request → Permission → Navigation →
  Screen` — permission is checked *before* a screen is reached, per
  Director's Q4 answer).
- Event Interface connection (real navigation operations produce
  `NavigationEvent` instances from `platforms/navigation_events.py` —
  still no dispatcher/consumer, per ADR-004).
- Platform Layer's own internal adapter integration — an abstract
  adapter *interface* living inside `platforms/`, not a concrete
  per-platform (e.g. Telegram) implementation.

**Forbidden**:
- Any change to Trading Core (`context/`, `strategies/`, `signals/`,
  `decision/`, `risk/`, `ai/`, `core/pipeline.py`).
- Touching the Signal Engine or Decision Engine specifically.
- Any database schema change.
- Breaking any existing Telegram public API/contract
  (`telegram/*.py` stays untouched, same as every prior Navigation
  task).
- Hardcoded platform-specific logic anywhere in the new code — the
  Platform Adapter interface is where platform-specific behavior is
  meant to live *later*, in a platform's own concrete implementation,
  never inline in Navigation Core itself.

## Depends on

TASK-002C (Navigation Registry) — ✅ Approved, Frozen.

## Notes

Per the Freeze Checklist (`docs/PLATFORM_WORKFLOW.md`), this task's
own close-out will state Backward Compatibility and No Silent
Decisions explicitly, same as TASK-002C's.
