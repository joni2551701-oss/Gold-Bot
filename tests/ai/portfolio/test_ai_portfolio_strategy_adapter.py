from ai.portfolio.strategy_adapter import strategy_records_to_portfolio_input
from ai.strategy.models import StrategyRecord, StrategyStatus, StrategyType


def _record(**overrides):
    defaults = dict(
        strategy_id="s1", strategy_name="Liquidity Sweep", strategy_type=StrategyType.LIQUIDITY_SWEEP,
    )
    defaults.update(overrides)
    return StrategyRecord(**defaults)


def test_empty_sequence_produces_zero_counts_not_an_exception():
    mapped = strategy_records_to_portfolio_input([])
    assert mapped["strategy_count"] == 0
    assert mapped["active_strategy_count"] == 0


def test_strategy_count_equals_total_records():
    records = [_record(strategy_id="s1"), _record(strategy_id="s2"), _record(strategy_id="s3")]
    mapped = strategy_records_to_portfolio_input(records)
    assert mapped["strategy_count"] == 3


def test_active_strategy_count_only_counts_active_status():
    records = [
        _record(strategy_id="s1", status=StrategyStatus.ACTIVE),
        _record(strategy_id="s2", status=StrategyStatus.ACTIVE),
        _record(strategy_id="s3", status=StrategyStatus.TESTING),
        _record(strategy_id="s4", status=StrategyStatus.DISABLED),
        _record(strategy_id="s5", status=StrategyStatus.ARCHIVED),
    ]
    mapped = strategy_records_to_portfolio_input(records)
    assert mapped["strategy_count"] == 5
    assert mapped["active_strategy_count"] == 2


def test_all_active_records():
    records = [_record(strategy_id="s1", status=StrategyStatus.ACTIVE), _record(strategy_id="s2", status=StrategyStatus.ACTIVE)]
    mapped = strategy_records_to_portfolio_input(records)
    assert mapped["active_strategy_count"] == mapped["strategy_count"]


def test_no_active_records():
    records = [_record(strategy_id="s1", status=StrategyStatus.TESTING)]
    mapped = strategy_records_to_portfolio_input(records)
    assert mapped["active_strategy_count"] == 0


def test_never_returns_notes():
    """With multiple source records, no single canonical note exists to relay without arbitrary selection."""
    mapped = strategy_records_to_portfolio_input([_record(notes="some note")])
    assert "notes" not in mapped


def test_never_returns_portfolio_name_status_risk_level_health():
    mapped = strategy_records_to_portfolio_input([_record()])
    assert "portfolio_name" not in mapped
    assert "status" not in mapped
    assert "risk_level" not in mapped
    assert "health" not in mapped


def test_returns_a_plain_dict():
    mapped = strategy_records_to_portfolio_input([_record()])
    assert isinstance(mapped, dict)


def test_mapping_is_deterministic():
    records = [_record(strategy_id="s1"), _record(strategy_id="s2", status=StrategyStatus.ACTIVE)]
    assert strategy_records_to_portfolio_input(records) == strategy_records_to_portfolio_input(records)


def test_mapping_never_mutates_input_records():
    records = [_record(strategy_id="s1", status=StrategyStatus.ACTIVE)]
    strategy_records_to_portfolio_input(records)
    assert records[0].status == StrategyStatus.ACTIVE


def test_different_sequences_produce_independent_mappings():
    mapped_a = strategy_records_to_portfolio_input([_record(strategy_id="s1")])
    mapped_b = strategy_records_to_portfolio_input([_record(strategy_id="s1"), _record(strategy_id="s2")])
    assert mapped_a["strategy_count"] != mapped_b["strategy_count"]
