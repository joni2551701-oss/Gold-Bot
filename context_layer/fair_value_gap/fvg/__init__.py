"""context_layer/fair_value_gap/fvg -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `fvg.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `fvg.py`.
"""
from context_layer.fair_value_gap.fvg.fvg import (
    dataclass,
    Enum,
    List,
    Sequence,
    datetime,
    Candle,
    FvgType,
    FairValueGap,
    detect_fvg,
)

__all__ = [
    "dataclass",
    "Enum",
    "List",
    "Sequence",
    "datetime",
    "Candle",
    "FvgType",
    "FairValueGap",
    "detect_fvg",
]
