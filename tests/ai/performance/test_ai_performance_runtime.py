from ai.access.permissions import AIRole
from ai.performance.performance_runtime import PerformanceRuntime
from goldbot.core_layer.configuration.feature_flags import FeatureFlags

ENABLED = FeatureFlags(enable_performance_intelligence=True)
DISABLED = FeatureFlags(enable_performance_intelligence=False)


def _runtime(flags=ENABLED):
    return PerformanceRuntime(flags=flags)


def _create(runtime, **overrides):
    defaults = dict(user_id="user_1", trade_id="trade_1", role=AIRole.OWNER)
    defaults.update(overrides)
    return runtime.create(**defaults)


def test_create_owner_succeeds():
    runtime = _runtime()
    result = _create(runtime)
    assert result is not None
    assert result.user_id == "user_1"
    assert result.trade_id == "trade_1"


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


def test_create_defaults_archived_false():
    runtime = _runtime()
    result = _create(runtime)
    assert result.archived is False


def test_create_relays_journal_id_result_direction_scores():
    runtime = _runtime()
    result = _create(
        runtime, journal_id="j1", result="WIN", direction="BUY",
        entry_quality=0.8, exit_quality=0.7, discipline_score=0.9,
        risk_score=0.6, confidence_score=0.75, notes="good entry",
    )
    assert result.journal_id == "j1"
    assert result.result == "WIN"
    assert result.direction == "BUY"
    assert result.entry_quality == 0.8
    assert result.exit_quality == 0.7
    assert result.discipline_score == 0.9
    assert result.risk_score == 0.6
    assert result.confidence_score == 0.75
    assert result.notes == "good entry"


def test_create_never_grades_result_of_its_own():
    """No inference: create() only relays the caller-supplied result, never computes one."""
    runtime = _runtime()
    for result in ("WIN", "LOSS", "BE"):
        record = _create(runtime, result=result)
        assert record.result == result


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
    assert {r.id for r in listed} == {a.id, b.id}
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


def test_update_notes_updates_notes():
    runtime = _runtime()
    created = _create(runtime)
    updated = runtime.update_notes(created.id, AIRole.OWNER, "revised notes")
    assert updated.notes == "revised notes"


def test_update_notes_leaves_other_fields_unchanged():
    runtime = _runtime()
    created = _create(runtime, result="WIN", direction="BUY")
    updated = runtime.update_notes(created.id, AIRole.OWNER, "revised notes")
    assert updated.result == "WIN"
    assert updated.direction == "BUY"
    assert updated.user_id == created.user_id
    assert updated.trade_id == created.trade_id


def test_update_notes_unknown_id_returns_none():
    runtime = _runtime()
    assert runtime.update_notes("does-not-exist", AIRole.OWNER, "x") is None


def test_update_notes_admin_blocked():
    runtime = _runtime()
    created = _create(runtime)
    assert runtime.update_notes(created.id, AIRole.ADMIN, "x") is None


def test_update_notes_blocked_when_flag_disabled():
    runtime = _runtime()
    created = _create(runtime)
    blocked_runtime = _runtime(flags=DISABLED)
    assert blocked_runtime.update_notes(created.id, AIRole.OWNER, "x") is None


def test_update_notes_persists_to_subsequent_get():
    runtime = _runtime()
    created = _create(runtime)
    runtime.update_notes(created.id, AIRole.OWNER, "revised notes")
    fetched = runtime.get(created.id, AIRole.OWNER)
    assert fetched.notes == "revised notes"


def test_archive_sets_archived_true():
    runtime = _runtime()
    created = _create(runtime)
    archived = runtime.archive(created.id, AIRole.OWNER)
    assert archived.archived is True


def test_archive_never_deletes_record():
    runtime = _runtime()
    created = _create(runtime)
    runtime.archive(created.id, AIRole.OWNER)
    fetched = runtime.get(created.id, AIRole.OWNER)
    assert fetched is not None
    assert fetched.archived is True


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


def test_archive_leaves_notes_unchanged():
    runtime = _runtime()
    created = _create(runtime, notes="original notes")
    archived = runtime.archive(created.id, AIRole.OWNER)
    assert archived.notes == "original notes"


def test_runtime_default_construction_never_raises():
    assert PerformanceRuntime() is not None


def test_create_never_raises_across_all_roles():
    runtime = _runtime()
    for role in AIRole:
        result = _create(runtime, role=role, user_id=f"user_{role.value}")
        assert result is None or result.user_id == f"user_{role.value}"


def test_multiple_records_independently_addressable():
    runtime = _runtime()
    a = _create(runtime, user_id="u1", result="WIN")
    b = _create(runtime, user_id="u2", result="LOSS")
    assert runtime.get(a.id, AIRole.OWNER).result == "WIN"
    assert runtime.get(b.id, AIRole.OWNER).result == "LOSS"


def test_runtime_never_computes_performance_or_evaluates_trades():
    """TASK 3: PerformanceRuntime has no method beyond create/get/list/update_notes/archive -- no evaluate/score/decide."""
    runtime = PerformanceRuntime()
    public_methods = {name for name in dir(runtime) if not name.startswith("_") and callable(getattr(runtime, name))}
    assert public_methods == {"create", "get", "list", "update_notes", "archive"}
