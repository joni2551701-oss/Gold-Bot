"""data_layer/historical_data/historical_data_collector -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `historical_data_collector.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `historical_data_collector.py`.
"""
from data_layer.historical_data.historical_data_collector.historical_data_collector import (
    dataclass,
    datetime,
    timezone,
    TYPE_CHECKING,
    List,
    Optional,
    INTERVAL_DELTAS,
    RawCandleRepository,
    setup_logger,
    logger,
    MAX_FETCH_LIMIT,
    CollectionResult,
    collect_historical_candles,
    sync_historical_candles,
)

__all__ = [
    "dataclass",
    "datetime",
    "timezone",
    "TYPE_CHECKING",
    "List",
    "Optional",
    "INTERVAL_DELTAS",
    "RawCandleRepository",
    "setup_logger",
    "logger",
    "MAX_FETCH_LIMIT",
    "CollectionResult",
    "collect_historical_candles",
    "sync_historical_candles",
]
