"""Phase 61.3 TASK 6 — Memory Runtime: thin facade over five namespaced ContextMemory instances."""

from ai.memory.memory_runtime import MemoryLayer, MemoryRuntime


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
