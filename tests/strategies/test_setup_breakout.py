"""Setup layer — Breakout / failed-breakout strategy (TASK-CORE-007)."""

from types import SimpleNamespace

from context_layer.liquidity.liquidity import LiquidityType
from context_layer.market_structure.bos import BosDirection

from strategies.breakout_strategy import BreakoutStrategy
from strategies.result import StrategyDirection, SetupStatus


def test_confirmed_breakout_long(make_ctx):
    ctx = make_ctx(
        liquidity_sweeps=[SimpleNamespace(index=5, type=LiquidityType.SSL, sweep_price=99.0)],
        bos_events=[SimpleNamespace(index=7, direction=BosDirection.BULLISH)],
    )
    r = BreakoutStrategy().evaluate(ctx)
    assert r.status is SetupStatus.SETUP_FOUND
    assert r.direction is StrategyDirection.LONG
    assert r.metadata["kind"] == "breakout"


def test_failed_breakout_reverses(make_ctx):
    # SSL sweep with no confirming bullish break -> failed breakout -> LONG reversal.
    ctx = make_ctx(liquidity_sweeps=[SimpleNamespace(index=5, type=LiquidityType.SSL, sweep_price=99.0)])
    r = BreakoutStrategy().evaluate(ctx)
    assert r.metadata["kind"] == "failed_breakout"
    assert r.direction is StrategyDirection.LONG
    assert r.confidence == 0.6


def test_no_sweep_is_no_setup(make_ctx):
    r = BreakoutStrategy().evaluate(make_ctx(candles=[SimpleNamespace(close=1.0)]))
    assert r.status is SetupStatus.NO_SETUP
