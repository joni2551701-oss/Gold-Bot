"""data_layer/normalization/symbol_mapper -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `symbol_mapper.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `symbol_mapper.py`.
"""
from data_layer.normalization.symbol_mapper.symbol_mapper import (
    Dict,
    to_provider_symbol,
    from_provider_symbol,
    is_known_symbol,
)

__all__ = [
    "Dict",
    "to_provider_symbol",
    "from_provider_symbol",
    "is_known_symbol",
]
