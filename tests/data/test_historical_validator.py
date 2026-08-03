"""
Phase 59.5, TASK 3 -- data_layer/data_validation/historical_validator.py tests.
"""

from datetime import datetime, timedelta, timezone

from data_layer.data_validation.historical_validator import validate_historical_candles
from database_layer.market_repository.raw_candle_models import create_raw_candle


def _candle(ts, provider="twelvedata", open=2000.0, high=2005.0, low=1995.0, close=2001.0):
    return create_raw_candle(
        symbol="XAUUSD", timeframe="M15", timestamp=ts,
        open=open, high=high, low=low, close=close, provider=provider,
    )


def test_empty_input_never_raises_and_is_valid():
    report = validate_historical_candles([])
    assert report.total_candles == 0
    assert report.valid is True


def test_clean_series_is_valid():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    candles = [_candle(start + i * timedelta(minutes=15)) for i in range(10)]

    report = validate_historical_candles(candles)

    assert report.valid is True
    assert report.total_candles == 10
    assert report.missing_count == 0
    assert report.duplicate_count == 0


def test_detects_missing_candle_gap():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    candles = [
        _candle(start),
        _candle(start + timedelta(minutes=15)),
        _candle(start + timedelta(hours=3)),  # a big gap
    ]

    report = validate_historical_candles(candles)

    assert report.missing_count == 1
    assert report.valid is False


def test_detects_duplicate_timestamp():
    ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
    candles = [_candle(ts), _candle(ts), _candle(ts + timedelta(minutes=15))]

    report = validate_historical_candles(candles)

    assert report.duplicate_count == 1
    assert report.valid is False


def test_detects_ordering_violation():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    candles = [_candle(start + timedelta(minutes=15)), _candle(start)]  # out of order

    report = validate_historical_candles(candles)

    assert report.ordering_violations == 1
    assert report.valid is False


def test_detects_future_timestamp():
    far_future = datetime.now(timezone.utc) + timedelta(days=3650)
    candles = [_candle(far_future)]

    report = validate_historical_candles(candles)

    assert report.future_timestamp_count == 1
    assert report.valid is False


def test_detects_timezone_naive_timestamp():
    naive = datetime(2026, 1, 1)  # no tzinfo
    candles = [_candle(naive)]

    report = validate_historical_candles(candles)

    assert report.timezone_issues == 1
    assert report.valid is False


def test_detects_invalid_ohlc():
    ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
    candles = [_candle(ts, high=1990.0)]  # high below open/close -- impossible

    report = validate_historical_candles(candles)

    assert report.invalid_ohlc_count == 1
    assert report.valid is False


def test_detects_provider_mismatch_when_expected_provider_given():
    ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
    candles = [_candle(ts, provider="binance")]

    report = validate_historical_candles(candles, expected_provider="twelvedata")

    assert report.provider_mismatch_count == 1
    assert report.valid is False


def test_provider_mismatch_is_zero_when_no_expected_provider_given():
    ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
    candles = [_candle(ts, provider="binance")]

    report = validate_historical_candles(candles)

    assert report.provider_mismatch_count == 0


def test_explicit_timeframe_overrides_candle_inference():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    candles = [_candle(start), _candle(start + timedelta(hours=1))]  # 1h gap

    report_m15 = validate_historical_candles(candles, timeframe="M15")
    report_h1 = validate_historical_candles(candles, timeframe="H1")

    assert report_m15.missing_count == 1  # 1h gap is way more than one M15 step
    assert report_h1.missing_count == 0  # matches exactly one H1 step


def test_mixed_timeframes_skip_missing_check_without_explicit_timeframe():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    m15 = create_raw_candle(symbol="XAUUSD", timeframe="M15", timestamp=start, open=2000.0, high=2005.0, low=1995.0, close=2001.0, provider="twelvedata")
    h1 = create_raw_candle(symbol="XAUUSD", timeframe="H1", timestamp=start + timedelta(hours=5), open=2000.0, high=2005.0, low=1995.0, close=2001.0, provider="twelvedata")

    report = validate_historical_candles([m15, h1])

    assert report.missing_count == 0  # can't infer a single timeframe, so the check is skipped, not guessed
