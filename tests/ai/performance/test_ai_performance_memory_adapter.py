from ai.performance.memory_adapter import performance_memory_key
from ai.performance.models import PerformanceRecord


def _record(**overrides):
    defaults = dict(id="p1", user_id="user_1", trade_id="trade_1")
    defaults.update(overrides)
    return PerformanceRecord(**defaults)


def test_performance_memory_key_includes_id():
    key = performance_memory_key(_record(id="p_123"))
    assert "p_123" in key


def test_performance_memory_key_includes_user_id():
    key = performance_memory_key(_record(user_id="user_99"))
    assert "user_99" in key


def test_performance_memory_key_has_performance_prefix():
    key = performance_memory_key(_record())
    assert key.startswith("performance:")


def test_performance_memory_key_is_deterministic():
    record = _record()
    assert performance_memory_key(record) == performance_memory_key(record)


def test_performance_memory_key_different_for_different_records():
    key_a = performance_memory_key(_record(id="p1"))
    key_b = performance_memory_key(_record(id="p2"))
    assert key_a != key_b


def test_performance_memory_key_returns_string():
    assert isinstance(performance_memory_key(_record()), str)


def test_performance_memory_key_never_raises_for_minimal_record():
    minimal = PerformanceRecord(id="p", user_id="u", trade_id="t")
    assert performance_memory_key(minimal) == "performance:u:p"
