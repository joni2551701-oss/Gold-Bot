"""data_layer/providers/fundamental_base -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `fundamental_base.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `fundamental_base.py`.
"""
from data_layer.providers.fundamental_base.fundamental_base import (
    abstractmethod,
    asdict,
    dataclass,
    field,
    datetime,
    Dict,
    Optional,
    DataProvider,
    FundamentalDataPoint,
    FundamentalSnapshot,
    FundamentalDataProvider,
)

__all__ = [
    "abstractmethod",
    "asdict",
    "dataclass",
    "field",
    "datetime",
    "Dict",
    "Optional",
    "DataProvider",
    "FundamentalDataPoint",
    "FundamentalSnapshot",
    "FundamentalDataProvider",
]
