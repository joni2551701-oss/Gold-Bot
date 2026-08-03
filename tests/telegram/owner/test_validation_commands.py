"""
Phase 59 Real Market Validation Foundation, TASK 8 --
telegram/owner/validation_commands.py tests.
"""

from datetime import datetime, timezone

from telegram.owner.provider_commands import ProviderCommandResult
from telegram.owner.validation_commands import (
    get_today_signals,
    get_validation_report,
    get_validation_status,
)
from analytics.signal_performance import SignalPerformance
from config import Config
from signal_layer.signal_builder.schema import SignalSchema

P0 = datetime(2026, 8, 1, tzinfo=timezone.utc)
P1 = datetime(2026, 8, 8, tzinfo=timezone.utc)


def _signal(signal_id, direction="BUY"):
    return SignalSchema(
        signal_id=signal_id, created_at=datetime.now(timezone.utc), symbol="XAUUSD",
        timeframe="M15", direction=direction, decision="APPROVED",
    )


def _perf(strategy_id="LIQUIDITY_SWEEP_STRATEGY", result=None):
    return SignalPerformance(
        performance_id="p", signal_id="s", strategy_id=strategy_id, result=result,
        created_at=datetime.now(timezone.utc),
    )


# --- get_validation_status ---

def test_get_validation_status_returns_off_by_default():
    result = get_validation_status()

    assert isinstance(result, ProviderCommandResult)
    assert result.success is True
    assert "OFF" in result.message


def test_get_validation_status_reflects_config_flag(monkeypatch):
    monkeypatch.setattr(Config, "VALIDATION_MODE", True)

    result = get_validation_status()

    assert "ON" in result.message


# --- get_today_signals ---

def test_get_today_signals_counts_buy_and_sell():
    signals = [_signal("s1", "BUY"), _signal("s2", "BUY"), _signal("s3", "SELL")]

    result = get_today_signals(signals)

    assert result.success is True
    assert "Total: 3" in result.message
    assert "BUY: 2" in result.message
    assert "SELL: 1" in result.message


def test_get_today_signals_empty_input_never_raises():
    result = get_today_signals([])
    assert result.success is True
    assert "Total: 0" in result.message


# --- get_validation_report ---

def test_get_validation_report_wraps_format_validation_report():
    signals = [_signal("s1", "BUY"), _signal("s2", "SELL")]
    performances = [_perf(result="TP"), _perf(result="SL")]

    result = get_validation_report(signals, performances, P0, P1)

    assert isinstance(result, ProviderCommandResult)
    assert result.success is True
    assert "GoldBot Validation Report" in result.message
    assert "Signals: 2" in result.message


def test_get_validation_report_empty_input_never_raises():
    result = get_validation_report([], [], P0, P1)

    assert result.success is True
    assert "Best Session: N/A" in result.message
