"""
AI Layer — AI Usage Accounting (Phase 61.4: AI Product & Control
Layer, TASK 6).

A per-`telegram_id` cost/usage aggregation over `ai/audit/request_log.py`
and `ai/audit/response_log.py` -- generalizes `ai/audit/trace.py`'s own
`request_id -> telegram_id` join (Phase 61.3 TASK 8) from "one
request_id" to "every request_id belonging to one telegram_id."
Neither log class is modified, no new log field -- pure aggregation
over already-recorded history, same posture as
`ai/audit/provider_stats.py`'s own `compute_provider_stats()`. The
Director's own "Today AI Cost: Gemini $12.40 / GPT $8.20 / Total
$20.60" worked example is a per-*provider* summary, not per-user --
that report is already fully satisfiable by the existing, unmodified
`compute_provider_stats()`; this module adds only the per-user
dimension that did not exist yet.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List

from ai.audit.request_log import AIRequestLogEntry
from ai.audit.response_log import AIResponseLogEntry


@dataclass(frozen=True)
class UserUsageStats:
    telegram_id: str
    total_calls: int
    total_tokens: int
    total_cost: float
    cost_by_provider: Dict[str, float] = field(default_factory=dict)


def compute_user_usage(
    requests: List[AIRequestLogEntry], responses: List[AIResponseLogEntry],
) -> Dict[str, UserUsageStats]:
    """
    Never raises: empty inputs return an empty dict. Requests with no
    `telegram_id` (an anonymous/internal call) are excluded -- there is
    no user to attribute them to, the same convention
    `compute_provider_stats()` uses for a `None` `provider_name`. A
    `response_log` entry whose `request_id` has no matching
    `request_log` entry (e.g. logs from two different `AIService`
    instances) is silently excluded rather than raising.
    """
    request_id_to_telegram_id: Dict[str, str] = {
        request.request_id: request.telegram_id
        for request in requests if request.telegram_id is not None
    }

    grouped: Dict[str, List[AIResponseLogEntry]] = defaultdict(list)
    for response in responses:
        telegram_id = request_id_to_telegram_id.get(response.request_id)
        if telegram_id is not None:
            grouped[telegram_id].append(response)

    stats: Dict[str, UserUsageStats] = {}
    for telegram_id, group in grouped.items():
        cost_by_provider: Dict[str, float] = defaultdict(float)
        for entry in group:
            if entry.provider_name is not None:
                cost_by_provider[entry.provider_name] += entry.cost

        stats[telegram_id] = UserUsageStats(
            telegram_id=telegram_id,
            total_calls=len(group),
            total_tokens=sum(entry.tokens for entry in group),
            total_cost=sum(entry.cost for entry in group),
            cost_by_provider=dict(cost_by_provider),
        )
    return stats
