"""data_layer.live_data.market_calendar — canonical module.

Code migrated from the pre-freeze package; internals unchanged (SMR-001).

Canonical documentation: 01_Data_Layer/Live_Data/MarketCalendar/README.md
"""

from data_layer.live_data.market_calendar.market_calendar import (
    ForexMarketCalendar,
    is_market_open,
    is_weekend,
)

__all__ = [
    "ForexMarketCalendar",
    "is_market_open",
    "is_weekend",
]
