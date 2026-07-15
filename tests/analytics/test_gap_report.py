"""
Phase 59.5, TASK 4 -- analytics/gap_report.py tests.
"""

from datetime import datetime, timedelta, timezone

from analytics.gap_report import GapReport, build_gap_report, format_gap_report
from database.raw_candle_models import create_raw_candle


def _candle(ts, provider="twelvedata"):
    return create_raw_candle(
        symbol="XAUUSD", timeframe="M15", timestamp=ts,
        open=2000.0, high=2005.0, low=1995.0, close=2001.0, provider=provider,
    )


def test_empty_input_never_raises():
    report = build_gap_report([], "XAUUSD", "M15")
    assert isinstance(report, GapReport)
    assert report.gaps == ()


def test_clean_series_has_no_gaps():
    start = datetime(2026, 7, 1, tzinfo=timezone.utc)
    candles = [_candle(start + i * timedelta(minutes=15)) for i in range(10)]

    report = build_gap_report(candles, "XAUUSD", "M15")

    assert report.gaps == ()


def test_matches_the_briefs_own_worked_example():
    base = datetime(2026, 7, 1, tzinfo=timezone.utc)
    candles = [
        _candle(base.replace(hour=2, minute=0)),
        # 02:15 and 02:30 missing (M15 step)
        _candle(base.replace(hour=2, minute=45)),
        _candle(base.replace(hour=4, minute=15)),
        # 04:30 missing
        _candle(base.replace(hour=4, minute=45)),
        _candle(base.replace(hour=17, minute=45)),
        _candle(base.replace(hour=17, minute=45)),  # duplicate
    ]

    report = build_gap_report(candles, "XAUUSD", "M15")
    text = format_gap_report(report)

    assert "XAUUSD" in text
    assert "M15" in text
    assert "02:15 missing" in text
    assert "02:30 missing" in text
    assert "04:30 missing" in text
    assert "17:45 duplicate" in text


def test_duplicate_reported_once_regardless_of_occurrence_count():
    ts = datetime(2026, 7, 1, 17, 45, tzinfo=timezone.utc)
    candles = [_candle(ts), _candle(ts), _candle(ts)]  # three occurrences

    report = build_gap_report(candles, "XAUUSD", "M15")

    duplicate_entries = [g for g in report.gaps if g.gap_type == "duplicate"]
    assert len(duplicate_entries) == 1


def test_unrecognized_timeframe_skips_missing_check():
    start = datetime(2026, 7, 1, tzinfo=timezone.utc)
    candles = [_candle(start), _candle(start + timedelta(hours=5))]

    report = build_gap_report(candles, "XAUUSD", "WEEKLY")

    assert all(g.gap_type != "missing" for g in report.gaps)


def test_gaps_are_chronologically_ascending():
    base = datetime(2026, 7, 1, tzinfo=timezone.utc)
    candles = [
        _candle(base.replace(hour=2, minute=0)),
        _candle(base.replace(hour=2, minute=45)),
        _candle(base.replace(hour=1, minute=0)),
        _candle(base.replace(hour=1, minute=45)),
    ]

    report = build_gap_report(candles, "XAUUSD", "M15")

    timestamps = [g.timestamp for g in report.gaps]
    assert timestamps == sorted(timestamps)


def test_format_reports_no_gaps_message_when_clean():
    report = build_gap_report([], "XAUUSD", "M15")
    text = format_gap_report(report)
    assert "No gaps detected." in text


def test_truncation_is_capped_and_disclosed():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    candles = [_candle(start), _candle(start + timedelta(days=365))]  # enormous gap

    report = build_gap_report(candles, "XAUUSD", "M15")
    text = format_gap_report(report)

    assert report.truncated is True
    assert "truncated" in text
