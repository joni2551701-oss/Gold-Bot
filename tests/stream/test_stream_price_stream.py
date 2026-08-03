"""TASK-CORE-004 -- PriceStream orchestration: flow, weekend pause, poll."""

from datetime import datetime, timedelta, timezone
from typing import List, Optional, Tuple

from data_layer.providers.base_provider import MarketCandle, MarketDataProvider, ProviderStatus
from data_layer.live_data.stream.price_stream import PriceStream
from data_layer.live_data.stream.stream_event import StreamEvent
from data_layer.live_data.stream.stream_subscriber import CallbackSubscriber

# 2026-01-05 is a Monday (market open); 2026-01-03 is a Saturday.
MONDAY = datetime(2026, 1, 5, 12, tzinfo=timezone.utc)
SATURDAY = datetime(2026, 1, 3, 12, tzinfo=timezone.utc)


def _event(ts, close=2005.0):
    return StreamEvent(symbol="XAUUSD", timeframe="M15", timestamp=ts,
                       open=2000.0, high=2010.0, low=1995.0, close=close, provider="twelvedata")


def test_valid_event_routes_on_weekday():
    stream = PriceStream()
    got = []
    stream.subscribe(CallbackSubscriber("market", lambda e: got.append(e)))
    result = stream.ingest_event(_event(MONDAY), now=MONDAY)
    assert result.routed is True
    assert got  # subscriber received it
    assert stream.current_price.price_of("XAUUSD") == 2005.0
    assert stream.state.last_price == 2005.0


def test_weekend_pauses_routing_but_updates_state():
    stream = PriceStream()
    got = []
    stream.subscribe(CallbackSubscriber("market", lambda e: got.append(e)))
    result = stream.ingest_event(_event(SATURDAY), now=SATURDAY)
    # Weekend -> not routed, but the event was accepted and current
    # price/state still updated (stream waits, doesn't break).
    assert result.routed is False
    assert result.mode.value == "weekend_wait"
    assert not got
    assert stream.current_price.price_of("XAUUSD") == 2005.0


def test_manual_hold_pauses_routing():
    stream = PriceStream()
    got = []
    stream.subscribe(CallbackSubscriber("market", lambda e: got.append(e)))
    result = stream.ingest_event(_event(MONDAY), now=MONDAY, manual_hold=True)
    assert result.routed is False
    assert result.mode.value == "manual_hold"
    assert not got


def test_invalid_event_dropped_not_routed():
    stream = PriceStream()
    got = []
    stream.subscribe(CallbackSubscriber("market", lambda e: got.append(e)))
    bad = StreamEvent(symbol="XAUUSD", timeframe="M15", timestamp=MONDAY,
                      open=2000.0, high=1990.0, low=1995.0, close=2005.0)  # high < low
    result = stream.ingest_event(bad, now=MONDAY)
    assert result.accepted is False
    assert result.routed is False
    assert not got


def test_duplicate_event_dropped():
    stream = PriceStream()
    stream.ingest_event(_event(MONDAY), now=MONDAY)
    result = stream.ingest_event(_event(MONDAY), now=MONDAY)  # same ts -> duplicate
    assert result.accepted is False
    assert result.validation.code == "duplicate"


def test_sequence_advances_across_events():
    stream = PriceStream()
    r1 = stream.ingest_event(_event(MONDAY, close=2005.0), now=MONDAY)
    r2 = stream.ingest_event(_event(MONDAY + timedelta(minutes=15), close=2008.0), now=MONDAY + timedelta(minutes=15))
    assert r1.routed and r2.routed
    assert stream.current_price.price_of("XAUUSD") == 2008.0


def test_ingest_candle_from_marketcandle():
    stream = PriceStream()
    got = []
    stream.subscribe(CallbackSubscriber("chart", lambda e: got.append(e)))
    candle = MarketCandle(symbol="XAUUSD", timeframe="M15", open=2000.0, high=2010.0,
                          low=1995.0, close=2008.0, timestamp=MONDAY, provider="twelvedata")
    result = stream.ingest_candle(candle, now=MONDAY)
    assert result.routed and got
    assert got[0].source == "provider"


# --- poll() against a ProviderManager-like object -----------------------

class _FakeLiveProvider(MarketDataProvider):
    def get_provider_name(self) -> str:
        return "twelvedata"

    def get_supported_timeframes(self) -> Tuple[str, ...]:
        return ("M15",)

    def get_candles(self, symbol, timeframe, limit) -> List[MarketCandle]:
        return [MarketCandle(symbol=symbol, timeframe=timeframe, open=2000.0, high=2010.0,
                             low=1995.0, close=2006.0, timestamp=MONDAY, provider="twelvedata")]

    def get_latest_price(self, symbol) -> Optional[float]:
        return 2006.0

    def get_market_status(self) -> ProviderStatus:
        return ProviderStatus(available=True)


class _FakeManager:
    def __init__(self, provider):
        self._provider = provider

    def resolve(self, symbol=None):
        return self._provider


def test_poll_ingests_from_active_provider():
    stream = PriceStream()
    got = []
    stream.subscribe(CallbackSubscriber("market", lambda e: got.append(e)))
    results = stream.poll(_FakeManager(_FakeLiveProvider()), "XAUUSD", "M15", now=MONDAY)
    assert len(results) == 1
    assert results[0].routed
    assert got[0].source == "poll"
    assert stream.current_price.price_of("XAUUSD") == 2006.0


def test_poll_no_provider_returns_empty():
    stream = PriceStream()
    results = stream.poll(_FakeManager(None), "XAUUSD", "M15", now=MONDAY)
    assert results == []


def test_poll_stub_provider_not_implemented_returns_empty():
    class _Stub(_FakeLiveProvider):
        def get_candles(self, symbol, timeframe, limit):
            raise NotImplementedError("stub")
    results = PriceStream().poll(_FakeManager(_Stub()), "XAUUSD", "M15", now=MONDAY)
    assert results == []
