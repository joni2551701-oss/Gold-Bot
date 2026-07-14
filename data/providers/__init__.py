"""
Data Layer — Market Provider package (Phase 59.1). See
docs/MARKET_PROVIDER.md for the full architecture. get_provider() is
the one factory function a future caller would use to obtain a
MarketDataProvider without hardcoding which one -- not called from
core/pipeline.py or anywhere else in this phase (zero pipeline wiring,
same posture as every other Phase A/AC/Phase-59-prep foundation
module).
"""

from typing import Optional

from config import Config
from data.providers.base_provider import MarketCandle, MarketDataProvider, ProviderStatus
from data.providers.mt5_provider import MT5Provider
from data.providers.twelve_data_provider import TwelveDataProvider

__all__ = [
    "MarketCandle",
    "MarketDataProvider",
    "ProviderStatus",
    "TwelveDataProvider",
    "MT5Provider",
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
