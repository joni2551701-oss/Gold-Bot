"""
Phase A2 -- HTF Bias tests (context/htf_bias.py).

Builds synthetic multi-timeframe candle series directly (no live
Twelve Data call -- MarketSnapshot is constructed by hand, same
pattern mock_pipeline/conftest.py already use elsewhere in this
suite to avoid any live network dependency in a test run).

Scope: HTF Bias classification only (BULLISH/BEARISH/NEUTRAL/UNKNOWN),
confidence bounds, and quality_score -- not the pipeline integration
(covered by tests/integration/test_pipeline_flow.py's existing
mock_pipeline-based cases, which already exercise the new "htf_bias"
pipeline stage as part of every pipeline.run() call in that file).
"""

from datetime import datetime, timedelta, timezone

from context.htf_bias import compute_htf_bias, HTFBias, SUPPORTED_HTF_TIMEFRAMES
from data.market_data import MarketSnapshot
from data.twelve_data_client import Candle


def _trending_candles(direction: str, count: int = 30):
    """
    A zigzag candle series with a monotonic drift, producing a clean
    sequence of increasing (direction="up") or decreasing
    (direction="down") swing highs/lows for
    context.market_structure.detect_swing_points()/classify_structure()
    (default ContextConfig: swing_left_strength=swing_right_strength=2)
    to classify as HH/HL (up) or LH/LL (down).
    """
    sign = 1.0 if direction == "up" else -1.0
    base_ts = datetime(2024, 1, 1, tzinfo=timezone.utc)
    oscillation = {0: 0.0, 1: 3.0, 2: 0.0, 3: -3.0}

    candles = []
    for i in range(count):
        drift = sign * i
        mid = 100.0 + drift + oscillation[i % 4]
        candles.append(
            Candle(
                timestamp=base_ts + timedelta(days=i),
                open=mid,
                high=mid + 1.5,
                low=mid - 1.5,
                close=mid,
            )
        )
    return candles


def _snapshot(candles_by_tf, quality_by_tf=None):
    quality = quality_by_tf or {tf: "OK" for tf in candles_by_tf}
    return MarketSnapshot(symbol="XAUUSD", candles=candles_by_tf, quality=quality)


def test_all_timeframes_bullish_returns_bullish():
    up = _trending_candles("up")
    snapshot = _snapshot({tf: up for tf in SUPPORTED_HTF_TIMEFRAMES})

    result = compute_htf_bias(snapshot)

    assert result.bias == HTFBias.BULLISH
    assert result.confidence == 100.0
    assert set(result.timeframes) == set(SUPPORTED_HTF_TIMEFRAMES)


def test_all_timeframes_bearish_returns_bearish():
    down = _trending_candles("down")
    snapshot = _snapshot({tf: down for tf in SUPPORTED_HTF_TIMEFRAMES})

    result = compute_htf_bias(snapshot)

    assert result.bias == HTFBias.BEARISH
    assert result.confidence == 100.0


def test_split_timeframes_returns_neutral():
    """Daily bullish, H4 bearish, H1 has no data -> a genuine 1-1 tie."""
    up = _trending_candles("up")
    down = _trending_candles("down")
    snapshot = _snapshot(
        {"Daily": up, "H4": down, "H1": []},
        quality_by_tf={"Daily": "OK", "H4": "OK", "H1": "ERROR_NO_DATA"},
    )

    result = compute_htf_bias(snapshot)

    assert result.bias == HTFBias.NEUTRAL
    assert result.confidence == 50.0


def test_missing_data_returns_unknown():
    """No candle data for any HTF timeframe -> UNKNOWN, confidence 0."""
    snapshot = MarketSnapshot(symbol="XAUUSD")  # empty candles + quality dicts

    result = compute_htf_bias(snapshot)

    assert result.bias == HTFBias.UNKNOWN
    assert result.confidence == 0.0
    assert result.timeframes == ()


def test_insufficient_candles_per_timeframe_returns_unknown():
    """A timeframe with candles but too few to confirm any swing stays UNKNOWN."""
    tiny = _trending_candles("up", count=3)  # fewer than left+right+1 = 5
    snapshot = _snapshot({tf: tiny for tf in SUPPORTED_HTF_TIMEFRAMES})

    result = compute_htf_bias(snapshot)

    assert result.bias == HTFBias.UNKNOWN
    assert result.confidence == 0.0


def test_confidence_always_within_0_to_100():
    scenarios = [
        _snapshot({tf: _trending_candles("up") for tf in SUPPORTED_HTF_TIMEFRAMES}),
        _snapshot({tf: _trending_candles("down") for tf in SUPPORTED_HTF_TIMEFRAMES}),
        _snapshot({"Daily": _trending_candles("up"), "H4": [], "H1": []}),
        MarketSnapshot(symbol="XAUUSD"),
    ]

    for snapshot in scenarios:
        result = compute_htf_bias(snapshot)
        assert 0.0 <= result.confidence <= 100.0


def test_quality_score_reflects_snapshot_quality_dict():
    up = _trending_candles("up")

    all_ok = _snapshot({tf: up for tf in SUPPORTED_HTF_TIMEFRAMES})
    assert compute_htf_bias(all_ok).quality_score == 1.0

    no_quality_data = MarketSnapshot(symbol="XAUUSD")
    assert compute_htf_bias(no_quality_data).quality_score == 0.0

    partial = _snapshot(
        {"Daily": up, "H4": up, "H1": up},
        quality_by_tf={"Daily": "OK", "H4": "WARNING_GAP", "H1": "OK"},
    )
    assert compute_htf_bias(partial).quality_score == round(2 / 3, 2)


def test_result_never_raises_on_malformed_quality_dict():
    """quality_score reads via .get() -- a missing key must not raise."""
    up = _trending_candles("up")
    snapshot = MarketSnapshot(
        symbol="XAUUSD",
        candles={tf: up for tf in SUPPORTED_HTF_TIMEFRAMES},
        quality={},  # no quality info at all
    )

    result = compute_htf_bias(snapshot)

    assert result.bias == HTFBias.BULLISH
    assert result.quality_score == 0.0


def test_supported_timeframes_are_exactly_daily_h4_h1():
    """Task 3: Daily/H4/H1 only -- no M1/M5 in the HTF set."""
    assert set(SUPPORTED_HTF_TIMEFRAMES) == {"Daily", "H4", "H1"}
    assert "M1" not in SUPPORTED_HTF_TIMEFRAMES
    assert "M5" not in SUPPORTED_HTF_TIMEFRAMES
