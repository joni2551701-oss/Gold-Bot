"""Unit tests for bootstrap state/strategy/progress/metrics models (module 5)."""

from datetime import datetime, timezone

from data_layer.historical_data.bootstrap_state import BootstrapState, BootstrapStrategy
from data_layer.historical_data.bootstrap_progress import BootstrapProgress
from data_layer.historical_data.bootstrap_metrics import BootstrapMetrics


def test_states_cover_lifecycle_incl_cancelled():
    names = {s.name for s in BootstrapState}
    assert {"PENDING", "LOADING", "VALIDATING", "HYDRATING",
            "READY", "FAILED", "CANCELLED"} <= names


def test_strategies_dd058():
    names = {s.name for s in BootstrapStrategy}
    assert names == {"AUTO", "FULL", "INCREMENTAL", "RECOVERY_ONLY", "CACHE_ONLY"}


def test_progress_fields_dd054():
    p = BootstrapProgress(asset="XAUUSD", status=BootstrapState.LOADING,
                          progress_pct=50.0, current_timeframe="M15",
                          remaining=["M15", "H1"])
    assert p.asset == "XAUUSD"
    assert p.progress_pct == 50.0
    assert p.current_timeframe == "M15"


def test_metrics_cache_percentages_dd057():
    m = BootstrapMetrics(asset="XAUUSD")
    assert m.cache_hit_pct == 0.0            # no accesses yet
    m.cache_hits = 3
    m.cache_misses = 1
    assert m.cache_hit_pct == 75.0
    assert m.cache_miss_pct == 25.0
    m.last_bootstrap = datetime(2026, 7, 24, tzinfo=timezone.utc)
    d = m.as_dict()
    assert d["cache_hit_pct"] == 75.0
    assert d["asset"] == "XAUUSD"
