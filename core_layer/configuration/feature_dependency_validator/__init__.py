"""core_layer/configuration/feature_dependency_validator -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `feature_dependency_validator.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `feature_dependency_validator.py`.
"""
from core_layer.configuration.feature_dependency_validator.feature_dependency_validator import (
    dataclass,
    Dict,
    List,
    Sequence,
    Tuple,
    FeatureDescriptor,
    DEPENDENCY_RULES,
    DependencyViolation,
    DependencyValidationResult,
    validate_feature_dependencies,
    format_dependency_violations,
)

__all__ = [
    "dataclass",
    "Dict",
    "List",
    "Sequence",
    "Tuple",
    "FeatureDescriptor",
    "DEPENDENCY_RULES",
    "DependencyViolation",
    "DependencyValidationResult",
    "validate_feature_dependencies",
    "format_dependency_violations",
]
