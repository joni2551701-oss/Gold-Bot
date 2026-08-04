"""
Gateway rate limiter (v1.1 Phase 1, module 10).

A clock-injected token bucket, keyed (per principal, per service, or any
key the router chooses). Deterministic: given the same `now` sequence it
always makes the same decisions, so it is fully unit-testable without real
time.

Pure; imports only the stdlib.
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict


class _Bucket:
    __slots__ = ("tokens", "last")

    def __init__(self, tokens: float, last: datetime):
        self.tokens = tokens
        self.last = last


class RateLimiter:
    def __init__(self, capacity: int = 60, refill_per_second: float = 1.0):
        self._capacity = float(max(1, capacity))
        self._rate = float(refill_per_second)
        self._buckets: Dict[str, _Bucket] = {}

    def allow(self, key: str, now: datetime) -> bool:
        """Consume one token for `key`; True if available, False if throttled."""
        bucket = self._buckets.get(key)
        if bucket is None:
            self._buckets[key] = _Bucket(self._capacity - 1.0, now)
            return True
        elapsed = max(0.0, (now - bucket.last).total_seconds())
        bucket.tokens = min(self._capacity, bucket.tokens + elapsed * self._rate)
        bucket.last = now
        if bucket.tokens >= 1.0:
            bucket.tokens -= 1.0
            return True
        return False

    def reset(self, key: str) -> None:
        self._buckets.pop(key, None)
