"""
Phase 59.4, TASK 5 -- telegram/owner/report_commands.py tests.
"""

from datetime import datetime, timezone

from analytics.signal_performance import SignalPerformance
from analytics.strategy_report import build_strategy_report
from signals.schema import SignalSchema
from telegram.owner.provider_commands import ProviderCommandResult
from telegram.owner.report_commands import format_daily_stats, pick_best_strategy


def _signal(signal_id, decision="APPROVED"):
    return SignalSchema(
        signal_id=signal_id, created_at=datetime.now(timezone.utc), symbol="XAUUSD",
        timeframe="M15", direction="BUY", decision=decision,
    )


def _perf(strategy_id, result):
    return SignalPerformance(
        performance_id="p", signal_id="s", strategy_id=strategy_id, result=result,
        created_at=datetime.now(timezone.utc),
    )


def test_format_daily_stats_counts_signals_and_approved():
    signals = [_signal("s1", "APPROVED"), _signal("s2", "REJECTED"), _signal("s3", "PENDING")]

    result = format_daily_stats(signals, [])

    assert result.success is True
    assert "Signals: 3" in result.message
    assert "Approved: 1" in result.message


def test_format_daily_stats_counts_results():
    performances = [
        _perf("LIQUIDITY_SWEEP_STRATEGY", "TP"),
        _perf("LIQUIDITY_SWEEP_STRATEGY", "TP"),
        _perf("LIQUIDITY_SWEEP_STRATEGY", "SL"),
        _perf("AMD_STRATEGY", "EXPIRED"),
        _perf("AMD_STRATEGY", "CANCELLED"),
    ]

    result = format_daily_stats([], performances)

    assert "TP: 2" in result.message
    assert "SL: 1" in result.message
    assert "Expired: 1" in result.message
    assert "Cancelled: 1" in result.message


def test_format_daily_stats_matches_the_briefs_own_worked_example():
    signals = [_signal(f"s{i}", "APPROVED" if i < 3 else "REJECTED") for i in range(5)]
    performances = [_perf("LIQUIDITY_SWEEP_STRATEGY", "TP"), _perf("LIQUIDITY_SWEEP_STRATEGY", "TP"),
                     _perf("LIQUIDITY_SWEEP_STRATEGY", "SL")]

    result = format_daily_stats(signals, performances)

    assert "Signals: 5" in result.message
    assert "Approved: 3" in result.message
    assert "TP: 2" in result.message
    assert "SL: 1" in result.message
    assert "Best Strategy: LIQUIDITY_SWEEP_STRATEGY" in result.message


def test_format_daily_stats_empty_input_never_raises():
    result = format_daily_stats([], [])
    assert result.success is True
    assert "Best Strategy: N/A" in result.message


def test_format_daily_stats_isinstance():
    result = format_daily_stats([], [])
    assert isinstance(result, ProviderCommandResult)


# --- pick_best_strategy ---

def test_pick_best_strategy_highest_win_rate():
    performances = (
        [_perf("A", "TP")] * 8 + [_perf("A", "SL")] * 2      # 80% win rate
        + [_perf("B", "TP")] * 5 + [_perf("B", "SL")] * 5    # 50% win rate
    )
    reports = build_strategy_report(performances)

    best = pick_best_strategy(reports)

    assert best.strategy_id == "A"


def test_pick_best_strategy_ties_broken_by_more_total_signals():
    performances = (
        [_perf("A", "TP")] * 1                                  # 100% win rate, 1 signal
        + [_perf("B", "TP")] * 10 + [_perf("B", "SL")] * 0       # 100% win rate, 10 signals
    )
    reports = build_strategy_report(performances)

    best = pick_best_strategy(reports)

    assert best.strategy_id == "B"


def test_pick_best_strategy_returns_none_for_empty_reports():
    assert pick_best_strategy({}) is None


def test_pick_best_strategy_never_raises():
    pick_best_strategy({})
