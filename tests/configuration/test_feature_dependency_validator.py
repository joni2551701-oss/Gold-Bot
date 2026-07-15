"""
Phase 59.6, TASK 5 -- configuration/feature_dependency_validator.py tests.
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
    """ENABLE_EXECUTION is disabled by default in build_feature_registry() -- nothing to require."""
    registry = build_feature_registry()

    result = validate_feature_dependencies(registry)

    assert isinstance(result, DependencyValidationResult)
    assert result.valid is True
    assert result.violations == ()


def test_enabled_feature_with_satisfied_dependencies_is_valid():
    registry = [
        _descriptor("ENABLE_EXECUTION", True),
        _descriptor("ENABLE_RISK", True),
        _descriptor("ENABLE_DECISION", True),
    ]

    result = validate_feature_dependencies(registry)

    assert result.valid is True


def test_enabled_feature_missing_one_dependency_is_invalid():
    registry = [
        _descriptor("ENABLE_EXECUTION", True),
        _descriptor("ENABLE_RISK", True),
        _descriptor("ENABLE_DECISION", False),
    ]

    result = validate_feature_dependencies(registry)

    assert result.valid is False
    assert len(result.violations) == 1
    assert result.violations[0].feature == "ENABLE_EXECUTION"
    assert result.violations[0].missing_dependency == "ENABLE_DECISION"


def test_enabled_feature_missing_both_dependencies_reports_both():
    registry = [_descriptor("ENABLE_EXECUTION", True)]

    result = validate_feature_dependencies(registry)

    assert result.valid is False
    assert len(result.violations) == 2


def test_disabled_feature_never_produces_a_violation():
    registry = [_descriptor("ENABLE_EXECUTION", False)]

    result = validate_feature_dependencies(registry)

    assert result.valid is True


def test_missing_dependency_entirely_absent_from_registry_is_a_violation():
    registry = [_descriptor("ENABLE_EXECUTION", True)]  # ENABLE_RISK/ENABLE_DECISION not in registry at all

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
    registry = [_descriptor("ENABLE_EXECUTION", True)]
    result = validate_feature_dependencies(registry)

    text = format_dependency_violations(result)

    assert "Invalid configuration" in text
    assert "ENABLE_EXECUTION requires ENABLE_RISK" in text
    assert "ENABLE_EXECUTION requires ENABLE_DECISION" in text
