from ai_layer.ai_service.access.permissions import AIRole
from ai_layer.personal_ai.senior.coaching_runtime import CoachingRuntime
from ai_layer.personal_ai.senior.models import CoachingPriority, CoachingStatus, CoachingTopic, CoachingType
from core_layer.configuration.feature_flags import FeatureFlags

ENABLED = FeatureFlags(enable_coaching_intelligence=True)
DISABLED = FeatureFlags(enable_coaching_intelligence=False)


def _runtime(flags=ENABLED):
    return CoachingRuntime(flags=flags)


def _create(runtime, **overrides):
    defaults = dict(user_id="user_1", topic=CoachingTopic.DISCIPLINE, message="stay disciplined", role=AIRole.OWNER)
    defaults.update(overrides)
    return runtime.create(**defaults)


def test_create_owner_succeeds():
    runtime = _runtime()
    result = _create(runtime)
    assert result is not None
    assert result.user_id == "user_1"
    assert result.topic == CoachingTopic.DISCIPLINE
    assert result.message == "stay disciplined"


def test_create_admin_blocked():
    runtime = _runtime()
    assert _create(runtime, role=AIRole.ADMIN) is None


def test_create_vip_blocked():
    runtime = _runtime()
    assert _create(runtime, role=AIRole.VIP) is None


def test_create_premium_blocked():
    runtime = _runtime()
    assert _create(runtime, role=AIRole.PREMIUM) is None


def test_create_free_blocked():
    runtime = _runtime()
    assert _create(runtime, role=AIRole.FREE) is None


def test_create_blocked_when_flag_disabled_even_for_owner():
    runtime = _runtime(flags=DISABLED)
    assert _create(runtime) is None


def test_create_generates_unique_id():
    runtime = _runtime()
    a = _create(runtime)
    b = _create(runtime)
    assert a.coach_id != b.coach_id


def test_create_stamps_created_at():
    runtime = _runtime()
    result = _create(runtime)
    assert result.created_at != ""


def test_create_defaults_status_pending():
    runtime = _runtime()
    result = _create(runtime)
    assert result.status == CoachingStatus.PENDING


def test_create_relays_learning_id_journal_id_priority_type_recommendation():
    runtime = _runtime()
    result = _create(
        runtime, learning_id="l1", journal_id="j1", priority=CoachingPriority.HIGH,
        type=CoachingType.WARNING, recommendation="review risk sizing",
    )
    assert result.learning_id == "l1"
    assert result.journal_id == "j1"
    assert result.priority == CoachingPriority.HIGH
    assert result.type == CoachingType.WARNING
    assert result.recommendation == "review risk sizing"


def test_create_relays_metadata():
    runtime = _runtime()
    result = _create(runtime, metadata={"session": "London"})
    assert result.metadata == {"session": "London"}


def test_create_defaults_metadata_to_empty_dict():
    runtime = _runtime()
    result = _create(runtime)
    assert result.metadata == {}


def test_create_never_grades_topic_of_its_own():
    """No inference: create() only relays the caller-supplied topic, never computes one."""
    runtime = _runtime()
    for topic in CoachingTopic:
        result = _create(runtime, topic=topic)
        assert result.topic == topic


def test_get_owner_succeeds():
    runtime = _runtime()
    created = _create(runtime)
    fetched = runtime.get(created.coach_id, AIRole.OWNER)
    assert fetched == created


def test_get_unknown_id_returns_none():
    runtime = _runtime()
    assert runtime.get("does-not-exist", AIRole.OWNER) is None


def test_get_admin_blocked():
    runtime = _runtime()
    created = _create(runtime)
    assert runtime.get(created.coach_id, AIRole.ADMIN) is None


def test_get_blocked_when_flag_disabled():
    runtime = _runtime()
    created = _create(runtime)
    blocked_runtime = _runtime(flags=DISABLED)
    assert blocked_runtime.get(created.coach_id, AIRole.OWNER) is None


def test_list_returns_all_created_records():
    """CoachingRecommendation carries a dict `metadata` field, so it is unhashable -- compare by coach_id instead of set membership."""
    runtime = _runtime()
    a = _create(runtime, user_id="u1")
    b = _create(runtime, user_id="u2")
    listed = runtime.list(AIRole.OWNER)
    assert {r.coach_id for r in listed} == {a.coach_id, b.coach_id}
    assert a in listed
    assert b in listed


def test_list_empty_when_nothing_created():
    runtime = _runtime()
    assert runtime.list(AIRole.OWNER) == ()


def test_list_admin_blocked_returns_empty_tuple():
    runtime = _runtime()
    _create(runtime)
    assert runtime.list(AIRole.ADMIN) == ()


def test_list_blocked_when_flag_disabled():
    runtime = _runtime()
    _create(runtime)
    blocked_runtime = _runtime(flags=DISABLED)
    assert blocked_runtime.list(AIRole.OWNER) == ()


