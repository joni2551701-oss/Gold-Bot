"""
AI Layer — Provider Stats (Phase 61.0: AI Infrastructure Foundation,
TASK 9; wired to real runtime data Phase 61.2: AI Runtime Foundation,
TASK 9; ranking added Phase 61.3: AI Intelligence Layer, TASK 9).

Pure aggregation over an already-recorded `response_log.py` history --
never fetches or computes latency/cost itself, matching every other
`ai/` foundation module's "reuse the already-computed record, don't
re-derive it" convention.

Phase 61.2 TASK 9: no new metrics module was created -- this file is
extended in place, per the brief's own instruction ("Yangi emas.
Mavjud... kengaytiriladi"). `ai/runtime/ai_service.py` is now this
module's real data source (`ResponseLog.record()` on every provider
call attempt, success or failure) -- `compute_provider_stats()`'s
logic itself is unchanged. **Observability only**: neither
`ai/runtime/ai_service.py` nor `ai/router/router.py` reads
`ProviderStats` to influence provider selection -- `AIRouter.route()`
has no import of this module at all, and `AIService.ask()`'s only use
of `ai/audit/` is to *write* `RequestLog`/`ResponseLog` entries, never
to read `ProviderStats` back.

Phase 61.3 TASK 9: `rank_providers()` is a ranking function over this
same, unmodified `ProviderStats` shape -- again extended in place, no
new metrics module and no new field. Still observability only: nothing
in `ai/router/` or `ai/runtime/` calls this function; it exists for a
future owner-facing report/command to read.

Phase 61.6 TASK 4: "Yangi emas. Mavjud provider_stats.py kengayadi."
(Not new. The existing provider_stats.py is extended.) Two additions,
both still in this same file:

- `compute_requests_per_minute()` -- a pure function over
  `ai.audit.request_log.AIRequestLogEntry.created_at`, the same
  "reuse the already-recorded timestamp, don't add a new counter"
  convention this file's own `compute_provider_stats()` already uses
  for `response_log.py`.
- `RuntimeMetrics`/`RuntimeMetricsCollector` -- cache hit/miss,
  validation-failure, retry, and failover counts, none of which are
  recorded anywhere in `request_log.py`/`response_log.py` today (a
  cache hit in `ai/runtime/ai_service.py` returns before either log is
  ever touched). `RuntimeMetricsCollector` subscribes to
  `ai.event_bus.EventBus` (Phase 61.6 TASK 5) and accumulates
  counts from the events `ai_service.py` now publishes at points that
  already existed in its control flow -- no new orchestration logic,
  only new event-publication calls at the cache-hit/cache-miss/
  validation-rejection/provider-failure/provider-switch points that
  were already there. In-memory only, same posture as every counter in
  this package; a caller (e.g. an Owner `/runtime_metrics` command)
  constructs a collector, attaches it to the same `EventBus` a live
  `AIService` was given, and reads its counts.
"""

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

from ai.audit.request_log import AIRequestLogEntry
from ai.audit.response_log import AIResponseLogEntry
from ai.event_bus import EventBus, EventType, RuntimeEvent


@dataclass(frozen=True)
class ProviderStats:
    provider_name: str
    total_calls: int
    success_count: int
    avg_latency_ms: float
    total_tokens: int
    total_cost: float

    @property
    def success_rate(self) -> float:
        return self.success_count / self.total_calls if self.total_calls else 0.0

    @property
    def failure_count(self) -> int:
        """Derived, not separately tracked -- every non-SUCCESS status (FAILED/REJECTED/NOT_IMPLEMENTED, from ai/runtime/ai_service.py's own recorded statuses) counts as a failure here."""
        return self.total_calls - self.success_count


def compute_provider_stats(entries: List[AIResponseLogEntry]) -> Dict[str, ProviderStats]:
    """Never raises: an empty `entries` list returns an empty dict. Entries with `provider_name=None` (no provider was ever selected) are excluded -- there is no provider to attribute them to."""
    grouped: Dict[str, List[AIResponseLogEntry]] = defaultdict(list)
    for entry in entries:
        if entry.provider_name is not None:
            grouped[entry.provider_name].append(entry)

    stats: Dict[str, ProviderStats] = {}
    for provider_name, group in grouped.items():
        total_calls = len(group)
        success_count = sum(1 for e in group if e.status == "SUCCESS")
        avg_latency = sum(e.latency_ms for e in group) / total_calls
        total_tokens = sum(e.tokens for e in group)
        total_cost = sum(e.cost for e in group)
        stats[provider_name] = ProviderStats(
            provider_name=provider_name, total_calls=total_calls, success_count=success_count,
            avg_latency_ms=avg_latency, total_tokens=total_tokens, total_cost=total_cost,
        )
    return stats


def rank_providers(stats: Dict[str, ProviderStats]) -> List[ProviderStats]:
    """
    Best-first ranking over `compute_provider_stats()`'s own output --
    no new metric, no re-fetch. Primary key: `success_rate` descending
    (a provider that answers reliably ranks above one that doesn't,
    regardless of speed). Tiebreaker 1: `avg_latency_ms` ascending
    (faster wins among equally reliable providers). Tiebreaker 2:
    `total_cost` ascending (cheaper wins among equally reliable,
    equally fast providers). Never raises: an empty `stats` dict
    returns an empty list.
    """
    return sorted(stats.values(), key=lambda s: (-s.success_rate, s.avg_latency_ms, s.total_cost))


