"""
TASK-CORE-006 gap-fill — dedicated unit tests for context_layer/order_block/order_block.py.

Read-only exercise of the existing frozen detect_order_blocks(): the
last opposing candle before a sweep-induced structural break. A bullish
OB = last bearish candle before an SSL sweep + bullish break; a bearish
OB = last bullish candle before a BSL sweep + bearish break.
"""

from datetime import datetime, timedelta, timezone

from data_layer.providers.twelve_data_client import Candle

from context_layer.liquidity.liquidity import LiquidityType, LiquidityZone, LiquiditySweepEvent
from context_layer.market_structure.bos import BosEvent, BosDirection
from context_layer.order_block.order_block import detect_order_blocks, OrderBlockType
from context_layer.market_structure.market_structure import SwingPoint, SwingType, StructurePoint, StructureType

BASE = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _c(i, open_, close):
    return Candle(timestamp=BASE + timedelta(minutes=15 * i),
                  open=open_, high=max(open_, close) + 1, low=min(open_, close) - 1, close=close)


def _ts(i):
    return BASE + timedelta(minutes=15 * i)


def _zone(ltype):
    return LiquidityZone(price=100.0, type=ltype, start_index=0, end_index=1, strength=2)


def _struct(index):
    return StructurePoint(SwingPoint(index=index, price=100.0, timestamp=_ts(index), type=SwingType.HIGH),
                          StructureType.HIGHER_HIGH)


def test_bullish_order_block_from_ssl_sweep_and_bullish_break():
    # idx1 bearish (10->8), idx2 bullish (8->10); sweep at 3 (SSL), bullish BOS at 4.
    candles = [_c(0, 9, 9), _c(1, 10, 8), _c(2, 8, 10), _c(3, 9, 9), _c(4, 9, 12)]
    sweeps = [LiquiditySweepEvent(3, _ts(3), LiquidityType.SSL, 7.0, _zone(LiquidityType.SSL))]
    bos = [BosEvent(4, _ts(4), BosDirection.BULLISH, _struct(2))]
    obs = detect_order_blocks(candles, sweeps, bos, [])
    assert len(obs) == 1
    assert obs[0].type is OrderBlockType.BULLISH
    assert obs[0].index == 1  # last bearish candle before the sweep


def test_bearish_order_block_from_bsl_sweep_and_bearish_break():
    # idx1 bullish (8->10), idx2 bearish (10->8); sweep at 3 (BSL), bearish BOS at 4.
    candles = [_c(0, 9, 9), _c(1, 8, 10), _c(2, 10, 8), _c(3, 9, 9), _c(4, 12, 7)]
    sweeps = [LiquiditySweepEvent(3, _ts(3), LiquidityType.BSL, 101.0, _zone(LiquidityType.BSL))]
    bos = [BosEvent(4, _ts(4), BosDirection.BEARISH, _struct(2))]
    obs = detect_order_blocks(candles, sweeps, bos, [])
    assert len(obs) == 1
    assert obs[0].type is OrderBlockType.BEARISH
    # Scanning back from the sweep, idx2 is bearish, so the last *bullish* candle is idx1.
    assert obs[0].index == 1


def test_no_order_block_without_a_following_break():
    candles = [_c(0, 10, 8), _c(1, 10, 8), _c(2, 9, 9)]
    sweeps = [LiquiditySweepEvent(2, _ts(2), LiquidityType.SSL, 7.0, _zone(LiquidityType.SSL))]
    assert detect_order_blocks(candles, sweeps, [], []) == []


def test_no_sweeps_is_empty():
    candles = [_c(0, 10, 8), _c(1, 8, 10)]
    assert detect_order_blocks(candles, [], [], []) == []
