"""Phase 63.3 TASK 2 — ai/memory/models.py: MemoryType/MemoryPriority/MemoryScope/MemoryEntry."""

from ai.memory.models import MemoryEntry, MemoryPriority, MemoryScope, MemoryType


def test_memory_entry_defaults_priority_to_normal():
    entry = MemoryEntry(key="k", scope=MemoryScope.MARKET, memory_type=MemoryType.SHORT_TERM, value=1)
    assert entry.priority is MemoryPriority.NORMAL


def test_memory_entry_accepts_explicit_priority():
    entry = MemoryEntry(
        key="k", scope=MemoryScope.EDUCATION, memory_type=MemoryType.LONG_TERM,
        value="lesson", priority=MemoryPriority.HIGH,
    )
    assert entry.priority is MemoryPriority.HIGH


def test_memory_entry_is_frozen():
    entry = MemoryEntry(key="k", scope=MemoryScope.MARKET, memory_type=MemoryType.SHORT_TERM, value=1)
    try:
        entry.value = "mutated"
        assert False, "MemoryEntry should be frozen"
    except AttributeError:
        pass


def test_memory_scope_has_the_six_brief_named_categories():
    expected = {
        "CONVERSATION", "MARKET", "EDUCATION",
        "USER_PREFERENCE", "EXPLANATION_HISTORY", "KNOWLEDGE_REFERENCE",
    }
    assert {scope.value for scope in MemoryScope} == expected


def test_memory_type_has_short_term_and_long_term():
    assert {t.value for t in MemoryType} == {"SHORT_TERM", "LONG_TERM"}


def test_memory_priority_has_three_levels():
    assert {p.value for p in MemoryPriority} == {"LOW", "NORMAL", "HIGH"}
