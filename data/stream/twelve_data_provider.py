"""
TwelveDataProvider -- a PriceProvider adapter over the existing
`data.twelve_data_client.TwelveDataClient` (v1.1 Phase 1, module 4).

This is the ONE place that knows about Twelve Data (DD-048). It presents
Twelve Data's polling HTTP client as a stream provider: each `read()`
pulls the latest candle and emits its close as a StreamEvent. Swapping in
a different vendor means writing another PriceProvider adapter; nothing
above the interface changes.

Reuse (Constitution Art. 11): wraps `TwelveDataClient` rather than
re-implementing any HTTP/fetch logic. Not exercised by unit tests (needs
a live key); the state machine is tested against a fake provider.

This module never imports from any layer above data/.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from core_layer.logger.logger import setup_logger
from data.twelve_data_client import TwelveDataClient
from data.memory.candle_record import CandleSource
from data.stream.provider import PriceProvider
from data.stream.stream_event import (
    StreamEvent, ProviderHealth, ProviderStatus, ProviderCapabilities,
)

logger = setup_logger("TwelveDataProvider")


class TwelveDataProvider(PriceProvider):
    """Polling-based Twelve Data adapter (close price as the stream tick)."""

    _CAPABILITIES = ProviderCapabilities(
        supports_streaming=False,
        supports_polling=True,
        supports_replay=False,
        supports_historical=True,
        supports_volume=False,
    )

    def __init__(self, asset: str, interval: str = "M1",
                 client: Optional[TwelveDataClient] = None):
        self._asset = asset
        self._interval = interval
        self._client = client or TwelveDataClient()
        self._status = ProviderStatus.DOWN
        self._last_error: Optional[str] = None
        self._last_ts: Optional[datetime] = None

    @property
    def capabilities(self) -> ProviderCapabilities:
        return self._CAPABILITIES

    def connect(self) -> None:
        # Stateless HTTP polling: nothing to open. Mark UP optimistically;
        # a failed read() will flip status to DOWN (isolated by PriceStream).
        self._status = ProviderStatus.UP
        self._last_error = None

    def disconnect(self) -> None:
        self._status = ProviderStatus.DOWN

    def read(self) -> List[StreamEvent]:
        candles = self._client.fetch_candles(self._asset, self._interval,
                                              outputsize=1)
        if not candles:
            return []
        candle = candles[-1]
        ts = candle.timestamp
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        # de-duplicate: only emit when a newer candle close is available
        if self._last_ts is not None and ts <= self._last_ts:
            return []
        self._last_ts = ts
        self._status = ProviderStatus.UP
        return [StreamEvent(
            asset=self._asset,
            price=candle.close,
            timestamp=ts,
            volume=None,
            source=CandleSource.STREAM,
        )]

    def health(self) -> ProviderHealth:
        return ProviderHealth(status=self._status, detail=self._interval,
                              last_error=self._last_error)

    def status(self) -> ProviderStatus:
        return self._status
