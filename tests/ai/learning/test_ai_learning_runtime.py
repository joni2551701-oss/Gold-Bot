from ai_layer.ai_service.access.permissions import AIRole
from ai_layer.knowledge_ai.learning_engine.learning_runtime import LearningRuntime
from ai_layer.knowledge_ai.learning_engine.models import LearningLevel, LearningSource, LearningStatus, LearningTopic
from core_layer.configuration.feature_flags import FeatureFlags

ENABLED = FeatureFlags(enable_learning_intelligence=True)
DISABLED = FeatureFlags(enable_learning_intelligence=False)


def _runtime(flags=ENABLED):
    return LearningRuntime(flags=flags)


def _create(runtime, **overrides):
    defaults = dict(user_id="user_1", topic=LearningTopic.DISCIPLINE, role=AIRole.OWNER)
    defaults.update(overrides)
    return runtime.create(**defaults)


def test_create_owner_succeeds():
    runtime = _runtime()
    result = _create(runtime)
    assert result is not None
    assert result.user_id == "user_1"
    assert result.topic == LearningTopic.DISCIPLINE


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
    assert a.id != b.id


def test_create_stamps_created_at():
    runtime = _runtime()
    result = _create(runtime)
    assert result.created_at != ""


def test_create_defaults_status_active():
    runtime = _runtime()
    result = _create(runtime)
    assert result.status == LearningStatus.ACTIVE


def test_create_relays_level_confidence_notes_source():
    runtime = _runtime()
    result = _create(
        runtime, level=LearningLevel.ADVANCED, confidence=0.9,
        notes="strong session", source=LearningSource.TRADE,
    )
    assert result.level == LearningLevel.ADVANCED
    assert result.confidence == 0.9
    assert result.notes == "strong session"
    assert result.source == LearningSource.TRADE


def test_create_never_grades_level_of_its_own():
    """Rule 6/7: create() only relays the caller-supplied level, never computes one."""
    runtime = _runtime()
    for level in LearningLevel:
        result = _create(runtime, level=level)
        assert result.level == level


def test_get_owner_succeeds():
    runtime = _runtime()
    created = _create(runtime)
    fetched = runtime.get(created.id, AIRole.OWNER)
    assert fetched == created


def test_get_unknown_id_returns_none():
    runtime = _runtime()
    assert runtime.get("does-not-exist", AIRole.OWNER) is None


def test_get_admin_blocked():
    runtime = _runtime()
    created = _create(runtime)
    assert runtime.get(created.id, AIRole.ADMIN) is None


def test_get_blocked_when_flag_disabled():
    runtime = _runtime()
    created = _create(runtime)
    blocked_runtime = _runtime(flags=DISABLED)
    assert blocked_runtime.get(created.id, AIRole.OWNER) is None


def test_list_returns_all_created_records():
    runtime = _runtime()
    a = _create(runtime, user_id="u1")
    b = _create(runtime, user_id="u2")
    listed = runtime.list(AIRole.OWNER)
    assert set(listed) == {a, b}


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


def test_update_updates_level():
    runtime = _runtime()
    created = _create(runtime, level=LearningLevel.BEGINNER)
    updated = runtime.update(created.id, AIRole.OWNER, level=LearningLevel.INTERMEDIATE)
    assert updated.level == LearningLevel.INTERMEDIATE


def test_update_updates_confidence():
    runtime = _runtime()
    created = _create(runtime)
    updated = runtime.update(created.id, AIRole.OWNER, confidence=0.75)
    assert updated.confidence == 0.75


def test_update_updates_notes():
    runtime = _runtime()
    created = _create(runtime)
    updated = runtime.update(created.id, AIRole.OWNER, notes="revised note")
    assert updated.notes == "revised note"


def test_update_leaves_unspecified_fields_unchanged():
    runtime = _runtime()
    created = _create(runtime, level=LearningLevel.BEGINNER, notes="original")
    updated = runtime.update(created.id, AIRole.OWNER, confidence=0.5)
    assert updated.level == LearningLevel.BEGINNER
    assert updated.notes == "original"


def test_update_never_changes_user_id_topic_source():
    """TASK 3's own narrow scope: only level/confidence/notes are updatable."""
    runtime = _runtime()
    created = _create(runtime, user_id="user_x", topic=LearningTopic.EXIT, source=LearningSource.CHART)
    updated = runtime.update(created.id, AIRole.OWNER, notes="updated")
    assert updated.user_id == "user_x"
    assert updated.topic == LearningTopic.EXIT
    assert updated.source == LearningSource.CHART


def test_update_unknown_id_returns_none():
    runtime = _runtime()
    assert runtime.update("does-not-exist", AIRole.OWNER, notes="x") is None


def test_update_admin_blocked():
    runtime = _runtime()
    created = _create(runtime)
    assert runtime.update(created.id, AIRole.ADMIN, notes="x") is None


def test_update_blocked_when_flag_disabled():
    runtime = _runtime()
    created = _create(runtime)
    blocked_runtime = _runtime(flags=DISABLED)
    assert blocked_runtime.update(created.id, AIRole.OWNER, notes="x") is None


def test_update_persists_to_subsequent_get():
    runtime = _runtime()
    created = _create(runtime)
    runtime.update(created.id, AIRole.OWNER, notes="persisted note")
    fetched = runtime.get(created.id, AIRole.OWNER)
    assert fetched.notes == "persisted note"


def test_archive_sets_status_archived():
    runtime = _runtime()
    created = _create(runtime)
    archived = runtime.archive(created.id, AIRole.OWNER)
    assert archived.status == LearningStatus.ARCHIVED


def test_archive_never_deletes_record():
    runtime = _runtime()
    created = _create(runtime)
    runtime.archive(created.id, AIRole.OWNER)
    fetched = runtime.get(created.id, AIRole.OWNER)
    assert fetched is not None
    assert fetched.status == LearningStatus.ARCHIVED


def test_archive_unknown_id_returns_none():
    runtime = _runtime()
    assert runtime.archive("does-not-exist", AIRole.OWNER) is None


def test_archive_admin_blocked():
    runtime = _runtime()
    created = _create(runtime)
    assert runtime.archive(created.id, AIRole.ADMIN) is None


def test_archive_blocked_when_flag_disabled():
    runtime = _runtime()
    created = _create(runtime)
    blocked_runtime = _runtime(flags=DISABLED)
    assert blocked_runtime.archive(created.id, AIRole.OWNER) is None


def test_runtime_default_construction_never_raises():
    assert LearningRuntime() is not None


def test_create_never_raises_across_all_roles():
    runtime = _runtime()
    for role in AIRole:
        result = _create(runtime, role=role, user_id=f"user_{role.value}")
        assert result is None or result.user_id == f"user_{role.value}"


def test_multiple_records_independently_addressable():
    runtime = _runtime()
    a = _create(runtime, user_id="u1", topic=LearningTopic.RISK)
    b = _create(runtime, user_id="u2", topic=LearningTopic.PATIENCE)
    assert runtime.get(a.id, AIRole.OWNER).topic == LearningTopic.RISK
    assert runtime.get(b.id, AIRole.OWNER).topic == LearningTopic.PATIENCE


def test_runtime_never_computes_performance():
    """Rule 6: LearningRuntime has no method beyond create/get/list/update/archive."""
    runtime = LearningRuntime()
    public_methods = {name for name in dir(runtime) if not name.startswith("_") and callable(getattr(runtime, name))}
    assert public_methods == {"create", "get", "list", "update", "archive"}
