# TASK-002E

**Title**: Navigation Tests (Navigation Validation)
**Status**: 🟢 AUTHORIZED, in progress.

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

**Permitted**: everything above, against `platforms/navigation_core.py`/
`platforms/platform_adapter.py`/`platforms/navigation_events.py`/
`platforms/menu_registry.py` as they exist today.

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
