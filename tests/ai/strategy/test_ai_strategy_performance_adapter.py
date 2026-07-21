from ai.performance.models import PerformanceRecord
from ai.strategy.performance_adapter import performance_record_to_strategy_input


def _record(**overrides):
    defaults = dict(id="p1", user_id="user_1", trade_id="trade_1")
    defaults.update(overrides)
    return PerformanceRecord(**defaults)


def test_maps_confidence_score_to_confidence():
    mapped = performance_record_to_strategy_input(_record(confidence_score=0.83))
    assert mapped["confidence"] == 0.83


def test_maps_notes_directly():
    mapped = performance_record_to_strategy_input(_record(notes="strong entry quality"))
    assert mapped["notes"] == "strong entry quality"


def test_none_confidence_relayed_as_none():
    mapped = performance_record_to_strategy_input(_record(confidence_score=None))
    assert mapped["confidence"] is None


def test_none_notes_relayed_as_none():
    mapped = performance_record_to_strategy_input(_record(notes=None))
    assert mapped["notes"] is None


def test_never_returns_strategy_name_type_or_version():
    """The adapter cannot infer strategy identity from a PerformanceRecord without real inference -- a caller supplies it."""
    mapped = performance_record_to_strategy_input(_record())
    assert "strategy_name" not in mapped
    assert "strategy_type" not in mapped
    assert "strategy_version" not in mapped


def test_never_returns_status():
    mapped = performance_record_to_strategy_input(_record())
    assert "status" not in mapped


def test_never_raises_for_minimal_record():
    minimal = PerformanceRecord(id="p", user_id="u", trade_id="t")
    mapped = performance_record_to_strategy_input(minimal)
    assert mapped["confidence"] is None
    assert mapped["notes"] is None


def test_returns_a_plain_dict():
    mapped = performance_record_to_strategy_input(_record())
    assert isinstance(mapped, dict)


def test_mapping_is_deterministic():
    record = _record()
    assert performance_record_to_strategy_input(record) == performance_record_to_strategy_input(record)


def test_mapping_never_mutates_the_record():
    record = _record(notes="original notes")
    performance_record_to_strategy_input(record)
    assert record.notes == "original notes"


def test_different_records_produce_independent_mappings():
    mapped_a = performance_record_to_strategy_input(_record(notes="a"))
    mapped_b = performance_record_to_strategy_input(_record(notes="b"))
    assert mapped_a["notes"] != mapped_b["notes"]
