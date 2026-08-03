"""
Data Layer — Market Provider package (Phase 59.1; extended Phase
59.2). See docs/MARKET_PROVIDER.md and docs/MARKET_DATA_ARCHITECTURE.md
for the full architecture. get_provider() is the one factory function
a future caller would use to obtain THE configured MarketDataProvider
without hardcoding which one; ProviderRegistry (registry.py, Phase
59.2) is the separate, broader catalog of every provider GoldBot has
-- see registry.py's own docstring for how the two relate. Neither is
called from core/pipeline.py or anywhere else in this phase (zero
pipeline wiring, same posture as every other Phase A/AC/Phase-59
foundation module).
"""

from typing import Optional

from config import Config
from data_layer.providers.base_provider import DataProvider, MarketCandle, MarketDataProvider, ProviderStatus
from data_layer.providers.binance_provider import BinanceProvider
from data_layer.providers.bitget_provider import BitgetProvider
from data_layer.providers.fred_provider import FredProvider
from data_layer.providers.fundamental_base import FundamentalDataPoint, FundamentalDataProvider, FundamentalSnapshot
from data_layer.providers.keynorq_provider import KeynorqProvider
from data_layer.providers.mt5_provider import MT5Provider
from data_layer.providers.provider_errors import (
    ProviderAuthError,
    ProviderError,
    ProviderRateLimitError,
    ProviderResponseError,
    ProviderTimeoutError,
    ProviderUnavailableError,
    provider_error_for_status,
)
from data_layer.providers.provider_manager import ProviderManager
from data_layer.providers.registry import ProviderRegistry, build_default_registry
from data_layer.providers.twelve_data_provider import TwelveDataProvider

__all__ = [
    "DataProvider",
    "MarketCandle",
    "MarketDataProvider",
    "ProviderStatus",
    "TwelveDataProvider",
    "MT5Provider",
    "BinanceProvider",
    "BitgetProvider",
    "KeynorqProvider",
    "FredProvider",
    "FundamentalDataPoint",
    "FundamentalDataProvider",
    "FundamentalSnapshot",
    "ProviderRegistry",
    "build_default_registry",
    "ProviderManager",
    "ProviderError",
    "ProviderAuthError",
    "ProviderTimeoutError",
    "ProviderRateLimitError",
    "ProviderResponseError",
    "ProviderUnavailableError",
    "provider_error_for_status",
    "get_provider",
]

_PROVIDERS = {
    "twelvedata": TwelveDataProvider,
    "mt5": MT5Provider,
}


def get_provider(name: Optional[str] = None) -> MarketDataProvider:
    """
    Constructs a MarketDataProvider by name -- config.Config.MARKET_DATA_PROVIDER
    when `name` is omitted, the same "read the real, existing Config"
    pattern configuration/settings.py's build_settings_from_config()
    already established. Raises ValueError (a genuine configuration
    error, not a data-driven condition) for an unknown provider name,
    or for "mt5" when config.Config.ENABLE_MT5 is False -- never
    silently falls back to a different provider than the one
    requested. "twelvedata" additionally requires
    config.Config.ENABLE_TWELVEDATA (default True); disabling it
    while it is also the selected MARKET_DATA_PROVIDER is treated the
    same way.
    """
    provider_name = (name or Config.MARKET_DATA_PROVIDER).strip().lower()

    if provider_name not in _PROVIDERS:
        raise ValueError(
            f"Unknown MARKET_DATA_PROVIDER {provider_name!r}. "
            f"Supported: {', '.join(sorted(_PROVIDERS))}"
        )

    if provider_name == "mt5" and not Config.ENABLE_MT5:
        raise ValueError(
            "MARKET_DATA_PROVIDER=mt5 requires ENABLE_MT5=True "
            "(MT5 integration is not implemented yet -- see docs/MARKET_PROVIDER.md)"
        )
    if provider_name == "twelvedata" and not Config.ENABLE_TWELVEDATA:
        raise ValueError("MARKET_DATA_PROVIDER=twelvedata requires ENABLE_TWELVEDATA=True")

    return _PROVIDERS[provider_name]()

# Canonical documentation: 01_Data_Layer/Providers/README.md
