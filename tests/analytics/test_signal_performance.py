"""
Phase 59 Preparation, TASK 3 -- backtesting_layer/statistics/signal_performance.py tests.
"""

import dataclasses
from datetime import datetime, timedelta, timezone

from backtesting_layer.statistics.signal_performance import (
    compute_r_multiple,
    compute_signal_performance,
    generate_performance_id,
)
from trade_monitoring_layer.paper_trading.paper_trade import cancel_paper_trade, create_paper_trade, open_paper_trade, close_paper_trade
from signal_layer.signal_builder.schema import SignalSchema


def _signal(**overrides) -> SignalSchema:
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
        strategy_name="LIQUIDITY_SWEEP_STRATEGY",
        context_id="ctx-1",
    )
    base.update(overrides)
    return SignalSchema(**base)


# --- compute_r_multiple ---

def test_r_multiple_buy_tp_is_planned_rr():
    value = compute_r_multiple("BUY", entry=2000.0, stop_loss=1990.0, take_profit=2020.0, result="TP")
    assert value == 2.0  # (2020-2000)/(2000-1990)


def test_r_multiple_sell_tp_is_planned_rr():
    value = compute_r_multiple("SELL", entry=2000.0, stop_loss=2010.0, take_profit=1980.0, result="TP")
    assert value == 2.0  # (2000-1980)/(2010-2000)


def test_r_multiple_sl_is_minus_one():
    value = compute_r_multiple("BUY", entry=2000.0, stop_loss=1990.0, take_profit=2020.0, result="SL")
    assert value == -1.0


def test_r_multiple_be_is_zero():
    value = compute_r_multiple("BUY", entry=2000.0, stop_loss=1990.0, take_profit=2020.0, result="BE")
    assert value == 0.0


def test_r_multiple_expired_is_none():
    value = compute_r_multiple("BUY", entry=2000.0, stop_loss=1990.0, take_profit=2020.0, result="EXPIRED")
    assert value is None


def test_r_multiple_none_result_is_none():
    value = compute_r_multiple("BUY", entry=2000.0, stop_loss=1990.0, take_profit=2020.0, result=None)
    assert value is None


def test_r_multiple_zero_denominator_never_raises():
    value = compute_r_multiple("BUY", entry=2000.0, stop_loss=2000.0, take_profit=2020.0, result="TP")
    assert value == 0.0


# --- compute_signal_performance ---

def test_no_paper_trade_produces_all_none_result_fields():
    signal = _signal()
    performance = compute_signal_performance(signal)

    assert performance.signal_id == "sig-1"
    assert performance.strategy_id == "LIQUIDITY_SWEEP_STRATEGY"
    assert performance.context_id == "ctx-1"
    assert performance.result is None
    assert performance.profit_loss is None
    assert performance.r_multiple is None
    assert performance.duration is None


def test_closed_paper_trade_populates_result_and_r_multiple():
    signal = _signal()
    trade = create_paper_trade(signal)
    opened = open_paper_trade(trade).trade
    closed = close_paper_trade(opened, "TP").trade

    performance = compute_signal_performance(signal, paper_trade=closed)

    assert performance.result == "TP"
    assert performance.r_multiple == 2.0


def test_duration_computed_from_opened_and_closed_at():
    signal = _signal()
    trade = create_paper_trade(signal)
    opened = open_paper_trade(trade).trade
    # Force a known, non-zero duration for a deterministic assertion.
    opened = dataclasses.replace(opened, opened_at=datetime.now(timezone.utc) - timedelta(seconds=30))
    closed = close_paper_trade(opened, "BE").trade

    performance = compute_signal_performance(signal, paper_trade=closed)

    assert performance.duration is not None
    assert performance.duration >= 30.0


def test_session_and_market_phase_pass_through_when_supplied():
    signal = _signal()
    performance = compute_signal_performance(signal, session="LONDON", market_phase="MARKUP")

    assert performance.session == "LONDON"
    assert performance.market_phase == "MARKUP"


def test_profit_loss_is_always_none():
    signal = _signal()
    trade = create_paper_trade(signal)
    opened = open_paper_trade(trade).trade
    closed = close_paper_trade(opened, "TP").trade

    performance = compute_signal_performance(signal, paper_trade=closed)

    assert performance.profit_loss is None  # honest hook, never fabricated


def test_missing_price_fields_never_raises():
    signal = _signal(entry_price=None, stop_loss=None, take_profit=None, direction="NONE", decision="REJECTED")
    performance = compute_signal_performance(signal)  # must not raise
    assert performance.r_multiple is None


def test_performance_id_is_unique_per_call():
    signal = _signal()
    a = compute_signal_performance(signal)
    b = compute_signal_performance(signal)
    assert a.performance_id != b.performance_id


def test_to_dict_and_to_json_never_raise():
    import json

    signal = _signal()
    performance = compute_signal_performance(signal)
    data = performance.to_dict()
    json.loads(performance.to_json())
    assert data["signal_id"] == "sig-1"


def test_generate_performance_id_returns_uuid_shaped_string():
    value = generate_performance_id()
    assert isinstance(value, str)
    assert len(value) == 36


# --- Phase 59.4 TASK 1: CANCELLED result derivation ---

def test_cancelled_trade_from_created_produces_cancelled_result():
    signal = _signal()
    trade = create_paper_trade(signal)
    cancelled = cancel_paper_trade(trade).trade

    performance = compute_signal_performance(signal, paper_trade=cancelled)

    assert performance.result == "CANCELLED"


def test_cancelled_trade_from_open_produces_cancelled_result():
    signal = _signal()
    trade = create_paper_trade(signal)
    opened = open_paper_trade(trade).trade
    cancelled = cancel_paper_trade(opened).trade

    performance = compute_signal_performance(signal, paper_trade=cancelled)

    assert performance.result == "CANCELLED"


def test_cancelled_trade_has_no_r_multiple():
    signal = _signal()
    trade = create_paper_trade(signal)
    cancelled = cancel_paper_trade(trade).trade

    performance = compute_signal_performance(signal, paper_trade=cancelled)

    assert performance.r_multiple is None


# --- Phase 59 Real Market Validation Foundation, TASK 6: timeframe field ---

def test_timeframe_copied_from_signal():
    signal = _signal(timeframe="H1")
    performance = compute_signal_performance(signal)

    assert performance.timeframe == "H1"


def test_closed_trade_result_is_unaffected_by_the_cancelled_fix():
    """Regression guard: a normally CLOSED trade's real TP/SL/BE/EXPIRED result must not be shadowed by the new CANCELLED-detection branch."""
    signal = _signal()
    trade = create_paper_trade(signal)
    opened = open_paper_trade(trade).trade
    closed = close_paper_trade(opened, "TP").trade

    performance = compute_signal_performance(signal, paper_trade=closed)

    assert performance.result == "TP"
