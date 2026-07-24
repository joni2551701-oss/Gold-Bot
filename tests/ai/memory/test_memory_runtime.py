"""Phase 61.3 TASK 6 — Memory Runtime: thin facade over five namespaced ContextMemory instances. Extended Phase 63.3 TASK 4 with a structured MemoryEntry surface (store/recall/search/filter/list_all/short_term/long_term/forget)."""

from ai.memory.memory_runtime import MemoryLayer, MemoryRuntime
from ai.memory.models import MemoryEntry, MemoryScope, MemoryType


def test_save_and_load_round_trips_within_a_layer():
    runtime = MemoryRuntime()
    runtime.save(MemoryLayer.CONVERSATION, "session-1", {"turns": 3})
    assert runtime.load(MemoryLayer.CONVERSATION, "session-1") == {"turns": 3}


def test_load_missing_key_returns_none():
    runtime = MemoryRuntime()
    assert runtime.load(MemoryLayer.USER, "unknown") is None


def test_same_key_in_different_layers_does_not_collide():
    runtime = MemoryRuntime()
    runtime.save(MemoryLayer.USER, "12345", "user-value")
    runtime.save(MemoryLayer.TRADE, "12345", "trade-value")

    assert runtime.load(MemoryLayer.USER, "12345") == "user-value"
    assert runtime.load(MemoryLayer.TRADE, "12345") == "trade-value"


def test_clear_one_key_within_a_layer():
    runtime = MemoryRuntime()
    runtime.save(MemoryLayer.LEARNING, "a", 1)
    runtime.save(MemoryLayer.LEARNING, "b", 2)

    runtime.clear(MemoryLayer.LEARNING, "a")

    assert runtime.load(MemoryLayer.LEARNING, "a") is None
    assert runtime.load(MemoryLayer.LEARNING, "b") == 2


def test_clear_without_key_clears_only_that_layer():
    runtime = MemoryRuntime()
    runtime.save(MemoryLayer.MARKET, "a", 1)
    runtime.save(MemoryLayer.USER, "a", 2)

    runtime.clear(MemoryLayer.MARKET)

    assert runtime.load(MemoryLayer.MARKET, "a") is None
    assert runtime.load(MemoryLayer.USER, "a") == 2


def test_clear_all_clears_every_layer():
    runtime = MemoryRuntime()
    for layer in MemoryLayer:
        runtime.save(layer, "k", "v")

    runtime.clear_all()

    for layer in MemoryLayer:
        assert runtime.load(layer, "k") is None


def test_every_memory_layer_has_its_own_context_memory_instance():
    runtime = MemoryRuntime()
    assert len(runtime._layers) == len(MemoryLayer)
    assert len(set(id(m) for m in runtime._layers.values())) == len(MemoryLayer)


def _entry(key="e1", scope=MemoryScope.MARKET, memory_type=MemoryType.SHORT_TERM, value=1):
    return MemoryEntry(key=key, scope=scope, memory_type=memory_type, value=value)


def test_store_and_recall_round_trips():
    runtime = MemoryRuntime()
    entry = _entry()
    runtime.store(entry)
    assert runtime.recall("e1") == entry


def test_recall_missing_key_returns_none():
    runtime = MemoryRuntime()
    assert runtime.recall("does-not-exist") is None


def test_store_overwrites_an_existing_key():
    runtime = MemoryRuntime()
    runtime.store(_entry(value=1))
    runtime.store(_entry(value=2))
    assert runtime.recall("e1").value == 2


def test_search_matches_key_case_insensitively():
    runtime = MemoryRuntime()
    runtime.store(_entry(key="market.gold.trend"))
    assert len(runtime.search("GOLD")) == 1
    assert runtime.search("").__len__() == 0


def test_filter_applies_arbitrary_predicate():
    runtime = MemoryRuntime()
    runtime.store(_entry(key="a", scope=MemoryScope.EDUCATION))
    runtime.store(_entry(key="b", scope=MemoryScope.MARKET))
    result = runtime.filter(lambda e: e.scope is MemoryScope.EDUCATION)
    assert [e.key for e in result] == ["a"]


def test_list_all_returns_every_stored_entry():
    runtime = MemoryRuntime()
    runtime.store(_entry(key="a"))
    runtime.store(_entry(key="b"))
    assert {e.key for e in runtime.list_all()} == {"a", "b"}


def test_short_term_and_long_term_split_by_memory_type():
    runtime = MemoryRuntime()
    runtime.store(_entry(key="s", memory_type=MemoryType.SHORT_TERM))
    runtime.store(_entry(key="l", memory_type=MemoryType.LONG_TERM))
    assert [e.key for e in runtime.short_term()] == ["s"]
    assert [e.key for e in runtime.long_term()] == ["l"]


def test_forget_removes_one_entry_and_is_a_no_op_for_unknown_key():
    runtime = MemoryRuntime()
    runtime.store(_entry(key="a"))
    runtime.store(_entry(key="b"))
    runtime.forget("a")
    assert runtime.recall("a") is None
    assert runtime.recall("b") is not None
    runtime.forget("does-not-exist")  # never raises


def test_structured_entries_are_isolated_from_the_original_layer_store():
    """Phase 63.3's store()/recall() never touches Phase 61.3's save()/load() -- two separate internal dicts on the same instance."""
    runtime = MemoryRuntime()
    runtime.save(MemoryLayer.MARKET, "shared-key", "layer-value")
    runtime.store(_entry(key="shared-key", value="entry-value"))

    assert runtime.load(MemoryLayer.MARKET, "shared-key") == "layer-value"
    assert runtime.recall("shared-key").value == "entry-value"


def test_memory_runtime_never_imports_trading_layers():
    """ai/memory/ stays pure foundation even with the Phase 63.3 extension -- no dependency on decision/risk/execution/strategies/database/telegram."""
    import ast
    import pathlib

    memory_dir = pathlib.Path(__file__).resolve().parents[3] / "ai" / "memory"
    forbidden_prefixes = ("decision", "risk", "execution", "strategies", "database", "telegram")

    for py_file in memory_dir.glob("*.py"):
        tree = ast.parse(py_file.read_text(), filename=str(py_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith(forbidden_prefixes), f"{py_file}: {alias.name}"
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    assert not node.module.startswith(forbidden_prefixes), f"{py_file}: {node.module}"
