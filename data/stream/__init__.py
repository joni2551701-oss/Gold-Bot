"""
data.stream -- GoldBot v1.1 Market Data Foundation: Price Stream
(Phase 1 module 4).

Provider-agnostic live price ingestion (DD-048): a universal lifecycle
state machine (DD-046) with a waiting mode (DD-047) that feeds
StreamEvents into the module-3 CandleBuilder (single-writer into
MarketMemory). Vendor SDKs live only behind provider adapters.

- stream_event.py        -- StreamEvent + state/status/capability models
- provider.py            -- PriceProvider abstract interface (DD-048/049)
- twelve_data_provider.py-- Twelve Data adapter (wraps data.twelve_data_client)
- price_stream.py        -- per-asset lifecycle state machine + waiting mode
- stream_manager.py      -- multi-asset supervision over the registry

This package never imports from telegram/, ai/, decision/, risk/,
strategies/, signals/, context/, or database/.
"""

from data.stream.stream_event import (
    StreamEvent,
    StreamState,
    ProviderStatus,
    ProviderHealth,
    ProviderCapabilities,
    AssetClass,
)
from data.stream.provider import PriceProvider
from data.stream.price_stream import (
    PriceStream,
    MarketCalendar,
    AlwaysOpenCalendar,
)
from data.stream.stream_manager import StreamManager

__all__ = [
    "StreamEvent",
    "StreamState",
    "ProviderStatus",
    "ProviderHealth",
    "ProviderCapabilities",
    "AssetClass",
    "PriceProvider",
    "PriceStream",
    "MarketCalendar",
    "AlwaysOpenCalendar",
    "StreamManager",
]
