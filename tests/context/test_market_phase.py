"""
Pre-Phase 59 Architecture Readiness Review, AC-02 -- MarketPhase
classifier tests (context_layer/trend/market_phase.py).

No mocking -- real ContextSnapshot/WyckoffEvent/AmdEvent/
MarketRegimeResult objects, same convention as
tests/features/test_feature_engine.py.
"""

from datetime import datetime, timezone

from context_layer.context_engine.context_orchestrator import ContextSnapshot
from context_layer.trend.market_phase import MarketPhase, compute_market_phase
from context_layer.trend.market_regime import MarketRegimeResult, MarketRegime, RegimeDirection
from context_layer.wyckoff.wyckoff import WyckoffEvent, WyckoffEventType, WyckoffPhase
from context_layer.amd.amd import AmdEvent, AmdEventType
from context_layer.liquidity.liquidity import LiquidityZone, LiquiditySweepEvent, LiquidityType

TS = datetime(2024, 1, 2, 9, 0, tzinfo=timezone.utc)


def _empty_context(**overrides) -> ContextSnapshot:
    base = dict(
        candles=(), structure=(), bos_events=(), choch_events=(),
        liquidity_zones=(), liquidity_sweeps=(), order_blocks=(), fair_value_gaps=(),
        amd_events=(), wyckoff_events=(), session_events=(),
        market_regime=MarketRegimeResult(regime=MarketRegime.UNKNOWN, direction=RegimeDirection.NEUTRAL, confidence=0.0, reasons=[]),
    )
    base.update(overrides)
    return ContextSnapshot(**base)


def _wyckoff_event(phase: WyckoffPhase) -> WyckoffEvent:
    zone = LiquidityZone(price=100.0, type=LiquidityType.SSL, start_index=0, end_index=1, strength=2)
    sweep = LiquiditySweepEvent(index=1, timestamp=TS, type=LiquidityType.SSL, sweep_price=99.5, zone=zone)
    event_type = WyckoffEventType.SPRING if phase == WyckoffPhase.ACCUMULATION else WyckoffEventType.UPTHRUST
    return WyckoffEvent(
        type=event_type, phase=phase, index=5, timestamp=TS,
        sweep=sweep, confirming_break_index=5, volume_confirmed=None,
    )


def _amd_event(event_type: AmdEventType) -> AmdEvent:
    return AmdEvent(type=event_type, index=3, timestamp=TS, is_bullish=True)


def test_wyckoff_accumulation_takes_top_priority():
    context = _empty_context(wyckoff_events=(_wyckoff_event(WyckoffPhase.ACCUMULATION),))
    result = compute_market_phase(context)
    assert result.phase == MarketPhase.ACCUMULATION
    assert "Wyckoff" in result.reason


def test_wyckoff_distribution_takes_top_priority():
    context = _empty_context(wyckoff_events=(_wyckoff_event(WyckoffPhase.DISTRIBUTION),))
    result = compute_market_phase(context)
    assert result.phase == MarketPhase.DISTRIBUTION


def test_wyckoff_outranks_amd_and_regime():
    """Even with a contradicting AMD event and TRENDING regime present, the most recent Wyckoff event wins."""
    context = _empty_context(
        wyckoff_events=(_wyckoff_event(WyckoffPhase.ACCUMULATION),),
        amd_events=(_amd_event(AmdEventType.DISTRIBUTION),),
        market_regime=MarketRegimeResult(regime=MarketRegime.TRENDING, direction=RegimeDirection.BEARISH, confidence=90.0, reasons=[]),
    )
    result = compute_market_phase(context)
    assert result.phase == MarketPhase.ACCUMULATION


def test_amd_manipulation_used_when_no_wyckoff_event():
    context = _empty_context(amd_events=(_amd_event(AmdEventType.MANIPULATION),))
    result = compute_market_phase(context)
    assert result.phase == MarketPhase.MANIPULATION
    assert "AMD" in result.reason


def test_amd_distribution_used_when_no_wyckoff_event():
    context = _empty_context(amd_events=(_amd_event(AmdEventType.DISTRIBUTION),))
    result = compute_market_phase(context)
    assert result.phase == MarketPhase.DISTRIBUTION


def test_amd_outranks_market_regime():
    context = _empty_context(
        amd_events=(_amd_event(AmdEventType.MANIPULATION),),
        market_regime=MarketRegimeResult(regime=MarketRegime.TRENDING, direction=RegimeDirection.BULLISH, confidence=90.0, reasons=[]),
    )
    result = compute_market_phase(context)
    assert result.phase == MarketPhase.MANIPULATION


def test_trending_bullish_regime_maps_to_markup():
    context = _empty_context(
        market_regime=MarketRegimeResult(regime=MarketRegime.TRENDING, direction=RegimeDirection.BULLISH, confidence=80.0, reasons=[]),
    )
    result = compute_market_phase(context)
    assert result.phase == MarketPhase.MARKUP


def test_trending_bearish_regime_maps_to_markdown():
    context = _empty_context(
        market_regime=MarketRegimeResult(regime=MarketRegime.TRENDING, direction=RegimeDirection.BEARISH, confidence=80.0, reasons=[]),
    )
    result = compute_market_phase(context)
    assert result.phase == MarketPhase.MARKDOWN


def test_trending_neutral_direction_falls_through_to_unknown():
    """A TRENDING regime with NEUTRAL direction matches neither MARKUP nor MARKDOWN -- must not fabricate a direction."""
    context = _empty_context(
        market_regime=MarketRegimeResult(regime=MarketRegime.TRENDING, direction=RegimeDirection.NEUTRAL, confidence=80.0, reasons=[]),
    )
    result = compute_market_phase(context)
    assert result.phase == MarketPhase.UNKNOWN


def test_range_regime_is_unknown():
    context = _empty_context(
        market_regime=MarketRegimeResult(regime=MarketRegime.RANGE, direction=RegimeDirection.NEUTRAL, confidence=50.0, reasons=[]),
    )
    result = compute_market_phase(context)
    assert result.phase == MarketPhase.UNKNOWN


def test_completely_empty_context_never_raises():
    result = compute_market_phase(_empty_context())
    assert result.phase == MarketPhase.UNKNOWN


def test_all_six_phase_values_exist():
    assert {p.value for p in MarketPhase} == {
        "ACCUMULATION", "MANIPULATION", "DISTRIBUTION", "MARKUP", "MARKDOWN", "UNKNOWN",
    }
