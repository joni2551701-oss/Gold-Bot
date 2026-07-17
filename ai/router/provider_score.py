"""
AI Layer — Provider Score (Phase 61.5: AI Production Integration
Foundation, TASK 2: Router Intelligence).

**Recommendation/analytics/owner-view only.** `ai/router/router.py`'s
own docstring already documents the exact invariant this task must
preserve: `provider_metrics()` "never calls or is influenced by
`route()`". This module adds a second, separate read-only view over
the same already-existing data (`ai.audit.provider_stats.ProviderStats`
+ `ai.providers.provider_health.ProviderHealthTracker`) -- `route()`
itself is not imported here, not modified, and does not import this
module. No auto-switching, no adaptive routing: that stays out of
scope for this phase, per the Director's own explicit brief.

Composes three already-computed signals into one 0.0-1.0 score, same
"reuse the already-computed record, don't re-derive it" convention
`ai/audit/provider_stats.py`'s own `rank_providers()` (Phase 61.3
TASK 9) established:

- **Health** (`ai.providers.provider_health.ProviderHealthTracker`) --
  observed reality, weighted highest: an OFFLINE/RATE_LIMITED provider
  should never outscore a healthy one regardless of its historical
  cost/latency numbers.
- **Quality** (`ProviderStats.success_rate`) -- how often a call to
  this provider actually succeeds.
- **Cost/latency** (`ProviderStats.avg_latency_ms` /
  `ProviderStats.total_cost`) -- cheaper and faster scores higher,
  each normalized independently so neither dominates the other.

A provider with no call history yet (no `ProviderStats` entry) scores
a neutral 0.5 on quality/cost/latency rather than 0.0 -- "no data" is
not the same as "bad data," and a brand-new provider should not be
permanently penalized just for lacking history.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from ai.audit.provider_stats import ProviderStats
from ai.providers.provider_health import ProviderHealthTracker
from ai.providers.provider_status import HealthStatus

_HEALTH_WEIGHT = 0.4
_QUALITY_WEIGHT = 0.3
_LATENCY_WEIGHT = 0.15
_COST_WEIGHT = 0.15

_NEUTRAL_SCORE = 0.5

_HEALTH_STATUS_SCORE: Dict[HealthStatus, float] = {
    HealthStatus.ONLINE: 1.0,
    HealthStatus.DEGRADED: 0.6,
    HealthStatus.RATE_LIMITED: 0.2,
    HealthStatus.OFFLINE: 0.0,
    HealthStatus.DISABLED: 0.0,
}


@dataclass(frozen=True)
class ProviderScore:
    provider_name: str
    score: float
    health_status: Optional[HealthStatus]
    success_rate: Optional[float]
    avg_latency_ms: Optional[float]
    total_cost: Optional[float]


def _health_component(health_status: Optional[HealthStatus]) -> float:
    """No recorded health -- neutral, same "no data is not bad data" posture as the other three components."""
    if health_status is None:
        return _NEUTRAL_SCORE
    return _HEALTH_STATUS_SCORE.get(health_status, _NEUTRAL_SCORE)


def _latency_component(avg_latency_ms: Optional[float]) -> float:
    """Lower latency scores higher; asymptotically approaches 0 as latency grows, never negative."""
    if avg_latency_ms is None:
        return _NEUTRAL_SCORE
    return 1.0 / (1.0 + (avg_latency_ms / 1000.0))


def _cost_component(total_cost: Optional[float]) -> float:
    """Lower cost scores higher; asymptotically approaches 0 as cost grows, never negative."""
    if total_cost is None:
        return _NEUTRAL_SCORE
    return 1.0 / (1.0 + total_cost)


def score_provider(
    provider_name: str, stats: Optional[ProviderStats], health_status: Optional[HealthStatus],
) -> ProviderScore:
    """Never raises: missing `stats`/`health_status` degrade to neutral component scores rather than erroring."""
    success_rate = stats.success_rate if stats is not None else None
    avg_latency_ms = stats.avg_latency_ms if stats is not None else None
    total_cost = stats.total_cost if stats is not None else None

    quality = success_rate if success_rate is not None else _NEUTRAL_SCORE
    score = (
        _HEALTH_WEIGHT * _health_component(health_status)
        + _QUALITY_WEIGHT * quality
        + _LATENCY_WEIGHT * _latency_component(avg_latency_ms)
        + _COST_WEIGHT * _cost_component(total_cost)
    )

    return ProviderScore(
        provider_name=provider_name, score=score, health_status=health_status,
        success_rate=success_rate, avg_latency_ms=avg_latency_ms, total_cost=total_cost,
    )


def score_providers(
    provider_names: List[str], stats: Dict[str, ProviderStats], health_tracker: Optional[ProviderHealthTracker] = None,
) -> List[ProviderScore]:
    """
    Best-first (score descending) over an explicit `provider_names` list
    -- deliberately not derived from `stats.keys()` alone, so a provider
    with zero call history (and therefore no `ProviderStats` entry)
    still gets scored (at neutral quality/cost/latency) rather than
    being silently omitted from an owner-facing comparison. Never
    raises: an empty `provider_names` list returns an empty list.
    """
    scores = [
        score_provider(
            name, stats.get(name),
            health_tracker.status_of(name) if health_tracker is not None else None,
        )
        for name in provider_names
    ]
    return sorted(scores, key=lambda s: -s.score)
