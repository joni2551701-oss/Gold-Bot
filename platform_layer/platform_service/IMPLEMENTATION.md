# IMPLEMENTATION.md -- platform_layer/platform_service

## `capability_model.py`

Platform Layer — capability model (PLATFORM-001).

Classes: `SupportStatus`, `PlatformCapability`

## `capability_registry.py`

Platform Layer — module capability registry (PLATFORM-001).

Classes: `DuplicateModuleCapabilityError`, `ModuleCapabilityRegistry`

## `cross_platform_checker.py`

Platform Layer — Cross Platform Checker (PLATFORM-001).

Classes: `CapabilityViolation`, `CheckResult`

Top-level functions: `check_module_capabilities()`, `format_capability_violations()`

## `menu_registry.py`

Platform Layer — Universal Menu Registry / Route Registry (PLATFORM-001;

Classes: `MenuDefinition`, `DuplicateMenuIdError`, `MenuRegistry`

Top-level functions: `build_default_menu_registry()`

## `navigation_core.py`

Platform Layer — Navigation Core (TASK-002D, per the approved

Classes: `NavigationResult`, `NavigationCore`

Top-level functions: `has_sufficient_permission()`

## `navigation_events.py`

Platform Layer — Navigation Event Bus interface (TASK-002C, per

Classes: `NavigationEventType`, `NavigationEvent`

## `navigation_model.py`

Platform Layer — Universal Navigation model (PLATFORM-001; extended

Classes: `NavigationNode`

Top-level functions: `is_valid_screen_id()`

## `platform_adapter.py`

Platform Layer — Platform Adapter interface (TASK-002D, per the

Classes: `PlatformAdapterBase`

## `platform_model.py`

Platform Layer — platform model (PLATFORM-001: Platform Foundation &

Classes: `PlatformName`, `PlatformStatus`, `PlatformDefinition`

## `platform_registry.py`

Platform Layer — registry (PLATFORM-001).

Classes: `DuplicatePlatformError`, `PlatformRegistry`

Top-level functions: `build_default_registry()`

## Runtime / Algorithms / Pipeline / Event Flow / Sequence / Design Decisions / Performance Notes

Not authored at rollout time -- this section requires domain understanding beyond what can be mechanically derived from code, and is left for a future Development Phase to fill in (per Director Order No. 012/013, this rollout is documentation standardization only, not new authorship of technical narrative).

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013).*
