from ai.access.permissions import AIRole
from ai.portfolio.models import PortfolioHealth, PortfolioRiskLevel, PortfolioStatus
from ai.portfolio.portfolio_runtime import PortfolioRuntime
from goldbot.core_layer.configuration.feature_flags import FeatureFlags

ENABLED = FeatureFlags(enable_portfolio_intelligence=True)
DISABLED = FeatureFlags(enable_portfolio_intelligence=False)


def _runtime(flags=ENABLED):
    return PortfolioRuntime(flags=flags)


def _create(runtime, **overrides):
    defaults = dict(portfolio_name="Main Portfolio", role=AIRole.OWNER)
    defaults.update(overrides)
    return runtime.create(**defaults)


def test_create_owner_succeeds():
    runtime = _runtime()
    result = _create(runtime)
    assert result is not None
    assert result.portfolio_name == "Main Portfolio"


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
    assert a.portfolio_id != b.portfolio_id


def test_create_stamps_created_at():
    runtime = _runtime()
    result = _create(runtime)
    assert result.created_at != ""


def test_create_defaults_status_active():
    runtime = _runtime()
    result = _create(runtime)
    assert result.status == PortfolioStatus.ACTIVE


def test_create_relays_status_risk_level_health_counts_notes():
    runtime = _runtime()
    result = _create(
        runtime, status=PortfolioStatus.PAUSED, risk_level=PortfolioRiskLevel.HIGH,
        health=PortfolioHealth.WARNING, strategy_count=5, active_strategy_count=3,
        notes="rebalancing needed",
    )
    assert result.status == PortfolioStatus.PAUSED
    assert result.risk_level == PortfolioRiskLevel.HIGH
    assert result.health == PortfolioHealth.WARNING
    assert result.strategy_count == 5
    assert result.active_strategy_count == 3
    assert result.notes == "rebalancing needed"


def test_create_never_grades_risk_level_of_its_own():
    """No inference: create() only relays the caller-supplied risk_level, never computes one."""
    runtime = _runtime()
    for risk_level in PortfolioRiskLevel:
        record = _create(runtime, risk_level=risk_level)
        assert record.risk_level == risk_level


def test_get_owner_succeeds():
    runtime = _runtime()
    created = _create(runtime)
    fetched = runtime.get(created.portfolio_id, AIRole.OWNER)
    assert fetched == created


def test_get_unknown_id_returns_none():
    runtime = _runtime()
    assert runtime.get("does-not-exist", AIRole.OWNER) is None


def test_get_admin_blocked():
    runtime = _runtime()
    created = _create(runtime)
    assert runtime.get(created.portfolio_id, AIRole.ADMIN) is None


def test_get_blocked_when_flag_disabled():
    runtime = _runtime()
    created = _create(runtime)
    blocked_runtime = _runtime(flags=DISABLED)
    assert blocked_runtime.get(created.portfolio_id, AIRole.OWNER) is None


def test_list_returns_all_created_records():
    runtime = _runtime()
    a = _create(runtime, portfolio_name="Portfolio A")
    b = _create(runtime, portfolio_name="Portfolio B")
    listed = runtime.list(AIRole.OWNER)
    assert {r.portfolio_id for r in listed} == {a.portfolio_id, b.portfolio_id}
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


def test_update_updates_status_risk_level_health_counts():
    runtime = _runtime()
    created = _create(runtime)
    updated = runtime.update(
        created.portfolio_id, AIRole.OWNER, status=PortfolioStatus.PAUSED,
        risk_level=PortfolioRiskLevel.CRITICAL, health=PortfolioHealth.POOR,
        strategy_count=10, active_strategy_count=2,
    )
    assert updated.status == PortfolioStatus.PAUSED
    assert updated.risk_level == PortfolioRiskLevel.CRITICAL
    assert updated.health == PortfolioHealth.POOR
    assert updated.strategy_count == 10
    assert updated.active_strategy_count == 2


def test_update_leaves_unspecified_fields_unchanged():
    runtime = _runtime()
    created = _create(runtime, risk_level=PortfolioRiskLevel.LOW)
    updated = runtime.update(created.portfolio_id, AIRole.OWNER, health=PortfolioHealth.GOOD)
    assert updated.risk_level == PortfolioRiskLevel.LOW


def test_update_leaves_other_fields_unchanged():
    runtime = _runtime()
    created = _create(runtime, portfolio_name="Main Portfolio")
    updated = runtime.update(created.portfolio_id, AIRole.OWNER, health=PortfolioHealth.GOOD)
    assert updated.portfolio_name == "Main Portfolio"


def test_update_unknown_id_returns_none():
    runtime = _runtime()
    assert runtime.update("does-not-exist", AIRole.OWNER, health=PortfolioHealth.GOOD) is None


def test_update_admin_blocked():
    runtime = _runtime()
    created = _create(runtime)
    assert runtime.update(created.portfolio_id, AIRole.ADMIN, health=PortfolioHealth.GOOD) is None


def test_update_blocked_when_flag_disabled():
    runtime = _runtime()
    created = _create(runtime)
    blocked_runtime = _runtime(flags=DISABLED)
    assert blocked_runtime.update(created.portfolio_id, AIRole.OWNER, health=PortfolioHealth.GOOD) is None


def test_update_persists_to_subsequent_get():
    runtime = _runtime()
    created = _create(runtime)
    runtime.update(created.portfolio_id, AIRole.OWNER, health=PortfolioHealth.GOOD)
    fetched = runtime.get(created.portfolio_id, AIRole.OWNER)
    assert fetched.health == PortfolioHealth.GOOD


