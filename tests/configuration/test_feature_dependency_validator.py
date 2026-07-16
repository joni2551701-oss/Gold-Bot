"""
Phase 59.6, TASK 5 -- configuration/feature_dependency_validator.py
tests. Re-anchored to the Infrastructure-only DEPENDENCY_RULES example
(ENABLE_BACKTEST requires ENABLE_DATASET_SYNC/ENABLE_ANALYTICS) in
Phase 60.9: Runtime Registry Separation -- see that module's own
docstring for why the original ENABLE_EXECUTION/ENABLE_RISK/
ENABLE_DECISION example was replaced.
"""

from configuration.feature_dependency_validator import (
    DependencyValidationResult,
    format_dependency_violations,
    validate_feature_dependencies,
)
from configuration.feature_registry import FeatureDescriptor, build_feature_registry


def _descriptor(name, enabled):
    return FeatureDescriptor(name=name, enabled=enabled, implemented=False, source="declared")


def test_default_registry_has_no_violations():
    """ENABLE_BACKTEST is disabled by default in build_feature_registry() -- nothing to require."""
    registry = build_feature_registry()

    result = validate_feature_dependencies(registry)

    assert isinstance(result, DependencyValidationResult)
    assert result.valid is True
    assert result.violations == ()


def test_enabled_feature_with_satisfied_dependencies_is_valid():
    registry = [
        _descriptor("ENABLE_BACKTEST", True),
        _descriptor("ENABLE_DATASET_SYNC", True),
        _descriptor("ENABLE_ANALYTICS", True),
    ]

    result = validate_feature_dependencies(registry)

    assert result.valid is True


def test_enabled_feature_missing_one_dependency_is_invalid():
    registry = [
        _descriptor("ENABLE_BACKTEST", True),
        _descriptor("ENABLE_DATASET_SYNC", True),
        _descriptor("ENABLE_ANALYTICS", False),
    ]

    result = validate_feature_dependencies(registry)

    assert result.valid is False
    assert len(result.violations) == 1
    assert result.violations[0].feature == "ENABLE_BACKTEST"
    assert result.violations[0].missing_dependency == "ENABLE_ANALYTICS"


def test_enabled_feature_missing_both_dependencies_reports_both():
    registry = [_descriptor("ENABLE_BACKTEST", True)]

    result = validate_feature_dependencies(registry)

    assert result.valid is False
    assert len(result.violations) == 2


def test_disabled_feature_never_produces_a_violation():
    registry = [_descriptor("ENABLE_BACKTEST", False)]

    result = validate_feature_dependencies(registry)

    assert result.valid is True


def test_missing_dependency_entirely_absent_from_registry_is_a_violation():
    registry = [_descriptor("ENABLE_BACKTEST", True)]  # ENABLE_DATASET_SYNC/ENABLE_ANALYTICS not in registry at all

    result = validate_feature_dependencies(registry)

    assert result.valid is False


def test_empty_registry_never_raises():
    result = validate_feature_dependencies([])
    assert result.valid is True


def test_custom_rules_override_the_default():
    registry = [_descriptor("ENABLE_AI", True)]
    custom_rules = {"ENABLE_AI": ("ENABLE_ANALYTICS",)}

    result = validate_feature_dependencies(registry, rules=custom_rules)

    assert result.valid is False
    assert result.violations[0].feature == "ENABLE_AI"


def test_format_dependency_violations_valid_case():
    result = validate_feature_dependencies([])
    text = format_dependency_violations(result)
    assert "Valid configuration" in text


def test_format_dependency_violations_invalid_case():
    registry = [_descriptor("ENABLE_BACKTEST", True)]
    result = validate_feature_dependencies(registry)

    text = format_dependency_violations(result)

    assert "Invalid configuration" in text
    assert "ENABLE_BACKTEST requires ENABLE_DATASET_SYNC" in text
    assert "ENABLE_BACKTEST requires ENABLE_ANALYTICS" in text
