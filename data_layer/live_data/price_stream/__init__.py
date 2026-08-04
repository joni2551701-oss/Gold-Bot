"""data_layer/live_data/price_stream -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `price_stream.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `price_stream.py`.
"""
from data_layer.live_data.price_stream.price_stream import (
    annotations,
    datetime,
    timedelta,
    timezone,
    Optional,
    List,
    Any,
    Dict,
    Protocol,
    runtime_checkable,
    setup_logger,
    PriceProvider,
    StreamEvent,
    StreamState,
    ProviderStatus,
    AssetClass,
    logger,
    MarketCalendar,
    AlwaysOpenCalendar,
    PriceStream,
)

__all__ = [
    "annotations",
    "datetime",
    "timedelta",
    "timezone",
    "Optional",
    "List",
    "Any",
    "Dict",
    "Protocol",
    "runtime_checkable",
    "setup_logger",
    "PriceProvider",
    "StreamEvent",
    "StreamState",
    "ProviderStatus",
    "AssetClass",
    "logger",
    "MarketCalendar",
    "AlwaysOpenCalendar",
    "PriceStream",
]
