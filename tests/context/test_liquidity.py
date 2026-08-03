"""
TASK-CORE-006 gap-fill — dedicated unit tests for context_layer/liquidity/liquidity.py.

Read-only exercise of the existing frozen detectors: detect_equal_levels
clusters near-equal swing highs into BSL (buy-side) and near-equal swing
lows into SSL (sell-side) zones; detect_sweeps flags a wick through a
zone that closes back inside it.
"""

from datetime import datetime, timedelta, timezone

from data_layer.providers.twelve_data_client import Candle

from context_layer.liquidity.liquidity import (
    LiquidityType,
    LiquidityZone,
    detect_equal_levels,
    detect_sweeps,
)
from context_layer.market_structure.market_structure import SwingPoint, SwingType

BASE = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _swing(index, price, stype):
    return SwingPoint(index=index, price=price, timestamp=BASE + timedelta(minutes=15 * index), type=stype)


def _c(i, high, low, close):
    return Candle(timestamp=BASE + timedelta(minutes=15 * i), open=close, high=high, low=low, close=close)


def test_equal_highs_form_buy_side_zone():
    swings = [_swing(0, 100.0, SwingType.HIGH), _swing(2, 100.4, SwingType.HIGH)]
    zones = detect_equal_levels(swings, tolerance=0.5)
    assert len(zones) == 1
    assert zones[0].type is LiquidityType.BSL
    assert zones[0].strength == 2
    assert abs(zones[0].price - 100.2) < 1e-9


def test_equal_lows_form_sell_side_zone():
    swings = [_swing(0, 50.0, SwingType.LOW), _swing(2, 49.8, SwingType.LOW)]
    zones = detect_equal_levels(swings, tolerance=0.5)
    assert len(zones) == 1
    assert zones[0].type is LiquidityType.SSL


def test_far_apart_swings_form_no_zone():
    swings = [_swing(0, 100.0, SwingType.HIGH), _swing(2, 110.0, SwingType.HIGH)]
    assert detect_equal_levels(swings, tolerance=0.5) == []


def test_sweep_of_buy_side_zone():
    zone = LiquidityZone(price=100.0, type=LiquidityType.BSL, start_index=0, end_index=2, strength=2)
    # idx 3 wicks above 100 (high 101) but closes back below (99) -> BSL sweep.
    candles = [_c(0, 100, 98, 99), _c(1, 100, 98, 99), _c(2, 100, 98, 99), _c(3, 101, 98, 99)]
    sweeps = detect_sweeps(candles, [zone])
    assert len(sweeps) == 1
    assert sweeps[0].type is LiquidityType.BSL
    assert sweeps[0].index == 3


def test_sweep_of_sell_side_zone():
    zone = LiquidityZone(price=50.0, type=LiquidityType.SSL, start_index=0, end_index=2, strength=2)
    # idx 3 wicks below 50 (low 49) but closes back above (51) -> SSL sweep.
    candles = [_c(0, 52, 50, 51), _c(1, 52, 50, 51), _c(2, 52, 50, 51), _c(3, 52, 49, 51)]
    sweeps = detect_sweeps(candles, [zone])
    assert len(sweeps) == 1
    assert sweeps[0].type is LiquidityType.SSL


def test_no_sweep_without_penetration():
    zone = LiquidityZone(price=100.0, type=LiquidityType.BSL, start_index=0, end_index=1, strength=2)
    candles = [_c(0, 99, 97, 98), _c(1, 99, 97, 98), _c(2, 99, 97, 98)]
    assert detect_sweeps(candles, [zone]) == []
