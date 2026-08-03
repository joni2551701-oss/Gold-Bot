"""
data_layer.live_data -- GoldBot v1.1 Market Data Foundation: Price Stream
(Phase 1 module 4).

Provider-agnostic live price ingestion (DD-048): a universal lifecycle
state machine (DD-046) with a waiting mode (DD-047) that feeds
StreamEvents into the module-3 CandleBuilder (single-writer into
MarketMemory). Vendor SDKs live only behind provider adapters.

- stream_event.py        -- StreamEvent + state/status/capability models
- provider.py            -- PriceProvider abstract interface (DD-048/049)
- twelve_data_provider.py-- Twelve Data adapter (wraps data_layer.providers.twelve_data_client)
- price_stream.py        -- per-asset lifecycle state machine + waiting mode
- stream_manager.py      -- multi-asset supervision over the registry

This package never imports from telegram/, ai/, decision/, risk/,
strategies/, signals/, context/, or database/.
"""

from data_layer.live_data.stream_event import (
    StreamEvent,
    StreamState,
    ProviderStatus,
    ProviderHealth,
    ProviderCapabilities,
    AssetClass,
)
from data_layer.live_data.provider import PriceProvider
from data_layer.live_data.price_stream import (
    PriceStream,
    MarketCalendar,
    AlwaysOpenCalendar,
)
from data_layer.live_data.stream_manager import StreamManager

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

# Canonical documentation: 01_Data_Layer/Live_Data/README.md
