"""core_layer/configuration/runtime_feature_manager -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `runtime_feature_manager.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `runtime_feature_manager.py`.
"""
from core_layer.configuration.runtime_feature_manager.runtime_feature_manager import (
    dataclass,
    datetime,
    timezone,
    Dict,
    List,
    Optional,
    DEPENDENCY_RULES,
    DependencyValidationResult,
    format_dependency_violations,
    validate_feature_dependencies,
    FeatureDescriptor,
    build_feature_registry,
    FeatureRuntimeState,
    RuntimeStateCache,
    AuditLogRepository,
    ConfigSnapshotRepository,
    create_config_snapshot,
    RuntimeFeatureRepository,
    setup_logger,
    logger,
    ToggleResult,
    RuntimeFeatureManager,
)

__all__ = [
    "dataclass",
    "datetime",
    "timezone",
    "Dict",
    "List",
    "Optional",
    "DEPENDENCY_RULES",
    "DependencyValidationResult",
    "format_dependency_violations",
    "validate_feature_dependencies",
    "FeatureDescriptor",
    "build_feature_registry",
    "FeatureRuntimeState",
    "RuntimeStateCache",
    "AuditLogRepository",
    "ConfigSnapshotRepository",
    "create_config_snapshot",
    "RuntimeFeatureRepository",
    "setup_logger",
    "logger",
    "ToggleResult",
    "RuntimeFeatureManager",
]
