# ai_layer / ai_engine / runtime

**Module**

## Purpose

No module-level docstring was present in `__init__.py` at the time this file was generated (2026-08-03) by the Engineering Standard v1.0 rollout (Director Order No. 012/013). This is a placeholder pending a real description from a future Development Phase -- content below is limited to what could be verified mechanically from the code.

## Files

- `__init__.py`
- `ai_service.py` -- AI Layer — AI Runtime Service (Phase 61.2: AI Runtime Foundation,
- `runtime_events.py` -- AI Layer — AI Runtime Lifecycle Events (Phase 61.6: AI Operations &
- `runtime_manager.py` -- AI Layer — AI Runtime Manager (Phase 61.6: AI Operations & Reliability
- `runtime_profiles.py` -- AI Layer — Runtime Configuration Profiles (Phase 61.6: AI Operations &
- `runtime_request.py` -- AI Layer — AI Runtime Request (Phase 61.2: AI Runtime Foundation,
- `runtime_response.py` -- AI Layer — AI Runtime Response (Phase 61.2: AI Runtime Foundation,
- `runtime_state.py` -- AI Layer — AI Runtime State Model (Phase 61.6: AI Operations &
- `self_check.py` -- AI Layer — Runtime Self Check (Phase 61.7: AI Platform Stabilization &

## Responsibilities

See `CONTRACTS.md` and `MODULE_MAP.md` in this directory.

## Dependencies

See `CONTRACTS.md` in this directory for cross-layer dependencies (mechanically derived from actual imports).

## Public API

- `ai_service.py`: class `_AttemptScopedHealthTracker`
- `ai_service.py`: class `AIService`
- `runtime_events.py`: class `RuntimeLifecycleEvent`
- `runtime_events.py`: function `create_lifecycle_event()`
- `runtime_manager.py`: class `RuntimeManager`
- `runtime_profiles.py`: class `RuntimeProfile`
- `runtime_profiles.py`: function `resolve_profile()`
- `runtime_profiles.py`: function `apply_provider_priority()`
- `runtime_request.py`: class `RuntimeRequest`
- `runtime_response.py`: class `RuntimeResponse`
- `runtime_state.py`: class `RuntimeState`
- `runtime_state.py`: class `RuntimeStateRecord`
- `runtime_state.py`: function `is_valid_transition()`
- `self_check.py`: class `CheckStatus`
- `self_check.py`: class `SelfCheckResult`
- `self_check.py`: class `RuntimeSelfCheckReport`
- `self_check.py`: function `run_self_check()`

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Documentation standardization only -- content mechanically derived from existing code, not authored from scratch.*
