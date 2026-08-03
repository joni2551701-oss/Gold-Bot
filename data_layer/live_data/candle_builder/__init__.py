"""data_layer.live_data.candle_builder — canonical module.

Code migrated from the pre-freeze package; internals unchanged (SMR-001).

Canonical documentation: 01_Data_Layer/Live_Data/CandleBuilder/README.md
"""

from data_layer.live_data.candle_builder.candle_builder import (
    CandleBuilder,
    CandleEventHook,
    logger,
)

__all__ = [
    "CandleBuilder",
    "CandleEventHook",
    "logger",
]
