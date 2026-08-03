"""
Monitoring Layer — Market Data Monitor (GoldBot Core Owner Monitoring
Alpha, TASK 3).

Reuses `core_layer.health_monitor.provider_health.check_provider_health()` for
latency/data-source-status -- no new provider health logic (per
`docs/PHASE_CORE_MONITORING_AUDIT.md`). `data_layer/providers/`'s own
`ProviderStatus` has no price or "last candle received" concept, so
`last_price`/`last_update` are optional, caller-supplied values only
-- this module never fabricates them (see the audit's own
"data_layer/providers/" section).

Data source logic itself is never changed (this brief's own header):
this module only reads `provider.get_market_status()` via
`check_provider_health()`, exactly as `core_layer/health_monitor/provider_health.py`
already does elsewhere.
"""

from typing import Optional

from core_layer.logger.logger import setup_logger
from data_layer.providers.registry import ProviderRegistry, build_default_registry
from core_layer.health_monitor.models import MarketHealth
from core_layer.health_monitor.provider_health import check_provider_health

logger = setup_logger("MarketMonitor")


def get_market_health(
    symbol: str,
    provider_name: str,
    last_price: Optional[float] = None,
    last_update: Optional[str] = None,
    registry: Optional[ProviderRegistry] = None,
) -> MarketHealth:
    """
    Never raises: an unknown provider name or a provider health-check
    failure both fall back to `data_source_status="UNKNOWN"` rather
    than propagating an exception -- a monitoring read must never
    itself crash a command.
    """
    reg = registry or build_default_registry()
    provider = reg.get(provider_name)
    if provider is None:
        return MarketHealth(
            symbol=symbol,
            data_source_status="UNKNOWN",
            last_price=last_price,
            last_update=last_update,
        )

    try:
        report = check_provider_health(provider)
    except Exception as e:
        logger.warning(f"get_market_health: check_provider_health failed for {provider_name}: {e}")
        return MarketHealth(
            symbol=symbol,
            data_source_status="UNKNOWN",
            last_price=last_price,
            last_update=last_update,
        )

    return MarketHealth(
        symbol=symbol,
        data_source_status=report.status.value,
        last_price=last_price,
        last_update=last_update,
        latency_ms=report.latency_ms,
    )
