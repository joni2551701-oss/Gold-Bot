"""Unit tests for data_layer/live_data/market_calendar.py (TASK-ARCH-101).

Anchor dates (UTC): 2026-07-20 Mon, -24 Fri, -25 Sat, -26 Sun, -27 Mon.
"""

from datetime import datetime, timezone

from data_layer.live_data.market_calendar import (
    ForexMarketCalendar, is_weekend, is_market_open,
)


def _utc(y, mo, d, h=0):
    return datetime(y, mo, d, h, tzinfo=timezone.utc)


# -- is_weekend / is_market_open (legacy clock, preserved) ------------

def test_saturday_is_weekend():
    assert is_weekend(_utc(2026, 7, 25, 12)) is True
    assert is_market_open(_utc(2026, 7, 25, 12)) is False


def test_sunday_before_2200_is_weekend_after_is_open():
    assert is_weekend(_utc(2026, 7, 26, 21)) is True     # Sun 21:00 -> closed
    assert is_weekend(_utc(2026, 7, 26, 22)) is False    # Sun 22:00 -> open
    assert is_market_open(_utc(2026, 7, 26, 22)) is True


def test_friday_after_2200_is_weekend():
    assert is_weekend(_utc(2026, 7, 24, 21)) is False    # Fri 21:00 -> open
    assert is_weekend(_utc(2026, 7, 24, 22)) is True     # Fri 22:00 -> closed


def test_weekday_is_open():
    assert is_market_open(_utc(2026, 7, 22, 12)) is True  # Wednesday


# -- ForexMarketCalendar (implements the MarketCalendar protocol) -----

def test_calendar_is_open_matches_clock():
    cal = ForexMarketCalendar()
    assert cal.is_open(_utc(2026, 7, 22, 12)) is True     # Wed
    assert cal.is_open(_utc(2026, 7, 25, 12)) is False    # Sat


def test_next_open_from_saturday_is_sunday_2200():
    cal = ForexMarketCalendar()
    nxt = cal.next_open(_utc(2026, 7, 25, 12))            # Sat -> next Sun 22:00
    assert nxt == _utc(2026, 7, 26, 22)


def test_next_open_from_sunday_morning_is_same_day_2200():
    cal = ForexMarketCalendar()
    nxt = cal.next_open(_utc(2026, 7, 26, 9))             # Sun 09:00 -> Sun 22:00
    assert nxt == _utc(2026, 7, 26, 22)


def test_next_open_from_friday_night_is_sunday_2200():
    cal = ForexMarketCalendar()
    nxt = cal.next_open(_utc(2026, 7, 24, 23))            # Fri 23:00 -> Sun 22:00
    assert nxt == _utc(2026, 7, 26, 22)


def test_next_open_when_already_open_returns_now():
    cal = ForexMarketCalendar()
    now = _utc(2026, 7, 22, 12)
    assert cal.next_open(now) == now


def test_satisfies_marketcalendar_protocol_in_pricestream():
    # ForexMarketCalendar plugs into PriceStream's existing calendar slot.
    from data_layer.live_data.price_stream import PriceStream
    from data_layer.live_data.stream_event import AssetClass
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from _fakes import FakeProvider, RecordingSink
    s = PriceStream("XAUUSD", FakeProvider(), RecordingSink(),
                    calendar=ForexMarketCalendar(), asset_class=AssetClass.METAL)
    assert s.asset == "XAUUSD"
