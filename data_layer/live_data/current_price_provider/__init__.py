"""data_layer.live_data.current_price_provider — canonical module.

Code migrated from the pre-freeze package; internals unchanged (SMR-001).

Canonical documentation: 01_Data_Layer/Live_Data/CurrentPriceProvider/README.md
"""

from data_layer.live_data.current_price_provider.current_price_provider import (
    CurrentPrice,
    CurrentPriceProvider,
    LastPriceSource,
    PriceStreamLastPriceSource,
    SmartCacheLastPriceSource,
    build_default_current_price_provider,
    logger,
)

__all__ = [
    "CurrentPrice",
    "CurrentPriceProvider",
    "LastPriceSource",
    "PriceStreamLastPriceSource",
    "SmartCacheLastPriceSource",
    "build_default_current_price_provider",
    "logger",
]
