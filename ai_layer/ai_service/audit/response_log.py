"""
AI Layer — AI Response Log (Phase 61.0: AI Infrastructure Foundation,
TASK 9).

Records the outcome of a request already logged in `request_log.py`
-- latency/token/cost/status/capability, exactly the field list the
brief names. In-memory only, same posture as `request_log.py`.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional

from ai_layer.ai_engine.capabilities.capability import Capability


@dataclass(frozen=True)
class AIResponseLogEntry:
    """status: free text, e.g. "SUCCESS"/"FAILED"/"TIMEOUT" -- no fixed enum, since this phase's placeholder providers never actually fail; a real-provider phase can tighten this to an enum then."""
    request_id: str
    capability: Capability
    provider_name: Optional[str]
    latency_ms: float
    tokens: int
    cost: float
    status: str
    created_at: datetime


class ResponseLog:
    def __init__(self) -> None:
        self._entries: List[AIResponseLogEntry] = []

    def record(
        self, request_id: str, capability: Capability, provider_name: Optional[str],
        latency_ms: float, tokens: int, cost: float, status: str,
    ) -> AIResponseLogEntry:
        entry = AIResponseLogEntry(
            request_id=request_id, capability=capability, provider_name=provider_name,
            latency_ms=latency_ms, tokens=tokens, cost=cost, status=status,
            created_at=datetime.now(timezone.utc),
        )
        self._entries.append(entry)
        return entry

    def all(self) -> List[AIResponseLogEntry]:
        return list(self._entries)
