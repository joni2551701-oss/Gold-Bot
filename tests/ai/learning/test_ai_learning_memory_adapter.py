from ai_layer.knowledge_ai.learning_engine.memory_adapter import memory_reference_key
from ai_layer.knowledge_ai.learning_engine.models import LearningRecord, LearningTopic


def _record(**overrides):
    defaults = dict(id="record_123", user_id="user_1", topic=LearningTopic.DISCIPLINE)
    defaults.update(overrides)
    return LearningRecord(**defaults)


def test_memory_reference_key_includes_record_id():
    key = memory_reference_key(_record(id="record_123"))
    assert "record_123" in key


def test_memory_reference_key_has_learning_prefix():
    key = memory_reference_key(_record())
    assert key.startswith("learning:")


def test_memory_reference_key_is_deterministic():
    record = _record()
    assert memory_reference_key(record) == memory_reference_key(record)


def test_memory_reference_key_different_for_different_records():
    key_a = memory_reference_key(_record(id="r1"))
    key_b = memory_reference_key(_record(id="r2"))
    assert key_a != key_b


def test_memory_reference_key_returns_string():
    assert isinstance(memory_reference_key(_record()), str)


def test_memory_reference_key_never_raises_for_minimal_record():
    minimal = LearningRecord(id="r", user_id="u", topic=LearningTopic.RISK)
    assert memory_reference_key(minimal) == "learning:r"
