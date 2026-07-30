# TASK-002D

**Title**: Navigation Implementation
**Status**: ✅ APPROVED. **Freeze: ✅ YES — Frozen from this point.**
No refactoring or new capability added to this task's own content
except for a critical bug, a security issue, a Director-approved ADR,
or a future Migration Task.

**CI resolution**: `ci.yml` run #158 (commit `b366971`) was cancelled
by supersession, not failure; run #159 (`8adf53b`, same tree + one
non-code line) completed `success`. Per the Director-approved CI
Supersession Rule (`communication/decisions/ADR-009.md`), run #159's
success is this task's official CI validation.

## Freeze Checklist

```
Freeze Checklist
☑ CI Passed              -- ci.yml run #159 success, per ADR-009 (CI Supersession Rule) resolving #158's cancellation-by-supersession
☑ Tests Passed            -- 12 new (51 total in tests/platforms/), full suite 4660/4660
☑ Documentation Updated   -- docs/PLATFORM_FOUNDATION.md (Documentation Policy)
☑ ADR Updated (if required) -- ADR-009 recorded as a direct consequence of this task's own CI review
☑ Constitution Impact Reviewed -- none; no new Article required
☑ Public Contracts Reviewed -- new NavigationCore/PlatformAdapterBase contracts; no existing platforms/ field removed or retyped
☑ Backward Compatibility Checked -- zero diff to Trading Core or any telegram/*.py file; NavigationCore/PlatformAdapterBase are additive, unwired modules
☑ No Silent Decisions     -- every design choice traces to Director-approved ADR-001/002/003/004 or the TASK-002D permitted/forbidden scope itself
☑ Director Approval       -- this review
☑ Freeze Applied          -- this document
```

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
