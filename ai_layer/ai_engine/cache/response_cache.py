"""
AI Layer — AI Response Cache (Phase 61.1: AI Provider Reliability
Foundation, TASK 9).

In-memory, TTL-bound cache keyed exclusively by `cache_policy.CacheKey`
-- no method here accepts a bare string key, so the "never cache by
prompt text alone" rule (TASK 9's brief) cannot be bypassed by a
caller. Not wired into any provider call this phase -- foundation
only, matching every other Phase 61.0/61.1 module's posture.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from ai_layer.ai_engine.cache.cache_policy import CacheKey, CachePolicy


@dataclass(frozen=True)
class CacheEntry:
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    cached_at: Optional[datetime] = None
    ttl_seconds: int = 0


class ResponseCache:
    def __init__(self, policy: Optional[CachePolicy] = None) -> None:
        self._policy = policy if policy is not None else CachePolicy()
        self._entries: Dict[str, CacheEntry] = {}

    def put(self, key: CacheKey, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        self._entries[key.as_string()] = CacheEntry(
            content=content, metadata=metadata or {}, cached_at=datetime.now(timezone.utc),
            ttl_seconds=self._policy.ttl_for(key.capability),
        )

    def get(self, key: CacheKey, now: Optional[datetime] = None) -> Optional[CacheEntry]:
        """Returns None for a missing OR expired entry -- an expired entry is also evicted, so a subsequent get() does not need to re-check expiry against stale state."""
        entry = self._entries.get(key.as_string())
        if entry is None:
            return None

        check_time = now if now is not None else datetime.now(timezone.utc)
        if (check_time - entry.cached_at).total_seconds() > entry.ttl_seconds:
            del self._entries[key.as_string()]
            return None

        return entry

    def is_expired(self, key: CacheKey, now: Optional[datetime] = None) -> bool:
        return self.get(key, now=now) is None

    def clear(self, key: Optional[CacheKey] = None) -> None:
        """Clears one entry, or every entry if `key` is omitted -- same shape as ai/memory/context_memory.py's ContextMemory.clear() and ai/access/usage_limits.py's UsageLimiter.reset()."""
        if key is None:
            self._entries.clear()
        else:
            self._entries.pop(key.as_string(), None)
