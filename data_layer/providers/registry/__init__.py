"""data_layer/providers/registry -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `registry.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `registry.py`.
"""
from data_layer.providers.registry.registry import (
    Dict,
    List,
    Optional,
    DataProvider,
    BinanceProvider,
    BitgetProvider,
    FredProvider,
    KeynorqProvider,
    MT5Provider,
    TwelveDataProvider,
    ProviderRegistry,
    build_default_registry,
)

__all__ = [
    "Dict",
    "List",
    "Optional",
    "DataProvider",
    "BinanceProvider",
    "BitgetProvider",
    "FredProvider",
    "KeynorqProvider",
    "MT5Provider",
    "TwelveDataProvider",
    "ProviderRegistry",
    "build_default_registry",
]
