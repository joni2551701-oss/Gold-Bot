"""
Phase 59.8, Owner Control Center -- telegram/owner/status_commands.py
tests. Real repositories (SQLite, tests/conftest.py's autouse
fresh_database fixture) -- no mocks. TWELVE_DATA_API_KEY="unused" is
set by conftest.py, so the twelvedata provider reports available=True
(see tests/conftest.py's own comment on this fact).
"""

from datetime import datetime, timedelta, timezone

from database_layer.trade_repository.signal_repository import SignalRepository
from telegram.owner.provider_commands import ProviderCommandResult
from telegram.owner.status_commands import _format_time_ago, get_system_status


def _signal_data(signal_id="s1"):
    return {
        "signal_id": signal_id, "symbol": "XAUUSD", "direction": "BUY",
        "entry_zone_min": 2000.0, "entry_zone_max": 2001.0, "stop_loss": 1990.0,
        "take_profit_1": 2020.0, "take_profit_2": 2030.0, "risk_percent": 1.0,
        "lot_size": 0.1, "strategy_name": "LIQUIDITY_SWEEP_STRATEGY",
        "confidence_score": 0.9, "ai_explanation": "fixture",
    }


def test_get_system_status_returns_a_provider_command_result():
    result = get_system_status()
    assert isinstance(result, ProviderCommandResult)
    assert result.success is True


def test_get_system_status_matches_the_briefs_own_field_order():
    result = get_system_status()
    for label in ("GoldBot Status", "System:", "Pipeline:", "Database:", "Provider:", "Mode:", "Last Signal:"):
        assert label in result.message


def test_get_system_status_reports_database_connected():
    result = get_system_status()
    assert "Database: CONNECTED" in result.message


def test_get_system_status_reports_validation_mode(monkeypatch):
    import config
    monkeypatch.setattr(config.Config, "VALIDATION_MODE", True)

    result = get_system_status()

    assert "Mode: VALIDATION" in result.message


def test_get_system_status_reports_running_mode_by_default():
    result = get_system_status()
    assert "Mode: RUNNING" in result.message


def test_get_system_status_reports_no_signal_as_na():
    result = get_system_status()
    assert "Last Signal: N/A" in result.message


def test_get_system_status_reports_last_signal_age():
    SignalRepository().create_signal(_signal_data())

    result = get_system_status()

    assert "Last Signal: " in result.message
    assert "N/A" not in result.message.split("Last Signal: ")[1]


# --- _format_time_ago ---

def test_format_time_ago_minutes():
    ts = datetime.now(timezone.utc) - timedelta(minutes=12)
    assert _format_time_ago(ts) == "12 min ago"


def test_format_time_ago_singular_minute():
    ts = datetime.now(timezone.utc) - timedelta(minutes=1)
    assert _format_time_ago(ts) == "1 min ago"


def test_format_time_ago_hours():
    ts = datetime.now(timezone.utc) - timedelta(hours=3)
    assert _format_time_ago(ts) == "3 hours ago"


def test_format_time_ago_singular_hour():
    ts = datetime.now(timezone.utc) - timedelta(hours=1)
    assert _format_time_ago(ts) == "1 hour ago"


def test_format_time_ago_days():
    ts = datetime.now(timezone.utc) - timedelta(days=2)
    assert _format_time_ago(ts) == "2 days ago"


def test_format_time_ago_never_negative():
    ts = datetime.now(timezone.utc) + timedelta(minutes=5)  # a clock-skew future timestamp
    assert _format_time_ago(ts) == "0 min ago"
