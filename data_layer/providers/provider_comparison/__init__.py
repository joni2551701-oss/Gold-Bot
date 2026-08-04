"""data_layer/providers/provider_comparison -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `provider_comparison.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `provider_comparison.py`.
"""
from data_layer.providers.provider_comparison.provider_comparison import (
    dataclass,
    datetime,
    Dict,
    List,
    Sequence,
    TYPE_CHECKING,
    DEFAULT_TOLERANCE,
    ProviderComparison,
    compare_providers,
)

__all__ = [
    "dataclass",
    "datetime",
    "Dict",
    "List",
    "Sequence",
    "TYPE_CHECKING",
    "DEFAULT_TOLERANCE",
    "ProviderComparison",
    "compare_providers",
]
