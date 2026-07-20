"""GoldBot Core Owner Snapshot Reporter Alpha, TASK 1 -- monitoring/snapshot_models.py tests."""

from dataclasses import fields

from monitoring.snapshot_models import OwnerSnapshot


def _snapshot(**overrides):
    defaults = dict(
        timestamp="2026-01-01T00:00:00+00:00",
        status="OK",
        core_status="RUNNING",
        database_status="OK",
        telegram_status="OK",
        market_data_status="ONLINE",
        last_signal=None,
        error_count=0,
        uptime_info="5m 0s",
    )
    defaults.update(overrides)
    return OwnerSnapshot(**defaults)


def test_owner_snapshot_constructs_with_all_required_fields():
    snap = _snapshot()
    assert isinstance(snap, OwnerSnapshot)


def test_owner_snapshot_is_frozen():
    snap = _snapshot()
    try:
        snap.status = "DEGRADED"
        assert False, "expected FrozenInstanceError"
    except Exception:
        pass


def test_owner_snapshot_field_names_match_brief_plus_additive_signals_today():
    field_names = {f.name for f in fields(OwnerSnapshot)}
    expected = {
        "timestamp", "status", "core_status", "database_status", "telegram_status",
        "market_data_status", "last_signal", "error_count", "uptime_info", "signals_today",
        # v1.1 additive fields (TASK 1-8) -- see monitoring/snapshot_models.py's own docstring.
        "pipeline_runs_today", "pipeline_last_at", "pipeline_last_status",
        "signals_approved", "signals_rejected", "strategy_breakdown", "last_signal_score",
        "decision_total", "decision_approved", "decision_rejected",
        "decision_avg_confidence_pct", "decision_risk_pass_rate_pct",
        "ai_requests_today", "ai_status",
        "market_provider", "market_symbol", "market_timeframe", "market_candles_configured",
        "errors_critical", "errors_warning", "last_error_module", "last_error_time",
        "runtime_execution_seconds", "runtime_next_check",
        "db_signals_total", "db_errors_total", "db_pipeline_events_total",
    }
    assert field_names == expected


def test_owner_snapshot_last_signal_accepts_none():
    snap = _snapshot(last_signal=None)
    assert snap.last_signal is None


def test_owner_snapshot_last_signal_accepts_string():
    snap = _snapshot(last_signal="BUY @ 2026-01-01T00:00:00")
    assert snap.last_signal == "BUY @ 2026-01-01T00:00:00"


def test_owner_snapshot_signals_today_defaults_to_zero():
    snap = _snapshot()
    assert snap.signals_today == 0


def test_owner_snapshot_signals_today_accepts_override():
    snap = _snapshot(signals_today=5)
    assert snap.signals_today == 5


def test_owner_snapshot_error_count_is_int():
    snap = _snapshot(error_count=3)
    assert snap.error_count == 3
    assert isinstance(snap.error_count, int)


def test_owner_snapshot_empty_state_all_unknowns():
    """Empty/degraded state -- every status field can independently be UNKNOWN without construction failing."""
    snap = _snapshot(
        core_status="UNKNOWN", database_status="UNKNOWN",
        telegram_status="NOT_CONFIGURED", market_data_status="UNKNOWN",
        uptime_info="N/A",
    )
    assert snap.core_status == "UNKNOWN"
    assert snap.telegram_status == "NOT_CONFIGURED"
    assert snap.uptime_info == "N/A"


def test_owner_snapshot_never_holds_a_trading_verdict():
    """Belt-and-suspenders: this is observability, never a signal/decision object (Strict Rule)."""
    field_names = {f.name for f in fields(OwnerSnapshot)}
    forbidden = {"signal", "decision", "verdict", "direction", "confidence"}
    assert field_names.isdisjoint(forbidden)


def test_owner_snapshot_module_imports_only_stdlib():
    import ast
    import pathlib

    module_file = pathlib.Path(__file__).resolve().parents[2] / "monitoring" / "snapshot_models.py"
    tree = ast.parse(module_file.read_text())
    allowed_prefixes = ("dataclasses", "typing")
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            assert node.module.startswith(allowed_prefixes), node.module
        elif isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.startswith(allowed_prefixes), alias.name
