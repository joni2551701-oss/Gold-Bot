"""01_Data_Layer / Data_Validation / DataQuality -- data_layer.data_validation.data_quality.

Canonical module package (GoldBot Engineering Law GEL-001: one module =
one package). The implementation lives in `data_quality.py` inside this
package; this `__init__` re-exports the module's public surface so the
established import path stays stable:

    from data_layer.data_validation.data_quality import assess_data_quality

DataQuality assesses market-data integrity (OHLC validity, duplicate and
missing candles, timeframe alignment) and returns an immutable
`DataQualityResult`. It never generates signals, never trades, never uses
AI -- pure data validation. See README.md / CONTRACTS.md in this package.
"""

from data_layer.data_validation.data_quality.data_quality import (
    INTERVAL_DELTAS,
    INVALID_OHLC_PENALTY,
    DUPLICATE_CANDLE_PENALTY,
    MISSING_CANDLE_PENALTY,
    TIMEFRAME_MISMATCH_PENALTY,
    DataQualityResult,
    assess_data_quality,
)

__all__ = [
    "INTERVAL_DELTAS",
    "INVALID_OHLC_PENALTY",
    "DUPLICATE_CANDLE_PENALTY",
    "MISSING_CANDLE_PENALTY",
    "TIMEFRAME_MISMATCH_PENALTY",
    "DataQualityResult",
    "assess_data_quality",
]
