"""data_layer/historical_data/gap_recovery -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `gap_recovery.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `gap_recovery.py`.
"""
from data_layer.historical_data.gap_recovery.gap_recovery import (
    annotations,
    datetime,
    timedelta,
    Optional,
    setup_logger,
    CandleClock,
    MarketMemory,
    CandleSource,
    HistoricalProvider,
    logger,
    GapRecovery,
)

__all__ = [
    "annotations",
    "datetime",
    "timedelta",
    "Optional",
    "setup_logger",
    "CandleClock",
    "MarketMemory",
    "CandleSource",
    "HistoricalProvider",
    "logger",
    "GapRecovery",
]
