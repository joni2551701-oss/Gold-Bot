"""
Data Layer — Provider Manager (TASK-CORE-003).

ProviderManager is the single seam a higher layer (stream/ next) talks
to instead of naming a concrete provider. It answers "which provider
should serve this request right now?" using three inputs, all already
built elsewhere in this package:

    ProviderRegistry (registry.py)  -- the catalog of every provider
    each provider's get_market_status()  -- live availability (safe, never raises)
    config.get_settings().providers      -- the configured primary + enable flags

Relationship to the two existing selectors (neither is replaced):
- __init__.py's get_provider(name) returns THE one configured provider
  by exact name, raising for unknown/disabled -- a strict, single-shot
  factory.
- ProviderRegistry answers "give me the full catalog / which are
  available".
- ProviderManager (this module) adds the missing piece: an ORDERED
  primary→fallback chain and symbol-based routing, choosing among the
  registry's providers by live availability. It reuses both of the
  above rather than re-reading config or re-instantiating providers.

DATA-ONLY (CLAUDE.md Architecture Rules / task "providers/ qilmasligi
kerak"): selection only. This module never computes a signal, never
knows a strategy/decision/risk rule, never writes a database, never
sends Telegram, never renders a chart. It returns a provider (or None)
and never raises for a data-driven "nothing available" condition --
None is that answer, matching this package's established fail-safe
posture. Secrets are never read or logged here (it only reads enable
flags and the provider name from config, never a key).
"""

from typing import Dict, List, Optional

import config
from data.providers.base_provider import MarketDataProvider
from data.providers.registry import ProviderRegistry, build_default_registry

# Stable fallback priority among market-data providers. TwelveData is
# the live provider today; the rest are inert stubs (so they report
# available=False and are skipped by get_active_provider()), listed in
# the order a future phase would most likely prefer them. The primary
# provider from config is always tried first, ahead of this order.
_PRIORITY = ("twelvedata", "mt5", "binance", "bitget", "keynorq")

# Coarse crypto detection for symbol-based routing. Bitget/Binance use
# the quote-suffixed, no-separator format ("BTCUSDT"); a real
# per-provider symbol-mapping step is a future concern, so this stays a
# deliberately simple, documented heuristic, not a lookup table.
_CRYPTO_PROVIDERS = ("bitget", "binance")


class ProviderManager:
    """
    Never raises on construction. `registry` defaults to
    build_default_registry() (TwelveData + MT5 + Binance + Bitget +
    Keynorq + FRED); `settings` defaults to the central config
    singleton. Both are injectable for tests.
    """

    def __init__(self, registry: Optional[ProviderRegistry] = None, settings=None) -> None:
        self._registry = registry or build_default_registry()
        self._settings = settings or config.get_settings()

    # -- internals ----------------------------------------------------
    def _market_providers(self) -> Dict[str, MarketDataProvider]:
        """Registered providers that are candle-shaped (MarketDataProvider) -- excludes FRED-family fundamental providers, which have no get_candles()."""
        result: Dict[str, MarketDataProvider] = {}
        for name in self._registry.all_names():
            provider = self._registry.get(name)
            if isinstance(provider, MarketDataProvider):
                result[name] = provider
        return result

    def _enabled(self, name: str) -> bool:
        """Config enable flag for a provider name -- unknown names default True (a provider present in the registry but without a flag is not silently hidden)."""
        providers = self._settings.providers
        return {
            "twelvedata": providers.enable_twelvedata,
            "mt5": providers.enable_mt5,
            "binance": providers.enable_binance,
            "bitget": providers.enable_bitget,
            "keynorq": providers.enable_keynorq,
        }.get(name, True)

    # -- public API ---------------------------------------------------
    @property
    def primary_name(self) -> str:
        """The configured primary market-data provider name (config.SETTINGS.providers.market_data_provider), lowercased."""
        return (self._settings.providers.market_data_provider or "").strip().lower()

    def provider_chain(self) -> List[str]:
        """
        The ordered primary→fallback name chain: the configured primary
        first (if it is a registered market provider), then every other
        enabled, registered market provider in _PRIORITY order. Purely
        a name list -- no availability check here (that's
        get_active_provider()'s job). Never raises.
        """
        market = self._market_providers()
        chain: List[str] = []
        if self.primary_name in market:
            chain.append(self.primary_name)
        for name in _PRIORITY:
            if name in market and name not in chain and self._enabled(name):
                chain.append(name)
        return chain

    def get_primary(self) -> Optional[MarketDataProvider]:
        """The configured primary provider instance, or None if it isn't a registered market provider."""
        return self._market_providers().get(self.primary_name)

    def is_available(self, name: str) -> bool:
        """Whether the named provider is registered and its get_market_status() reports available. Never raises."""
        provider = self._registry.get(name)
        return bool(provider and provider.get_market_status().available)

    def available_providers(self) -> List[str]:
        """Names of all registered providers currently reporting available -- delegates to ProviderRegistry.available()."""
        return self._registry.available()

    def get_active_provider(self) -> Optional[MarketDataProvider]:
        """
        The first provider in provider_chain() that currently reports
        available, or None if none are (e.g. only stubs registered and
        no API key). Never raises -- None is the honest "no live
        provider right now" answer, not an exception.
        """
        market = self._market_providers()
        for name in self.provider_chain():
            provider = market.get(name)
            if provider is not None and provider.get_market_status().available:
                return provider
        return None

    def resolve(self, symbol: Optional[str] = None) -> Optional[MarketDataProvider]:
        """
        Choose a provider for `symbol`. A crypto-looking symbol (quote
        suffix "USDT") prefers an available crypto provider
        (bitget/binance) before falling back to the normal chain;
        everything else uses the normal primary→fallback chain. Returns
        None if nothing suitable is available. Never raises, never
        fabricates -- symbol routing is a coarse, documented heuristic,
        not a real per-provider symbol map (that is a future step).
        """
        market = self._market_providers()
        if symbol and symbol.strip().upper().endswith("USDT"):
            for name in _CRYPTO_PROVIDERS:
                provider = market.get(name)
                if (
                    provider is not None
                    and self._enabled(name)
                    and provider.get_market_status().available
                ):
                    return provider
        return self.get_active_provider()
