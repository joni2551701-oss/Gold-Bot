"""data_layer/live_data/bitget_price_source -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `bitget_price_source.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `bitget_price_source.py`.
"""
from data_layer.live_data.bitget_price_source.bitget_price_source import (
    annotations,
    datetime,
    timezone,
    List,
    Optional,
    setup_logger,
    CandleSource,
    BitgetProvider,
    PriceProvider,
    StreamEvent,
    ProviderHealth,
    ProviderStatus,
    ProviderCapabilities,
    logger,
    BitgetPriceSource,
)

__all__ = [
    "annotations",
    "datetime",
    "timezone",
    "List",
    "Optional",
    "setup_logger",
    "CandleSource",
    "BitgetProvider",
    "PriceProvider",
    "StreamEvent",
    "ProviderHealth",
    "ProviderStatus",
    "ProviderCapabilities",
    "logger",
    "BitgetPriceSource",
]
