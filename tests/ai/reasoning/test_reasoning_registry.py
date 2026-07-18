"""Phase 63.4 TASK 3 — ai/reasoning/reasoning_registry.py: static ReasoningType catalog."""

from ai.reasoning.models import ReasoningType
from ai.reasoning.reasoning_registry import build_reasoning_type_registry, describe


def test_registry_has_one_descriptor_per_reasoning_type():
    registry = build_reasoning_type_registry()
    types = {descriptor.reasoning_type for descriptor in registry}
    assert types == set(ReasoningType)


def test_describe_returns_matching_descriptor():
    descriptor = describe(ReasoningType.PROBABILITY_ESTIMATE)
    assert descriptor is not None
    assert descriptor.label == "Probability Estimate"


def test_describe_never_raises_and_is_total():
    for reasoning_type in ReasoningType:
        assert describe(reasoning_type) is not None


def test_registry_has_no_duplicate_types():
    registry = build_reasoning_type_registry()
    types = [descriptor.reasoning_type for descriptor in registry]
    assert len(types) == len(set(types))
