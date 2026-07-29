"""Setup layer — Trend continuation strategy (TASK-CORE-007)."""

from types import SimpleNamespace

from context.market_structure import StructureType

from strategies.trend_strategy import TrendStrategy
from strategies.result import StrategyDirection, SetupStatus


def _regime(name, direction, conf=85.0):
    return SimpleNamespace(regime=SimpleNamespace(value=name),
                           direction=SimpleNamespace(value=direction), confidence=conf)


def test_trend_long_when_structure_and_regime_agree(make_ctx):
    ctx = make_ctx(
        structure=[SimpleNamespace(structure=StructureType.HIGHER_HIGH)],
        market_regime=_regime("TRENDING", "BULLISH"),
    )
    r = TrendStrategy().evaluate(ctx)
    assert r.status is SetupStatus.SETUP_FOUND
    assert r.direction is StrategyDirection.LONG
    assert r.confidence > 0.6  # boosted by agreeing TRENDING regime


def test_no_setup_when_regime_contradicts(make_ctx):
    ctx = make_ctx(
        structure=[SimpleNamespace(structure=StructureType.HIGHER_HIGH)],  # bullish
        market_regime=_regime("TRENDING", "BEARISH"),
    )
    r = TrendStrategy().evaluate(ctx)
    assert r.status is SetupStatus.NO_SETUP


def test_no_bias_is_no_setup(make_ctx):
    ctx = make_ctx(structure=[SimpleNamespace(structure=StructureType.UNKNOWN)],
                   market_regime=_regime("RANGE", "NEUTRAL"))
    r = TrendStrategy().evaluate(ctx)
    assert r.status is SetupStatus.NO_SETUP
