"""Shared fakes for Historical Bootstrap tests (module 5)."""

from datetime import datetime, timezone, timedelta

from data_layer.providers.twelve_data_client import Candle
from data_layer.historical_data.historical_provider import HistoricalProvider
from data_layer.live_data.stream_event import (
    ProviderHealth, ProviderStatus, ProviderCapabilities,
)


def ts(i, tf_minutes=1):
    return datetime(2026, 7, 24, tzinfo=timezone.utc) + timedelta(
        minutes=i * tf_minutes)


def candle(i, close=100.0, tf_minutes=1):
    t = ts(i, tf_minutes)
    return Candle(timestamp=t, open=close, high=close, low=close, close=close)


class FakeHistoricalProvider(HistoricalProvider):
    def __init__(self):
        self._caps = ProviderCapabilities(supports_historical=True,
                                          supports_polling=True)
        self.recent = {}          # (asset, tf) -> list[Candle]
        self.range_pool = {}      # (asset, tf) -> list[Candle]
        self.recent_calls = 0
        self.range_calls = 0

    @property
    def capabilities(self):
        return self._caps

    def fetch_recent(self, asset, timeframe, count):
        self.recent_calls += 1
        return list(self.recent.get((asset, timeframe), []))[-count:]

    def fetch_range(self, asset, timeframe, start, end):
        self.range_calls += 1
        return [c for c in self.range_pool.get((asset, timeframe), [])
                if start <= c.timestamp < end]

    def health(self):
        return ProviderHealth(status=ProviderStatus.UP)
