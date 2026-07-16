"""
AI Layer — AI Response Cache Policy (Phase 61.1: AI Provider
Reliability Foundation, TASK 9; extended Phase 61.1.1: AI Foundation
Corrections, TASK 2; extended Phase 61.2: AI Runtime Foundation,
TASK 7).

Defines the cache key shape and TTL policy for `response_cache.py`.
The key is structurally forbidden from being bare prompt text --
`CacheKey` is now a seven-field dataclass (Capability + Context
Version + Provider + Prompt Version + Context Hash + Snapshot ID +
User Role), the same "enforce the rule in the type, not just the
docstring" posture `ai/context/context_adapter.py`'s
`sanitize_market_context()` already uses for the raw-market-data
boundary. A market-context-dependent answer (e.g. "Gold trend?") must
never be served from a cache entry built against a stale context.

Phase 61.2 TASK 7 adds `user_role` -- a lower-privileged role's cache
lookup must never return an entry a higher-privileged role's call
produced (or vice versa), even for an identical snapshot/capability/
provider. This is a privilege-boundary concern layered on top of the
freshness concern `snapshot_id` already solves -- the two are
independent axes, both required.

Freshness chain (Phase 61.1.1 TASK 2, documented per the Director's
own required order): **Snapshot identity -> Cache freshness -> TTL**.
`snapshot_id` (produced exclusively by
`ai.context.context_builder.build_ai_context()`, never by a caller)
establishes *which* underlying context this cache entry answers for --
identical content always produces the identical `snapshot_id`,
different content always produces a different one, so a cache hit is
only ever possible for a genuinely-matching snapshot. `CachePolicy`'s
`default_ttl_seconds` is the second, independent layer on top: even a
snapshot whose content hasn't changed (e.g. a quiet market between
provider polls) stops being served from cache once the TTL elapses,
so a cache entry can never be treated as permanently fresh just
because nothing observable changed.
"""

import hashlib
import json
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

from ai.capabilities.capability import Capability

if TYPE_CHECKING:
    from ai.context.context_snapshot import AIContext


@dataclass(frozen=True)
class CacheKey:
    """Every field is required -- there is no constructor path that produces a key from prompt text alone. `snapshot_id` is the canonical freshness identity (Phase 61.1.1); `context_hash` remains a general-purpose content fingerprint a caller may still compute over whatever payload it chooses (e.g. to additionally distinguish two calls with the same snapshot but different request-specific parameters)."""
    capability: Capability
    context_version: str
    provider_name: str
    prompt_version: str
    context_hash: str
    snapshot_id: str
    user_role: str

    def as_string(self) -> str:
        """Deterministic, human-inspectable serialization -- used as the actual dict key inside ResponseCache."""
        return "|".join([
            self.capability.value, self.context_version, self.provider_name,
            self.prompt_version, self.context_hash, self.snapshot_id, self.user_role,
        ])


def compute_context_hash(context_payload: dict) -> str:
    """
    Deterministic SHA-256 hash of a JSON-serializable payload (e.g.
    `AIContext.to_dict()`) -- `sort_keys=True` so field ordering never
    changes the hash. A caller building a `CacheKey` is expected to
    pass this function's output as `context_hash`, not roll its own
    hashing.
    """
    serialized = json.dumps(context_payload, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def build_cache_key_from_context(
    ai_context: "AIContext", capability: Capability, provider_name: str, prompt_version: str,
    user_role: str, context_hash: Optional[str] = None,
) -> CacheKey:
    """
    The blessed way to construct a `CacheKey` (Phase 61.1.1 TASK 2) --
    pulls `snapshot_id` directly from an already-built `AIContext`
    rather than letting a caller invent one. Raises `ValueError` if
    `ai_context.snapshot_id` is `None`: that only happens for an
    `AIContext` never passed through
    `ai.context.context_builder.build_ai_context()` (e.g. one
    constructed directly in a test), and this function never silently
    falls back to a caller-supplied or freshly-generated id in that
    case -- "Caller o'zi yaratmaydi" (the caller does not generate it
    itself) is enforced here, not just documented.

    `context_hash` defaults to `ai_context.snapshot_id` itself when
    omitted -- deliberately NOT a fresh hash of `ai_context.to_dict()`,
    since `to_dict()` includes `built_at`, which would make
    `context_hash` differ between two calls with identical content
    (the exact "har safar cache miss" trap `snapshot_id` exists to
    avoid). A caller only needs to pass an explicit `context_hash` if
    it wants to additionally distinguish otherwise-identical snapshots
    by some request-specific detail outside the `AIContext` itself.
    """
    if ai_context.snapshot_id is None:
        raise ValueError(
            "ai_context.snapshot_id is None -- build_ai_context() always sets it; "
            "construct AIContext via that function, not directly, before building a CacheKey."
        )

    resolved_context_hash = context_hash if context_hash is not None else ai_context.snapshot_id

    return CacheKey(
        capability=capability, context_version=ai_context.context_version, provider_name=provider_name,
        prompt_version=prompt_version, context_hash=resolved_context_hash, snapshot_id=ai_context.snapshot_id,
        user_role=user_role,
    )


@dataclass(frozen=True)
class CachePolicy:
    """default_ttl_seconds: how long a cache entry stays valid after being written -- 300s (5 minutes) default, short enough that a market-context-dependent answer does not linger far past the context it was computed from."""
    default_ttl_seconds: int = 300

    def ttl_for(self, capability: Capability) -> int:
        """A single default today -- kept as a method (not a bare attribute read) so a future phase can differentiate TTL per capability without changing this class's public shape."""
        return self.default_ttl_seconds
