"""data_layer/live_data/market_data_service -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `market_data_service.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `market_data_service.py`.
"""
from data_layer.live_data.market_data_service.market_data_service import (
    annotations,
    Any,
    List,
    Optional,
    setup_logger,
    MarketDataNormalizer,
    MarketSnapshot,
    Candle,
    logger,
    MarketDataService,
    build_default_market_data_service,
    get_shared_market_data_service,
    reset_shared_market_data_service,
)

__all__ = [
    "annotations",
    "Any",
    "List",
    "Optional",
    "setup_logger",
    "MarketDataNormalizer",
    "MarketSnapshot",
    "Candle",
    "logger",
    "MarketDataService",
    "build_default_market_data_service",
    "get_shared_market_data_service",
    "reset_shared_market_data_service",
]
