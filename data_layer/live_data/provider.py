"""
PriceProvider -- the abstract, vendor-agnostic provider interface
(DD-048, DD-049). Price Stream depends ONLY on this; it never names
Twelve Data, Binance, Polygon, AlphaVantage, etc. Swapping a provider
implementation changes nothing above this interface.

This module never imports from any layer above data/.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from data_layer.live_data.stream_event import (
    StreamEvent,
    ProviderHealth,
    ProviderStatus,
    ProviderCapabilities,
)


class PriceProvider(ABC):
    """Abstract price provider. Exactly the DD-048 surface + capabilities."""

    @property
    @abstractmethod
    def capabilities(self) -> ProviderCapabilities:
        """Declared capabilities (DD-049) the stream reads, not guesses."""
        raise NotImplementedError

    @abstractmethod
    def connect(self) -> None:
        """Open the connection / session. May raise; PriceStream isolates it."""
        raise NotImplementedError

    @abstractmethod
    def disconnect(self) -> None:
        """Close the connection. Must be safe to call idempotently."""
        raise NotImplementedError

    @abstractmethod
    def read(self) -> List[StreamEvent]:
        """Return 0+ StreamEvents observed since the last read."""
        raise NotImplementedError

    @abstractmethod
    def health(self) -> ProviderHealth:
        """A standardized health snapshot."""
        raise NotImplementedError

    @abstractmethod
    def status(self) -> ProviderStatus:
        """Current provider status (UP/DOWN/MARKET_CLOSED/RATE_LIMITED)."""
        raise NotImplementedError
