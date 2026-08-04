"""core_layer/features/atr -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `atr.py`; this `__init__` re-exports the public surface
so the import path stays stable.
"""
from core_layer.features.atr.atr import compute_atr

__all__ = [
    "compute_atr",
]
