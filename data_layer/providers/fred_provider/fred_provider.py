"""
Data Layer — FRED Provider stub (Phase 59.2, TASK 4).

The Director's own brief marks this "juda muhim" (very important) for
Gold specifically -- DXY, interest rates, CPI, inflation, and Fed data
are all established macro drivers of XAUUSD. Still a **foundation
only** in this phase: no real connection to FRED's API (api.stlouisfed.org)
exists in this file -- no `requests` call, no API key read, no
`core/secrets.py` entry. Every data-fetch method raises
NotImplementedError, the same honest-stub pattern
mt5_provider.py/binance_provider.py already established.

Series IDs below were verified against fred.stlouisfed.org (not
guessed) -- see docs/PROVIDER_CONTRACTS.md's sources. One deliberate
disclosure: "DXY" (the popular ICE US Dollar Index most traders mean
by that name) is not itself a free FRED series; DTWEXBGS (FRED's own
"Nominal Broad U.S. Dollar Index") is the closest available public
proxy, a different but related calculation -- not the same number,
never claimed to be.

Phase 60.5 (Fundamental Intelligence Foundation, TASK 3) adds
collect_snapshot() -- an extension of this same class (Module Reuse
Principle: extend, don't create a new collector module), not a new
file. It composes the three methods above into one
data_layer.providers.fundamental_base.FundamentalSnapshot, catching each
NotImplementedError individually so today's honest "not implemented
yet" stub still returns a real (all-empty) FundamentalSnapshot rather
than raising -- the same fail-safe, "no data" -> None/empty posture
every other foundation module in this codebase uses. Once a real FRED
HTTP integration exists (a separate, explicitly-approvable future
step -- needs an API key via core/secrets.py, per this module's own
prior docstring), collect_snapshot() starts returning real values with
no change to its own code.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from data_layer.providers.base_provider import ProviderStatus
from data_layer.providers.fundamental_base import FundamentalDataPoint, FundamentalDataProvider, FundamentalSnapshot

# Verified real FRED series IDs (fred.stlouisfed.org) -- a future
# implementation's exact request targets, not invented labels.
SERIES_INTEREST_RATE = "FEDFUNDS"     # Effective Federal Funds Rate
SERIES_INFLATION = "CPIAUCSL"         # Consumer Price Index for All Urban Consumers
SERIES_DOLLAR_INDEX = "DTWEXBGS"      # Nominal Broad U.S. Dollar Index -- FRED's closest public proxy for "DXY", not identical to it (see module docstring)

SUPPORTED_SERIES = (SERIES_INTEREST_RATE, SERIES_INFLATION, SERIES_DOLLAR_INDEX)


class FredProvider(FundamentalDataProvider):
    """
    A deliberate, inert stub -- no `requests` call, no FRED API key.
    See docs/PROVIDER_CONTRACTS.md for what a real implementation
    would need to add (a FRED API key via core/secrets.py, the
    `fred/series/observations` endpoint, and a real
    FundamentalSnapshot builder combining all three series).
    """

    UNIMPLEMENTED_REASON = "FRED integration is not implemented yet (foundation only)"

    def get_provider_name(self) -> str:
        return "fred"

    def get_market_status(self) -> ProviderStatus:
        """Always available=False. Never raises -- same safe-status-check pattern as MT5Provider/BinanceProvider."""
        return ProviderStatus(available=False, reason=self.UNIMPLEMENTED_REASON)

    def _validate_series(self, series_id: str) -> None:
        """Raises ValueError for a series outside SUPPORTED_SERIES -- a genuine input error, checked before the "not implemented" signal (same pattern as BinanceProvider's _validate_symbol())."""
        if series_id not in SUPPORTED_SERIES:
            raise ValueError(
                f"Unsupported FRED series {series_id!r}. Supported: {', '.join(SUPPORTED_SERIES)}"
            )

    def get_macro_indicator(self, series_id: str) -> Optional[FundamentalDataPoint]:
        self._validate_series(series_id)
        raise NotImplementedError(self.UNIMPLEMENTED_REASON)

    def get_interest_rate(self) -> Optional[FundamentalDataPoint]:
        raise NotImplementedError(self.UNIMPLEMENTED_REASON)

    def get_inflation_data(self) -> Optional[FundamentalDataPoint]:
        raise NotImplementedError(self.UNIMPLEMENTED_REASON)

    def collect_snapshot(self) -> FundamentalSnapshot:
        """
        Phase 60.5, TASK 3 -- calls get_interest_rate()/
        get_inflation_data()/get_macro_indicator(SERIES_DOLLAR_INDEX)
        and bundles whichever succeed into one FundamentalSnapshot,
        keyed by logical name ("interest_rate"/"inflation"/
        "dollar_index"), matching FundamentalSnapshot's own documented
        convention. Never raises: today every call raises
        NotImplementedError (this provider is still a stub), each
        caught individually here, so the result is a real
        FundamentalSnapshot with an empty `indicators` dict, not an
        exception.
        """
        fetchers = {
            "interest_rate": self.get_interest_rate,
            "inflation": self.get_inflation_data,
            "dollar_index": lambda: self.get_macro_indicator(SERIES_DOLLAR_INDEX),
        }

        indicators = {}
        for name, fetch in fetchers.items():
            try:
                point = fetch()
            except NotImplementedError:
                continue
            if point is not None:
                indicators[name] = point

        return FundamentalSnapshot(
            snapshot_id=str(uuid.uuid4()),
            created_at=datetime.now(timezone.utc),
            indicators=indicators,
        )
