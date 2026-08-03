"""Setup layer — Reversal strategy (TASK-CORE-007)."""

from types import SimpleNamespace

from context_layer.market_structure.choch import ChochDirection
from context_layer.liquidity.liquidity import LiquidityType

from strategies.reversal_strategy import ReversalStrategy
from strategies.result import StrategyDirection, SetupStatus


def _choch(index, direction, price=105.0):
    return SimpleNamespace(index=index, direction=direction,
                           broken_structure=SimpleNamespace(swing=SimpleNamespace(price=price)))


def test_bullish_reversal_from_choch(make_ctx):
    ctx = make_ctx(choch_events=[_choch(8, ChochDirection.BULLISH)])
    r = ReversalStrategy().evaluate(ctx)
    assert r.status is SetupStatus.SETUP_FOUND
    assert r.direction is StrategyDirection.LONG
    assert r.metadata["sweep_confirmed"] is False
    assert r.confidence == 0.65


def test_sweep_confirmed_reversal_is_stronger(make_ctx):
    ctx = make_ctx(
        choch_events=[_choch(8, ChochDirection.BULLISH)],
        liquidity_sweeps=[SimpleNamespace(index=6, type=LiquidityType.SSL, sweep_price=95.0)],
    )
    r = ReversalStrategy().evaluate(ctx)
    assert r.metadata["sweep_confirmed"] is True
    assert r.confidence == 0.8
    assert r.invalidation == 95.0


def test_no_choch_is_no_setup(make_ctx):
    r = ReversalStrategy().evaluate(make_ctx(candles=[SimpleNamespace(close=1.0)]))
    assert r.status is SetupStatus.NO_SETUP
