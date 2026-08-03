from ai_layer.ai_service.access.permissions import AIRole
from ai_layer.fundamental_ai.models import ResearchCategory, ResearchPriority, ResearchStatus
from ai_layer.fundamental_ai.research_runtime import ResearchRuntime
from core_layer.configuration.feature_flags import FeatureFlags

ENABLED = FeatureFlags(enable_research_intelligence=True)
DISABLED = FeatureFlags(enable_research_intelligence=False)


def _runtime(flags=ENABLED):
    return ResearchRuntime(flags=flags)


def _create(runtime, **overrides):
    defaults = dict(title="Liquidity Sweep Study", category=ResearchCategory.STRATEGY, role=AIRole.OWNER)
    defaults.update(overrides)
    return runtime.create(**defaults)


def test_create_owner_succeeds():
    runtime = _runtime()
    result = _create(runtime)
    assert result is not None
    assert result.title == "Liquidity Sweep Study"
    assert result.category == ResearchCategory.STRATEGY


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
    assert a.research_id != b.research_id


def test_create_stamps_created_at():
    runtime = _runtime()
    result = _create(runtime)
    assert result.created_at != ""


def test_create_defaults_priority_medium():
    runtime = _runtime()
    result = _create(runtime)
    assert result.priority == ResearchPriority.MEDIUM


def test_create_defaults_status_active():
    runtime = _runtime()
    result = _create(runtime)
    assert result.status == ResearchStatus.ACTIVE


def test_create_defaults_source_count_zero():
    runtime = _runtime()
    result = _create(runtime)
    assert result.source_count == 0


def test_create_relays_priority_status_summary_source_count_notes():
    runtime = _runtime()
    result = _create(
        runtime, priority=ResearchPriority.CRITICAL, status=ResearchStatus.ARCHIVED,
        summary="London liquidity sweeps outperform Asia session", source_count=5,
        notes="needs peer review",
    )
    assert result.priority == ResearchPriority.CRITICAL
    assert result.status == ResearchStatus.ARCHIVED
    assert result.summary == "London liquidity sweeps outperform Asia session"
    assert result.source_count == 5
    assert result.notes == "needs peer review"


def test_create_never_grades_priority_of_its_own():
    """No inference: create() only relays the caller-supplied priority, never computes one."""
    runtime = _runtime()
    for priority in ResearchPriority:
        record = _create(runtime, priority=priority)
        assert record.priority == priority


def test_get_owner_succeeds():
    runtime = _runtime()
    created = _create(runtime)
    fetched = runtime.get(created.research_id, AIRole.OWNER)
    assert fetched == created


def test_get_unknown_id_returns_none():
    runtime = _runtime()
    assert runtime.get("does-not-exist", AIRole.OWNER) is None


def test_get_admin_blocked():
    runtime = _runtime()
    created = _create(runtime)
    assert runtime.get(created.research_id, AIRole.ADMIN) is None


def test_get_blocked_when_flag_disabled():
    runtime = _runtime()
    created = _create(runtime)
    blocked_runtime = _runtime(flags=DISABLED)
    assert blocked_runtime.get(created.research_id, AIRole.OWNER) is None


def test_list_returns_all_created_records():
    runtime = _runtime()
    a = _create(runtime, title="Study A")
    b = _create(runtime, title="Study B", category=ResearchCategory.PERFORMANCE)
    listed = runtime.list(AIRole.OWNER)
    assert {r.research_id for r in listed} == {a.research_id, b.research_id}
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


def test_update_updates_priority_status_summary_source_count():
    runtime = _runtime()
    created = _create(runtime)
    updated = runtime.update(
        created.research_id, AIRole.OWNER, priority=ResearchPriority.HIGH,
        status=ResearchStatus.ARCHIVED, summary="revised summary", source_count=3,
    )
    assert updated.priority == ResearchPriority.HIGH
    assert updated.status == ResearchStatus.ARCHIVED
    assert updated.summary == "revised summary"
    assert updated.source_count == 3


def test_update_leaves_unspecified_fields_unchanged():
    runtime = _runtime()
    created = _create(runtime, priority=ResearchPriority.LOW)
    updated = runtime.update(created.research_id, AIRole.OWNER, status=ResearchStatus.ARCHIVED)
    assert updated.priority == ResearchPriority.LOW


def test_update_leaves_other_fields_unchanged():
    runtime = _runtime()
    created = _create(runtime, title="Liquidity Sweep Study")
    updated = runtime.update(created.research_id, AIRole.OWNER, priority=ResearchPriority.HIGH)
    assert updated.title == "Liquidity Sweep Study"
    assert updated.category == created.category


def test_update_unknown_id_returns_none():
    runtime = _runtime()
    assert runtime.update("does-not-exist", AIRole.OWNER, priority=ResearchPriority.HIGH) is None


def test_update_admin_blocked():
    runtime = _runtime()
    created = _create(runtime)
    assert runtime.update(created.research_id, AIRole.ADMIN, priority=ResearchPriority.HIGH) is None


