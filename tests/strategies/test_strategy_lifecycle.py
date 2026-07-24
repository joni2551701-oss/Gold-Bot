"""
Phase A11 -- Strategy Lifecycle foundation tests
(strategies/lifecycle/).

No mocking -- real StrategyDefinition/StrategyRegistry objects, same
convention as tests/features/test_feature_engine.py.

Strategy Lifecycle stores metadata only: it does not generate a
signal, does not run a strategy, and does not write to the database.
"""

import dataclasses

import pytest

from strategies.lifecycle.strategy_model import StrategyDefinition
from strategies.lifecycle.strategy_status import StrategyStatus
from strategies.lifecycle.strategy_registry import (
    StrategyRegistry,
    DuplicateStrategyIdError,
    DEFAULT_STRATEGIES,
    build_default_registry,
)


def _definition(id="TEST_STRATEGY", status=StrategyStatus.ACTIVE):
    return StrategyDefinition(
        id=id,
        name="Test Strategy",
        version="1.0",
        status=status,
        supported_assets=["XAUUSD"],
        supported_styles=["INTRADAY"],
        supported_timeframes=["M15"],
    )


def test_strategy_creation_matches_director_example():
    definition = StrategyDefinition(
        id="liquidity_sweep",
        name="Liquidity Sweep",
        version="1.0",
        status=StrategyStatus.ACTIVE,
        supported_assets=["GOLD"],
        supported_styles=["INTRADAY"],
        supported_timeframes=["M15"],
    )

    assert definition.id == "liquidity_sweep"
    assert definition.name == "Liquidity Sweep"
    assert definition.version == "1.0"
    assert definition.status == StrategyStatus.ACTIVE
    assert definition.supported_assets == ["GOLD"]
    assert definition.supported_styles == ["INTRADAY"]
    assert definition.supported_timeframes == ["M15"]
    # Future hooks -- never fabricated, always None unless explicitly passed.
    assert definition.performance is None
    assert definition.win_rate is None
    assert definition.last_validation is None


def test_registry_register_get_list():
    registry = StrategyRegistry()
    a = _definition(id="A")
    b = _definition(id="B")

    registry.register(a)
    registry.register(b)

    assert registry.get("A") is a
    assert registry.get("B") is b
    listed = registry.list()
    assert len(listed) == 2
    assert a in listed
    assert b in listed


def test_get_returns_none_for_unknown_id():
    registry = StrategyRegistry()
    assert registry.get("DOES_NOT_EXIST") is None


def test_duplicate_id_raises():
    registry = StrategyRegistry()
    registry.register(_definition(id="DUP"))

    with pytest.raises(DuplicateStrategyIdError):
        registry.register(_definition(id="DUP"))


def test_active_filter_excludes_non_active_statuses():
    registry = StrategyRegistry()
    registry.register(_definition(id="A", status=StrategyStatus.ACTIVE))
    registry.register(_definition(id="B", status=StrategyStatus.TESTING))
    registry.register(_definition(id="C", status=StrategyStatus.DISABLED))
    registry.register(_definition(id="D", status=StrategyStatus.DEPRECATED))

    active_ids = {d.id for d in registry.active()}
    assert active_ids == {"A"}


def test_status_transition_produces_a_new_immutable_definition():
    """StrategyDefinition is frozen -- a status transition is a new object, not a mutation."""
    testing = _definition(id="X", status=StrategyStatus.TESTING)
    promoted = dataclasses.replace(testing, status=StrategyStatus.ACTIVE)

    assert testing.status == StrategyStatus.TESTING  # original untouched
    assert promoted.status == StrategyStatus.ACTIVE
    assert promoted.id == testing.id  # only status changed

    with pytest.raises(dataclasses.FrozenInstanceError):
        testing.status = StrategyStatus.ACTIVE


def test_future_compatibility_field_shape_is_stable():
    """StrategyDefinition is a plain, introspectable dataclass -- a future consumer can rely on its field set."""
    field_names = {f.name for f in dataclasses.fields(StrategyDefinition)}
    assert field_names == {
        "id", "name", "version", "status", "supported_assets",
        "supported_styles", "supported_timeframes",
        "performance", "win_rate", "last_validation",
    }

    # Direct construction without the three hooks must still work (defaults apply).
    minimal = StrategyDefinition(
        id="MINIMAL", name="Minimal", version="1.0", status=StrategyStatus.TESTING,
        supported_assets=[], supported_styles=[], supported_timeframes=[],
    )
    assert minimal.performance is None
    assert minimal.win_rate is None
    assert minimal.last_validation is None


def test_default_registry_contains_only_existing_strategies():
    """
    build_default_registry() must register exactly the three strategies
    strategies/strategy_manager.py's StrategyManager already runs --
    LiquidityStrategy, FVGStrategy, AMDStrategy -- no new strategy, no
    strategy removed. ids must match the exact strategy_name string
    literals each strategy already produces (strategies/liquidity_strategy.py:45,
    strategies/fvg_strategy.py:45, strategies/amd_strategy.py:51).
    """
    registry = build_default_registry()
    ids = {d.id for d in registry.list()}

    assert ids == {"LIQUIDITY_SWEEP_STRATEGY", "FVG_STRATEGY", "AMD_STRATEGY"}
    assert len(DEFAULT_STRATEGIES) == 3

    # All three are the current production set -- none disabled/deprecated/testing-only.
    assert {d.status for d in registry.list()} == {StrategyStatus.ACTIVE}
    assert registry.active() == registry.list()


def test_default_registry_never_fabricates_performance():
    registry = build_default_registry()
    for definition in registry.list():
        assert definition.performance is None
        assert definition.win_rate is None
        assert definition.last_validation is None


def test_build_default_registry_returns_independent_instances():
    """Each call returns its own registry -- mutating one must not affect another."""
    first = build_default_registry()
    second = build_default_registry()

    first.register(_definition(id="EXTRA"))

    assert first.get("EXTRA") is not None
    assert second.get("EXTRA") is None