def compute_requests_per_minute(requests: List[AIRequestLogEntry], now: Optional[datetime] = None) -> float:
    """Count of requests whose created_at falls within the last 60 seconds of `now` (defaults to the real current time). Never raises: an empty `requests` list returns 0.0."""
    now = now if now is not None else datetime.now(timezone.utc)
    window_start = now - timedelta(seconds=60)
    return float(sum(1 for entry in requests if window_start <= entry.created_at <= now))


@dataclass(frozen=True)
class DailyUsage:
    """Platform-wide (every provider, every user) cost/token total over the trailing 24h -- the Phase 62.2 TASK 8 AI Cost Protection input. Distinct from ai.access.usage_limits.UsageLimiter (a per-(telegram_id, capability) daily call quota, a different concern: one user's abuse vs. the whole platform's spend)."""
    total_cost: float
    total_tokens: int


def compute_daily_usage(responses: List[AIResponseLogEntry], now: Optional[datetime] = None) -> DailyUsage:
    """
    Sums cost/tokens across every provider for entries within the last
    24h of `now` (defaults to the real current time) -- same trailing-
    window convention `compute_requests_per_minute()` already uses,
    scaled from 60 seconds to 24 hours. Never raises: an empty
    `responses` list returns a zeroed DailyUsage.
    """
    now = now if now is not None else datetime.now(timezone.utc)
    window_start = now - timedelta(hours=24)
    windowed = [e for e in responses if window_start <= e.created_at <= now]
    return DailyUsage(total_cost=sum(e.cost for e in windowed), total_tokens=sum(e.tokens for e in windowed))


def evaluate_cost_protection(
    usage: DailyUsage, cost_limit: Optional[float], token_limit: Optional[int],
) -> Optional[str]:
    """
    Returns a human-readable breach reason if `usage` exceeds either
    configured limit, else None. `cost_limit`/`token_limit` of `None`
    means "no limit configured" for that dimension -- never
    fabricates a default ceiling nobody configured. Cost is checked
    before tokens; a caller only needs the first breach reason to act.
    """
    if cost_limit is not None and usage.total_cost > cost_limit:
        return f"daily cost ${usage.total_cost:.2f} exceeds ${cost_limit:.2f} limit"
    if token_limit is not None and usage.total_tokens > token_limit:
        return f"daily tokens {usage.total_tokens} exceeds {token_limit} limit"
    return None


@dataclass(frozen=True)
class RuntimeMetrics:
    requests_per_minute: float
    cache_hits: int
    cache_misses: int
    validation_failures: int
    retries: int
    failover_count: int

    @property
    def cache_hit_rate(self) -> float:
        total = self.cache_hits + self.cache_misses
        return self.cache_hits / total if total else 0.0


class RuntimeMetricsCollector:
    """
    Subscribes to an `EventBus` and accumulates in-memory counts --
    never reaches into `ai/runtime/ai_service.py` or any provider
    directly, only reacts to events already published onto the bus
    (Rule 5's "Event Bus... nobody calls anybody directly" preserved).
    `CACHE_HIT`/`CACHE_MISS`/`VALIDATION_FAILED` map one-to-one;
    `PROVIDER_FAILED` counts as a retry (each failed attempt is exactly
    the reason `AIService.ask()` tries the next candidate);
    `PROVIDER_CHANGED` counts as a failover (the router actually
    switched to a different provider than the previous attempt within
    one request).
    """

    def __init__(self, event_bus: EventBus) -> None:
        self._cache_hits = 0
        self._cache_misses = 0
        self._validation_failures = 0
        self._retries = 0
        self._failover_count = 0
        event_bus.subscribe(EventType.CACHE_HIT, self._on_cache_hit)
        event_bus.subscribe(EventType.CACHE_MISS, self._on_cache_miss)
        event_bus.subscribe(EventType.VALIDATION_FAILED, self._on_validation_failed)
        event_bus.subscribe(EventType.PROVIDER_FAILED, self._on_provider_failed)
        event_bus.subscribe(EventType.PROVIDER_CHANGED, self._on_provider_changed)

    def _on_cache_hit(self, event: RuntimeEvent) -> None:
        self._cache_hits += 1

    def _on_cache_miss(self, event: RuntimeEvent) -> None:
        self._cache_misses += 1

    def _on_validation_failed(self, event: RuntimeEvent) -> None:
        self._validation_failures += 1

    def _on_provider_failed(self, event: RuntimeEvent) -> None:
        self._retries += 1

    def _on_provider_changed(self, event: RuntimeEvent) -> None:
        self._failover_count += 1

    def snapshot(self, requests: Optional[List[AIRequestLogEntry]] = None, now: Optional[datetime] = None) -> RuntimeMetrics:
        """requests_per_minute is computed fresh from an optional RequestLog snapshot -- omitted (None/empty) reports 0.0 rather than a stale cached rate."""
        rpm = compute_requests_per_minute(requests, now) if requests else 0.0
        return RuntimeMetrics(
            requests_per_minute=rpm, cache_hits=self._cache_hits, cache_misses=self._cache_misses,
            validation_failures=self._validation_failures, retries=self._retries,
            failover_count=self._failover_count,
        )
