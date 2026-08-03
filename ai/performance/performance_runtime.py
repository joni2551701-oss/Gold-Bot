"""
AI Layer — Performance Runtime (Phase 66.5: AI Performance
Intelligence Foundation, TASK 3).

`PerformanceRuntime` is CRUD-only Foundation, exactly as TASK 3
requires ("AI xulosa bermaydi. GPT chaqirmaydi. Scoring algoritm
yaratmaydi." -- no AI conclusions, no GPT call, no scoring algorithm):
`create()`/`get()`/`list()`/`update_notes()`/`archive()`, nothing
else. No trade evaluation, no BUY/SELL decision, no Risk computation,
no Trading Core interaction of any kind.

In-memory only (isolation list: no `database/` import) -- a private
dict, the same "Foundation, not a real persistence layer" convention
`ai/coaching/coaching_runtime.py`'s own `_records` dict already
established. No SQLite/Postgres/Redis import anywhere in this file.

Owner-gated: every method re-checks
`ai.performance.access.is_performance_intelligence_enabled_for()`
itself, the same "each method re-checks independently" posture every
other `65.x`/`66.x` Runtime already uses.
"""

import dataclasses
from datetime import datetime, timezone
from typing import Dict, Optional, Sequence

from ai.access.permissions import AIRole
from ai.performance.access import is_performance_intelligence_enabled_for
from ai.performance.models import PerformanceRecord, generate_performance_id
from core_layer.configuration.feature_flags import DEFAULT_FLAGS, FeatureFlags


class PerformanceRuntime:
    """Every dependency is injectable, same convention as every other Phase 61.x-66.4 runtime/manager."""

    def __init__(self, flags: FeatureFlags = DEFAULT_FLAGS) -> None:
        self._flags = flags
        self._records: Dict[str, PerformanceRecord] = {}

    def create(
        self,
        user_id: str,
        trade_id: str,
        role: AIRole,
        journal_id: Optional[str] = None,
        result: Optional[str] = None,
        direction: Optional[str] = None,
        entry_quality: Optional[float] = None,
        exit_quality: Optional[float] = None,
        discipline_score: Optional[float] = None,
        risk_score: Optional[float] = None,
        confidence_score: Optional[float] = None,
        notes: Optional[str] = None,
    ) -> Optional[PerformanceRecord]:
        """Never raises: a denied role returns None before any record is constructed. Every score/result/direction field is relayed exactly as supplied -- never computed or graded here (TASK 3's own rule)."""
        if not is_performance_intelligence_enabled_for(role, self._flags):
            return None

        record = PerformanceRecord(
            id=generate_performance_id(),
            user_id=user_id,
            trade_id=trade_id,
            journal_id=journal_id,
            result=result,
            direction=direction,
            entry_quality=entry_quality,
            exit_quality=exit_quality,
            discipline_score=discipline_score,
            risk_score=risk_score,
            confidence_score=confidence_score,
            notes=notes,
            archived=False,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._records[record.id] = record
        return record

    def get(self, record_id: str, role: AIRole) -> Optional[PerformanceRecord]:
        """Never raises: an unknown record_id or a denied role both return None."""
        if not is_performance_intelligence_enabled_for(role, self._flags):
            return None
        return self._records.get(record_id)

    def list(self, role: AIRole) -> Sequence[PerformanceRecord]:
        """Never raises: a denied role returns an empty tuple, never a partial or fabricated list."""
        if not is_performance_intelligence_enabled_for(role, self._flags):
            return ()
        return tuple(self._records.values())

    def update_notes(self, record_id: str, role: AIRole, notes: str) -> Optional[PerformanceRecord]:
        """
        Never raises: a denied role or unknown record_id both return
        None. Only `notes` is ever updated by this method -- every
        other field (`result`/`direction`/the four quality scores) is
        immutable after `create()`, the same narrow-scope convention
        `ai/trade_journal/journal_runtime.py`'s own `update_notes()`
        already established.
        """
        if not is_performance_intelligence_enabled_for(role, self._flags):
            return None

        existing = self._records.get(record_id)
        if existing is None:
            return None

        updated = dataclasses.replace(existing, notes=notes)
        self._records[record_id] = updated
        return updated

    def archive(self, record_id: str, role: AIRole) -> Optional[PerformanceRecord]:
        """Never raises: sets `archived=True` only -- never deletes a record (append-only-in-memory posture, no real database anywhere in this package)."""
        if not is_performance_intelligence_enabled_for(role, self._flags):
            return None

        existing = self._records.get(record_id)
        if existing is None:
            return None

        archived = dataclasses.replace(existing, archived=True)
        self._records[record_id] = archived
        return archived
