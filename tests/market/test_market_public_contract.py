"""
market/ facade — binds to context/'s PUBLIC contract only (TASK-CORE-005).

Director constraint: market/ must never depend on context/'s internal
implementation -- it reads ONLY context/'s public contract. That public
contract is context.snapshot.ContextSnapshotSchema (the standard,
documented, JSON-serializable view -- see docs/CONTEXT_SNAPSHOT.md),
which is deliberately distinct from the internal
context.context_orchestrator.ContextSnapshot.

This suite feeds a REAL ContextSnapshotSchema (built from the public
context.snapshot factory) through the market façade and asserts every
projection matches the contract's own values. It is the proof that the
façade consumes the genuine public contract, not a look-alike -- while
the other market suites use fakes to prove the façade never reaches into
any context internal.
"""

from datetime import datetime, timezone

from context_layer.context_engine.snapshot import (
    ContextSnapshotSchema,
    LiquidityInfo,
    SessionInfo,
    StructureInfo,
    ZonesInfo,
    generate_snapshot_id,
)

from market.market_manager import MarketManager
from market.trend_state import TrendState
from market.volatility_state import VolatilityLevel

# Deterministic non-weekend instant (Wed 2026-01-07 12:00 UTC).
_WEEKDAY = datetime(2026, 1, 7, 12, 0, tzinfo=timezone.utc)


def _real_contract() -> ContextSnapshotSchema:
    """A genuine public-contract instance -- the exact type context/ hands downstream consumers."""
    return ContextSnapshotSchema(
        snapshot_id=generate_snapshot_id(),
        created_at=datetime.now(timezone.utc),
        symbol="XAUUSD",
        timeframe="M15",
        timestamp=_WEEKDAY,
        structure=StructureInfo(trend="BULLISH", bos=True, choch=False, swing_state="HH"),
        liquidity=LiquidityInfo(sweep_detected=True, liquidity_type="BUY_SIDE_LIQUIDITY"),
        zones=ZonesInfo(order_block=True, fvg=True),
        session=SessionInfo(current_session="LONDON"),
        regime="HIGH_VOLATILITY",
    )


def test_facade_reads_the_real_public_contract():
    data = MarketManager().build_market_data(_real_contract(), now=_WEEKDAY)
    # symbol/timeframe/timestamp come straight off the contract.
    assert data.symbol == "XAUUSD"
    assert data.timeframe == "M15"
    assert data.timestamp == _WEEKDAY
    # Structure projection matches contract.structure verbatim.
    assert data.trend is TrendState.BULLISH
    assert data.structure.bos is True
    assert data.structure.swing_state == "HH"
    assert data.structure.order_block is True
    assert data.structure.fvg is True
    # Liquidity projection matches contract.liquidity.
    assert data.liquidity.sweep_detected is True
    assert data.liquidity.buy_side is True
    # Session projection matches contract.session (weekday -> label kept).
    assert data.session.current_session == "LONDON"
    assert data.session.label == "LONDON"
    # Regime + volatility projected from contract.regime.
    assert data.regime.regime == "HIGH_VOLATILITY"
    assert data.volatility is VolatilityLevel.HIGH


def test_snapshot_of_real_contract_round_trips_to_primitives():
    snap = MarketManager().build_snapshot(_real_contract(), now=_WEEKDAY)
    d = snap.to_dict()
    assert d["symbol"] == "XAUUSD"
    assert d["trend"] == TrendState.BULLISH.value
    assert d["regime"] == "HIGH_VOLATILITY"
    assert d["volatility"] == VolatilityLevel.HIGH.value
    assert d["order_block"] is True and d["fvg"] is True
    assert d["liquidity_sweep"] is True
    assert d["liquidity_type"] == "BUY_SIDE_LIQUIDITY"


def test_empty_real_contract_projects_to_honest_defaults():
    empty = ContextSnapshotSchema(
        snapshot_id=generate_snapshot_id(),
        created_at=datetime.now(timezone.utc),
        symbol="XAUUSD",
        timeframe="M15",
    )
    data = MarketManager().build_market_data(empty, now=_WEEKDAY)
    assert data.trend is TrendState.UNKNOWN
    assert data.structure.bos is False
    assert data.liquidity.sweep_detected is False
    assert data.regime.regime == "UNKNOWN"
    assert data.volatility is VolatilityLevel.UNKNOWN
