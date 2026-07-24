"""
AI Layer — AI Request Log (Phase 61.0: AI Infrastructure Foundation,
TASK 9).

In-memory record of an AI call *attempt* -- distinct from
`database/audit_log_repository.py`'s `AuditLogRepository`, which is
real, persisted, and scoped to Infrastructure/Trading-control actions
(Runtime Feature toggles, Emergency transitions). "Real DB yozish
shart emas... Foundation" (no real DB write required) per the brief --
this module never imports `database/`.
"""

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional

from ai.capabilities.capability import Capability


@dataclass(frozen=True)
class AIRequestLogEntry:
    request_id: str
    capability: Capability
    provider_name: Optional[str]
    telegram_id: Optional[str]
    created_at: datetime


class RequestLog:
    def __init__(self) -> None:
        self._entries: List[AIRequestLogEntry] = []

    def record(self, capability: Capability, provider_name: Optional[str], telegram_id: Optional[str] = None) -> AIRequestLogEntry:
        entry = AIRequestLogEntry(
            request_id=str(uuid.uuid4()), capability=capability, provider_name=provider_name,
            telegram_id=telegram_id, created_at=datetime.now(timezone.utc),
        )
        self._entries.append(entry)
        return entry

    def all(self) -> List[AIRequestLogEntry]:
        return list(self._entries)