def test_update_zero_counts_are_applied_not_treated_as_none():
    runtime = _runtime()
    created = _create(runtime, strategy_count=5, active_strategy_count=5)
    updated = runtime.update(created.portfolio_id, AIRole.OWNER, active_strategy_count=0)
    assert updated.active_strategy_count == 0


def test_update_notes_updates_notes():
    runtime = _runtime()
    created = _create(runtime)
    updated = runtime.update_notes(created.portfolio_id, AIRole.OWNER, "revised notes")
    assert updated.notes == "revised notes"


def test_update_notes_leaves_other_fields_unchanged():
    runtime = _runtime()
    created = _create(runtime, strategy_count=5)
    updated = runtime.update_notes(created.portfolio_id, AIRole.OWNER, "revised notes")
    assert updated.strategy_count == 5
    assert updated.portfolio_name == created.portfolio_name


def test_update_notes_unknown_id_returns_none():
    runtime = _runtime()
    assert runtime.update_notes("does-not-exist", AIRole.OWNER, "x") is None


def test_update_notes_admin_blocked():
    runtime = _runtime()
    created = _create(runtime)
    assert runtime.update_notes(created.portfolio_id, AIRole.ADMIN, "x") is None


def test_update_notes_blocked_when_flag_disabled():
    runtime = _runtime()
    created = _create(runtime)
    blocked_runtime = _runtime(flags=DISABLED)
    assert blocked_runtime.update_notes(created.portfolio_id, AIRole.OWNER, "x") is None


def test_archive_sets_status_archived():
    runtime = _runtime()
    created = _create(runtime)
    archived = runtime.archive(created.portfolio_id, AIRole.OWNER)
    assert archived.status == PortfolioStatus.ARCHIVED


def test_archive_never_deletes_record():
    runtime = _runtime()
    created = _create(runtime)
    runtime.archive(created.portfolio_id, AIRole.OWNER)
    fetched = runtime.get(created.portfolio_id, AIRole.OWNER)
    assert fetched is not None
    assert fetched.status == PortfolioStatus.ARCHIVED


def test_archive_unknown_id_returns_none():
    runtime = _runtime()
    assert runtime.archive("does-not-exist", AIRole.OWNER) is None


def test_archive_admin_blocked():
    runtime = _runtime()
    created = _create(runtime)
    assert runtime.archive(created.portfolio_id, AIRole.ADMIN) is None


def test_archive_blocked_when_flag_disabled():
    runtime = _runtime()
    created = _create(runtime)
    blocked_runtime = _runtime(flags=DISABLED)
    assert blocked_runtime.archive(created.portfolio_id, AIRole.OWNER) is None


def test_archive_from_any_status():
    runtime = _runtime()
    created = _create(runtime)
    runtime.update(created.portfolio_id, AIRole.OWNER, status=PortfolioStatus.PAUSED)
    archived = runtime.archive(created.portfolio_id, AIRole.OWNER)
    assert archived.status == PortfolioStatus.ARCHIVED


def test_archive_leaves_notes_unchanged():
    runtime = _runtime()
    created = _create(runtime, notes="original notes")
    archived = runtime.archive(created.portfolio_id, AIRole.OWNER)
    assert archived.notes == "original notes"


def test_runtime_default_construction_never_raises():
    assert PortfolioRuntime() is not None


def test_create_never_raises_across_all_roles():
    runtime = _runtime()
    for role in AIRole:
        result = _create(runtime, role=role, portfolio_name=f"portfolio_{role.value}")
        assert result is None or result.portfolio_name == f"portfolio_{role.value}"


def test_multiple_records_independently_addressable():
    runtime = _runtime()
    a = _create(runtime, portfolio_name="A", risk_level=PortfolioRiskLevel.LOW)
    b = _create(runtime, portfolio_name="B", risk_level=PortfolioRiskLevel.HIGH)
    assert runtime.get(a.portfolio_id, AIRole.OWNER).risk_level == PortfolioRiskLevel.LOW
    assert runtime.get(b.portfolio_id, AIRole.OWNER).risk_level == PortfolioRiskLevel.HIGH


def test_runtime_never_computes_performance_or_evaluates_trades():
    """TASK 3: PortfolioRuntime has no method beyond create/get/list/update/update_notes/archive -- no evaluate/optimize/decide."""
    runtime = PortfolioRuntime()
    public_methods = {name for name in dir(runtime) if not name.startswith("_") and callable(getattr(runtime, name))}
    assert public_methods == {"create", "get", "list", "update", "update_notes", "archive"}


def test_update_with_no_arguments_returns_unchanged_record():
    runtime = _runtime()
    created = _create(runtime, risk_level=PortfolioRiskLevel.MEDIUM, strategy_count=4)
    updated = runtime.update(created.portfolio_id, AIRole.OWNER)
    assert updated.risk_level == PortfolioRiskLevel.MEDIUM
    assert updated.strategy_count == 4
    assert updated.status == created.status


def test_create_defaults_strategy_counts_to_zero():
    runtime = _runtime()
    result = _create(runtime)
    assert result.strategy_count == 0
    assert result.active_strategy_count == 0


def test_update_health_independently_of_risk_level():
    runtime = _runtime()
    created = _create(runtime, risk_level=PortfolioRiskLevel.LOW, health=PortfolioHealth.GOOD)
    updated = runtime.update(created.portfolio_id, AIRole.OWNER, health=PortfolioHealth.POOR)
    assert updated.health == PortfolioHealth.POOR
    assert updated.risk_level == PortfolioRiskLevel.LOW
