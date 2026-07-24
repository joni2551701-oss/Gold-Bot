"""
Phase A15 -- Signal Schema tests: validate_signal()
(signals/schema.py).
"""

from datetime import datetime, timezone

from signals.schema import SignalSchema, generate_signal_id, validate_signal


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


def test_valid_buy_signal_passes():
    result = validate_signal(_schema(direction="BUY", stop_loss=4190.0, entry_price=4200.0, take_profit=4220.0))
    assert result.valid is True
    assert result.errors == []


def test_valid_sell_signal_passes():
    result = validate_signal(_schema(direction="SELL", take_profit=4180.0, entry_price=4200.0, stop_loss=4210.0))
    assert result.valid is True
    assert result.errors == []


def test_valid_none_direction_signal_passes_without_prices():
    schema = _schema(direction="NONE", entry_price=None, stop_loss=None, take_profit=None)
    result = validate_signal(schema)
    assert result.valid is True
    assert result.errors == []


def test_missing_required_fields_is_blocked():
    schema = _schema(signal_id="", symbol="", timeframe="")
    result = validate_signal(schema)

    assert result.valid is False
    assert "signal_id is required" in result.errors
    assert "symbol is required" in result.errors
    assert "timeframe is required" in result.errors


def test_missing_direction_and_created_at_is_blocked():
    schema = _schema(direction="", created_at=None, entry_price=None, stop_loss=None, take_profit=None)
    result = validate_signal(schema)

    assert result.valid is False
    assert "direction is required" in result.errors
    assert "created_at is required" in result.errors


def test_invalid_direction_is_blocked():
    for bad_direction in ("LONGGG", "SHORT", "long", "buy"):
        schema = _schema(direction=bad_direction, entry_price=None, stop_loss=None, take_profit=None)
        result = validate_signal(schema)
        assert result.valid is False
        assert any("direction must be one of" in e for e in result.errors)


def test_buy_requires_stop_loss_below_entry_below_take_profit():
    # inverted: entry above take_profit
    schema = _schema(direction="BUY", stop_loss=4190.0, entry_price=4225.0, take_profit=4220.0)
    result = validate_signal(schema)
    assert result.valid is False
    assert any("BUY requires stop_loss < entry_price < take_profit" in e for e in result.errors)


def test_sell_requires_take_profit_below_entry_below_stop_loss():
    # inverted: take_profit above entry
    schema = _schema(direction="SELL", take_profit=4205.0, entry_price=4200.0, stop_loss=4210.0)
    result = validate_signal(schema)
    assert result.valid is False
    assert any("SELL requires take_profit < entry_price < stop_loss" in e for e in result.errors)


def test_buy_or_sell_without_prices_is_blocked():
    schema = _schema(direction="BUY", entry_price=None, stop_loss=None, take_profit=None)
    result = validate_signal(schema)
    assert result.valid is False
    assert any("required for a BUY/SELL direction" in e for e in result.errors)


def test_invalid_decision_status_is_blocked():
    schema = _schema(decision="MAYBE")
    result = validate_signal(schema)
    assert result.valid is False
    assert any("decision must be one of" in e for e in result.errors)


def test_pending_decision_is_always_valid():
    schema = _schema(decision="PENDING")
    result = validate_signal(schema)
    assert result.valid is True


def test_multiple_errors_all_reported_together():
    schema = _schema(direction="INVALID", symbol="", stop_loss=None, entry_price=None, take_profit=None)
    result = validate_signal(schema)

    assert result.valid is False
    assert len(result.errors) >= 2  # symbol required + invalid direction, at minimum
