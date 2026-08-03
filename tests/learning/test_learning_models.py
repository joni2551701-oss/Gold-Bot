"""
Phase 60.6: Learning Loop Foundation, TASK 2 -- ai_layer/knowledge_ai/learning_loop/models.py
tests.
"""

from datetime import datetime, timezone

from ai_layer.knowledge_ai.learning_loop.models import LEARNING_ENGINE_VERSION, LearningRecord, create_learning_record, generate_learning_record_id


def test_create_learning_record_stamps_identity_and_timestamp():
    record = create_learning_record(trade_id="t1", signal_id="s1")

    assert isinstance(record, LearningRecord)
    assert record.trade_id == "t1"
    assert record.signal_id == "s1"
    assert record.record_id
    assert record.created_at is not None


def test_create_learning_record_matches_the_directors_own_worked_example():
    record = create_learning_record(
        trade_id="t1", signal_id="s1", strategy_name="Liquidity Sweep",
        market_phase="DISTRIBUTION", session="London", result="LOSS", failure_type="No HTF confirmation",
    )

    assert record.strategy_name == "Liquidity Sweep"
    assert record.market_phase == "DISTRIBUTION"
    assert record.session == "London"
    assert record.result == "LOSS"
    assert record.failure_type == "No HTF confirmation"
    assert record.success_pattern is None


def test_success_pattern_and_failure_type_are_independent():
    win = create_learning_record(trade_id="t1", signal_id="s1", success_pattern="HTF aligned + OB reaction")

    assert win.success_pattern == "HTF aligned + OB reaction"
    assert win.failure_type is None


def test_optional_fields_default_to_none():
    record = create_learning_record(trade_id="t1", signal_id="s1")

    assert record.strategy_name is None
    assert record.market_phase is None
    assert record.session is None
    assert record.timeframe is None
    assert record.result is None
    assert record.r_multiple is None
    assert record.failure_type is None
    assert record.success_pattern is None


def test_generate_learning_record_id_returns_uuid_shaped_string():
    value = generate_learning_record_id()

    assert isinstance(value, str)
    assert len(value) == 36


def test_record_id_is_unique_per_call():
    a = create_learning_record(trade_id="t1", signal_id="s1")
    b = create_learning_record(trade_id="t1", signal_id="s1")

    assert a.record_id != b.record_id


def test_record_is_frozen():
    record = create_learning_record(trade_id="t1", signal_id="s1")

    try:
        record.result = "TP"
        assert False, "LearningRecord must be immutable"
    except AttributeError:
        pass


def test_to_dict_is_json_safe():
    import json

    record = create_learning_record(trade_id="t1", signal_id="s1", r_multiple=2.0)
    data = record.to_dict()

    json.dumps(data)  # must not raise
    assert data["r_multiple"] == 2.0
    assert isinstance(data["created_at"], str)


def test_manual_construction_with_explicit_timestamp():
    ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
    record = LearningRecord(record_id="r1", trade_id="t1", signal_id="s1", created_at=ts)

    assert record.created_at == ts


# --- Phase 60.7 TASK 3: Enhanced Learning Schema (additive) ---

def test_engine_version_defaults_to_the_current_version():
    record = create_learning_record(trade_id="t1", signal_id="s1")

    assert record.engine_version == LEARNING_ENGINE_VERSION


def test_new_phase_607_fields_default_to_none_except_engine_version():
    record = create_learning_record(trade_id="t1", signal_id="s1")

    assert record.htf_bias is None
    assert record.volatility_state is None
    assert record.fundamental_bias is None
    assert record.confidence_score is None
    assert record.sample_size is None


def test_new_phase_607_fields_can_be_set_explicitly():
    record = create_learning_record(
        trade_id="t1", signal_id="s1", htf_bias="BULLISH", volatility_state="LOW_VOLATILITY",
        fundamental_bias="BULLISH GOLD", confidence_score=0.78, engine_version="60.8", sample_size=42,
    )

    assert record.htf_bias == "BULLISH"
    assert record.volatility_state == "LOW_VOLATILITY"
    assert record.fundamental_bias == "BULLISH GOLD"
    assert record.confidence_score == 0.78
    assert record.engine_version == "60.8"
    assert record.sample_size == 42


def test_phase_606_callers_are_unaffected_by_the_extension():
    """A Phase 60.6-shaped call (no new kwargs) must still work identically."""
    record = create_learning_record(
        trade_id="t1", signal_id="s1", strategy_name="A", result="TP", r_multiple=1.5,
    )

    assert record.strategy_name == "A"
    assert record.result == "TP"
    assert record.r_multiple == 1.5
    assert record.engine_version == LEARNING_ENGINE_VERSION


def test_never_generates_a_signal_or_decision():
    """Structural guard matching this whole phase's boundary: no signal/decision-shaped attribute anywhere on the module."""
    import ai_layer.knowledge_ai.learning_loop.models as module

    forbidden_terms = ("signal_", "decision", "approve", "reject")
    public_names = [name for name in dir(module) if not name.startswith("_")]
    for name in public_names:
        assert not any(term in name.lower() for term in forbidden_terms), name
