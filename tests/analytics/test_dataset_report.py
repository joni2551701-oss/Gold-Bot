"""
Phase 59.5, TASK 5 -- backtesting_layer/statistics/dataset_report.py tests.
"""

from datetime import datetime, timedelta, timezone

from backtesting_layer.statistics.dataset_report import DatasetReport, build_dataset_report, format_dataset_report
from database_layer.market_repository.raw_candle_models import create_raw_candle


def _candle(symbol, timeframe, ts, provider="twelvedata"):
    return create_raw_candle(
        symbol=symbol, timeframe=timeframe, timestamp=ts,
        open=2000.0, high=2005.0, low=1995.0, close=2001.0, provider=provider,
    )


def test_empty_input_never_raises():
    report = build_dataset_report([])
    assert isinstance(report, DatasetReport)
    assert report.total_candles == 0
    assert report.oldest_candle is None
    assert report.coverage_pct == 0.0


def test_counts_candles_and_span():
    start = datetime(2026, 7, 1, tzinfo=timezone.utc)
    candles = [_candle("XAUUSD", "M15", start + i * timedelta(minutes=15)) for i in range(10)]

    report = build_dataset_report(candles)

    assert report.total_candles == 10
    assert report.symbols == ("XAUUSD",)
    assert report.timeframes == ("M15",)
    assert report.providers == ("twelvedata",)
    assert report.oldest_candle == start
    assert report.newest_candle == start + timedelta(minutes=135)


def test_full_coverage_series_is_100_percent():
    start = datetime(2026, 7, 1, tzinfo=timezone.utc)
    candles = [_candle("XAUUSD", "M15", start + i * timedelta(minutes=15)) for i in range(10)]

    report = build_dataset_report(candles)

    assert report.coverage_pct == 100.0


def test_sparse_series_has_partial_coverage():
    start = datetime(2026, 7, 1, tzinfo=timezone.utc)
    # 3 candles spanning what should be 9 (start, +15, +120min) -- far under 100%.
    candles = [_candle("XAUUSD", "M15", start), _candle("XAUUSD", "M15", start + timedelta(minutes=15)), _candle("XAUUSD", "M15", start + timedelta(hours=2))]

    report = build_dataset_report(candles)

    assert 0.0 < report.coverage_pct < 100.0


def test_multi_symbol_and_timeframe_are_all_listed():
    start = datetime(2026, 7, 1, tzinfo=timezone.utc)
    candles = [
        _candle("XAUUSD", "M15", start),
        _candle("EURUSD", "H1", start),
    ]

    report = build_dataset_report(candles)

    assert report.symbols == ("EURUSD", "XAUUSD")
    assert report.timeframes == ("H1", "M15")


def test_duplicate_and_invalid_counts_are_aggregated_across_groups():
    start = datetime(2026, 7, 1, tzinfo=timezone.utc)
    candles = [
        _candle("XAUUSD", "M15", start),
        _candle("XAUUSD", "M15", start),  # duplicate
        create_raw_candle(symbol="EURUSD", timeframe="H1", timestamp=start, open=1.0, high=0.5, low=0.9, close=1.0, provider="twelvedata"),  # invalid OHLC
    ]

    report = build_dataset_report(candles)

    assert report.duplicate_count == 1
    assert report.invalid_count == 1


def test_format_matches_the_briefs_own_field_order():
    start = datetime(2026, 7, 1, tzinfo=timezone.utc)
    candles = [_candle("XAUUSD", "M15", start)]

    report = build_dataset_report(candles)
    text = format_dataset_report(report)

    for label in ("Provider:", "Symbols:", "Timeframes:", "Candles:", "Oldest candle:", "Newest candle:", "Coverage %:", "Duplicates:", "Missing:", "Invalid:"):
        assert label in text


def test_format_never_raises_on_empty_report():
    report = build_dataset_report([])
    text = format_dataset_report(report)
    assert "N/A" in text
