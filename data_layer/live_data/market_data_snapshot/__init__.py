"""data_layer/live_data/market_data_snapshot -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `market_data_snapshot.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `market_data_snapshot.py`.
"""
from data_layer.live_data.market_data_snapshot.market_data_snapshot import (
    hashlib,
    json,
    uuid,
    asdict,
    dataclass,
    datetime,
    timezone,
    Optional,
    Sequence,
    Candle,
    MarketDataSnapshot,
    generate_market_snapshot_id,
    compute_candles_reference,
    capture_market_data_snapshot,
)

__all__ = [
    "hashlib",
    "json",
    "uuid",
    "asdict",
    "dataclass",
    "datetime",
    "timezone",
    "Optional",
    "Sequence",
    "Candle",
    "MarketDataSnapshot",
    "generate_market_snapshot_id",
    "compute_candles_reference",
    "capture_market_data_snapshot",
]
