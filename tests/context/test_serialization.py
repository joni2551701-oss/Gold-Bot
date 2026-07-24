"""
Phase A16 -- Context Snapshot tests: serialization
(context/snapshot.py's to_dict()/to_json()/from_dict()/from_json()).
"""

import json
from datetime import datetime, timezone

from context.snapshot import (
    ContextSnapshotSchema,
    StructureInfo,
    LiquidityInfo,
    ZonesInfo,
    SessionInfo,
    SnapshotMetadata,
    generate_snapshot_id,
)


def _full_schema():
    return ContextSnapshotSchema(
        snapshot_id=generate_snapshot_id(),
        created_at=datetime.now(timezone.utc),
        symbol="XAUUSD",
        timeframe="M15",
        timestamp=datetime(2026, 7, 14, 10, 0, tzinfo=timezone.utc),
        structure=StructureInfo(trend="BULLISH", bos=True, choch=False, swing_state="HH"),
        liquidity=LiquidityInfo(sweep_detected=True, liquidity_type="SELL_SIDE_LIQUIDITY"),
        zones=ZonesInfo(order_block=True, fvg=False, premium_discount=None),
        session=SessionInfo(current_session="LONDON"),
        regime="TRENDING",
        metadata=SnapshotMetadata(source="ContextEngine", engine_version="1.0"),
    )


def test_to_dict_is_json_safe_and_nested():
    schema = _full_schema()
    data = schema.to_dict()

    assert isinstance(data, dict)
    assert isinstance(data["structure"], dict)
    assert data["structure"]["trend"] == "BULLISH"
    assert isinstance(data["created_at"], str)
    assert isinstance(data["timestamp"], str)
    json.dumps(data)  # raises TypeError if anything isn't JSON-native


def test_to_dict_renders_none_timestamp_as_none_not_a_string():
    schema = ContextSnapshotSchema(snapshot_id=generate_snapshot_id(), created_at=datetime.now(timezone.utc))
    data = schema.to_dict()
    assert data["timestamp"] is None


def test_to_json_produces_valid_json():
    schema = _full_schema()
    parsed = json.loads(schema.to_json())

    assert parsed["snapshot_id"] == schema.snapshot_id
    assert parsed["symbol"] == "XAUUSD"
    assert parsed["structure"]["swing_state"] == "HH"
    assert parsed["liquidity"]["liquidity_type"] == "SELL_SIDE_LIQUIDITY"


def test_json_roundtrip_produces_an_equal_object():
    """Python object -> JSON -> object must return the same value (Phase A16's explicit round-trip requirement)."""
    original = _full_schema()

    restored = ContextSnapshotSchema.from_json(original.to_json())

    assert restored == original


def test_dict_roundtrip_produces_an_equal_object():
    original = _full_schema()

    restored = ContextSnapshotSchema.from_dict(original.to_dict())

    assert restored == original


def test_roundtrip_preserves_none_fields():
    original = ContextSnapshotSchema(snapshot_id=generate_snapshot_id(), created_at=datetime.now(timezone.utc))

    restored = ContextSnapshotSchema.from_dict(original.to_dict())

    assert restored == original
    assert restored.symbol is None
    assert restored.timestamp is None
    assert restored.structure.trend is None


def test_from_dict_tolerates_missing_optional_keys():
    """A minimal dict (only the required identity fields) must still reconstruct cleanly."""
    minimal = {
        "snapshot_id": generate_snapshot_id(),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    restored = ContextSnapshotSchema.from_dict(minimal)

    assert restored.version == "1.0"
    assert restored.regime == "UNKNOWN"
    assert restored.structure == StructureInfo()
    assert restored.metadata == SnapshotMetadata()
