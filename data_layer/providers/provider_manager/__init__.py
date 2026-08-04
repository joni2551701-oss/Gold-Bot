"""data_layer/providers/provider_manager -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `provider_manager.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `provider_manager.py`.
"""
from data_layer.providers.provider_manager.provider_manager import (
    Dict,
    List,
    Optional,
    config,
    MarketDataProvider,
    ProviderRegistry,
    build_default_registry,
    ProviderManager,
)

__all__ = [
    "Dict",
    "List",
    "Optional",
    "config",
    "MarketDataProvider",
    "ProviderRegistry",
    "build_default_registry",
    "ProviderManager",
]
