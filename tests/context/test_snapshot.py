"""
Phase A16 -- Context Snapshot tests: creation, immutability, and the
from_context_snapshot() adapter (context/snapshot.py).

No mocking -- real ContextSnapshot objects, built either via
build_context_snapshot() over real candles or hand-constructed (same
convention as tests/features/test_feature_engine.py).
"""

import dataclasses
from datetime import datetime, timedelta, timezone

import pytest

from context.context_orchestrator import build_context_snapshot, ContextSnapshot
from context.market_regime import MarketRegimeResult, MarketRegime, RegimeDirection
from context.snapshot import (
    ContextSnapshotSchema,
    StructureInfo,
    LiquidityInfo,
    ZonesInfo,
    SessionInfo,
    SnapshotMetadata,
    generate_snapshot_id,
    from_context_snapshot,
)
from data.twelve_data_client import Candle

BASE = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _candles(n=60):
    return [
        Candle(
            timestamp=BASE + timedelta(minutes=15 * i),
            open=100.0 + i * 0.1, high=105.0 + i * 0.1, low=95.0 + i * 0.1, close=101.0 + i * 0.1,
        )
        for i in range(n)
    ]


def _empty_context(**overrides) -> ContextSnapshot:
    base = dict(
        candles=(), structure=(), bos_events=(), choch_events=(),
        liquidity_zones=(), liquidity_sweeps=(), order_blocks=(), fair_value_gaps=(),
        amd_events=(), wyckoff_events=(), session_events=(),
        market_regime=MarketRegimeResult(regime=MarketRegime.UNKNOWN, direction=RegimeDirection.NEUTRAL, confidence=0.0, reasons=[]),
    )
    base.update(overrides)
    return ContextSnapshot(**base)


def test_snapshot_creation_with_minimal_fields():
    snapshot_id = generate_snapshot_id()
    created_at = datetime.now(timezone.utc)

    schema = ContextSnapshotSchema(snapshot_id=snapshot_id, created_at=created_at)

    assert schema.snapshot_id == snapshot_id
    assert schema.created_at == created_at
    assert schema.version == "1.0"
    assert schema.symbol is None
    assert schema.timeframe is None
    assert schema.timestamp is None
    assert schema.structure == StructureInfo()
    assert schema.liquidity == LiquidityInfo()
    assert schema.zones == ZonesInfo()
    assert schema.session == SessionInfo()
    assert schema.regime == "UNKNOWN"
    assert schema.metadata == SnapshotMetadata()


def test_snapshot_creation_with_full_fields_matches_director_example_shape():
    schema = ContextSnapshotSchema(
        snapshot_id=generate_snapshot_id(),
        created_at=datetime.now(timezone.utc),
        symbol="XAUUSD",
        timeframe="M15",
        timestamp=datetime(2026, 7, 14, 10, 0, tzinfo=timezone.utc),
        structure=StructureInfo(trend="BULLISH", bos=True, choch=False, swing_state="HH"),
        liquidity=LiquidityInfo(sweep_detected=True, liquidity_type="SELL_SIDE_LIQUIDITY"),
        session=SessionInfo(current_session="LONDON"),
        regime="TRENDING",
    )

    assert schema.symbol == "XAUUSD"
    assert schema.timeframe == "M15"
    assert schema.structure.trend == "BULLISH"
    assert schema.structure.bos is True
    assert schema.structure.choch is False
    assert schema.liquidity.sweep_detected is True
    assert schema.liquidity.liquidity_type == "SELL_SIDE_LIQUIDITY"
    assert schema.session.current_session == "LONDON"
    assert schema.regime == "TRENDING"


def test_generate_snapshot_id_produces_unique_real_ids():
    ids = {generate_snapshot_id() for _ in range(100)}
    assert len(ids) == 100
    for snapshot_id in ids:
        assert isinstance(snapshot_id, str)
        assert len(snapshot_id) == 36  # standard UUID4 string length


def test_snapshot_cannot_mutate():
    schema = ContextSnapshotSchema(snapshot_id=generate_snapshot_id(), created_at=datetime.now(timezone.utc))
    with pytest.raises(dataclasses.FrozenInstanceError):
        schema.symbol = "EURUSD"


def test_nested_info_groups_cannot_mutate():
    with pytest.raises(dataclasses.FrozenInstanceError):
        StructureInfo().trend = "BULLISH"
    with pytest.raises(dataclasses.FrozenInstanceError):
        LiquidityInfo().sweep_detected = True


def test_future_compatibility_field_shape_is_stable():
    field_names = {f.name for f in dataclasses.fields(ContextSnapshotSchema)}
    assert field_names == {
        "snapshot_id", "created_at", "version", "symbol", "timeframe", "timestamp",
        "structure", "liquidity", "zones", "session", "regime", "metadata",
    }
    assert {f.name for f in dataclasses.fields(StructureInfo)} == {"trend", "bos", "choch", "swing_state"}
    assert {f.name for f in dataclasses.fields(LiquidityInfo)} == {"sweep_detected", "liquidity_type"}
    assert {f.name for f in dataclasses.fields(ZonesInfo)} == {"order_block", "fvg", "premium_discount"}
    assert {f.name for f in dataclasses.fields(SessionInfo)} == {"current_session"}
    assert {f.name for f in dataclasses.fields(SnapshotMetadata)} == {"source", "engine_version"}


def test_adapter_builds_valid_schema_from_real_context():
    context = build_context_snapshot(_candles())
    schema = from_context_snapshot(context)

    assert schema.symbol == "XAUUSD"
    assert schema.timeframe == "M15"
    assert schema.timestamp == context.candles[-1].timestamp
    assert schema.regime == context.market_regime.regime.value
    assert schema.metadata.source == "ContextEngine"


def test_adapter_handles_empty_context_without_crashing():
    schema = from_context_snapshot(_empty_context())

    assert schema.timestamp is None
    assert schema.structure.trend is None
    assert schema.liquidity.sweep_detected is False
    assert schema.zones.premium_discount is None  # no detector exists -- always None
    assert schema.session.current_session is None
    assert schema.regime == "UNKNOWN"


def test_adapter_accepts_symbol_and_timeframe_overrides():
    schema = from_context_snapshot(_empty_context(), symbol="EURUSD", timeframe="H1", engine_version="2.0")
    assert schema.symbol == "EURUSD"
    assert schema.timeframe == "H1"
    assert schema.metadata.engine_version == "2.0"


def test_adapter_reflects_bos_and_choch_presence():
    from context.bos import BosEvent, BosDirection
    from context.market_structure import StructurePoint, SwingPoint, SwingType, StructureType

    swing = SwingPoint(index=0, price=100.0, timestamp=BASE, type=SwingType.HIGH)
    structure_point = StructurePoint(swing=swing, structure=StructureType.HIGHER_HIGH)
    bos_event = BosEvent(index=1, timestamp=BASE, direction=BosDirection.BULLISH, broken_structure=structure_point)

    context = _empty_context(bos_events=(bos_event,), structure=(structure_point,))
    schema = from_context_snapshot(context)

    assert schema.structure.bos is True
    assert schema.structure.choch is False
    assert schema.structure.swing_state == "HH"
    assert schema.structure.trend == "BULLISH"


def test_existing_context_snapshot_and_detectors_are_untouched():
    """The adapter is purely additive -- constructing the real ContextSnapshot the exact way core/pipeline.py already does must keep working identically."""
    context = build_context_snapshot(_candles())
    assert isinstance(context, ContextSnapshot)
    assert hasattr(context, "market_regime")
