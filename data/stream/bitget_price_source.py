"""
BitgetPriceSource -- a PriceProvider adapter over the existing
`data.providers.bitget_provider.BitgetProvider` stub (TASK-DATA-001,
Price Stream Foundation).

Mirrors `twelve_data_provider.py`'s role for BTCUSDT: the ONE place
Price Stream knows about Bitget (DD-048). It presents the existing,
honest `BitgetProvider` stub (no real exchange connection --
`get_latest_price()` raises `NotImplementedError`) as a stream
provider rather than re-implementing the stub -- Module Reuse
Principle.

`connect()`/`status()` reflect `BitgetProvider.get_market_status()`
(always `available=False` today, per the stub); `read()` propagates
the stub's `NotImplementedError`, which `PriceStream` already isolates
(DD-051) into a standardized provider-error state -- no new failure
path is introduced. When a real Bitget connection is implemented in
`BitgetProvider`, this adapter starts working with no change above the
`PriceProvider` interface (DD-048).

This module never imports from any layer above data/.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from core.logger import setup_logger
from data.memory.candle_record import CandleSource
from data.providers.bitget_provider import BitgetProvider
from data.stream.provider import PriceProvider
from data.stream.stream_event import (
    StreamEvent, ProviderHealth, ProviderStatus, ProviderCapabilities,
)

logger = setup_logger("BitgetPriceSource")


class BitgetPriceSource(PriceProvider):
    """Polling-based Bitget adapter (BTCUSDT). Inert until BitgetProvider
    itself gains a real exchange connection -- see module docstring."""

    _CAPABILITIES = ProviderCapabilities(
        supports_streaming=False,
        supports_polling=True,
        supports_replay=False,
        supports_historical=False,
        supports_volume=True,
    )

    def __init__(self, asset: str = "BTCUSDT",
                 provider: Optional[BitgetProvider] = None):
        self._asset = asset
        self._provider = provider or BitgetProvider()
        self._status = ProviderStatus.DOWN
        self._last_error: Optional[str] = None

    @property
    def capabilities(self) -> ProviderCapabilities:
        return self._CAPABILITIES

    def connect(self) -> None:
        # Stateless HTTP polling: nothing to open. Status reflects the
        # underlying stub's own honest availability check.
        market_status = self._provider.get_market_status()
        self._status = ProviderStatus.UP if market_status.available else ProviderStatus.DOWN
        self._last_error = None if market_status.available else market_status.reason

    def disconnect(self) -> None:
        self._status = ProviderStatus.DOWN

    def read(self) -> List[StreamEvent]:
        price = self._provider.get_latest_price(self._asset)
        if price is None:
            return []
        ts = datetime.now(timezone.utc)
        self._status = ProviderStatus.UP
        return [StreamEvent(
            asset=self._asset,
            price=price,
            timestamp=ts,
            volume=None,
            source=CandleSource.STREAM,
        )]

    def health(self) -> ProviderHealth:
        return ProviderHealth(status=self._status, detail=self._asset,
                              last_error=self._last_error)

    def status(self) -> ProviderStatus:
        return self._status
