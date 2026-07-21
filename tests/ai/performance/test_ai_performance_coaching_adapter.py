from ai.performance.coaching_adapter import performance_record_to_coaching_input
from ai.performance.models import PerformanceRecord


def _record(**overrides):
    defaults = dict(id="p1", user_id="user_1", trade_id="trade_1")
    defaults.update(overrides)
    return PerformanceRecord(**defaults)


def test_maps_user_id_directly():
    mapped = performance_record_to_coaching_input(_record(user_id="u42"))
    assert mapped["user_id"] == "u42"


def test_maps_notes_to_message():
    mapped = performance_record_to_coaching_input(_record(notes="review your risk plan"))
    assert mapped["message"] == "review your risk plan"


def test_falls_back_to_empty_string_when_no_notes():
    mapped = performance_record_to_coaching_input(_record(notes=None))
    assert mapped["message"] == ""


def test_maps_journal_id_directly():
    mapped = performance_record_to_coaching_input(_record(journal_id="j99"))
    assert mapped["journal_id"] == "j99"


def test_maps_trade_id_direction_result_into_metadata():
    mapped = performance_record_to_coaching_input(
        _record(trade_id="t1", direction="SELL", result="LOSS")
    )
    assert mapped["metadata"] == {"trade_id": "t1", "direction": "SELL", "result": "LOSS"}


def test_metadata_defaults_direction_and_result_to_empty_string():
    mapped = performance_record_to_coaching_input(_record(direction=None, result=None))
    assert mapped["metadata"]["direction"] == ""
    assert mapped["metadata"]["result"] == ""


def test_never_returns_topic_priority_type_or_recommendation():
    """The adapter cannot infer topic from a PerformanceRecord without real AI inference -- a caller supplies it."""
    mapped = performance_record_to_coaching_input(_record())
    assert "topic" not in mapped
    assert "priority" not in mapped
    assert "type" not in mapped
    assert "recommendation" not in mapped


def test_never_raises_for_minimal_record():
    minimal = PerformanceRecord(id="p", user_id="u", trade_id="t")
    mapped = performance_record_to_coaching_input(minimal)
    assert mapped["user_id"] == "u"
    assert mapped["message"] == ""


def test_returns_a_plain_dict():
    mapped = performance_record_to_coaching_input(_record())
    assert isinstance(mapped, dict)


def test_mapping_is_deterministic():
    record = _record()
    assert performance_record_to_coaching_input(record) == performance_record_to_coaching_input(record)


def test_mapping_never_mutates_the_record():
    record = _record(notes="original notes")
    performance_record_to_coaching_input(record)
    assert record.notes == "original notes"


def test_different_records_produce_independent_mappings():
    mapped_a = performance_record_to_coaching_input(_record(user_id="u1"))
    mapped_b = performance_record_to_coaching_input(_record(user_id="u2"))
    assert mapped_a["user_id"] != mapped_b["user_id"]
