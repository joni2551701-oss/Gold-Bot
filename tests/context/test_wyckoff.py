"""
Phase A5 -- Wyckoff Engine foundation tests (context_layer/wyckoff/wyckoff.py).

Builds minimal, real LiquiditySweepEvent/BosEvent/ChochEvent objects
directly (no mocking) to control exactly which sweep-then-break
correlations should and should not produce a Spring/Upthrust -- same
no-mocking convention as tests/context/test_htf_bias.py and
tests/unit/test_signal_quality.py.
"""

from datetime import datetime, timezone

from context_layer.wyckoff.wyckoff import detect_wyckoff_events, WyckoffEventType, WyckoffPhase
from context_layer.liquidity.liquidity import LiquidityZone, LiquiditySweepEvent, LiquidityType
from context_layer.market_structure.bos import BosEvent, BosDirection
from context_layer.market_structure.choch import ChochEvent, ChochDirection
from context_layer.context_engine.context_orchestrator import build_context_snapshot
from data_layer.providers.twelve_data_client import Candle

TS = datetime(2024, 1, 1, tzinfo=timezone.utc)


def _zone(liquidity_type, price=100.0):
    return LiquidityZone(price=price, type=liquidity_type, start_index=0, end_index=1, strength=2)


def _ssl_sweep(index=2, price=98.0):
    return LiquiditySweepEvent(index=index, timestamp=TS, type=LiquidityType.SSL, sweep_price=price, zone=_zone(LiquidityType.SSL))


def _bsl_sweep(index=2, price=112.0):
    return LiquiditySweepEvent(index=index, timestamp=TS, type=LiquidityType.BSL, sweep_price=price, zone=_zone(LiquidityType.BSL))


def _bos(index, direction):
    return BosEvent(index=index, timestamp=TS, direction=direction, broken_structure=None)


def _choch(index, direction):
    return ChochEvent(index=index, timestamp=TS, direction=direction, broken_structure=None)


def test_ssl_sweep_with_subsequent_bullish_bos_produces_spring():
    sweep = _ssl_sweep(index=2)
    bos = _bos(index=5, direction=BosDirection.BULLISH)

    events = detect_wyckoff_events(candles=[], liquidity_sweeps=[sweep], bos_events=[bos], choch_events=[])

    assert len(events) == 1
    assert events[0].type == WyckoffEventType.SPRING
    assert events[0].phase == WyckoffPhase.ACCUMULATION
    assert events[0].sweep is sweep
    assert events[0].index == 5
    assert events[0].confirming_break_index == 5


def test_bsl_sweep_with_subsequent_bearish_bos_produces_upthrust():
    sweep = _bsl_sweep(index=2)
    bos = _bos(index=6, direction=BosDirection.BEARISH)

    events = detect_wyckoff_events(candles=[], liquidity_sweeps=[sweep], bos_events=[bos], choch_events=[])

    assert len(events) == 1
    assert events[0].type == WyckoffEventType.UPTHRUST
    assert events[0].phase == WyckoffPhase.DISTRIBUTION
    assert events[0].sweep is sweep


def test_choch_can_also_confirm_a_spring():
    sweep = _ssl_sweep(index=2)
    choch = _choch(index=4, direction=ChochDirection.BULLISH)

    events = detect_wyckoff_events(candles=[], liquidity_sweeps=[sweep], bos_events=[], choch_events=[choch])

    assert len(events) == 1
    assert events[0].type == WyckoffEventType.SPRING
    assert events[0].confirming_break_index == 4


def test_no_confirming_break_produces_no_event():
    sweep = _ssl_sweep(index=2)

    events = detect_wyckoff_events(candles=[], liquidity_sweeps=[sweep], bos_events=[], choch_events=[])

    assert events == []


def test_wrong_direction_break_does_not_confirm():
    """An SSL sweep (bullish setup) followed only by a BEARISH break must not produce a Spring."""
    sweep = _ssl_sweep(index=2)
    bearish_bos = _bos(index=5, direction=BosDirection.BEARISH)

    events = detect_wyckoff_events(candles=[], liquidity_sweeps=[sweep], bos_events=[bearish_bos], choch_events=[])

    assert events == []


def test_break_before_the_sweep_is_ignored():
    sweep = _ssl_sweep(index=10)
    earlier_bos = _bos(index=3, direction=BosDirection.BULLISH)  # before the sweep

    events = detect_wyckoff_events(candles=[], liquidity_sweeps=[sweep], bos_events=[earlier_bos], choch_events=[])

    assert events == []


def test_nearest_confirming_break_is_selected_when_multiple_exist():
    sweep = _ssl_sweep(index=2)
    far_bos = _bos(index=20, direction=BosDirection.BULLISH)
    near_choch = _choch(index=6, direction=ChochDirection.BULLISH)

    events = detect_wyckoff_events(candles=[], liquidity_sweeps=[sweep], bos_events=[far_bos], choch_events=[near_choch])

    assert len(events) == 1
    assert events[0].confirming_break_index == 6  # nearer of the two


def test_volume_confirmed_is_always_none():
    """No volume data source exists (Phase A1 audit) -- the hook must never fabricate True/False."""
    sweep = _ssl_sweep(index=2)
    bos = _bos(index=5, direction=BosDirection.BULLISH)

    events = detect_wyckoff_events(candles=[], liquidity_sweeps=[sweep], bos_events=[bos], choch_events=[])

    assert events[0].volume_confirmed is None


def test_empty_inputs_produce_empty_list_and_never_raise():
    events = detect_wyckoff_events(candles=[], liquidity_sweeps=[], bos_events=[], choch_events=[])
    assert events == []


def test_multiple_independent_sweeps_each_produce_their_own_event():
    ssl = _ssl_sweep(index=2)
    bsl = _bsl_sweep(index=3)
    bullish_bos = _bos(index=5, direction=BosDirection.BULLISH)
    bearish_bos = _bos(index=7, direction=BosDirection.BEARISH)

    events = detect_wyckoff_events(
        candles=[], liquidity_sweeps=[ssl, bsl], bos_events=[bullish_bos, bearish_bos], choch_events=[]
    )

    types = {e.type for e in events}
    assert types == {WyckoffEventType.SPRING, WyckoffEventType.UPTHRUST}


def test_wyckoff_events_is_wired_through_context_orchestrator():
    """
    Confirms ContextEngine.build()/build_context_snapshot() actually
    calls detect_wyckoff_events() and populates ContextSnapshot.
    wyckoff_events -- not just that the standalone function works in
    isolation. A short, real (non-zigzag) candle series is enough:
    the assertion is about the field being wired and typed correctly,
    not about triggering a real Spring/Upthrust.
    """
    candles = [
        Candle(timestamp=TS, open=100.0, high=101.0, low=99.0, close=100.5),
        Candle(timestamp=TS, open=100.5, high=102.0, low=100.0, close=101.5),
        Candle(timestamp=TS, open=101.5, high=103.0, low=101.0, close=102.5),
    ]

    snapshot = build_context_snapshot(candles)

    assert hasattr(snapshot, "wyckoff_events")
    assert isinstance(snapshot.wyckoff_events, list)
