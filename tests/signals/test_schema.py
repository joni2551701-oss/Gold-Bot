"""
Phase A15 -- Signal Schema tests: creation and serialization
(signals/schema.py).
"""

import dataclasses
import json
from datetime import datetime, timezone

import pytest

from signals.schema import SignalSchema, generate_signal_id


def _schema(**overrides):
    base = dict(
        signal_id=generate_signal_id(),
        created_at=datetime.now(timezone.utc),
        symbol="XAUUSD",
        timeframe="M15",
        direction="BUY",
        entry_price=4200.0,
        stop_loss=4190.0,
        take_profit=4220.0,
    )
    base.update(overrides)
    return SignalSchema(**base)


def test_signal_creation_with_minimal_required_fields():
    signal_id = generate_signal_id()
    created_at = datetime.now(timezone.utc)

    schema = SignalSchema(
        signal_id=signal_id,
        created_at=created_at,
        symbol="XAUUSD",
        timeframe="M15",
        direction="NONE",
    )

    assert schema.signal_id == signal_id
    assert schema.created_at == created_at
    assert schema.symbol == "XAUUSD"
    assert schema.timeframe == "M15"
    assert schema.direction == "NONE"
    assert schema.version == "1.0"  # default
    assert schema.decision == "PENDING"  # default


def test_signal_creation_matches_director_example_shape():
    schema = _schema(
        symbol="XAUUSD",
        asset_type="GOLD",
        timeframe="M15",
        session="LONDON",
        direction="BUY",
        entry_price=4200,
        stop_loss=4190,
        take_profit=4220,
        strategy_name="Liquidity Sweep",
        strategy_version="1.0",
        quality_grade="A",
        confidence_score=87,
        explanation_id="EXP-00125",
        decision="APPROVED",
        decision_score=0.87,
        risk_id="RISK-001",
        context_id="CTX-001",
    )

    assert schema.symbol == "XAUUSD"
    assert schema.asset_type == "GOLD"
    assert schema.session == "LONDON"
    assert schema.strategy_name == "Liquidity Sweep"
    assert schema.quality_grade == "A"
    assert schema.confidence_score == 87
    assert schema.explanation_id == "EXP-00125"
    assert schema.decision == "APPROVED"
    assert schema.risk_id == "RISK-001"
    assert schema.context_id == "CTX-001"


def test_generate_signal_id_produces_unique_real_ids():
    """Same generation convention as database/signal_record.py's create_signal_record() -- str(uuid.uuid4())."""
    ids = {generate_signal_id() for _ in range(100)}
    assert len(ids) == 100
    for signal_id in ids:
        assert isinstance(signal_id, str)
        assert len(signal_id) == 36  # standard UUID4 string length


def test_signal_schema_is_immutable():
    schema = _schema()
    with pytest.raises(dataclasses.FrozenInstanceError):
        schema.direction = "SELL"


def test_to_dict_is_json_safe():
    schema = _schema()
    data = schema.to_dict()

    assert isinstance(data, dict)
    assert data["symbol"] == "XAUUSD"
    assert data["direction"] == "BUY"
    assert isinstance(data["created_at"], str)  # datetime rendered as ISO-8601 string
    # every value must already be JSON-native (no datetime/Enum objects survive)
    json.dumps(data)  # raises TypeError if not


def test_to_json_round_trips():
    schema = _schema()
    parsed = json.loads(schema.to_json())

    assert parsed["signal_id"] == schema.signal_id
    assert parsed["symbol"] == schema.symbol
    assert parsed["entry_price"] == schema.entry_price
    assert parsed["created_at"] == schema.created_at.isoformat()


def test_future_compatibility_field_shape_is_stable():
    """SignalSchema is a plain, introspectable dataclass -- a future consumer can rely on its field set."""
    field_names = {f.name for f in dataclasses.fields(SignalSchema)}
    assert field_names == {
        "signal_id", "created_at", "version", "symbol", "timeframe", "direction",
        "asset_type", "session", "entry_price", "stop_loss", "take_profit",
        "context_id", "strategy_name", "strategy_version", "quality_grade",
        "confidence_score", "explanation_id", "decision", "decision_score", "risk_id",
    }
