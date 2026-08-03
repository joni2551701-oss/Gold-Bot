"""Setup layer — Order Block strategy (TASK-CORE-007)."""

from types import SimpleNamespace

from context_layer.order_block.order_block import OrderBlockType

from strategies.ob_strategy import OBStrategy
from strategies.result import StrategyDirection, SetupStatus


def test_bullish_ob_retest_when_price_in_zone(make_ctx):
    ctx = make_ctx(
        order_blocks=[SimpleNamespace(index=5, type=OrderBlockType.BULLISH, low=100.0, high=105.0)],
        candles=[SimpleNamespace(close=102.0)],
    )
    r = OBStrategy().evaluate(ctx)
    assert r.status is SetupStatus.SETUP_FOUND
    assert r.direction is StrategyDirection.LONG
    assert r.entry_zone == (100.0, 105.0)
    assert r.invalidation == 100.0
    assert r.metadata["at_zone"] is True
    assert r.confidence == 0.68


def test_bearish_ob_pending_when_price_away(make_ctx):
    ctx = make_ctx(
        order_blocks=[SimpleNamespace(index=5, type=OrderBlockType.BEARISH, low=100.0, high=105.0)],
        candles=[SimpleNamespace(close=120.0)],
    )
    r = OBStrategy().evaluate(ctx)
    assert r.direction is StrategyDirection.SHORT
    assert r.metadata["at_zone"] is False
    assert r.confidence == 0.55


def test_no_ob_is_no_setup(make_ctx):
    r = OBStrategy().evaluate(make_ctx(candles=[SimpleNamespace(close=1.0)]))
    assert r.status is SetupStatus.NO_SETUP
