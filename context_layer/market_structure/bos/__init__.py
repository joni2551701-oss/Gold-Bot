"""context_layer/market_structure/bos -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `bos.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `bos.py`.
"""
from context_layer.market_structure.bos.bos import (
    dataclass,
    Enum,
    List,
    Sequence,
    datetime,
    Candle,
    StructurePoint,
    StructureType,
    setup_logger,
    logger,
    BosDirection,
    BosEvent,
    detect_bos,
)

__all__ = [
    "dataclass",
    "Enum",
    "List",
    "Sequence",
    "datetime",
    "Candle",
    "StructurePoint",
    "StructureType",
    "setup_logger",
    "logger",
    "BosDirection",
    "BosEvent",
    "detect_bos",
]