def test_update_status_updates_status():
    runtime = _runtime()
    created = _create(runtime)
    updated = runtime.update_status(created.coach_id, AIRole.OWNER, CoachingStatus.ACTIVE)
    assert updated.status == CoachingStatus.ACTIVE


def test_update_status_to_acknowledged():
    runtime = _runtime()
    created = _create(runtime)
    updated = runtime.update_status(created.coach_id, AIRole.OWNER, CoachingStatus.ACKNOWLEDGED)
    assert updated.status == CoachingStatus.ACKNOWLEDGED


def test_update_status_leaves_other_fields_unchanged():
    runtime = _runtime()
    created = _create(runtime, message="original message")
    updated = runtime.update_status(created.coach_id, AIRole.OWNER, CoachingStatus.ACTIVE)
    assert updated.message == "original message"
    assert updated.user_id == created.user_id
    assert updated.topic == created.topic


def test_update_status_rejects_archived():
    """archive() is the only path to ARCHIVED -- update_status() refuses it."""
    runtime = _runtime()
    created = _create(runtime)
    result = runtime.update_status(created.coach_id, AIRole.OWNER, CoachingStatus.ARCHIVED)
    assert result is None


def test_update_status_unknown_id_returns_none():
    runtime = _runtime()
    assert runtime.update_status("does-not-exist", AIRole.OWNER, CoachingStatus.ACTIVE) is None


def test_update_status_admin_blocked():
    runtime = _runtime()
    created = _create(runtime)
    assert runtime.update_status(created.coach_id, AIRole.ADMIN, CoachingStatus.ACTIVE) is None


def test_update_status_blocked_when_flag_disabled():
    runtime = _runtime()
    created = _create(runtime)
    blocked_runtime = _runtime(flags=DISABLED)
    assert blocked_runtime.update_status(created.coach_id, AIRole.OWNER, CoachingStatus.ACTIVE) is None


def test_update_status_persists_to_subsequent_get():
    runtime = _runtime()
    created = _create(runtime)
    runtime.update_status(created.coach_id, AIRole.OWNER, CoachingStatus.ACTIVE)
    fetched = runtime.get(created.coach_id, AIRole.OWNER)
    assert fetched.status == CoachingStatus.ACTIVE


def test_archive_sets_status_archived():
    runtime = _runtime()
    created = _create(runtime)
    archived = runtime.archive(created.coach_id, AIRole.OWNER)
    assert archived.status == CoachingStatus.ARCHIVED


def test_archive_never_deletes_record():
    runtime = _runtime()
    created = _create(runtime)
    runtime.archive(created.coach_id, AIRole.OWNER)
    fetched = runtime.get(created.coach_id, AIRole.OWNER)
    assert fetched is not None
    assert fetched.status == CoachingStatus.ARCHIVED


def test_archive_unknown_id_returns_none():
    runtime = _runtime()
    assert runtime.archive("does-not-exist", AIRole.OWNER) is None


def test_archive_admin_blocked():
    runtime = _runtime()
    created = _create(runtime)
    assert runtime.archive(created.coach_id, AIRole.ADMIN) is None


def test_archive_blocked_when_flag_disabled():
    runtime = _runtime()
    created = _create(runtime)
    blocked_runtime = _runtime(flags=DISABLED)
    assert blocked_runtime.archive(created.coach_id, AIRole.OWNER) is None


def test_archive_from_any_status():
    runtime = _runtime()
    created = _create(runtime)
    runtime.update_status(created.coach_id, AIRole.OWNER, CoachingStatus.ACKNOWLEDGED)
    archived = runtime.archive(created.coach_id, AIRole.OWNER)
    assert archived.status == CoachingStatus.ARCHIVED


def test_runtime_default_construction_never_raises():
    assert CoachingRuntime() is not None


def test_create_never_raises_across_all_roles():
    runtime = _runtime()
    for role in AIRole:
        result = _create(runtime, role=role, user_id=f"user_{role.value}")
        assert result is None or result.user_id == f"user_{role.value}"


def test_multiple_records_independently_addressable():
    runtime = _runtime()
    a = _create(runtime, user_id="u1", topic=CoachingTopic.RISK)
    b = _create(runtime, user_id="u2", topic=CoachingTopic.PATIENCE)
    assert runtime.get(a.coach_id, AIRole.OWNER).topic == CoachingTopic.RISK
    assert runtime.get(b.coach_id, AIRole.OWNER).topic == CoachingTopic.PATIENCE


def test_runtime_never_computes_performance_or_evaluates_trades():
    """TASK 3: CoachingRuntime has no method beyond create/get/list/archive/update_status -- no evaluate/coach/generate_lesson/decide."""
    runtime = CoachingRuntime()
    public_methods = {name for name in dir(runtime) if not name.startswith("_") and callable(getattr(runtime, name))}
    assert public_methods == {"create", "get", "list", "archive", "update_status"}
