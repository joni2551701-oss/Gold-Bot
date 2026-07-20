import dataclasses

from ai.coaching.models import (
    CoachingPriority,
    CoachingRecommendation,
    CoachingStatus,
    CoachingTopic,
    CoachingType,
    generate_coach_id,
)


def _record(**overrides):
    defaults = dict(coach_id="c1", user_id="user_1", topic=CoachingTopic.DISCIPLINE, message="stay disciplined")
    defaults.update(overrides)
    return CoachingRecommendation(**defaults)


def test_coaching_topic_has_twelve_members():
    assert len(list(CoachingTopic)) == 12


def test_coaching_topic_members():
    values = {m.value for m in CoachingTopic}
    assert values == {
        "DISCIPLINE", "ENTRY", "EXIT", "RISK", "PATIENCE", "STRUCTURE",
        "FVG", "OB", "LIQUIDITY", "TREND", "SESSION", "PSYCHOLOGY",
    }


def test_coaching_priority_has_four_members():
    assert len(list(CoachingPriority)) == 4


def test_coaching_priority_members():
    values = {m.value for m in CoachingPriority}
    assert values == {"LOW", "MEDIUM", "HIGH", "CRITICAL"}


def test_coaching_type_has_five_members():
    assert len(list(CoachingType)) == 5


def test_coaching_type_members():
    values = {m.value for m in CoachingType}
    assert values == {"FEEDBACK", "RECOMMENDATION", "WARNING", "MOTIVATION", "REMINDER"}


def test_coaching_status_has_four_members():
    assert len(list(CoachingStatus)) == 4


def test_coaching_status_members():
    values = {m.value for m in CoachingStatus}
    assert values == {"PENDING", "ACTIVE", "ACKNOWLEDGED", "ARCHIVED"}


def test_coaching_recommendation_defaults():
    record = _record()
    assert record.learning_id is None
    assert record.journal_id is None
    assert record.priority == CoachingPriority.MEDIUM
    assert record.type == CoachingType.RECOMMENDATION
    assert record.recommendation is None
    assert record.status == CoachingStatus.PENDING
    assert record.created_at == ""
    assert record.metadata == {}


def test_coaching_recommendation_is_frozen():
    record = _record()
    try:
        record.user_id = "someone_else"
        assert False, "expected FrozenInstanceError"
    except dataclasses.FrozenInstanceError:
        pass


def test_coaching_recommendation_accepts_all_fields():
    record = _record(
        learning_id="l1", journal_id="j1", priority=CoachingPriority.HIGH,
        type=CoachingType.WARNING, recommendation="review your risk plan",
        status=CoachingStatus.ACTIVE, created_at="2026-01-01T00:00:00Z",
        metadata={"session": "London"},
    )
    assert record.learning_id == "l1"
    assert record.journal_id == "j1"
    assert record.priority == CoachingPriority.HIGH
    assert record.type == CoachingType.WARNING
    assert record.recommendation == "review your risk plan"
    assert record.status == CoachingStatus.ACTIVE
    assert record.created_at == "2026-01-01T00:00:00Z"
    assert record.metadata == {"session": "London"}


def test_coaching_recommendation_field_names_match_task_2_contract():
    field_names = {f.name for f in dataclasses.fields(CoachingRecommendation)}
    assert field_names == {
        "coach_id", "user_id", "learning_id", "journal_id", "topic",
        "priority", "type", "message", "recommendation", "status",
        "created_at", "metadata",
    }


def test_coaching_recommendation_coach_id_user_id_topic_message_required():
    field_by_name = {f.name: f for f in dataclasses.fields(CoachingRecommendation)}
    for required in ("coach_id", "user_id", "topic", "message"):
        assert field_by_name[required].default is dataclasses.MISSING


def test_coaching_recommendation_has_no_trading_core_object_fields():
    field_names = {f.name for f in dataclasses.fields(CoachingRecommendation)}
    forbidden = {"trade_decision", "risk_result", "signal_candidate", "decision", "risk", "execution"}
    assert field_names.isdisjoint(forbidden)


def test_coaching_recommendation_never_carries_a_verdict_field():
    """No BUY/SELL/NO_TRADE field of any kind (brief's own MUHIM section)."""
    field_names = {f.name for f in dataclasses.fields(CoachingRecommendation)}
    forbidden = {"signal", "verdict", "direction", "buy_sell", "trade_decision"}
    assert field_names.isdisjoint(forbidden)


def test_coaching_recommendation_never_carries_a_performance_field():
    field_names = {f.name for f in dataclasses.fields(CoachingRecommendation)}
    forbidden = {"win_rate", "profit", "sharpe", "drawdown", "performance", "risk_amount"}
    assert field_names.isdisjoint(forbidden)


def test_coaching_recommendation_relays_topic_never_infers():
    for topic in CoachingTopic:
        record = _record(topic=topic)
        assert record.topic == topic


def test_coaching_recommendation_relays_priority_never_computes():
    for priority in CoachingPriority:
        record = _record(priority=priority)
        assert record.priority == priority


def test_coaching_recommendation_relays_type_never_classifies():
    for coaching_type in CoachingType:
        record = _record(type=coaching_type)
        assert record.type == coaching_type


def test_coaching_recommendation_message_relayed_verbatim():
    record = _record(message="exact text supplied by caller")
    assert record.message == "exact text supplied by caller"


def test_coaching_recommendation_recommendation_relayed_verbatim():
    record = _record(recommendation="exact suggestion supplied by caller")
    assert record.recommendation == "exact suggestion supplied by caller"


def test_coaching_recommendation_equality():
    a = _record()
    b = _record()
    assert a == b


def test_coaching_recommendation_inequality_on_coach_id():
    a = _record(coach_id="c1")
    b = _record(coach_id="c2")
    assert a != b


def test_coaching_recommendation_metadata_is_flat_string_mapping():
    record = _record(metadata={"level": "BEGINNER", "source": "TRADE"})
    for key, value in record.metadata.items():
        assert isinstance(key, str)
        assert isinstance(value, str)


def test_generate_coach_id_returns_string():
    coach_id = generate_coach_id()
    assert isinstance(coach_id, str)
    assert coach_id != ""


def test_generate_coach_id_unique():
    ids = {generate_coach_id() for _ in range(20)}
    assert len(ids) == 20


def test_coaching_topic_and_knowledge_category_are_distinct_enums():
    """docs/PHASE66_4_AUDIT.md: CoachingTopic is not a duplicate of knowledge.models.KnowledgeCategory despite some name overlap (RISK, PSYCHOLOGY)."""
    from knowledge.models import KnowledgeCategory

    assert CoachingTopic is not KnowledgeCategory
    assert set(CoachingTopic) != set(KnowledgeCategory)


def test_coaching_topic_and_learning_topic_are_distinct_enums():
    """docs/PHASE66_4_AUDIT.md: CoachingTopic mirrors LearningTopic's value set for coherence but is a separate, local enum -- models.py never imports ai.learning."""
    from ai.learning.models import LearningTopic

    assert CoachingTopic is not LearningTopic


def test_coaching_recommendation_status_defaults_pending_not_archived():
    record = _record()
    assert record.status == CoachingStatus.PENDING
