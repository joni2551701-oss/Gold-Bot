"""
Phase 59 Preparation, TASK 2 -- trade_monitoring_layer/paper_trading/paper_trade.py tests.
"""

from datetime import datetime, timezone

import pytest

from trade_monitoring_layer.paper_trading.paper_trade import (
    ALLOWED_PAPER_TRADE_RESULTS,
    cancel_paper_trade,
    close_paper_trade,
    create_paper_trade,
    generate_trade_id,
    open_paper_trade,
)
from trade_monitoring_layer.paper_trading.trade_state import TradeState
from signal_layer.signal_builder.schema import SignalSchema


def _approved_signal(**overrides) -> SignalSchema:
    base = dict(
        signal_id="sig-1",
        created_at=datetime.now(timezone.utc),
        symbol="XAUUSD",
        timeframe="M15",
        direction="BUY",
        entry_price=2000.0,
        stop_loss=1990.0,
        take_profit=2020.0,
        decision="APPROVED",
    )
    base.update(overrides)
    return SignalSchema(**base)


def test_create_paper_trade_from_approved_signal():
    signal = _approved_signal()
    trade = create_paper_trade(signal)

    assert trade.status == TradeState.CREATED
    assert trade.signal_id == "sig-1"
    assert trade.symbol == "XAUUSD"
    assert trade.direction == "BUY"
    assert trade.entry == 2000.0
    assert trade.stop_loss == 1990.0
    assert trade.take_profit == 2020.0
    assert trade.result is None
    assert trade.opened_at is None
    assert trade.closed_at is None


def test_create_paper_trade_rejects_non_approved_signal():
    signal = _approved_signal(decision="PENDING")
    with pytest.raises(ValueError):
        create_paper_trade(signal)


def test_create_paper_trade_rejects_missing_prices():
    signal = _approved_signal(entry_price=None)
    with pytest.raises(ValueError):
        create_paper_trade(signal)


def test_trade_id_is_unique_per_trade():
    signal = _approved_signal()
    trade_a = create_paper_trade(signal)
    trade_b = create_paper_trade(signal)
    assert trade_a.trade_id != trade_b.trade_id


def test_open_paper_trade_transitions_created_to_open():
    trade = create_paper_trade(_approved_signal())
    result = open_paper_trade(trade)

    assert result.success is True
    assert result.trade.status == TradeState.OPEN
    assert result.trade.opened_at is not None


def test_open_paper_trade_fails_when_not_created():
    trade = create_paper_trade(_approved_signal())
    opened = open_paper_trade(trade).trade

    result = open_paper_trade(opened)  # already OPEN

    assert result.success is False
    assert result.trade is opened  # unchanged, original returned


def test_close_paper_trade_transitions_open_to_closed():
    trade = create_paper_trade(_approved_signal())
    opened = open_paper_trade(trade).trade

    result = close_paper_trade(opened, "TP")

    assert result.success is True
    assert result.trade.status == TradeState.CLOSED
    assert result.trade.result == "TP"
    assert result.trade.closed_at is not None


def test_close_paper_trade_fails_when_not_open():
    trade = create_paper_trade(_approved_signal())  # still CREATED

    result = close_paper_trade(trade, "TP")

    assert result.success is False
    assert result.trade is trade


def test_close_paper_trade_rejects_invalid_result():
    trade = create_paper_trade(_approved_signal())
    opened = open_paper_trade(trade).trade

    result = close_paper_trade(opened, "WIN")  # not in ALLOWED_PAPER_TRADE_RESULTS

    assert result.success is False
    assert opened.status == TradeState.OPEN  # unchanged


@pytest.mark.parametrize("result_value", ALLOWED_PAPER_TRADE_RESULTS)
def test_close_paper_trade_accepts_every_allowed_result(result_value):
    trade = create_paper_trade(_approved_signal())
    opened = open_paper_trade(trade).trade

    result = close_paper_trade(opened, result_value)

    assert result.success is True
    assert result.trade.result == result_value


def test_cancel_paper_trade_from_created():
    trade = create_paper_trade(_approved_signal())

    result = cancel_paper_trade(trade)

    assert result.success is True
    assert result.trade.status == TradeState.CANCELLED
    assert result.trade.result is None


def test_cancel_paper_trade_from_open():
    trade = create_paper_trade(_approved_signal())
    opened = open_paper_trade(trade).trade

    result = cancel_paper_trade(opened)

    assert result.success is True
    assert result.trade.status == TradeState.CANCELLED


def test_cancel_paper_trade_fails_when_already_closed():
    trade = create_paper_trade(_approved_signal())
    opened = open_paper_trade(trade).trade
    closed = close_paper_trade(opened, "SL").trade

    result = cancel_paper_trade(closed)

    assert result.success is False
    assert result.trade is closed


def test_full_happy_path_created_open_closed():
    signal = _approved_signal()
    trade = create_paper_trade(signal)
    assert trade.status == TradeState.CREATED

    trade = open_paper_trade(trade).trade
    assert trade.status == TradeState.OPEN

    trade = close_paper_trade(trade, "TP").trade
    assert trade.status == TradeState.CLOSED
    assert trade.result == "TP"


def test_paper_trade_is_frozen():
    trade = create_paper_trade(_approved_signal())
    with pytest.raises(Exception):
        trade.status = TradeState.OPEN


def test_to_dict_renders_status_and_result_as_plain_strings():
    trade = create_paper_trade(_approved_signal())
    opened = open_paper_trade(trade).trade
    closed = close_paper_trade(opened, "BE").trade

    data = closed.to_dict()

    assert data["status"] == "CLOSED"
    assert data["result"] == "BE"
    assert isinstance(data["opened_at"], str)
    assert isinstance(data["closed_at"], str)


def test_generate_trade_id_returns_uuid_shaped_string():
    value = generate_trade_id()
    assert isinstance(value, str)
    assert len(value) == 36
