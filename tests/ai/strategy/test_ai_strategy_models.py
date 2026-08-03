import dataclasses

from ai_layer.ai_engine.strategy.models import (
    StrategyConfidence,
    StrategyRecord,
    StrategyStatus,
    StrategyType,
    generate_strategy_id,
)


def _record(**overrides):
    defaults = dict(
        strategy_id="s1", strategy_name="Liquidity Sweep", strategy_type=StrategyType.LIQUIDITY_SWEEP,
    )
    defaults.update(overrides)
    return StrategyRecord(**defaults)


def test_strategy_type_has_eight_members():
    assert len(list(StrategyType)) == 8


def test_strategy_type_members():
    values = {m.value for m in StrategyType}
    assert values == {
        "LIQUIDITY_SWEEP", "FVG", "AMD", "TREND_BREAKOUT", "ORDER_BLOCK",
        "WYCKOFF", "SMC", "CUSTOM",
    }


def test_strategy_status_has_four_members():
    assert len(list(StrategyStatus)) == 4


def test_strategy_status_members():
    values = {m.value for m in StrategyStatus}
    assert values == {"ACTIVE", "TESTING", "DISABLED", "ARCHIVED"}


def test_strategy_confidence_has_four_members():
    assert len(list(StrategyConfidence)) == 4


def test_strategy_confidence_members():
    values = {m.value for m in StrategyConfidence}
    assert values == {"LOW", "MEDIUM", "HIGH", "VERY_HIGH"}


def test_strategy_record_defaults():
    record = _record()
    assert record.strategy_version is None
    assert record.confidence is None
    assert record.notes is None
    assert record.status == StrategyStatus.TESTING
    assert record.created_at == ""


def test_strategy_record_is_frozen():
    record = _record()
    try:
        record.strategy_name = "someone_else"
        assert False, "expected FrozenInstanceError"
    except dataclasses.FrozenInstanceError:
        pass


def test_strategy_record_accepts_all_fields():
    record = _record(
        strategy_version="v2", confidence="HIGH", notes="works well in London session",
        status=StrategyStatus.ACTIVE, created_at="2026-01-01T00:00:00Z",
    )
    assert record.strategy_version == "v2"
    assert record.confidence == "HIGH"
    assert record.notes == "works well in London session"
    assert record.status == StrategyStatus.ACTIVE
    assert record.created_at == "2026-01-01T00:00:00Z"


def test_strategy_record_field_names_match_task_2_contract():
    field_names = {f.name for f in dataclasses.fields(StrategyRecord)}
    assert field_names == {
        "strategy_id", "strategy_name", "strategy_type", "strategy_version",
        "confidence", "notes", "status", "created_at",
    }


def test_strategy_record_strategy_id_name_type_required():
    field_by_name = {f.name: f for f in dataclasses.fields(StrategyRecord)}
    for required in ("strategy_id", "strategy_name", "strategy_type"):
        assert field_by_name[required].default is dataclasses.MISSING


def test_strategy_record_has_no_trading_core_object_fields():
    field_names = {f.name for f in dataclasses.fields(StrategyRecord)}
    forbidden = {"trade_decision", "risk_result", "signal_candidate", "decision", "risk", "execution"}
    assert field_names.isdisjoint(forbidden)


def test_strategy_record_never_carries_a_verdict_field():
    field_names = {f.name for f in dataclasses.fields(StrategyRecord)}
    forbidden = {"signal", "verdict", "direction", "buy_sell", "trade_decision"}
    assert field_names.isdisjoint(forbidden)


def test_strategy_record_never_carries_a_performance_field():
    field_names = {f.name for f in dataclasses.fields(StrategyRecord)}
    forbidden = {"win_rate", "profit", "sharpe", "drawdown", "risk_amount"}
    assert field_names.isdisjoint(forbidden)


def test_strategy_record_relays_strategy_type_never_infers():
    for strategy_type in StrategyType:
        record = _record(strategy_type=strategy_type)
        assert record.strategy_type == strategy_type


def test_strategy_record_relays_status_never_computes():
    for status in StrategyStatus:
        record = _record(status=status)
        assert record.status == status


def test_strategy_record_notes_relayed_verbatim():
    record = _record(notes="exact text supplied by caller")
    assert record.notes == "exact text supplied by caller"


def test_strategy_record_confidence_relayed_verbatim():
    record = _record(confidence="exact confidence supplied by caller")
    assert record.confidence == "exact confidence supplied by caller"


def test_strategy_record_equality():
    a = _record()
    b = _record()
    assert a == b


def test_strategy_record_inequality_on_strategy_id():
    a = _record(strategy_id="s1")
    b = _record(strategy_id="s2")
    assert a != b


def test_strategy_record_status_defaults_testing_not_archived():
    record = _record()
    assert record.status == StrategyStatus.TESTING


def test_generate_strategy_id_returns_string():
    strategy_id = generate_strategy_id()
    assert isinstance(strategy_id, str)
    assert strategy_id != ""


def test_generate_strategy_id_unique():
    ids = {generate_strategy_id() for _ in range(20)}
    assert len(ids) == 20


def test_strategy_status_and_trading_core_strategy_status_are_distinct_enums():
    """docs/PHASE66_6_AUDIT.md: ai.strategy.models.StrategyStatus is not the same enum as strategy_layer.strategy_manager.lifecycle.strategy_status.StrategyStatus (import forbidden, different value sets)."""
    from strategy_layer.strategy_manager.lifecycle.strategy_status import StrategyStatus as TradingCoreStrategyStatus

    assert StrategyStatus is not TradingCoreStrategyStatus
    assert set(StrategyStatus) != set(TradingCoreStrategyStatus)


def test_strategy_record_has_no_trading_core_object_field_type():
    """Belt-and-suspenders: no dataclass field on StrategyRecord may be typed as a Trading Core object -- every field is a primitive/enum/Optional only."""
    allowed_type_fragments = ("str", "StrategyType", "StrategyStatus", "Optional")
    for f in dataclasses.fields(StrategyRecord):
        type_str = str(f.type)
        assert any(fragment in type_str for fragment in allowed_type_fragments), f"StrategyRecord.{f.name}: {type_str}"
