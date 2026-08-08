"""data_layer/providers/twelve_data_client -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `twelve_data_client.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `twelve_data_client.py`.
"""
from data_layer.providers.twelve_data_client.twelve_data_client import (
    time,
    requests,
    List,
    Optional,
    dataclass,
    datetime,
    timezone,
    Secrets,
    setup_logger,
    logger,
    Candle,
    TwelveDataClient,
)

__all__ = [
    "time",
    "requests",
    "List",
    "Optional",
    "dataclass",
    "datetime",
    "timezone",
    "Secrets",
    "setup_logger",
    "logger",
    "Candle",
    "TwelveDataClient",
]
