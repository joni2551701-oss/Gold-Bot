"""
TASK-CORE-006 gap-fill — ContextEngine orchestration (context_layer/context_engine/context_orchestrator.py).

Read-only exercise of the existing frozen engine: build() assembles one
immutable ContextSnapshot with every detector field present (the context
snapshot test), tolerates empty candle input, and never raises on
non-ascending (invalid-order) candles.
"""

from datetime import datetime, timedelta, timezone

from data_layer.providers.twelve_data_client import Candle

from context_layer.context_engine.context_orchestrator import (
    ContextEngine,
    ContextSnapshot,
    build_context_snapshot,
)
from context_layer.trend.market_regime import MarketRegime, MarketRegimeResult

BASE = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _wave(n=60):
    """A gently oscillating series so structure/regime have something to read."""
    candles = []
    for i in range(n):
        drift = i * 0.2
        osc = 3.0 if i % 4 < 2 else -3.0
        mid = 100.0 + drift + osc
        candles.append(Candle(
            timestamp=BASE + timedelta(minutes=15 * i),
            open=mid - 0.5, high=mid + 2.0, low=mid - 2.0, close=mid + 0.5,
        ))
    return candles


def test_build_returns_complete_immutable_snapshot():
    snap = build_context_snapshot(_wave())
    assert isinstance(snap, ContextSnapshot)
    # Every detector field is present (sequence or a real result), never None.
    for field in ("candles", "structure", "bos_events", "choch_events",
                  "liquidity_zones", "liquidity_sweeps", "order_blocks",
                  "fair_value_gaps", "amd_events", "wyckoff_events", "session_events"):
        assert getattr(snap, field) is not None
    assert isinstance(snap.market_regime, MarketRegimeResult)
    # Immutable contract.
    try:
        snap.structure = ()  # type: ignore[misc]
    except Exception as exc:
        assert "frozen" in type(exc).__name__.lower() or "cannot assign" in str(exc).lower()
    else:
        raise AssertionError("ContextSnapshot must be immutable")


def test_empty_candles_yield_empty_snapshot():
    snap = ContextEngine().build([])
    assert list(snap.candles) == []
    assert list(snap.structure) == []
    assert list(snap.bos_events) == []
    assert list(snap.fair_value_gaps) == []
    assert snap.market_regime.regime is MarketRegime.UNKNOWN


def test_non_ascending_candles_do_not_raise():
    # Deliberately out-of-order timestamps: engine logs a warning, never raises.
    candles = list(reversed(_wave(10)))
    snap = ContextEngine().build(candles)
    assert isinstance(snap, ContextSnapshot)
    assert isinstance(snap.market_regime, MarketRegimeResult)


def test_deterministic_for_same_input():
    candles = _wave(40)
    a = build_context_snapshot(candles)
    b = build_context_snapshot(candles)
    assert [p.structure for p in a.structure] == [p.structure for p in b.structure]
    assert len(a.fair_value_gaps) == len(b.fair_value_gaps)
    assert a.market_regime.regime == b.market_regime.regime
