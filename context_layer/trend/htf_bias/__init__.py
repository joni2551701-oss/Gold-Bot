"""context_layer/trend/htf_bias -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `htf_bias.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `htf_bias.py`.
"""
from context_layer.trend.htf_bias.htf_bias import (
    dataclass,
    Enum,
    Dict,
    Sequence,
    Tuple,
    MarketSnapshot,
    Candle,
    ContextConfig,
    detect_swing_points,
    classify_structure,
    most_recent_bias,
    setup_logger,
    logger,
    SUPPORTED_HTF_TIMEFRAMES,
    HTFBias,
    HTFBiasResult,
    compute_htf_bias,
)

__all__ = [
    "dataclass",
    "Enum",
    "Dict",
    "Sequence",
    "Tuple",
    "MarketSnapshot",
    "Candle",
    "ContextConfig",
    "detect_swing_points",
    "classify_structure",
    "most_recent_bias",
    "setup_logger",
    "logger",
    "SUPPORTED_HTF_TIMEFRAMES",
    "HTFBias",
    "HTFBiasResult",
    "compute_htf_bias",
]
