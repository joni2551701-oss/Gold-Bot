"""
TwelveDataPriceSource -- a PriceProvider adapter over the existing
`data_layer.providers.twelve_data_client.TwelveDataClient.get_price()`
real-time `/price` endpoint (REAL-DATA-008).

Why this module exists (Module Reuse Principle, steps 1-2 both "no"):
  1. Does a current-price PriceProvider already exist? No. The only
     existing XAUUSD PriceProvider is `TwelveDataProvider`, which sources
     from the CANDLE endpoint (`fetch_candles()` -> candle.close, only on
     candle close) -- that is candle polling, not a real-time price tick
     (the REAL-DATA-007 finding).
  2. Can `TwelveDataProvider` be extended without breaking its contract?
     No. Its `read()` semantics (candle close + candle timestamp +
     de-dupe on candle timestamp) are a different, still-used contract
     (its own unit tests assert it). Changing it in place would break
     that contract; a separate, small adapter is the correct reuse.

This is the ONE place Price Stream knows about TwelveData's /price
endpoint (DD-048). It presents `TwelveDataClient.get_price()` (real
current spot price, NOT candle close) as a stream provider. Each
`read()` is ONE observation with a fresh `datetime.now(timezone.utc)`
timestamp -- correct semantics for a current-price tick, since /price
returns no timestamp of its own. No de-duplication on price: a repeated
identical price is a valid tick (an unchanged current value is fine).

Fail-safe like the other sources: a failed read flips status DOWN and
propagates the exception, which `PriceStream` already isolates (DD-051).
Never logs/prints/embeds the API key (the client keeps it in params).

This module never imports from any layer above data/.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from core_layer.logger.logger import setup_logger
from data_layer.providers.twelve_data_client import TwelveDataClient
from data_layer.market_memory.candle_record import CandleSource
from data_layer.live_data.provider import PriceProvider
from data_layer.live_data.stream_event import (
    StreamEvent, ProviderHealth, ProviderStatus, ProviderCapabilities,
)

logger = setup_logger("TwelveDataPriceSource")


class TwelveDataPriceSource(PriceProvider):
    """Polling-based TwelveData /price adapter: real current spot price as
    the stream tick (NOT candle close). REAL-DATA-008."""

    _CAPABILITIES = ProviderCapabilities(
        supports_streaming=False,
        supports_polling=True,
        supports_replay=False,
        supports_historical=False,
        supports_volume=False,
    )

    def __init__(self, asset: str = "XAUUSD",
                 client: Optional[TwelveDataClient] = None):
        self._asset = asset
        self._client = client or TwelveDataClient()
        self._status = ProviderStatus.DOWN
        self._last_error: Optional[str] = None

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
        price = self._client.get_price(self._asset)
        if price is None:
            return []
        # Observation timestamp: /price returns no timestamp of its own, so
        # the moment we observed the tick IS the correct timestamp for a
        # current-price observation. No de-dupe on price (a repeated value
        # is a valid tick).
        self._status = ProviderStatus.UP
        return [StreamEvent(
            asset=self._asset,
            price=price,
            timestamp=datetime.now(timezone.utc),
            volume=None,
            source=CandleSource.STREAM,
        )]

    def health(self) -> ProviderHealth:
        return ProviderHealth(status=self._status, detail=self._asset,
                              last_error=self._last_error)

    def status(self) -> ProviderStatus:
        return self._status
