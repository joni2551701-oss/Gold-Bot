"""
AI Layer — Runtime Configuration Profiles (Phase 61.6: AI Operations &
Reliability Foundation, TASK 8).

Genuinely new (Module Reuse Principle steps 1/2 both "no" -- no
environment-shaped configuration bundle exists anywhere in `ai/`
today), but deliberately a thin, in-place addition to `ai/runtime/`
rather than a new package (Rule 3) -- one more file alongside
`runtime_manager.py`/`event_bus.py`, same as every other TASK this
phase.

A `RuntimeProfile` is pure data: a named bundle of the five knobs the
Director's brief calls out (retry/timeout/cache ttl/validation level/
provider priority). It reuses this codebase's own existing types for
each knob rather than inventing a parallel representation:

    cache_ttl_seconds     -> ai.cache.cache_policy.CachePolicy(default_ttl_seconds=...)
    validation_schema     -> ai.validation.schemas.ResponseSchema (already the
                              injectable "validation level" seam --
                              validate_response(result, schema=...))
    provider_priority     -> a Tuple[str, ...] consumed by
                              apply_provider_priority() below, which
                              reorders whatever
                              ai.router.routing_rules.get_candidate_providers()
                              already returns -- never a second,
                              competing source of candidate order.

`max_retries`/`timeout_seconds` have no existing injectable seam yet
(`ai/runtime/ai_service.py`'s own attempt count is derived from
`len(provider_manager.list_providers())`, and
`ai/providers/gemini_provider.py`'s `_REQUEST_TIMEOUT_SECONDS` is a
module-level constant) -- carried here as plain data for a future
phase to actually thread through, not fabricated as already-live
behavior. **This phase does not wire `RuntimeProfile` into
`ai_service.py`** -- exactly the same scoping decision already made
for `ai_layer.ai_engine.providers.circuit_breaker.ProviderCircuitBreaker` (built real
and tested, wiring deferred): `ai_service.py`'s own control flow stays
untouched, so no existing test's behavior can regress. A future,
separately-approved phase reads `profile.timeout_seconds`/
`profile.max_retries` at the point `AIService.ask()` currently hardcodes
its own attempt/timeout behavior.

Three named profiles (Development/Testing/Production), matching the
Director's own list -- no fourth invented:

    DEVELOPMENT_PROFILE -- generous timeout (debugging), short cache
        TTL (see fresh results while iterating), lenient validation
        (DEFAULT_SCHEMA), default provider order.
    TESTING_PROFILE     -- fast timeout (fail fast in CI), caching
        effectively off (0s TTL -- a cached response must never mask
        a test's own assertion), lenient validation, default provider
        order.
    PRODUCTION_PROFILE  -- matches this codebase's own existing
        production defaults exactly (15s, the real
        `_REQUEST_TIMEOUT_SECONDS`; 300s, the real
        `CachePolicy.default_ttl_seconds`), strict validation
        (requires a `confidence` metadata key), default provider
        order (`ai/router/routing_rules.py`'s own declared order is
        already the production-intended one -- this profile does not
        override it).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from ai_layer.ai_engine.cache.cache_policy import CachePolicy
from ai_layer.confidence_ai.schemas import DEFAULT_SCHEMA, ResponseSchema


@dataclass(frozen=True)
class RuntimeProfile:
    name: str
    max_retries: int
    timeout_seconds: int
    cache_ttl_seconds: int
    validation_schema: ResponseSchema
    provider_priority: Tuple[str, ...] = field(default_factory=tuple)

    def to_cache_policy(self) -> CachePolicy:
        """The blessed way to turn a profile's cache_ttl_seconds into something ai.cache.response_cache.ResponseCache(policy=...) already accepts -- no new cache type."""
        return CachePolicy(default_ttl_seconds=self.cache_ttl_seconds)


_STRICT_SCHEMA = ResponseSchema(min_content_length=1, required_metadata_keys=("confidence",), confidence_range=(0.0, 1.0))


DEVELOPMENT_PROFILE = RuntimeProfile(
    name="development", max_retries=1, timeout_seconds=30, cache_ttl_seconds=60,
    validation_schema=DEFAULT_SCHEMA,
)

TESTING_PROFILE = RuntimeProfile(
    name="testing", max_retries=1, timeout_seconds=5, cache_ttl_seconds=0,
    validation_schema=DEFAULT_SCHEMA,
)

PRODUCTION_PROFILE = RuntimeProfile(
    name="production", max_retries=3, timeout_seconds=15, cache_ttl_seconds=300,
    validation_schema=_STRICT_SCHEMA,
)

_PROFILES: Dict[str, RuntimeProfile] = {
    "development": DEVELOPMENT_PROFILE,
    "testing": TESTING_PROFILE,
    "production": PRODUCTION_PROFILE,
}


def resolve_profile(name: str) -> Optional[RuntimeProfile]:
    """Case-insensitive lookup by name. Never raises: an unknown name returns None rather than a fabricated default profile."""
    return _PROFILES.get(name.strip().lower())


def apply_provider_priority(candidates: List[str], priority: Tuple[str, ...]) -> List[str]:
    """
    Reorders an already-computed candidate list (e.g.
    `ai_layer.ai_coordinator.routing_rules.get_candidate_providers()`'s own output)
    so any name present in `priority` comes first, in `priority`'s own
    order; every other candidate keeps its original relative order
    afterward. Never invents a candidate `priority` names but
    `candidates` does not contain -- this is a reordering, never a
    second source of "which providers exist." An empty `priority`
    returns `candidates` unchanged.
    """
    if not priority:
        return list(candidates)

    candidate_set = set(candidates)
    prioritized = [name for name in priority if name in candidate_set]
    remaining = [name for name in candidates if name not in priority]
    return prioritized + remaining
