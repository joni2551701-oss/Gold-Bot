"""Shared fakes for Price Stream tests (module 4)."""

from datetime import datetime, timezone, timedelta
from typing import List

from data_layer.live_data.provider import PriceProvider
from data_layer.live_data.stream_event import (
    StreamEvent, ProviderStatus, ProviderHealth, ProviderCapabilities,
)
from data_layer.market_memory.candle_record import CandleSource


def ts(i):
    return datetime(2026, 7, 24, 13, tzinfo=timezone.utc) + timedelta(seconds=i)


class FakeProvider(PriceProvider):
    """Scriptable provider for state-machine tests."""

    def __init__(self, capabilities=None):
        self._caps = capabilities or ProviderCapabilities(supports_polling=True)
        self.connect_should_fail = False
        self.read_should_fail = False
        self.connected = False
        self.connect_calls = 0
        self.disconnect_calls = 0
        self._status = ProviderStatus.DOWN
        self.batches: List[List[StreamEvent]] = []   # returned per read()

    @property
    def capabilities(self):
        return self._caps

    def connect(self):
        self.connect_calls += 1
        if self.connect_should_fail:
            raise RuntimeError("connect failed")
        self.connected = True
        self._status = ProviderStatus.UP

    def disconnect(self):
        self.disconnect_calls += 1
        self.connected = False
        self._status = ProviderStatus.DOWN

    def read(self):
        if self.read_should_fail:
            raise RuntimeError("read failed")
        return self.batches.pop(0) if self.batches else []

    def set_status(self, status):
        self._status = status

    def health(self):
        return ProviderHealth(status=self._status)

    def status(self):
        return self._status


class FakeCalendar:
    def __init__(self, open_flag=True):
        self.open_flag = open_flag

    def is_open(self, now):
        return self.open_flag

    def next_open(self, now):
        return now


class RecordingSink:
    """Minimal CandleBuilder-shaped sink that records forwarded events."""
    def __init__(self):
        self.events = []

    def on_event(self, event):
        self.events.append(event)


def event(asset="XAUUSD", price=100.0, i=0, source=CandleSource.STREAM):
    return StreamEvent(asset=asset, price=price, timestamp=ts(i), source=source)
