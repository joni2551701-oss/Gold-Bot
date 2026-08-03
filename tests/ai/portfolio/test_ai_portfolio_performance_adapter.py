from ai_layer.ai_engine.performance.models import PerformanceRecord
from ai_layer.ai_engine.portfolio.performance_adapter import performance_record_to_portfolio_input


def _record(**overrides):
    defaults = dict(id="p1", user_id="user_1", trade_id="trade_1")
    defaults.update(overrides)
    return PerformanceRecord(**defaults)


def test_maps_notes_directly():
    mapped = performance_record_to_portfolio_input(_record(notes="strong quarter"))
    assert mapped["notes"] == "strong quarter"


def test_none_notes_relayed_as_none():
    mapped = performance_record_to_portfolio_input(_record(notes=None))
    assert mapped["notes"] is None


def test_never_returns_portfolio_name_status_risk_level_health():
    """The adapter cannot infer portfolio identity/state from a PerformanceRecord without real inference -- a caller supplies it."""
    mapped = performance_record_to_portfolio_input(_record())
    assert "portfolio_name" not in mapped
    assert "status" not in mapped
    assert "risk_level" not in mapped
    assert "health" not in mapped


def test_never_returns_strategy_counts():
    mapped = performance_record_to_portfolio_input(_record())
    assert "strategy_count" not in mapped
    assert "active_strategy_count" not in mapped


def test_never_raises_for_minimal_record():
    minimal = PerformanceRecord(id="p", user_id="u", trade_id="t")
    mapped = performance_record_to_portfolio_input(minimal)
    assert mapped["notes"] is None


def test_returns_a_plain_dict():
    mapped = performance_record_to_portfolio_input(_record())
    assert isinstance(mapped, dict)


def test_mapping_is_deterministic():
    record = _record()
    assert performance_record_to_portfolio_input(record) == performance_record_to_portfolio_input(record)


def test_mapping_never_mutates_the_record():
    record = _record(notes="original notes")
    performance_record_to_portfolio_input(record)
    assert record.notes == "original notes"


def test_different_records_produce_independent_mappings():
    mapped_a = performance_record_to_portfolio_input(_record(notes="a"))
    mapped_b = performance_record_to_portfolio_input(_record(notes="b"))
    assert mapped_a["notes"] != mapped_b["notes"]
