from ai_layer.ai_engine.strategy.memory_adapter import strategy_reference_key
from ai_layer.ai_engine.strategy.models import StrategyRecord, StrategyType


def _record(**overrides):
    defaults = dict(
        strategy_id="s1", strategy_name="Liquidity Sweep", strategy_type=StrategyType.LIQUIDITY_SWEEP,
    )
    defaults.update(overrides)
    return StrategyRecord(**defaults)


def test_strategy_reference_key_includes_strategy_id():
    key = strategy_reference_key(_record(strategy_id="s_123"))
    assert "s_123" in key


def test_strategy_reference_key_has_strategy_prefix():
    key = strategy_reference_key(_record())
    assert key.startswith("strategy:")


def test_strategy_reference_key_is_deterministic():
    record = _record()
    assert strategy_reference_key(record) == strategy_reference_key(record)


def test_strategy_reference_key_different_for_different_records():
    key_a = strategy_reference_key(_record(strategy_id="s1"))
    key_b = strategy_reference_key(_record(strategy_id="s2"))
    assert key_a != key_b


def test_strategy_reference_key_returns_string():
    assert isinstance(strategy_reference_key(_record()), str)


def test_strategy_reference_key_never_raises_for_minimal_record():
    minimal = StrategyRecord(strategy_id="s", strategy_name="n", strategy_type=StrategyType.CUSTOM)
    assert strategy_reference_key(minimal) == "strategy:s"