def test_update_blocked_when_flag_disabled():
    runtime = _runtime()
    created = _create(runtime)
    blocked_runtime = _runtime(flags=DISABLED)
    assert blocked_runtime.update(created.research_id, AIRole.OWNER, priority=ResearchPriority.HIGH) is None


def test_update_persists_to_subsequent_get():
    runtime = _runtime()
    created = _create(runtime)
    runtime.update(created.research_id, AIRole.OWNER, priority=ResearchPriority.HIGH)
    fetched = runtime.get(created.research_id, AIRole.OWNER)
    assert fetched.priority == ResearchPriority.HIGH


def test_update_zero_source_count_is_applied_not_treated_as_none():
    runtime = _runtime()
    created = _create(runtime, source_count=5)
    updated = runtime.update(created.research_id, AIRole.OWNER, source_count=0)
    assert updated.source_count == 0


def test_update_notes_updates_notes():
    runtime = _runtime()
    created = _create(runtime)
    updated = runtime.update_notes(created.research_id, AIRole.OWNER, "revised notes")
    assert updated.notes == "revised notes"


def test_update_notes_leaves_other_fields_unchanged():
    runtime = _runtime()
    created = _create(runtime, source_count=5)
    updated = runtime.update_notes(created.research_id, AIRole.OWNER, "revised notes")
    assert updated.source_count == 5
    assert updated.title == created.title


def test_update_notes_unknown_id_returns_none():
    runtime = _runtime()
    assert runtime.update_notes("does-not-exist", AIRole.OWNER, "x") is None


def test_update_notes_admin_blocked():
    runtime = _runtime()
    created = _create(runtime)
    assert runtime.update_notes(created.research_id, AIRole.ADMIN, "x") is None


def test_update_notes_blocked_when_flag_disabled():
    runtime = _runtime()
    created = _create(runtime)
    blocked_runtime = _runtime(flags=DISABLED)
    assert blocked_runtime.update_notes(created.research_id, AIRole.OWNER, "x") is None


def test_archive_sets_status_archived():
    runtime = _runtime()
    created = _create(runtime)
    archived = runtime.archive(created.research_id, AIRole.OWNER)
    assert archived.status == ResearchStatus.ARCHIVED


def test_archive_never_deletes_record():
    runtime = _runtime()
    created = _create(runtime)
    runtime.archive(created.research_id, AIRole.OWNER)
    fetched = runtime.get(created.research_id, AIRole.OWNER)
    assert fetched is not None
    assert fetched.status == ResearchStatus.ARCHIVED


def test_archive_unknown_id_returns_none():
    runtime = _runtime()
    assert runtime.archive("does-not-exist", AIRole.OWNER) is None


def test_archive_admin_blocked():
    runtime = _runtime()
    created = _create(runtime)
    assert runtime.archive(created.research_id, AIRole.ADMIN) is None


def test_archive_blocked_when_flag_disabled():
    runtime = _runtime()
    created = _create(runtime)
    blocked_runtime = _runtime(flags=DISABLED)
    assert blocked_runtime.archive(created.research_id, AIRole.OWNER) is None


def test_archive_from_active_status():
    runtime = _runtime()
    created = _create(runtime, status=ResearchStatus.ACTIVE)
    archived = runtime.archive(created.research_id, AIRole.OWNER)
    assert archived.status == ResearchStatus.ARCHIVED


def test_archive_leaves_notes_unchanged():
    runtime = _runtime()
    created = _create(runtime, notes="original notes")
    archived = runtime.archive(created.research_id, AIRole.OWNER)
    assert archived.notes == "original notes"


def test_runtime_default_construction_never_raises():
    assert ResearchRuntime() is not None


def test_create_never_raises_across_all_roles():
    runtime = _runtime()
    for role in AIRole:
        result = _create(runtime, role=role, title=f"study_{role.value}")
        assert result is None or result.title == f"study_{role.value}"


def test_multiple_records_independently_addressable():
    runtime = _runtime()
    a = _create(runtime, title="A", category=ResearchCategory.STRATEGY)
    b = _create(runtime, title="B", category=ResearchCategory.PERFORMANCE)
    assert runtime.get(a.research_id, AIRole.OWNER).category == ResearchCategory.STRATEGY
    assert runtime.get(b.research_id, AIRole.OWNER).category == ResearchCategory.PERFORMANCE


def test_runtime_never_computes_performance_or_evaluates_trades():
    """TASK 3: ResearchRuntime has no method beyond create/get/list/update/update_notes/archive -- no evaluate/mine/decide."""
    runtime = ResearchRuntime()
    public_methods = {name for name in dir(runtime) if not name.startswith("_") and callable(getattr(runtime, name))}
    assert public_methods == {"create", "get", "list", "update", "update_notes", "archive"}


def test_create_relays_category_across_all_values():
    runtime = _runtime()
    for category in ResearchCategory:
        record = _create(runtime, category=category)
        assert record.category == category


def test_update_with_no_arguments_returns_unchanged_record():
    runtime = _runtime()
    created = _create(runtime, priority=ResearchPriority.HIGH, source_count=7)
    updated = runtime.update(created.research_id, AIRole.OWNER)
    assert updated.priority == ResearchPriority.HIGH
    assert updated.source_count == 7
