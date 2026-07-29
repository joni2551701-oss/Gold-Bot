"""Setup layer — Support/Resistance strategy (TASK-CORE-007, Director-required)."""

from types import SimpleNamespace

from context.liquidity import LiquidityType

from strategies.snr_strategy import SNRStrategy
from strategies.result import StrategyDirection, SetupStatus


def _zone(price, ltype, start=0, end=2, strength=2):
    return SimpleNamespace(price=price, type=ltype, start_index=start, end_index=end, strength=strength)


def test_support_bounce_is_long(make_ctx):
    ctx = make_ctx(
        liquidity_zones=[_zone(100.0, LiquidityType.SSL)],
        candles=[SimpleNamespace(close=100.1)],  # just above support, within tol
    )
    r = SNRStrategy().evaluate(ctx)
    assert r.status is SetupStatus.SETUP_FOUND
    assert r.direction is StrategyDirection.LONG
    assert "support bounce" in r.metadata["pattern"]


def test_resistance_rejection_is_short(make_ctx):
    ctx = make_ctx(
        liquidity_zones=[_zone(100.0, LiquidityType.BSL)],
        candles=[SimpleNamespace(close=99.9)],  # just below resistance, within tol
    )
    r = SNRStrategy().evaluate(ctx)
    assert r.direction is StrategyDirection.SHORT
    assert r.metadata["pattern"] == "resistance rejection"


def test_support_break_is_short(make_ctx):
    ctx = make_ctx(
        liquidity_zones=[_zone(100.0, LiquidityType.SSL)],
        candles=[SimpleNamespace(close=90.0)],  # well below support
    )
    r = SNRStrategy().evaluate(ctx)
    assert r.metadata["pattern"] == "support break"
    assert r.direction is StrategyDirection.SHORT


def test_resistance_break_is_long(make_ctx):
    ctx = make_ctx(
        liquidity_zones=[_zone(100.0, LiquidityType.BSL)],
        candles=[SimpleNamespace(close=110.0)],  # well above resistance
    )
    r = SNRStrategy().evaluate(ctx)
    assert r.metadata["pattern"] == "resistance break"
    assert r.direction is StrategyDirection.LONG


def test_retest_confluence_raises_confidence(make_ctx):
    ctx = make_ctx(
        liquidity_zones=[_zone(100.0, LiquidityType.SSL, start=0, end=2)],
        candles=[SimpleNamespace(close=100.1)],
        bos_events=[SimpleNamespace(index=1)],  # break inside the zone window
    )
    r = SNRStrategy().evaluate(ctx)
    assert r.metadata["confluence"] is True
    assert r.confidence == 0.7


def test_no_zones_is_no_setup(make_ctx):
    r = SNRStrategy().evaluate(make_ctx(candles=[SimpleNamespace(close=100.0)]))
    assert r.status is SetupStatus.NO_SETUP
