"""GoldBot Core Owner Monitoring Alpha, TASK 1 -- monitoring/models.py tests."""

import dataclasses

from monitoring.models import (
    DecisionPipelineEntry,
    ErrorEvent,
    ErrorSeverity,
    MarketHealth,
    SignalHealth,
    SystemHealth,
)


def test_system_health_field_names():
    field_names = {f.name for f in dataclasses.fields(SystemHealth)}
    assert field_names == {"status", "uptime_seconds", "data_connection", "database_status", "last_scan", "last_error"}


def test_system_health_last_scan_last_error_default_none():
    health = SystemHealth(status="RUNNING", uptime_seconds=1.0, data_connection="1/1 ONLINE", database_status="OK")
    assert health.last_scan is None
    assert health.last_error is None


def test_system_health_is_frozen():
    health = SystemHealth(status="RUNNING", uptime_seconds=1.0, data_connection="1/1 ONLINE", database_status="OK")
    try:
        health.status = "DOWN"
        assert False, "expected FrozenInstanceError"
    except dataclasses.FrozenInstanceError:
        pass


def test_market_health_field_names():
    field_names = {f.name for f in dataclasses.fields(MarketHealth)}
    assert field_names == {"symbol", "data_source_status", "last_price", "last_update", "latency_ms"}


def test_market_health_optional_fields_default_none():
    health = MarketHealth(symbol="XAUUSD", data_source_status="ONLINE")
    assert health.last_price is None
    assert health.last_update is None
    assert health.latency_ms is None


def test_signal_health_field_names():
    field_names = {f.name for f in dataclasses.fields(SignalHealth)}
    assert field_names == {"total_signals", "buy_count", "sell_count", "none_count", "average_confidence"}


def test_signal_health_never_carries_a_pnl_field():
    field_names = {f.name for f in dataclasses.fields(SignalHealth)}
    forbidden = {"win_rate", "profit", "pnl", "sharpe"}
    assert field_names.isdisjoint(forbidden)


def test_error_severity_relayed_never_graded():
    for severity in ErrorSeverity:
        event = ErrorEvent(timestamp="", module="m", error_type="t", message="msg", severity=severity)
        assert event.severity == severity


def test_error_event_field_names():
    field_names = {f.name for f in dataclasses.fields(ErrorEvent)}
    assert field_names == {"timestamp", "module", "error_type", "message", "severity"}


def test_decision_pipeline_entry_field_names():
    """Phase B.0 added stage_durations_ms (additive, defaults to ()) -- see docs/PHASE_B0_AUDIT.md."""
    field_names = {f.name for f in dataclasses.fields(DecisionPipelineEntry)}
    assert field_names == {
        "timestamp", "symbol", "timeframe", "criteria_met", "criteria_total", "decision", "reason",
        "stage_durations_ms",
    }


def test_decision_pipeline_entry_reason_defaults_empty_string():
    entry = DecisionPipelineEntry(
        timestamp="", symbol="XAUUSD", timeframe="M15", criteria_met=(), criteria_total=5, decision="NO TRADE",
    )
    assert entry.reason == ""


def test_decision_pipeline_entry_never_carries_a_risk_field():
    field_names = {f.name for f in dataclasses.fields(DecisionPipelineEntry)}
    forbidden = {"stop_loss", "take_profit", "lot_size", "risk_amount"}
    assert field_names.isdisjoint(forbidden)
