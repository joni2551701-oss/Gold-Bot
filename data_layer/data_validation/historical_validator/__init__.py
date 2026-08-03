"""01_Data_Layer / Data_Validation / HistoricalValidator -- data_layer.data_validation.historical_validator.

Canonical module package (GoldBot Engineering Law GEL-001: one module =
one package). The implementation lives in `historical_validator.py` inside
this package; this `__init__` re-exports the module's public surface so the
established import path stays stable:

    from data_layer.data_validation.historical_validator import validate_historical_candles

HistoricalValidator validates a completed historical candle series
(coverage, ordering, gaps) and returns an immutable `ValidationReport`. It
reuses DataQuality's INTERVAL_DELTAS and never generates signals, trades,
or uses AI. See README.md / CONTRACTS.md in this package.
"""

from data_layer.data_validation.historical_validator.historical_validator import (
    ValidationReport,
    validate_historical_candles,
)

__all__ = [
    "ValidationReport",
    "validate_historical_candles",
]
