# core_layer/configuration/runtime_feature_manager

**Canonical module** (runtime_feature_manager) — GEL-001 package form.

## Purpose

See `IMPLEMENTATION.md` and the module docstring in `runtime_feature_manager.py`.

## Public API

- `dataclass`
- `datetime`
- `timezone`
- `Dict`
- `List`
- `Optional`
- `DEPENDENCY_RULES`
- `DependencyValidationResult`
- `format_dependency_violations`
- `validate_feature_dependencies`
- `FeatureDescriptor`
- `build_feature_registry`
- `FeatureRuntimeState`
- `RuntimeStateCache`
- `AuditLogRepository`
- `ConfigSnapshotRepository`
- `create_config_snapshot`
- `RuntimeFeatureRepository`
- `setup_logger`
- `logger`
- `ToggleResult`
- `RuntimeFeatureManager`

## Import

    from core_layer.configuration.runtime_feature_manager import <name>

---
*Generated 2026-08-04 under GoldBot Engineering Law GEL-001 (Strict Canonical Module Rule). Flat `runtime_feature_manager.py` converted to package form; implementation moved intact, public import path preserved via `__init__` re-export.*
