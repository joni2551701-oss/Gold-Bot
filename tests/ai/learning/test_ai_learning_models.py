import dataclasses

from ai_layer.knowledge_ai.learning_engine.models import (
    LearningLevel,
    LearningRecord,
    LearningSource,
    LearningStatus,
    LearningTopic,
    generate_learning_id,
)


def _record(**overrides):
    defaults = dict(id="r1", user_id="user_1", topic=LearningTopic.DISCIPLINE)
    defaults.update(overrides)
    return LearningRecord(**defaults)


def test_learning_topic_has_twelve_members():
    assert len(list(LearningTopic)) == 12


def test_learning_topic_members():
    values = {m.value for m in LearningTopic}
    assert values == {
        "DISCIPLINE", "ENTRY", "EXIT", "RISK", "PATIENCE", "STRUCTURE",
        "FVG", "OB", "LIQUIDITY", "TREND", "SESSION", "PSYCHOLOGY",
    }


def test_learning_level_has_five_members():
    assert len(list(LearningLevel)) == 5


def test_learning_level_members():
    values = {m.value for m in LearningLevel}
    assert values == {"UNKNOWN", "BEGINNER", "INTERMEDIATE", "ADVANCED", "MASTERED"}


def test_learning_source_has_five_members():
    assert len(list(LearningSource)) == 5


def test_learning_source_members():
    values = {m.value for m in LearningSource}
    assert values == {"TRADE", "JOURNAL", "CHART", "MANUAL", "SIMULATION"}


def test_learning_status_has_three_members():
    assert len(list(LearningStatus)) == 3


def test_learning_status_members():
    values = {m.value for m in LearningStatus}
    assert values == {"ACTIVE", "ARCHIVED", "PENDING"}


def test_learning_record_defaults():
    record = _record()
    assert record.level == LearningLevel.UNKNOWN
    assert record.confidence is None
    assert record.notes is None
    assert record.source == LearningSource.MANUAL
    assert record.status == LearningStatus.ACTIVE
    assert record.created_at == ""


def test_learning_record_is_frozen():
    record = _record()
    try:
        record.user_id = "someone_else"
        assert False, "expected FrozenInstanceError"
    except dataclasses.FrozenInstanceError:
        pass


def test_learning_record_accepts_all_fields():
    record = _record(
        level=LearningLevel.ADVANCED, confidence=0.9, notes="strong discipline today",
        source=LearningSource.TRADE, status=LearningStatus.PENDING, created_at="2026-01-01T00:00:00Z",
    )
    assert record.level == LearningLevel.ADVANCED
    assert record.confidence == 0.9
    assert record.notes == "strong discipline today"
    assert record.source == LearningSource.TRADE
    assert record.status == LearningStatus.PENDING
    assert record.created_at == "2026-01-01T00:00:00Z"


def test_learning_record_field_names_match_task_2_and_task_7_contract():
    field_names = {f.name for f in dataclasses.fields(LearningRecord)}
    assert field_names == {
        "id", "user_id", "topic", "level", "confidence", "notes",
        "source", "status", "created_at",
    }


def test_learning_record_id_and_user_id_and_topic_required():
    field_by_name = {f.name: f for f in dataclasses.fields(LearningRecord)}
    for required in ("id", "user_id", "topic"):
        assert field_by_name[required].default is dataclasses.MISSING


def test_learning_record_has_no_trading_core_object_fields():
    field_names = {f.name for f in dataclasses.fields(LearningRecord)}
    forbidden = {"trade_decision", "risk_result", "signal_candidate", "decision", "risk", "execution"}
    assert field_names.isdisjoint(forbidden)


def test_learning_record_relays_topic_never_infers():
    for topic in LearningTopic:
        record = _record(topic=topic)
        assert record.topic == topic


def test_learning_record_relays_level_never_grades():
    """Rule 6/7: level is always exactly what the caller supplied."""
    for level in LearningLevel:
        record = _record(level=level)
        assert record.level == level


def test_learning_record_confidence_relayed_as_is_no_scale_conversion():
    record = _record(confidence=82.0)
    assert record.confidence == 82.0
    record2 = _record(confidence=0.82)
    assert record2.confidence == 0.82


def test_learning_record_equality():
    a = _record()
    b = _record()
    assert a == b


def test_learning_record_inequality_on_id():
    a = _record(id="r1")
    b = _record(id="r2")
    assert a != b


def test_generate_learning_id_returns_string():
    record_id = generate_learning_id()
    assert isinstance(record_id, str)
    assert record_id != ""


def test_generate_learning_id_unique():
    ids = {generate_learning_id() for _ in range(20)}
    assert len(ids) == 20


def test_learning_topic_and_knowledge_category_are_distinct_enums():
    """docs/PHASE66_3_AUDIT.md: LearningTopic is not a duplicate of knowledge.models.KnowledgeCategory despite some name overlap (RISK, PSYCHOLOGY)."""
    from ai_layer.knowledge_ai.knowledge_base.models import KnowledgeCategory

    assert LearningTopic is not KnowledgeCategory
    assert set(LearningTopic) != set(KnowledgeCategory)


def test_learning_record_never_carries_a_verdict_field():
    """Rule 6: no win_rate/profit/performance field of any kind."""
    field_names = {f.name for f in dataclasses.fields(LearningRecord)}
    forbidden = {"win_rate", "profit", "sharpe", "drawdown", "performance"}
    assert field_names.isdisjoint(forbidden)


def test_learning_record_status_defaults_active_not_archived():
    record = _record()
    assert record.status == LearningStatus.ACTIVE
