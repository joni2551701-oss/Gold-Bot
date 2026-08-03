# IMPLEMENTATION.md -- ai_layer/ai_engine/runtime

## `ai_service.py`

AI Layer — AI Runtime Service (Phase 61.2: AI Runtime Foundation,

Classes: `_AttemptScopedHealthTracker`, `AIService`

## `runtime_events.py`

AI Layer — AI Runtime Lifecycle Events (Phase 61.6: AI Operations &

Classes: `RuntimeLifecycleEvent`

Top-level functions: `create_lifecycle_event()`

## `runtime_manager.py`

AI Layer — AI Runtime Manager (Phase 61.6: AI Operations & Reliability

Classes: `RuntimeManager`

## `runtime_profiles.py`

AI Layer — Runtime Configuration Profiles (Phase 61.6: AI Operations &

Classes: `RuntimeProfile`

Top-level functions: `resolve_profile()`, `apply_provider_priority()`

## `runtime_request.py`

AI Layer — AI Runtime Request (Phase 61.2: AI Runtime Foundation,

Classes: `RuntimeRequest`

## `runtime_response.py`

AI Layer — AI Runtime Response (Phase 61.2: AI Runtime Foundation,

Classes: `RuntimeResponse`

## `runtime_state.py`

AI Layer — AI Runtime State Model (Phase 61.6: AI Operations &

Classes: `RuntimeState`, `RuntimeStateRecord`

Top-level functions: `is_valid_transition()`

## `self_check.py`

AI Layer — Runtime Self Check (Phase 61.7: AI Platform Stabilization &

Classes: `CheckStatus`, `SelfCheckResult`, `RuntimeSelfCheckReport`

Top-level functions: `run_self_check()`

## Runtime / Algorithms / Pipeline / Event Flow / Sequence / Design Decisions / Performance Notes

Not authored at rollout time -- this section requires domain understanding beyond what can be mechanically derived from code, and is left for a future Development Phase to fill in (per Director Order No. 012/013, this rollout is documentation standardization only, not new authorship of technical narrative).

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013).*
