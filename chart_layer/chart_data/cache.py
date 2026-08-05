"""Chart Service Foundation — chart cache (FLOW-016).

Cache rule (Director Order): request hash -> chart object, with an
expiration and an invalidate path. Pure in-memory store; it knows
nothing about how the chart object was built. Lives in Chart_Data,
whose canonical responsibility is caching chart data.
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class _Entry:
    value: object
    expires_at: Optional[float]  # None => never expires

    def is_expired(self, now: float) -> bool:
        return self.expires_at is not None and now >= self.expires_at


class ChartCache:
    """Maps a request hash to a chart object with TTL expiration."""

    def __init__(self, default_ttl: Optional[float] = 300.0) -> None:
        self._default_ttl = default_ttl
        self._store: dict = {}

    def get(self, key: str):
        entry = self._store.get(key)
        if entry is None:
            return None
        if entry.is_expired(time.time()):
            self._store.pop(key, None)
            return None
        return entry.value

    def set(self, key: str, value, ttl: Optional[float] = -1.0):
        # ttl == -1.0 sentinel => use default_ttl; None => never expire.
        effective = self._default_ttl if ttl == -1.0 else ttl
        expires_at = None if effective is None else time.time() + effective
        self._store[key] = _Entry(value=value, expires_at=expires_at)
        return value

    def invalidate(self, key: str) -> bool:
        return self._store.pop(key, None) is not None

    def clear(self) -> None:
        self._store.clear()

    def __contains__(self, key: str) -> bool:
        return self.get(key) is not None

    def __len__(self) -> int:
        now = time.time()
        return sum(1 for e in self._store.values() if not e.is_expired(now))
