from ai.coaching.learning_adapter import learning_record_to_coaching_input
from ai.learning.models import LearningLevel, LearningRecord, LearningSource, LearningTopic


def _record(**overrides):
    defaults = dict(id="l1", user_id="user_1", topic=LearningTopic.RISK)
    defaults.update(overrides)
    return LearningRecord(**defaults)


def test_maps_user_id_directly():
    mapped = learning_record_to_coaching_input(_record(user_id="user_42"))
    assert mapped["user_id"] == "user_42"


def test_maps_learning_id_from_record_id():
    mapped = learning_record_to_coaching_input(_record(id="l99"))
    assert mapped["learning_id"] == "l99"


def test_relays_topic_directly_not_inferred():
    """Unlike journal_adapter, learning_adapter CAN relay topic -- LearningRecord already carries an explicit one."""
    for topic in LearningTopic:
        mapped = learning_record_to_coaching_input(_record(topic=topic))
        assert mapped["topic"] == topic


def test_maps_notes_to_message():
    mapped = learning_record_to_coaching_input(_record(notes="struggled with patience today"))
    assert mapped["message"] == "struggled with patience today"


def test_falls_back_to_empty_string_when_no_notes():
    mapped = learning_record_to_coaching_input(_record(notes=None))
    assert mapped["message"] == ""


def test_maps_level_and_source_into_metadata():
    mapped = learning_record_to_coaching_input(_record(level=LearningLevel.INTERMEDIATE, source=LearningSource.TRADE))
    assert mapped["metadata"] == {"level": "INTERMEDIATE", "source": "TRADE"}


def test_never_returns_priority_type_or_recommendation():
    mapped = learning_record_to_coaching_input(_record())
    assert "priority" not in mapped
    assert "type" not in mapped
    assert "recommendation" not in mapped


def test_never_returns_journal_id():
    mapped = learning_record_to_coaching_input(_record())
    assert "journal_id" not in mapped


def test_never_raises_for_minimal_record():
    minimal = LearningRecord(id="l", user_id="u", topic=LearningTopic.ENTRY)
    mapped = learning_record_to_coaching_input(minimal)
    assert mapped["user_id"] == "u"
    assert mapped["message"] == ""


def test_returns_a_plain_dict():
    mapped = learning_record_to_coaching_input(_record())
    assert isinstance(mapped, dict)


def test_mapping_is_deterministic():
    record = _record()
    assert learning_record_to_coaching_input(record) == learning_record_to_coaching_input(record)


def test_mapping_never_mutates_the_record():
    record = _record(notes="original note")
    learning_record_to_coaching_input(record)
    assert record.notes == "original note"


def test_different_records_produce_independent_mappings():
    mapped_a = learning_record_to_coaching_input(_record(user_id="u1"))
    mapped_b = learning_record_to_coaching_input(_record(user_id="u2"))
    assert mapped_a["user_id"] != mapped_b["user_id"]
