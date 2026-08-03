"""
Monitoring Layer — Provider Health (Phase 59.2, TASK 6).

Reports each registered data_layer/providers/ DataProvider's current health
by timing its own get_market_status() call -- the one method every
DataProvider guarantees never raises (see data_layer/providers/base_provider.py's
own docstring), so this module can call it on every registered
provider (including a stub like MT5Provider/BinanceProvider/FredProvider)
without a try/except.

Same "monitoring, never mutates behavior" posture as
monitoring/performance.py's pre-existing PerformanceTracker (reads
already-persisted signals, computes stats, changes nothing) and
performance/timer.py (Phase A19, measures duration, decides nothing).
This module does not gate, retry, or fail over between providers --
it only reports.

Not the same concept as performance/ (Phase A19, system-timing
infrastructure like pipeline stage duration) or
analytics/signal_performance.py (Phase 59 Preparation, trading
outcome performance) -- this is a third, distinct kind of
"performance": a data provider's own live availability/latency, not
the pipeline's or a trade's.
"""

import time
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional

from data_layer.providers.base_provider import DataProvider
from data_layer.providers.registry import ProviderRegistry

# The example in this task's own brief:
#   TwelveData: Latency 240ms, Status: ONLINE
#   MT5: Status: DISABLED
# "DISABLED" is not one of the three states this task's own brief
# defines (ONLINE/DEGRADED/OFFLINE) -- reconciled here as OFFLINE with
# a `reason` explaining why (e.g. "MT5 integration is not implemented
# yet"), rather than inventing a fourth status value. See
# ProviderHealthReport's own docstring.
DEFAULT_DEGRADED_THRESHOLD_MS = 500.0


class ProviderHealthStatus(Enum):
    ONLINE = "ONLINE"
    DEGRADED = "DEGRADED"
    OFFLINE = "OFFLINE"


@dataclass(frozen=True)
class ProviderHealthReport:
    """
    provider_name: the provider's own get_provider_name() -- never a
        caller-supplied label.
    status: ONLINE (available, fast), DEGRADED (available, slow), or
        OFFLINE (unavailable -- covers both "genuinely down" and "not
        implemented yet", both indistinguishable from the outside;
        `reason` carries the distinction, sourced from the provider's
        own ProviderStatus.reason, never guessed).
    latency_ms: how long get_market_status() itself took to return, in
        milliseconds. Always a real, measured number (time.perf_counter()),
        never estimated.
    reason: relayed directly from the provider's own
        ProviderStatus.reason -- empty string when status is ONLINE.
    checked_at (Phase 59.3, TASK 4: Provider Health Integration): when
        this health check itself ran -- the brief's own "Last Update:
        10:30:00" example. Always datetime.now(timezone.utc) at the
        moment check_provider_health() ran, never estimated or
        inherited from the provider.
    """
    provider_name: str
    status: ProviderHealthStatus
    latency_ms: float
    reason: str = ""
    checked_at: Optional[datetime] = None


def check_provider_health(
    provider: DataProvider,
    degraded_threshold_ms: float = DEFAULT_DEGRADED_THRESHOLD_MS,
) -> ProviderHealthReport:
    """
    Never raises: relies entirely on DataProvider.get_market_status()'s
    own "never raises" contract. A provider whose get_market_status()
    itself somehow raised would be a genuine programmer error in that
    provider (a contract violation), not something this function
    silently masks -- it is deliberately NOT wrapped in a try/except,
    so such a bug surfaces immediately in tests rather than being
    reported as a misleading "OFFLINE".
    """
    start = time.perf_counter()
    provider_status = provider.get_market_status()
    latency_ms = (time.perf_counter() - start) * 1000

    if not provider_status.available:
        status = ProviderHealthStatus.OFFLINE
    elif latency_ms > degraded_threshold_ms:
        status = ProviderHealthStatus.DEGRADED
    else:
        status = ProviderHealthStatus.ONLINE

    return ProviderHealthReport(
        provider_name=provider.get_provider_name(),
        status=status,
        latency_ms=latency_ms,
        reason=provider_status.reason,
        checked_at=datetime.now(timezone.utc),
    )


def check_registry_health(
    registry: ProviderRegistry,
    degraded_threshold_ms: float = DEFAULT_DEGRADED_THRESHOLD_MS,
) -> List[ProviderHealthReport]:
    """One report per registered provider, in registration order. Never raises -- see check_provider_health()'s own docstring."""
    return [
        check_provider_health(registry.get(name), degraded_threshold_ms)
        for name in registry.all_names()
    ]
