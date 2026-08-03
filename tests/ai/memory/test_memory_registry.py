"""Phase 63.3 TASK 3 — ai/memory/memory_registry.py: static MemoryScope catalog."""

from ai_layer.knowledge_ai.memory_manager.memory_registry import build_memory_scope_registry, describe
from ai_layer.knowledge_ai.memory_manager.models import MemoryScope, MemoryType


def test_registry_has_one_descriptor_per_scope():
    registry = build_memory_scope_registry()
    scopes = {descriptor.scope for descriptor in registry}
    assert scopes == set(MemoryScope)


def test_describe_returns_matching_descriptor():
    descriptor = describe(MemoryScope.EDUCATION)
    assert descriptor is not None
    assert descriptor.label == "Education Memory"
    assert descriptor.default_memory_type is MemoryType.LONG_TERM


def test_describe_never_raises_and_is_total():
    for scope in MemoryScope:
        assert describe(scope) is not None


def test_registry_is_metadata_only_no_duplicate_scopes():
    registry = build_memory_scope_registry()
    scopes = [descriptor.scope for descriptor in registry]
    assert len(scopes) == len(set(scopes))
