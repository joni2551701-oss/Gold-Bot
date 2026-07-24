"""
BootstrapMetrics -- per-asset bootstrap metrics (DD-057).

Monitoring-friendly counters. Cache hit/miss percentages are derived.
This module never imports from any layer above data/.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class BootstrapMetrics:
    """Mutable metrics accumulator for one asset's bootstrap (DD-057)."""
    asset: str
    candles_loaded: int = 0
    api_requests: int = 0
    duration_seconds: float = 0.0
    validation_errors: int = 0
    recovery_count: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    last_bootstrap: Optional[datetime] = None

    @property
    def cache_hit_pct(self) -> float:
        total = self.cache_hits + self.cache_misses
        return 100.0 * self.cache_hits / total if total else 0.0

    @property
    def cache_miss_pct(self) -> float:
        total = self.cache_hits + self.cache_misses
        return 100.0 * self.cache_misses / total if total else 0.0

    def as_dict(self) -> dict:
        return {
            "asset": self.asset,
            "candles_loaded": self.candles_loaded,
            "api_requests": self.api_requests,
            "duration_seconds": round(self.duration_seconds, 6),
            "validation_errors": self.validation_errors,
            "recovery_count": self.recovery_count,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "cache_hit_pct": round(self.cache_hit_pct, 2),
            "cache_miss_pct": round(self.cache_miss_pct, 2),
            "last_bootstrap": self.last_bootstrap.isoformat() if self.last_bootstrap else None,
        }
