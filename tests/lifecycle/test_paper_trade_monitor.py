"""
Phase 59.4, TASK 2 -- trade_monitoring_layer/paper_trading/paper_trade_monitor.py tests.
"""

from datetime import datetime, timezone

from data_layer.providers.twelve_data_client import Candle
from trade_monitoring_layer.paper_trading.paper_trade import create_paper_trade, open_paper_trade
from trade_monitoring_layer.paper_trading.paper_trade_monitor import check_paper_trade_against_candles
from trade_monitoring_layer.paper_trading.trade_state import TradeState
from signal_layer.signal_builder.schema import SignalSchema


def _signal(direction="BUY", entry=2000.0, sl=1990.0, tp=2020.0):
    return SignalSchema(
        signal_id="sig-1", created_at=datetime.now(timezone.utc), symbol="XAUUSD", timeframe="M15",
        direction=direction, entry_price=entry, stop_loss=sl, take_profit=tp, decision="APPROVED",
    )


def _opened_trade(**signal_kwargs):
    trade = create_paper_trade(_signal(**signal_kwargs))
    return open_paper_trade(trade).trade


def _candle(ts, open_, high, low, close):
    return Candle(timestamp=ts, open=open_, high=high, low=low, close=close)


T0 = datetime(2026, 1, 1, 0, 0, tzinfo=timezone.utc)
T1 = datetime(2026, 1, 1, 0, 15, tzinfo=timezone.utc)
T2 = datetime(2026, 1, 1, 0, 30, tzinfo=timezone.utc)


def test_monitoring_a_non_open_trade_fails_cleanly():
    trade = create_paper_trade(_signal())  # still CREATED, never opened

    result = check_paper_trade_against_candles(trade, [])

    assert result.success is False
    assert result.trade is trade


def test_empty_candle_list_marks_expired_since_entry_never_touched():
    trade = _opened_trade()

    result = check_paper_trade_against_candles(trade, [])

    assert result.success is True
    assert result.trade.status == TradeState.CLOSED
    assert result.trade.result == "EXPIRED"


def test_entry_never_touched_across_the_whole_window_is_expired():
    trade = _opened_trade(entry=2000.0)
    candles = [_candle(T0, 2100, 2105, 2095, 2100)]  # never near 2000

    result = check_paper_trade_against_candles(trade, candles)

    assert result.trade.result == "EXPIRED"


def test_entry_touched_then_take_profit_hit_buy():
    trade = _opened_trade(direction="BUY", entry=2000.0, sl=1990.0, tp=2020.0)
    candles = [
        _candle(T0, 2005, 2005, 1999, 2000),   # touches entry
        _candle(T1, 2000, 2021, 1999, 2020),   # touches TP
    ]

    result = check_paper_trade_against_candles(trade, candles)

    assert result.trade.status == TradeState.CLOSED
    assert result.trade.result == "TP"


def test_entry_touched_then_stop_loss_hit_buy():
    trade = _opened_trade(direction="BUY", entry=2000.0, sl=1990.0, tp=2020.0)
    candles = [
        _candle(T0, 2005, 2005, 1999, 2000),
        _candle(T1, 2000, 2001, 1989, 1990),   # touches SL
    ]

    result = check_paper_trade_against_candles(trade, candles)

    assert result.trade.result == "SL"


def test_entry_touched_but_still_undecided_stays_open():
    trade = _opened_trade(direction="BUY", entry=2000.0, sl=1990.0, tp=2020.0)
    candles = [_candle(T0, 2005, 2005, 1999, 2000)]  # touches entry, nowhere near TP/SL

    result = check_paper_trade_against_candles(trade, candles)

    assert result.success is True
    assert result.trade.status == TradeState.OPEN  # unchanged


def test_entry_and_tp_and_sl_all_in_one_candle_assumes_sl_first():
    """Ambiguity rule: conservative -- SL wins when a single candle's range covers both."""
    trade = _opened_trade(direction="BUY", entry=2000.0, sl=1990.0, tp=2020.0)
    candles = [_candle(T0, 2000, 2025, 1985, 2010)]  # covers entry, TP, and SL all at once

    result = check_paper_trade_against_candles(trade, candles)

    assert result.trade.result == "SL"


def test_sell_direction_take_profit():
    trade = _opened_trade(direction="SELL", entry=2000.0, sl=2010.0, tp=1980.0)
    candles = [
        _candle(T0, 2000, 2001, 1999, 2000),   # touches entry
        _candle(T1, 2000, 2001, 1979, 1980),   # low touches TP for SELL
    ]

    result = check_paper_trade_against_candles(trade, candles)

    assert result.trade.result == "TP"


def test_sell_direction_stop_loss():
    trade = _opened_trade(direction="SELL", entry=2000.0, sl=2010.0, tp=1980.0)
    candles = [
        _candle(T0, 2000, 2001, 1999, 2000),
        _candle(T1, 2005, 2011, 2004, 2010),   # high touches SL for SELL
    ]

    result = check_paper_trade_against_candles(trade, candles)

    assert result.trade.result == "SL"


def test_entry_touched_in_the_same_candle_as_take_profit():
    """Entry and TP resolving within the same candle -- entry check and TP check both happen against that candle."""
    trade = _opened_trade(direction="BUY", entry=2000.0, sl=1990.0, tp=2020.0)
    candles = [_candle(T0, 2000, 2025, 1999, 2020)]  # touches entry AND TP in one candle

    result = check_paper_trade_against_candles(trade, candles)

    assert result.trade.result == "TP"


def test_candles_before_entry_touch_are_ignored_for_tp_sl():
    """A candle that touches SL/TP price levels BEFORE entry is ever reached must not close the trade -- it was never actually 'in' the market yet."""
    trade = _opened_trade(direction="BUY", entry=2000.0, sl=1990.0, tp=2020.0)
    candles = [
        _candle(T0, 2100, 2105, 2095, 2100),   # far away, no entry yet -- even though unrelated to SL/TP
        _candle(T1, 2005, 2005, 1999, 2000),   # entry touched here
        _candle(T2, 2000, 2021, 1999, 2020),   # TP hit here
    ]

    result = check_paper_trade_against_candles(trade, candles)

    assert result.trade.result == "TP"


def test_never_raises_on_malformed_direction():
    trade = _opened_trade(direction="BUY")
    # Force an unexpected direction value onto a copy, defensively.
    import dataclasses
    weird_trade = dataclasses.replace(trade, direction="SIDEWAYS")

    result = check_paper_trade_against_candles(weird_trade, [_candle(T0, 2000, 2005, 1995, 2000)])

    assert result.success is True  # still open, no crash, no false TP/SL
    assert result.trade.status == TradeState.OPEN
