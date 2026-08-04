"""
Feature Layer — Average True Range (GFL-001 FLOW-007, Indicator Engine).

compute_atr() fills the atr hook that core_layer/features/feature_engine.py
and core_layer/features/feature_model.py have carried since Phase A10
(previously always None, "an explicit hook for a future phase" -- see
both modules' own docstrings). Output is consumed only by
MarketFeatures, which feature_engine.py's own docstring already
documents as purely advisory: not passed into
SignalEngine/AIAnalyzer/DecisionEngine/RiskManager in this phase.

Wilder's smoothing (the textbook ATR definition): True Range is the
greatest of (high-low), abs(high-prev_close), abs(low-prev_close);
the first ATR is a simple average of the first `period` True Range
values, every subsequent value is a running smoothed average. Assumes
candles are in chronological (oldest-first) order -- the same
convention ContextSnapshot.candles and every other context_layer
detector already relies on.
"""

from typing import Optional, Sequence


def compute_atr(candles: Sequence, period: int = 14) -> Optional[float]:
    """
    Never raises: fewer than period + 1 candles (not enough closed bars
    to derive `period` True Range values) returns None, not an error
    or a fabricated value.
    """
    if period <= 0 or len(candles) < period + 1:
        return None

    true_ranges = []
    for i in range(1, len(candles)):
        high = candles[i].high
        low = candles[i].low
        prev_close = candles[i - 1].close
        true_ranges.append(max(
            high - low,
            abs(high - prev_close),
            abs(low - prev_close),
        ))

    atr = sum(true_ranges[:period]) / period
    for tr in true_ranges[period:]:
        atr = (atr * (period - 1) + tr) / period

    return round(atr, 5)
