"""data_layer/live_data/provider -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `provider.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `provider.py`.
"""
from data_layer.live_data.provider.provider import (
    annotations,
    ABC,
    abstractmethod,
    List,
    StreamEvent,
    ProviderHealth,
    ProviderStatus,
    ProviderCapabilities,
    PriceProvider,
)

__all__ = [
    "annotations",
    "ABC",
    "abstractmethod",
    "List",
    "StreamEvent",
    "ProviderHealth",
    "ProviderStatus",
    "ProviderCapabilities",
    "PriceProvider",
]
