"""
TwelveDataHistoricalProvider -- a HistoricalProvider adapter over the
existing `data_layer.providers.twelve_data_client.TwelveDataClient` (v1.1 Phase 1,
module 5). The one place that knows Twelve Data for historical loads.

Reuse (Art. 11): wraps `TwelveDataClient.fetch_candles` (the same raw
fetch the stream's TwelveDataProvider uses) rather than re-implementing
HTTP. Not exercised by unit tests (needs a live key); the orchestrator is
tested against a fake historical provider.

This module never imports from any layer above data/.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from data_layer.providers.twelve_data_client import TwelveDataClient, Candle
from data_layer.live_data.stream_event import (
    ProviderHealth, ProviderStatus, ProviderCapabilities,
)
from data_layer.historical_data.historical_provider import HistoricalProvider


class TwelveDataHistoricalProvider(HistoricalProvider):
    """Polling historical adapter (Twelve Data)."""

    _CAPABILITIES = ProviderCapabilities(
        supports_streaming=False,
        supports_polling=True,
        supports_replay=False,
        supports_historical=True,
        supports_volume=False,
    )

    def __init__(self, client: Optional[TwelveDataClient] = None):
        self._client = client or TwelveDataClient()
        self._last_error: Optional[str] = None

    @property
    def capabilities(self) -> ProviderCapabilities:
        return self._CAPABILITIES

    def fetch_recent(self, asset: str, timeframe: str, count: int) -> List[Candle]:
        return self._sorted(self._client.fetch_candles(asset, timeframe, count))

    def fetch_range(self, asset: str, timeframe: str,
                    start: datetime, end: datetime) -> List[Candle]:
        # Twelve Data returns the most recent N; fetch a generous window
        # and filter to [start, end). Module 6/live tuning may refine the
        # requested size; the filter keeps correctness provider-agnostic.
        candles = self._client.fetch_candles(asset, timeframe, outputsize=5000)
        return [c for c in self._sorted(candles)
                if start <= self._utc(c.timestamp) < end]

    def health(self) -> ProviderHealth:
        status = ProviderStatus.UP if self._last_error is None else ProviderStatus.DOWN
        return ProviderHealth(status=status, last_error=self._last_error)

    @staticmethod
    def _sorted(candles: List[Candle]) -> List[Candle]:
        return sorted(candles, key=lambda c: c.timestamp)

    @staticmethod
    def _utc(dt: datetime) -> datetime:
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
