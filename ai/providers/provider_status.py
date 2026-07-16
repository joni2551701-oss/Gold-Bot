"""
AI Layer — Provider Health Status (Phase 61.1: AI Provider Reliability
Foundation, TASK 2).

`HealthStatus` is a distinct axis from `provider_manager.ProviderStatus`
(PREFERRED/FALLBACK/DISABLED) -- that enum is the owner's *intent* for
a provider; this one is *observed reality*. A provider can be
`ProviderStatus.PREFERRED` while its `HealthStatus` degrades under it.
No real API call anywhere in this phase -- foundation only.
"""

from enum import Enum


class HealthStatus(Enum):
    """
    ONLINE: fully healthy, the normal state.
    DEGRADED: responding, but with elevated latency/errors -- still
        usable, not preferred over an ONLINE alternative.
    RATE_LIMITED: temporarily throttled (e.g. HTTP 429) -- not
        currently usable, expected to recover on its own.
    OFFLINE: not responding / erroring -- not currently usable, no
        recovery timeline known.
    DISABLED: intentionally taken out of rotation (owner action, not
        an observed failure) -- mirrors `provider_manager.ProviderStatus.DISABLED`
        in name, kept as its own value here since a caller reading only
        `HealthStatus` should not need to cross-reference the other enum
        to know a provider is unusable.
    """
    ONLINE = "ONLINE"
    DEGRADED = "DEGRADED"
    RATE_LIMITED = "RATE_LIMITED"
    OFFLINE = "OFFLINE"
    DISABLED = "DISABLED"


# Statuses under which a provider may still be selected -- DEGRADED is
# usable (worse latency, not broken); everything else is not.
AVAILABLE_STATUSES = frozenset({HealthStatus.ONLINE, HealthStatus.DEGRADED})
