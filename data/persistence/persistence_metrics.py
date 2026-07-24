"""
PersistenceMetrics -- counters for the Persistent Memory Layer (module 6).
Monitoring-friendly, mirrors the bootstrap metrics style. This module
never imports from any layer above data/.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PersistenceMetrics:
    snapshots_saved: int = 0
    snapshots_restored: int = 0
    restore_failures: int = 0
    candles_serialized: int = 0
    candles_restored: int = 0
    cache_hits: int = 0
    cache_misses: int = 0

    @property
    def cache_hit_pct(self) -> float:
        total = self.cache_hits + self.cache_misses
        return 100.0 * self.cache_hits / total if total else 0.0

    def as_dict(self) -> dict:
        return {
            "snapshots_saved": self.snapshots_saved,
            "snapshots_restored": self.snapshots_restored,
            "restore_failures": self.restore_failures,
            "candles_serialized": self.candles_serialized,
            "candles_restored": self.candles_restored,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "cache_hit_pct": round(self.cache_hit_pct, 2),
        }
