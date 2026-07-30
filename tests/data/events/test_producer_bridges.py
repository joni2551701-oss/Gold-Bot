"""
End-to-end tests: producer hooks -> bus (module 7), verifying producers
stay decoupled (wired only via their existing hook parameter).
"""

from datetime import datetime, timezone, timedelta

from data.candle_builder import CandleBuilder
from data.memory.market_memory import MarketMemory
from data.bootstrap.bootstrap_state import BootstrapState
from data.events.event_bus import EventBus
from data.events.event_model import EventType
from data.events.producer_bridges import CandleEventBridge, BootstrapEventBridge


def _dt(minute, second=0):
    return datetime(2026, 7, 24, 13, tzinfo=timezone.utc) + timedelta(
        minutes=minute, seconds=second)


def test_candle_builder_publishes_to_bus():
    bus = EventBus()
    seen = []
    bus.subscribe("MARKET", lambda e: seen.append((e.type, e.asset, e.correlation_id)))

    mem = MarketMemory("XAUUSD", {"M1": 100})
    builder = CandleBuilder("XAUUSD", mem,
                            event_hook=CandleEventBridge(bus, "XAUUSD"))

    builder.on_price(100.0, _dt(0, 10))     # open M1 (13:00)
    builder.on_price(105.0, _dt(0, 30))     # update
    builder.on_price(110.0, _dt(1, 5))      # boundary -> close + open (13:01)

    types = [t for (t, _a, _c) in seen]
    assert EventType.MARKET_CANDLE_OPENED in types
    assert EventType.MARKET_CANDLE_UPDATED in types
    assert EventType.MARKET_CANDLE_CLOSED in types
    assert all(a == "XAUUSD" for (_t, a, _c) in seen)
    # the first candle's open+update share one correlation id (candle_id)
    first_open = next(c for (t, _a, c) in seen if t is EventType.MARKET_CANDLE_OPENED)
    first_update = next(c for (t, _a, c) in seen if t is EventType.MARKET_CANDLE_UPDATED)
    assert first_open == first_update


def test_bootstrap_bridge_publishes_with_correlation():
    bus = EventBus()
    seen = []
    bus.subscribe("BOOTSTRAP", lambda e: seen.append((e.type, e.correlation_id)))

    bridge = BootstrapEventBridge(bus)
    bridge.on_bootstrap_started("XAUUSD")
    bridge.on_timeframe_completed("XAUUSD", "M1", BootstrapState.READY)
    bridge.on_bootstrap_completed("XAUUSD")

    types = [t for (t, _c) in seen]
    assert types == [EventType.BOOTSTRAP_STARTED,
                     EventType.BOOTSTRAP_TIMEFRAME_COMPLETED,
                     EventType.BOOTSTRAP_COMPLETED]
    # all three events of one run share the same correlation id (amendment 2)
    corrs = {c for (_t, c) in seen}
    assert len(corrs) == 1
