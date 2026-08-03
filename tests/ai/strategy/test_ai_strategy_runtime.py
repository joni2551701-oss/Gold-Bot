from ai.access.permissions import AIRole
from ai.strategy.models import StrategyStatus, StrategyType
from ai.strategy.strategy_runtime import StrategyRuntime
from goldbot.core_layer.configuration.feature_flags import FeatureFlags

ENABLED = FeatureFlags(enable_strategy_intelligence=True)
DISABLED = FeatureFlags(enable_strategy_intelligence=False)


def _runtime(flags=ENABLED):
    return StrategyRuntime(flags=flags)


def _create(runtime, **overrides):
    defaults = dict(
        strategy_name="Liquidity Sweep", strategy_type=StrategyType.LIQUIDITY_SWEEP, role=AIRole.OWNER,
    )
    defaults.update(overrides)
    return runtime.create(**defaults)


def test_create_owner_succeeds():
    runtime = _runtime()
    result = _create(runtime)
    assert result is not None
    assert result.strategy_name == "Liquidity Sweep"
    assert result.strategy_type == StrategyType.LIQUIDITY_SWEEP


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
    assert a.strategy_id != b.strategy_id


def test_create_stamps_created_at():
    runtime = _runtime()
    result = _create(runtime)
    assert result.created_at != ""


def test_create_defaults_status_testing():
    runtime = _runtime()
    result = _create(runtime)
    assert result.status == StrategyStatus.TESTING


def test_create_relays_version_confidence_notes_status():
    runtime = _runtime()
    result = _create(
        runtime, strategy_version="v2", confidence="HIGH", notes="works well in London",
        status=StrategyStatus.ACTIVE,
    )
    assert result.strategy_version == "v2"
    assert result.confidence == "HIGH"
    assert result.notes == "works well in London"
    assert result.status == StrategyStatus.ACTIVE


def test_create_never_grades_confidence_of_its_own():
    """No inference: create() only relays the caller-supplied confidence, never computes one."""
    runtime = _runtime()
    for confidence in ("LOW", "MEDIUM", "HIGH", "VERY_HIGH"):
        record = _create(runtime, confidence=confidence)
        assert record.confidence == confidence


def test_get_owner_succeeds():
    runtime = _runtime()
    created = _create(runtime)
    fetched = runtime.get(created.strategy_id, AIRole.OWNER)
    assert fetched == created


def test_get_unknown_id_returns_none():
    runtime = _runtime()
    assert runtime.get("does-not-exist", AIRole.OWNER) is None


def test_get_admin_blocked():
    runtime = _runtime()
    created = _create(runtime)
    assert runtime.get(created.strategy_id, AIRole.ADMIN) is None


def test_get_blocked_when_flag_disabled():
    runtime = _runtime()
    created = _create(runtime)
    blocked_runtime = _runtime(flags=DISABLED)
    assert blocked_runtime.get(created.strategy_id, AIRole.OWNER) is None


def test_list_returns_all_created_records():
    runtime = _runtime()
    a = _create(runtime, strategy_name="Liquidity Sweep")
    b = _create(runtime, strategy_name="FVG", strategy_type=StrategyType.FVG)
    listed = runtime.list(AIRole.OWNER)
    assert {r.strategy_id for r in listed} == {a.strategy_id, b.strategy_id}
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


def test_update_updates_version_confidence_status():
    runtime = _runtime()
    created = _create(runtime)
    updated = runtime.update(
        created.strategy_id, AIRole.OWNER, strategy_version="v2", confidence="HIGH", status=StrategyStatus.ACTIVE,
    )
    assert updated.strategy_version == "v2"
    assert updated.confidence == "HIGH"
    assert updated.status == StrategyStatus.ACTIVE


def test_update_leaves_unspecified_fields_unchanged():
    runtime = _runtime()
    created = _create(runtime, strategy_version="v1")
    updated = runtime.update(created.strategy_id, AIRole.OWNER, confidence="HIGH")
    assert updated.strategy_version == "v1"


def test_update_leaves_other_fields_unchanged():
    runtime = _runtime()
    created = _create(runtime, strategy_name="Liquidity Sweep")
    updated = runtime.update(created.strategy_id, AIRole.OWNER, confidence="HIGH")
    assert updated.strategy_name == "Liquidity Sweep"
    assert updated.strategy_type == created.strategy_type


def test_update_unknown_id_returns_none():
    runtime = _runtime()
    assert runtime.update("does-not-exist", AIRole.OWNER, confidence="HIGH") is None


def test_update_admin_blocked():
    runtime = _runtime()
    created = _create(runtime)
    assert runtime.update(created.strategy_id, AIRole.ADMIN, confidence="HIGH") is None


