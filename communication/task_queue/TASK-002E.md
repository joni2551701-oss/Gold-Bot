# TASK-002E

**Title**: Navigation Tests (Navigation Validation)
**Status**: ✅ APPROVED. **Freeze: ✅ YES — Frozen from this point.**

## Freeze Checklist

```
Freeze Checklist
☑ CI Passed              -- ci.yml run #163 success, commit aea1b22
☑ Tests Passed            -- 29 new (80 total in tests/platforms/), full suite 4689/4689
☑ Documentation Updated   -- docs/PLATFORM_FOUNDATION.md (Documentation Policy)
☑ ADR Updated (if required) -- ADR-010 (Fail Closed Permission Policy), ADR-011 (Security Review Layer) recorded as a direct consequence of this task's own security finding
☑ Constitution Impact Reviewed -- none; no new Article required
☑ Public Contracts Reviewed -- zero change to any existing platforms/ contract; test-only additions
☑ Backward Compatibility Checked -- zero diff to Trading Core, telegram/, .github/, or any existing platforms/*.py file
☑ No Silent Decisions     -- has_sufficient_permission() finding surfaced, not self-fixed; Director classified it as a Security Backlog item (docs/TECHNICAL_DEBT.md), not applied without authorization
☑ Director Approval       -- this review
☑ Freeze Applied          -- this document
```

## Objective

Take Navigation from "works" to "verifiably reliable," per Director
brief:

- Navigation Validation
- Edge Cases
- Stack Consistency
- Multi-session Validation
- Permission Validation
- Event Validation
- Recovery Scenarios
- Integration Validation

**Permitted**: everything above, against `platform_layer/platform_service/navigation_core.py`/
`platform_layer/platform_service/platform_adapter.py`/`platform_layer/platform_service/navigation_events.py`/
`platform_layer/platform_service/menu_registry.py` as they exist today.

**Forbidden**: redesigning the Navigation architecture, changing any
existing public contract (`NavigationResult`, `NavigationEvent`,
`MenuDefinition`, `PlatformAdapterBase`'s method signatures, etc. —
ADR-006/007/008's proposed changes to `NavigationResult`/events remain
deferred to their own future task, not this one), touching Trading
Core, or turning `PlatformAdapterBase` into a concrete Telegram/
Android/iOS implementation.

## Depends on

TASK-002D (Navigation Implementation) — ✅ APPROVED, Frozen.

## Notes

`tests/platforms/test_navigation_core.py` (TASK-002D) already covers
several of these at a basic level (permission denial, empty-stack
back, session isolation) — this task's job is depth (stress/edge
cases, recovery, integration), not first coverage. Whatever this task
adds is additional test coverage against the existing, frozen
TASK-002D contracts — not a change to those contracts themselves.

## Delivered

`tests/platforms/test_navigation_validation.py` — 29 new tests across
8 sections (Navigation Validation, Edge Cases/Invalid Route Handling,
Stack Consistency, Multi-session Validation, Permission Validation,
Event Validation, Recovery Scenarios, Integration Validation, plus a
Stress section). `tests/platforms/` total: 80 tests, all passing.
Full suite: 4689 passed. `pyflakes`/`compileall` clean. `main.py`
smoke run clean, matching baseline log shape. Zero diff to Trading
Core (`core/`, `context/`, `strategies/`, `signals/`, `decision/`,
`risk/`, `ai/`, `execution/`, `database/`), `telegram/`, `.github/`, or
any existing `platforms/*.py` file — confirmed via
`git diff --cached --stat`.

**Validation finding (documented, not fixed — `navigation_core.py` is
Frozen)**: `has_sufficient_permission()` ranks an unrecognized
*required* tier at -1, so it is permissive (returns `True`) rather
than restrictive for an empty/malformed *required*-tier input; the
*user*-tier direction correctly fails closed. Not exploitable today
since every `DEFAULT_MENUS.permission` is independently validated to
be exactly USER/ADMIN/OWNER. Raised for Director awareness per the No
Silent Decisions Policy; a fix requires future authorization.

`docs/PLATFORM_FOUNDATION.md`'s Testing section updated accordingly.
