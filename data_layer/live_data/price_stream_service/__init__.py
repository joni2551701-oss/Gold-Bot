"""data_layer.live_data.price_stream_service — canonical module.

Code migrated from the pre-freeze package; internals unchanged (SMR-001).

Canonical documentation: 01_Data_Layer/Live_Data/PriceStreamService/README.md
"""

from data_layer.live_data.price_stream_service.price_stream_service import (
    PriceStreamService,
    build_default_price_stream_service,
    logger,
)

__all__ = [
    "PriceStreamService",
    "build_default_price_stream_service",
    "logger",
]
