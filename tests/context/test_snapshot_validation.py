"""
Phase A16 -- Context Snapshot tests: validate_snapshot()
(context/snapshot.py).
"""

from datetime import datetime, timezone

from context.snapshot import (
    ContextSnapshotSchema,
    generate_snapshot_id,
    validate_snapshot,
)


def _valid_schema(**overrides):
    base = dict(
        snapshot_id=generate_snapshot_id(),
        created_at=datetime.now(timezone.utc),
        symbol="XAUUSD",
        timeframe="M15",
        timestamp=datetime.now(timezone.utc),
        version="1.0",
    )
    base.update(overrides)
    return ContextSnapshotSchema(**base)


def test_valid_snapshot_passes():
    result = validate_snapshot(_valid_schema())
    assert result.valid is True
    assert result.errors == []


def test_missing_symbol_is_rejected():
    result = validate_snapshot(_valid_schema(symbol=None))
    assert result.valid is False
    assert "symbol is required" in result.errors


def test_missing_timeframe_is_rejected():
    result = validate_snapshot(_valid_schema(timeframe=None))
    assert result.valid is False
    assert "timeframe is required" in result.errors


def test_missing_timestamp_is_rejected():
    result = validate_snapshot(_valid_schema(timestamp=None))
    assert result.valid is False
    assert "timestamp is required" in result.errors


def test_missing_version_is_rejected():
    result = validate_snapshot(_valid_schema(version=""))
    assert result.valid is False
    assert "version is required" in result.errors


def test_invalid_snapshot_rejected_multiple_missing_fields():
    """Matches the roadmap's own {"symbol": null} example -- an invalid snapshot is rejected, not silently accepted."""
    schema = _valid_schema(symbol=None, timeframe=None, timestamp=None)
    result = validate_snapshot(schema)

    assert result.valid is False
    assert len(result.errors) == 3


def test_invalid_regime_is_rejected():
    result = validate_snapshot(_valid_schema(regime="MOON_PHASE"))
    assert result.valid is False
    assert any("regime must be one of" in e for e in result.errors)


def test_every_real_regime_value_is_accepted():
    for regime in ("TRENDING", "RANGE", "ACCUMULATION", "DISTRIBUTION", "HIGH_VOLATILITY", "LOW_VOLATILITY", "UNKNOWN"):
        result = validate_snapshot(_valid_schema(regime=regime))
        assert result.valid is True, f"{regime} should be valid"


def test_default_minimal_snapshot_is_invalid_until_fields_supplied():
    """Constructing with just identity fields never raises, but IS invalid per validate_snapshot()."""
    minimal = ContextSnapshotSchema(snapshot_id=generate_snapshot_id(), created_at=datetime.now(timezone.utc))
    result = validate_snapshot(minimal)

    assert result.valid is False
    assert "symbol is required" in result.errors
    assert "timeframe is required" in result.errors
    assert "timestamp is required" in result.errors
