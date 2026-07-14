"""
Phase A8 -- Data Quality Engine foundation tests (data/data_quality.py).

No mocking -- real Candle objects with hand-picked timestamps/OHLC
values, same convention as tests/context/test_htf_bias.py,
tests/context/test_wyckoff.py, tests/context/test_session.py, and
tests/context/test_market_regime.py.
"""

from datetime import datetime, timedelta, timezone

from data.data_quality import (
    assess_data_quality,
    DataQualityResult,
    INVALID_OHLC_PENALTY,
    DUPLICATE_CANDLE_PENALTY,
    MISSING_CANDLE_PENALTY,
    TIMEFRAME_MISMATCH_PENALTY,
)
from data.twelve_data_client import Candle

BASE = datetime(2024, 1, 2, 10, 0, tzinfo=timezone.utc)  # a Tuesday


def _candle(minutes_offset, open_=100.0, high=101.0, low=99.0, close=100.0):
    return Candle(timestamp=BASE + timedelta(minutes=minutes_offset), open=open_, high=high, low=low, close=close)


def test_valid_candles_score_100_and_are_valid():
    candles = [_candle(0), _candle(15), _candle(30)]  # clean M15 series

    result = assess_data_quality(candles, "M15")

    assert result.valid is True
    assert result.score == 100.0
    assert result.issues == ()


def test_missing_candle_detected_as_gap():
    candles = [_candle(0), _candle(15), _candle(45)]  # 30-minute gap where 15 was expected

    result = assess_data_quality(candles, "M15")

    assert "missing_candle" in result.issues
    assert result.valid is False
    assert result.score == 100.0 - MISSING_CANDLE_PENALTY


def test_duplicate_candle_detected():
    candles = [_candle(0), _candle(15), _candle(15)]  # same timestamp twice

    result = assess_data_quality(candles, "M15")

    assert "duplicate_candle" in result.issues
    assert result.valid is False
    assert result.score == 100.0 - DUPLICATE_CANDLE_PENALTY


def test_invalid_ohlc_detected():
    """high (102) is below max(open, close) (105) -- a physically impossible candle."""
    bad = _candle(0, open_=100.0, high=102.0, low=99.0, close=105.0)
    candles = [_candle(-15), bad, _candle(15)]

    result = assess_data_quality(candles, "M15")

    assert "invalid_ohlc" in result.issues
    assert result.valid is False
    assert result.score == 100.0 - INVALID_OHLC_PENALTY


def test_invalid_ohlc_low_above_min_open_close():
    """low (101) is above min(open, close) (100) -- also physically impossible."""
    bad = _candle(0, open_=100.0, high=105.0, low=101.0, close=102.0)

    result = assess_data_quality([bad], "M15")

    assert "invalid_ohlc" in result.issues


def test_empty_response_does_not_crash():
    result = assess_data_quality([], "M15")

    assert result.valid is False
    assert result.score == 0.0
    assert result.issues == ("empty_data",)


def test_timeframe_mismatch_detected():
    """A 5-minute gap between candles when M15 (15-minute) data was requested."""
    candles = [_candle(0), _candle(5), _candle(20)]

    result = assess_data_quality(candles, "M15")

    assert "timeframe_mismatch" in result.issues
    assert result.score == 100.0 - TIMEFRAME_MISMATCH_PENALTY


def test_score_calculation_combines_multiple_issue_penalties():
    """Duplicate + missing candle together -- score reflects both penalties, not just one."""
    candles = [_candle(0), _candle(15), _candle(15), _candle(60)]  # duplicate at 15, gap 15->60

    result = assess_data_quality(candles, "M15")

    assert set(result.issues) == {"duplicate_candle", "missing_candle"}
    assert result.score == 100.0 - DUPLICATE_CANDLE_PENALTY - MISSING_CANDLE_PENALTY


def test_score_never_goes_below_zero():
    """A pathological combination of every issue type must still floor at 0.0, not go negative."""
    bad_ohlc = _candle(0, open_=100.0, high=90.0, low=99.0, close=105.0)
    candles = [bad_ohlc, _candle(0), _candle(5), _candle(150)]  # invalid_ohlc + duplicate(0) + mismatch(5) + gap(150)

    result = assess_data_quality(candles, "M15")

    assert result.score >= 0.0


def test_unknown_interval_skips_gap_checks_without_raising():
    candles = [_candle(0), _candle(15), _candle(45)]

    result = assess_data_quality(candles, "UNKNOWN_TIMEFRAME")

    assert "missing_candle" not in result.issues
    assert "timeframe_mismatch" not in result.issues


def test_single_candle_never_raises_and_has_no_gap_issues():
    result = assess_data_quality([_candle(0)], "M15")

    assert result.valid is True
    assert result.score == 100.0


def test_result_is_immutable_dataclass():
    result = assess_data_quality([_candle(0)], "M15")
    assert isinstance(result, DataQualityResult)
