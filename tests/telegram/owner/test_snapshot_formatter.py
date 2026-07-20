"""
GoldBot Core Owner Snapshot Reporter Alpha, TASK 3 --
telegram/owner/snapshot_formatter.py tests. Extended for the v1.1
Operational Intelligence Upgrade, TASK 9 (new format).
"""

from monitoring.snapshot_models import OwnerSnapshot
from telegram.owner.snapshot_formatter import format_snapshot


def _snapshot(**overrides):
    defaults = dict(
        timestamp="2026-01-01T20:00:00+00:00",
        status="OK",
        core_status="RUNNING",
        database_status="OK",
        telegram_status="OK",
        market_data_status="ONLINE",
        last_signal="BUY @ 2026-01-01T19:55:00",
        error_count=0,
        uptime_info="15h 20m",
        signals_today=3,
    )
    defaults.update(overrides)
    return OwnerSnapshot(**defaults)


def test_format_snapshot_returns_string():
    assert isinstance(format_snapshot(_snapshot()), str)


def test_format_snapshot_contains_goldbot_snapshot_header():
    assert "GoldBot Snapshot v1.1" in format_snapshot(_snapshot())


def test_format_snapshot_contains_formatted_time():
    assert "20:00 UTC" in format_snapshot(_snapshot())


def test_format_snapshot_contains_core_status():
    assert "RUNNING" in format_snapshot(_snapshot())


def test_format_snapshot_contains_database_status():
    message = format_snapshot(_snapshot(database_status="OK"))
    assert "\U0001F4BE Database:" in message
    assert "HEALTHY" in message


def test_format_snapshot_contains_market_data_status():
    message = format_snapshot(_snapshot(market_data_status="ONLINE"))
    assert "\U0001F4C8 Market:" in message
    assert "ONLINE" in message


def test_format_snapshot_contains_signals_today_count():
    message = format_snapshot(_snapshot(signals_today=3))
    assert "\U0001F3AF Signals:" in message
    assert "Today: 3" in message


def test_format_snapshot_contains_error_count():
    message = format_snapshot(_snapshot(error_count=2))
    assert "⚠️ Errors:" in message
    assert "Today: 2" in message


def test_format_snapshot_contains_runtime():
    message = format_snapshot(_snapshot(uptime_info="15h 20m"))
    assert "Runtime:" in message
    assert "15h 20m" in message


def test_format_snapshot_shows_na_for_missing_last_signal():
    message = format_snapshot(_snapshot(last_signal=None))
    assert "N/A" in message


def test_format_snapshot_shows_last_signal_when_present():
    message = format_snapshot(_snapshot(last_signal="SELL @ 2026-01-01T18:00:00"))
    assert "SELL @ 2026-01-01T18:00:00" in message


def test_format_snapshot_uses_green_marker_when_status_ok():
    message = format_snapshot(_snapshot(status="OK"))
    assert "\U0001F7E2" in message


def test_format_snapshot_uses_yellow_marker_when_status_degraded():
    message = format_snapshot(_snapshot(status="DEGRADED"))
    assert "\U0001F7E1" in message


def test_format_snapshot_shows_telegram_status():
    message = format_snapshot(_snapshot(telegram_status="OK"))
    assert "\U0001F4E1 Telegram:" in message


def test_format_snapshot_unknown_status_gets_question_icon():
    message = format_snapshot(_snapshot(core_status="SOMETHING_NEW"))
    assert "❓" in message


def test_format_snapshot_never_raises_on_malformed_timestamp():
    message = format_snapshot(_snapshot(timestamp="not-a-timestamp"))
    assert "not-a-timestamp" in message


# v1.1 TASK 1 -- Pipeline Activity
def test_format_snapshot_contains_pipeline_section():
    message = format_snapshot(_snapshot(pipeline_runs_today=5, pipeline_last_status="SUCCESS"))
    assert "\U0001F4CA Pipeline:" in message
    assert "Runs Today: 5" in message
    assert "SUCCESS" in message


def test_format_snapshot_pipeline_duration_is_never_fabricated():
    message = format_snapshot(_snapshot())
    assert "Duration: N/A" in message


# v1.1 TASK 2 -- Signal Intelligence
def test_format_snapshot_contains_approved_rejected_and_strategies():
    message = format_snapshot(_snapshot(
        signals_approved=1, signals_rejected=4, strategy_breakdown="FVG: 2, AMD: 3",
    ))
    assert "Approved: 1" in message
    assert "Rejected: 4" in message
    assert "Strategies: FVG: 2, AMD: 3" in message


def test_format_snapshot_shows_last_signal_score_when_present():
    message = format_snapshot(_snapshot(last_signal_score=82))
    assert "Score: 82" in message


def test_format_snapshot_shows_na_score_when_missing():
    message = format_snapshot(_snapshot(last_signal_score=None))
    assert "Score: N/A" in message


# v1.1 TASK 3 -- Decision Engine Snapshot
def test_format_snapshot_contains_decision_section():
    message = format_snapshot(_snapshot(
        decision_total=10, decision_approved=2, decision_rejected=8,
        decision_avg_confidence_pct=74.0, decision_risk_pass_rate_pct=32.0,
    ))
    assert "⚖️ Decision:" in message
    assert "Total: 10" in message
    assert "Avg Confidence: 74.0%" in message
    assert "Risk Pass Rate: 32.0%" in message


# v1.1 TASK 4 -- AI Layer Monitoring
def test_format_snapshot_shows_no_data_collected_yet_for_ai():
    message = format_snapshot(_snapshot(ai_status="NO_DATA"))
    assert "No data collected yet" in message


def test_format_snapshot_shows_ai_requests_when_data_present():
    message = format_snapshot(_snapshot(ai_status="ONLINE", ai_requests_today=15))
    assert "Requests: 15" in message


# v1.1 TASK 5 -- Market Data Monitoring Upgrade
def test_format_snapshot_shows_market_provider_symbol_timeframe():
    message = format_snapshot(_snapshot(
        market_provider="twelvedata", market_symbol="XAUUSD", market_timeframe="M15",
    ))
    assert "XAUUSD (M15)" in message
    assert "twelvedata:" in message


# v1.1 TASK 6 -- Error Intelligence
def test_format_snapshot_contains_error_breakdown():
    message = format_snapshot(_snapshot(
        error_count=3, errors_critical=0, errors_warning=3,
        last_error_module="MarketDataNormalizer", last_error_time="2026-01-01T17:25:00+00:00",
    ))
    assert "Critical: 0" in message
    assert "Warning: 3" in message
    assert "MarketDataNormalizer @ 17:25 UTC" in message


def test_format_snapshot_shows_na_for_no_last_error():
    message = format_snapshot(_snapshot(last_error_module=None))
    assert "Last: N/A" in message


# v1.1 TASK 7 -- System Runtime Metrics
def test_format_snapshot_shows_next_check_time():
    message = format_snapshot(_snapshot(runtime_next_check="18:30 UTC"))
    assert "Next Check: 18:30 UTC" in message


# v1.1 TASK 8 -- Database Statistics
def test_format_snapshot_contains_database_statistics():
    message = format_snapshot(_snapshot(
        db_signals_total=245, db_errors_total=12, db_pipeline_events_total=0,
    ))
    assert "Signals: 245" in message
    assert "Errors: 12" in message
    assert "Pipeline Events: 0" in message
