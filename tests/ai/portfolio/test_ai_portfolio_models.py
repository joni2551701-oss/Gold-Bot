import dataclasses

from ai.portfolio.models import (
    PortfolioHealth,
    PortfolioRecord,
    PortfolioRiskLevel,
    PortfolioStatus,
    generate_portfolio_id,
)


def _record(**overrides):
    defaults = dict(portfolio_id="p1", portfolio_name="Main Portfolio")
    defaults.update(overrides)
    return PortfolioRecord(**defaults)


def test_portfolio_status_has_three_members():
    assert len(list(PortfolioStatus)) == 3


def test_portfolio_status_members():
    values = {m.value for m in PortfolioStatus}
    assert values == {"ACTIVE", "PAUSED", "ARCHIVED"}


def test_portfolio_risk_level_has_four_members():
    assert len(list(PortfolioRiskLevel)) == 4


def test_portfolio_risk_level_members():
    values = {m.value for m in PortfolioRiskLevel}
    assert values == {"LOW", "MEDIUM", "HIGH", "CRITICAL"}


def test_portfolio_health_has_three_members():
    assert len(list(PortfolioHealth)) == 3


def test_portfolio_health_members():
    values = {m.value for m in PortfolioHealth}
    assert values == {"GOOD", "WARNING", "POOR"}


def test_portfolio_record_defaults():
    record = _record()
    assert record.status == PortfolioStatus.ACTIVE
    assert record.risk_level is None
    assert record.health is None
    assert record.strategy_count == 0
    assert record.active_strategy_count == 0
    assert record.notes is None
    assert record.created_at == ""


def test_portfolio_record_is_frozen():
    record = _record()
    try:
        record.portfolio_name = "someone_else"
        assert False, "expected FrozenInstanceError"
    except dataclasses.FrozenInstanceError:
        pass


def test_portfolio_record_accepts_all_fields():
    record = _record(
        status=PortfolioStatus.PAUSED, risk_level=PortfolioRiskLevel.HIGH,
        health=PortfolioHealth.WARNING, strategy_count=5, active_strategy_count=3,
        notes="rebalancing needed", created_at="2026-01-01T00:00:00Z",
    )
    assert record.status == PortfolioStatus.PAUSED
    assert record.risk_level == PortfolioRiskLevel.HIGH
    assert record.health == PortfolioHealth.WARNING
    assert record.strategy_count == 5
    assert record.active_strategy_count == 3
    assert record.notes == "rebalancing needed"
    assert record.created_at == "2026-01-01T00:00:00Z"


def test_portfolio_record_field_names_match_task_2_contract():
    field_names = {f.name for f in dataclasses.fields(PortfolioRecord)}
    assert field_names == {
        "portfolio_id", "portfolio_name", "status", "risk_level", "health",
        "strategy_count", "active_strategy_count", "notes", "created_at",
    }


def test_portfolio_record_portfolio_id_name_required():
    field_by_name = {f.name: f for f in dataclasses.fields(PortfolioRecord)}
    for required in ("portfolio_id", "portfolio_name"):
        assert field_by_name[required].default is dataclasses.MISSING


def test_portfolio_record_has_no_trading_core_object_fields():
    field_names = {f.name for f in dataclasses.fields(PortfolioRecord)}
    forbidden = {"trade_decision", "risk_result", "signal_candidate", "decision", "risk", "execution"}
    assert field_names.isdisjoint(forbidden)


def test_portfolio_record_never_carries_a_verdict_field():
    field_names = {f.name for f in dataclasses.fields(PortfolioRecord)}
    forbidden = {"signal", "verdict", "direction", "buy_sell", "trade_decision", "lot_size"}
    assert field_names.isdisjoint(forbidden)


def test_portfolio_record_never_carries_an_optimization_field():
    field_names = {f.name for f in dataclasses.fields(PortfolioRecord)}
    forbidden = {"optimization_score", "allocation", "correlation_matrix", "benchmark_score"}
    assert field_names.isdisjoint(forbidden)


def test_portfolio_record_relays_status_never_computes():
    for status in PortfolioStatus:
        record = _record(status=status)
        assert record.status == status


def test_portfolio_record_relays_risk_level_never_grades():
    for risk_level in PortfolioRiskLevel:
        record = _record(risk_level=risk_level)
        assert record.risk_level == risk_level


def test_portfolio_record_relays_health_never_grades():
    for health in PortfolioHealth:
        record = _record(health=health)
        assert record.health == health


def test_portfolio_record_notes_relayed_verbatim():
    record = _record(notes="exact text supplied by caller")
    assert record.notes == "exact text supplied by caller"


def test_portfolio_record_equality():
    a = _record()
    b = _record()
    assert a == b


def test_portfolio_record_inequality_on_portfolio_id():
    a = _record(portfolio_id="p1")
    b = _record(portfolio_id="p2")
    assert a != b


def test_portfolio_record_status_defaults_active_not_archived():
    record = _record()
    assert record.status == PortfolioStatus.ACTIVE


def test_generate_portfolio_id_returns_string():
    portfolio_id = generate_portfolio_id()
    assert isinstance(portfolio_id, str)
    assert portfolio_id != ""


def test_generate_portfolio_id_unique():
    ids = {generate_portfolio_id() for _ in range(20)}
    assert len(ids) == 20


def test_portfolio_record_has_no_trading_core_object_field_type():
    """Belt-and-suspenders: no dataclass field on PortfolioRecord may be typed as a Trading Core object -- every field is a primitive/enum/Optional only."""
    allowed_type_fragments = ("str", "int", "PortfolioStatus", "PortfolioRiskLevel", "PortfolioHealth", "Optional")
    for f in dataclasses.fields(PortfolioRecord):
        type_str = str(f.type)
        assert any(fragment in type_str for fragment in allowed_type_fragments), f"PortfolioRecord.{f.name}: {type_str}"


def test_portfolio_record_strategy_counts_default_to_zero_not_none():
    record = _record()
    assert record.strategy_count == 0
    assert record.active_strategy_count == 0
