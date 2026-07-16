"""
AI Layer — AI Response Cache Policy (Phase 61.1: AI Provider
Reliability Foundation, TASK 9).

Defines the cache key shape and TTL policy for `response_cache.py`.
The key is structurally forbidden from being bare prompt text --
`CacheKey` is a five-field dataclass (Capability + Context Version +
Provider + Prompt Version + Context Hash), the same "enforce the rule
in the type, not just the docstring" posture
`ai/context/context_adapter.py`'s `sanitize_market_context()` already
uses for the raw-market-data boundary. A market-context-dependent
answer (e.g. "Gold trend?") must never be served from a cache entry
built against a stale context -- `context_hash` is what prevents that,
not a bare prompt-text key.
"""

import hashlib
import json
from dataclasses import dataclass

from ai.capabilities.capability import Capability


@dataclass(frozen=True)
class CacheKey:
    """Every field is required -- there is no constructor path that produces a key from prompt text alone."""
    capability: Capability
    context_version: str
    provider_name: str
    prompt_version: str
    context_hash: str

    def as_string(self) -> str:
        """Deterministic, human-inspectable serialization -- used as the actual dict key inside ResponseCache."""
        return "|".join([
            self.capability.value, self.context_version, self.provider_name,
            self.prompt_version, self.context_hash,
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


@dataclass(frozen=True)
class CachePolicy:
    """default_ttl_seconds: how long a cache entry stays valid after being written -- 300s (5 minutes) default, short enough that a market-context-dependent answer does not linger far past the context it was computed from."""
    default_ttl_seconds: int = 300

    def ttl_for(self, capability: Capability) -> int:
        """A single default today -- kept as a method (not a bare attribute read) so a future phase can differentiate TTL per capability without changing this class's public shape."""
        return self.default_ttl_seconds
