"""STEP-08: canonical signal model + registry (TASK-CORE-008)."""

from datetime import datetime, timezone

from signals.signal import CanonicalSignal, generate_signal_id, validate_signal
from signals.schema import SignalSchema
from signals.registry import SignalKind, kind_for_direction, is_registered, all_kinds


def _sig(direction="BUY", entry=100.0, sl=98.0, tp=104.0):
    return CanonicalSignal(
        signal_id=generate_signal_id(),
        created_at=datetime.now(timezone.utc),
        symbol="XAUUSD",
        timeframe="M15",
        direction=direction,
        entry_price=entry,
        stop_loss=sl,
        take_profit=tp,
    )


def test_canonical_signal_is_signalschema():
    # Reuse-first: CanonicalSignal IS SignalSchema, not a new duplicate model.
    assert CanonicalSignal is SignalSchema


def test_canonical_signal_serialization_roundtrip():
    s = _sig()
    d = s.to_dict()
    assert d["symbol"] == "XAUUSD" and d["direction"] == "BUY"
    assert isinstance(d["created_at"], str)  # ISO string, JSON-safe


def test_valid_and_invalid_signal():
    assert validate_signal(_sig()).valid
    bad = _sig(sl=105.0)  # BUY with SL above entry -> inverted
    assert not validate_signal(bad).valid


def test_generate_signal_id_unique():
    assert generate_signal_id() != generate_signal_id()


def test_registry_kinds():
    assert kind_for_direction("BUY") is SignalKind.BUY
    assert kind_for_direction("SELL") is SignalKind.SELL
    assert kind_for_direction("NONE") is None
    assert kind_for_direction(None) is None
    assert is_registered("WATCHLIST") and not is_registered("BOGUS")
    assert len(all_kinds()) == 6
