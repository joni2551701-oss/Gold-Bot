"""
Configuration Layer — Feature Dependency Validator (Phase 59.6: Audit
& Observability Foundation, TASK 5).

Checks a feature registry (configuration/feature_registry.py, same
phase, TASK 4) against a small set of declared dependency rules --
this task's own worked example: ENABLE_EXECUTION requires ENABLE_RISK
and ENABLE_DECISION. Read-only: this module never enables, disables,
or corrects a feature -- it only reports whether the CURRENT registry
state is internally consistent.

Every name referenced in DEPENDENCY_RULES below (ENABLE_EXECUTION,
ENABLE_RISK, ENABLE_DECISION) is one of
feature_registry.py's own declared-only entries (implemented=False,
always disabled) -- so with today's registry, no dependency rule is
ever violated (a disabled feature has nothing to require). This
validator becomes meaningful once a future phase gives one of these
names a real, toggleable backing; the rule itself is documented now so
that future work has a stable, tested contract to build against.
"""

from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

from configuration.feature_registry import FeatureDescriptor

# feature_name -> the other feature_names it requires to also be
# enabled. A tuple of (name, required_names) pairs would work equally
# well; a dict is used since every name in this codebase's registry is
# unique (see feature_registry.py's own test_registry_names_are_unique).
DEPENDENCY_RULES: Dict[str, Tuple[str, ...]] = {
    "ENABLE_EXECUTION": ("ENABLE_RISK", "ENABLE_DECISION"),
}


@dataclass(frozen=True)
class DependencyViolation:
    """feature: the enabled feature whose dependency isn't satisfied. missing_dependency: the specific required feature that is disabled (or entirely absent from the registry)."""
    feature: str
    missing_dependency: str


@dataclass(frozen=True)
class DependencyValidationResult:
    """valid: True only when `violations` is empty."""
    valid: bool
    violations: Tuple[DependencyViolation, ...]


def validate_feature_dependencies(
    registry: Sequence[FeatureDescriptor],
    rules: Dict[str, Tuple[str, ...]] = DEPENDENCY_RULES,
) -> DependencyValidationResult:
    """
    Never raises: an empty registry, or a rule referencing a name not
    present in the registry at all, both simply count that dependency
    as missing (treated the same as "disabled") -- "Invalid
    configuration" is reported structurally, not via an exception.
    """
    enabled_names = {entry.name for entry in registry if entry.enabled}

    violations: List[DependencyViolation] = []
    for feature, required_names in rules.items():
        if feature not in enabled_names:
            continue  # a disabled feature has nothing to require
        for required in required_names:
            if required not in enabled_names:
                violations.append(DependencyViolation(feature=feature, missing_dependency=required))

    return DependencyValidationResult(valid=(len(violations) == 0), violations=tuple(violations))


def format_dependency_violations(result: DependencyValidationResult) -> str:
    """Text-format rendering matching this task's own "Invalid configuration" framing."""
    if result.valid:
        return "Valid configuration -- no dependency violations."

    lines = ["Invalid configuration:"]
    for violation in result.violations:
        lines.append(f"  {violation.feature} requires {violation.missing_dependency}")
    return "\n".join(lines)
