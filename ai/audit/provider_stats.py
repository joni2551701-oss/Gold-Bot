"""
AI Layer — Provider Stats (Phase 61.0: AI Infrastructure Foundation,
TASK 9).

Pure aggregation over an already-recorded `response_log.py` history --
never fetches or computes latency/cost itself, matching every other
`ai/` foundation module's "reuse the already-computed record, don't
re-derive it" convention.
"""

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List

from ai.audit.response_log import AIResponseLogEntry


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
