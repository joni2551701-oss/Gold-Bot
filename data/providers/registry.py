"""
Data Layer — Provider Registry (Phase 59.2, TASK 5).

ProviderRegistry is a catalog of every DataProvider instance GoldBot
knows about (candle-based or fundamental) -- "TwelveData, MT5,
TradingView, Binance, FRED bitta joydan boshqariladi" (all managed
from one place), per this task's own brief. Consumed by
monitoring/provider_health.py (TASK 6) to report status for every
registered provider, and named as the future backing store for the
Owner Mode /providers command (docs/OWNER_COMMANDS.md, TASK 7 --
contract only, not implemented).

Relationship to __init__.py's get_provider() (Phase 59.1): NOT a
replacement. get_provider(name=None) answers "give me THE one
configured MarketDataProvider" (reads config.Config.MARKET_DATA_PROVIDER,
a single active choice, raises for an unknown/disabled name).
ProviderRegistry answers a different question -- "give me the full
catalog of every provider GoldBot has, with each one's own
availability" -- needed by TASK 6's health monitoring (which must
report on every provider, not just the one active choice) and a
future /providers listing command. build_default_registry() below
constructs its own provider instances directly (TwelveDataProvider(),
MT5Provider(), etc.) rather than depending on get_provider(), since
the registry must include Binance/FRED too -- providers get_provider()'s
Config-driven single-choice model was never designed to select among.
Neither function calls the other.

TradingView is deliberately NOT registered here -- Phase 59.2 TASK 2's
own audit (docs/TRADINGVIEW_PROVIDER.md) concluded no
`MarketDataProvider`-shaped TradingView implementation should be
built at all (a real commercial/ToS risk, not a coding gap) -- there
is no class to register.
"""

from typing import Dict, List, Optional

from data.providers.base_provider import DataProvider
from data.providers.binance_provider import BinanceProvider
from data.providers.bitget_provider import BitgetProvider
from data.providers.fred_provider import FredProvider
from data.providers.keynorq_provider import KeynorqProvider
from data.providers.mt5_provider import MT5Provider
from data.providers.twelve_data_provider import TwelveDataProvider


class ProviderRegistry:
    """
    A plain catalog -- register()/get()/available() only, no
    Config-reading, no default-selection logic (that's get_provider()'s
    job, see module docstring). Never raises on construction; an empty
    registry is a valid, if useless, state.
    """

    def __init__(self):
        self._providers: Dict[str, DataProvider] = {}

    def register(self, provider: DataProvider) -> None:
        """
        Keys by provider.get_provider_name() -- never a caller-supplied
        string, so the registry key and the provider's own
        self-reported name can never drift apart. Registering a second
        provider under the same name replaces the first (last write
        wins) -- deliberate, not guarded: swapping a provider instance
        (e.g. a test double) is a legitimate, common use of this
        method, not an error condition.
        """
        self._providers[provider.get_provider_name()] = provider

    def get(self, name: str) -> Optional[DataProvider]:
        """Returns None for an unregistered name -- never raises, matching this codebase's established "structured absence, not exception" convention for a lookup miss."""
        return self._providers.get(name.strip().lower())

    def available(self) -> List[str]:
        """
        Names of every registered provider whose own get_market_status()
        currently reports available=True. Calls get_market_status() on
        each -- safe by contract (DataProvider.get_market_status() must
        never raise, see base_provider.py), so this method itself never
        raises either.
        """
        return [
            name for name, provider in self._providers.items()
            if provider.get_market_status().available
        ]

    def all_names(self) -> List[str]:
        """Every registered provider's name, regardless of availability -- for a full listing (e.g. a future /providers command)."""
        return list(self._providers.keys())


def build_default_registry() -> ProviderRegistry:
    """
    Registers every provider this codebase has built so far --
    TwelveData (real, live), MT5/Binance/Bitget/Keynorq/FRED (honest,
    inert stubs).
    Each provider's own __init__ never raises (TwelveDataProvider's
    lazily-constructed TwelveDataClient() degrades to api_key=None
    rather than raising, see data/twelve_data_client.py; the three
    stubs take no arguments at all), so this factory itself never
    raises.
    """
    registry = ProviderRegistry()
    registry.register(TwelveDataProvider())
    registry.register(MT5Provider())
    registry.register(BinanceProvider())
    registry.register(BitgetProvider())
    registry.register(KeynorqProvider())
    registry.register(FredProvider())
    return registry
