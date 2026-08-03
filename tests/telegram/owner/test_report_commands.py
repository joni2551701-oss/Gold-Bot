"""
Phase 59.4, TASK 5 -- platform_layer/telegram/owner/report_commands.py tests.
"""

from datetime import datetime, timezone

from backtesting_layer.statistics.signal_performance import SignalPerformance
from backtesting_layer.statistics.strategy_report import build_strategy_report
from signal_layer.signal_builder.schema import SignalSchema
from platform_layer.telegram.owner.provider_commands import ProviderCommandResult
from platform_layer.telegram.owner.report_commands import format_daily_stats, get_validation_summary, pick_best_strategy

P0 = datetime(2026, 8, 1, tzinfo=timezone.utc)
P1 = datetime(2026, 8, 8, tzinfo=timezone.utc)


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


# --- get_validation_summary ---

def test_get_validation_summary_matches_the_briefs_own_worked_example():
    signals = [_signal(f"s{i}") for i in range(34)]
    performances = (
        [_perf("LIQUIDITY_SWEEP_STRATEGY", "TP") for _ in range(21)]
        + [_perf("LIQUIDITY_SWEEP_STRATEGY", "SL") for _ in range(13)]
    )

    result = get_validation_summary(signals, performances, P0, P1)

    assert isinstance(result, ProviderCommandResult)
    assert result.success is True
    assert "Last 7 days" in result.message
    assert "Signals: 34" in result.message
    assert "Win: 21" in result.message
    assert "Loss: 13" in result.message
    assert "Accuracy: 61.8%" in result.message  # 21/34 = 0.6176...
    assert "Best Strategy: LIQUIDITY_SWEEP_STRATEGY" in result.message


def test_get_validation_summary_empty_input_never_raises():
    result = get_validation_summary([], [], P0, P1)

    assert result.success is True
    assert "Signals: 0" in result.message
    assert "Accuracy: 0.0%" in result.message
    assert "Best Strategy: N/A" in result.message


def test_get_validation_summary_accuracy_excludes_breakeven_and_expired():
    performances = [
        _perf("A", "TP"), _perf("A", "TP"), _perf("A", "SL"),
        _perf("A", "BE"), _perf("A", "EXPIRED"),
    ]

    result = get_validation_summary([], performances, P0, P1)

    assert "Accuracy: 66.7%" in result.message  # 2/(2+1), BE/EXPIRED excluded