def test_update_blocked_when_flag_disabled():
    runtime = _runtime()
    created = _create(runtime)
    blocked_runtime = _runtime(flags=DISABLED)
    assert blocked_runtime.update(created.strategy_id, AIRole.OWNER, confidence="HIGH") is None


def test_update_persists_to_subsequent_get():
    runtime = _runtime()
    created = _create(runtime)
    runtime.update(created.strategy_id, AIRole.OWNER, confidence="HIGH")
    fetched = runtime.get(created.strategy_id, AIRole.OWNER)
    assert fetched.confidence == "HIGH"


def test_update_notes_updates_notes():
    runtime = _runtime()
    created = _create(runtime)
    updated = runtime.update_notes(created.strategy_id, AIRole.OWNER, "revised notes")
    assert updated.notes == "revised notes"


def test_update_notes_leaves_other_fields_unchanged():
    runtime = _runtime()
    created = _create(runtime, strategy_version="v1")
    updated = runtime.update_notes(created.strategy_id, AIRole.OWNER, "revised notes")
    assert updated.strategy_version == "v1"
    assert updated.strategy_name == created.strategy_name


def test_update_notes_unknown_id_returns_none():
    runtime = _runtime()
    assert runtime.update_notes("does-not-exist", AIRole.OWNER, "x") is None


def test_update_notes_admin_blocked():
    runtime = _runtime()
    created = _create(runtime)
    assert runtime.update_notes(created.strategy_id, AIRole.ADMIN, "x") is None


def test_update_notes_blocked_when_flag_disabled():
    runtime = _runtime()
    created = _create(runtime)
    blocked_runtime = _runtime(flags=DISABLED)
    assert blocked_runtime.update_notes(created.strategy_id, AIRole.OWNER, "x") is None


def test_archive_sets_status_archived():
    runtime = _runtime()
    created = _create(runtime)
    archived = runtime.archive(created.strategy_id, AIRole.OWNER)
    assert archived.status == StrategyStatus.ARCHIVED


def test_archive_never_deletes_record():
    runtime = _runtime()
    created = _create(runtime)
    runtime.archive(created.strategy_id, AIRole.OWNER)
    fetched = runtime.get(created.strategy_id, AIRole.OWNER)
    assert fetched is not None
    assert fetched.status == StrategyStatus.ARCHIVED


def test_archive_unknown_id_returns_none():
    runtime = _runtime()
    assert runtime.archive("does-not-exist", AIRole.OWNER) is None


def test_archive_admin_blocked():
    runtime = _runtime()
    created = _create(runtime)
    assert runtime.archive(created.strategy_id, AIRole.ADMIN) is None


def test_archive_blocked_when_flag_disabled():
    runtime = _runtime()
    created = _create(runtime)
    blocked_runtime = _runtime(flags=DISABLED)
    assert blocked_runtime.archive(created.strategy_id, AIRole.OWNER) is None


def test_archive_from_any_status():
    runtime = _runtime()
    created = _create(runtime)
    runtime.update(created.strategy_id, AIRole.OWNER, status=StrategyStatus.ACTIVE)
    archived = runtime.archive(created.strategy_id, AIRole.OWNER)
    assert archived.status == StrategyStatus.ARCHIVED


def test_archive_leaves_notes_unchanged():
    runtime = _runtime()
    created = _create(runtime, notes="original notes")
    archived = runtime.archive(created.strategy_id, AIRole.OWNER)
    assert archived.notes == "original notes"


def test_runtime_default_construction_never_raises():
    assert StrategyRuntime() is not None


def test_create_never_raises_across_all_roles():
    runtime = _runtime()
    for role in AIRole:
        result = _create(runtime, role=role, strategy_name=f"strategy_{role.value}")
        assert result is None or result.strategy_name == f"strategy_{role.value}"


def test_multiple_records_independently_addressable():
    runtime = _runtime()
    a = _create(runtime, strategy_name="Liquidity Sweep", strategy_type=StrategyType.LIQUIDITY_SWEEP)
    b = _create(runtime, strategy_name="FVG", strategy_type=StrategyType.FVG)
    assert runtime.get(a.strategy_id, AIRole.OWNER).strategy_type == StrategyType.LIQUIDITY_SWEEP
    assert runtime.get(b.strategy_id, AIRole.OWNER).strategy_type == StrategyType.FVG


def test_runtime_never_computes_performance_or_evaluates_trades():
    """TASK 3: StrategyRuntime has no method beyond create/get/list/update/update_notes/archive -- no evaluate/score/decide."""
    runtime = StrategyRuntime()
    public_methods = {name for name in dir(runtime) if not name.startswith("_") and callable(getattr(runtime, name))}
    assert public_methods == {"create", "get", "list", "update", "update_notes", "archive"}
