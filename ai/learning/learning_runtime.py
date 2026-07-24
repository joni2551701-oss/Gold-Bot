"""
AI Layer — Learning Runtime (Phase 66.3: AI Learning Intelligence
Foundation, TASK 3).

`LearningRuntime` is CRUD-only Foundation, exactly as Rule 10 requires
("Hech qanday real AI inference yo'q" -- no real AI inference):
`create()`/`get()`/`list()`/`update()`/`archive()`, nothing else. No
LLM call, no network call (Rule 4/5), no trade evaluation, no win
rate/profit computation (Rule 6), no coaching (Rule 7), no lesson/quiz
generation (Rule 8/9).

In-memory only (Rule 3: "Database ishlatilmaydi") -- a private dict,
the same "Foundation, not a real persistence layer" convention
`ai/trade_journal/journal_runtime.py`'s own `_entries` dict already
established. No SQLite/Postgres/Redis import anywhere in this file.

Owner-gated: every method re-checks
`ai.learning.access.is_learning_intelligence_enabled_for()` itself,
the same "each method re-checks independently" posture every other
`65.x`/`66.x` Runtime already uses.
"""

import dataclasses
from datetime import datetime, timezone
from typing import Dict, Optional, Sequence

from ai.access.permissions import AIRole
from ai.learning.access import is_learning_intelligence_enabled_for
from ai.learning.models import (
    LearningLevel,
    LearningRecord,
    LearningSource,
    LearningStatus,
    LearningTopic,
    generate_learning_id,
)
from configuration.feature_flags import DEFAULT_FLAGS, FeatureFlags


class LearningRuntime:
    """Every dependency is injectable, same convention as every other Phase 61.x-66.2 runtime/manager."""

    def __init__(self, flags: FeatureFlags = DEFAULT_FLAGS) -> None:
        self._flags = flags
        self._records: Dict[str, LearningRecord] = {}

    def create(
        self,
        user_id: str,
        topic: LearningTopic,
        role: AIRole,
        level: LearningLevel = LearningLevel.UNKNOWN,
        confidence: Optional[float] = None,
        notes: Optional[str] = None,
        source: LearningSource = LearningSource.MANUAL,
    ) -> Optional[LearningRecord]:
        """Never raises: a denied role returns None before any record is constructed. `level`/`confidence` are relayed exactly as supplied -- never graded or computed here (Rule 6/7)."""
        if not is_learning_intelligence_enabled_for(role, self._flags):
            return None

        record = LearningRecord(
            id=generate_learning_id(),
            user_id=user_id,
            topic=topic,
            level=level,
            confidence=confidence,
            notes=notes,
            source=source,
            status=LearningStatus.ACTIVE,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._records[record.id] = record
        return record

    def get(self, record_id: str, role: AIRole) -> Optional[LearningRecord]:
        """Never raises: an unknown record_id or a denied role both return None."""
        if not is_learning_intelligence_enabled_for(role, self._flags):
            return None
        return self._records.get(record_id)

    def list(self, role: AIRole) -> Sequence[LearningRecord]:
        """Never raises: a denied role returns an empty tuple, never a partial or fabricated list."""
        if not is_learning_intelligence_enabled_for(role, self._flags):
            return ()
        return tuple(self._records.values())

    def update(
        self,
        record_id: str,
        role: AIRole,
        level: Optional[LearningLevel] = None,
        confidence: Optional[float] = None,
        notes: Optional[str] = None,
    ) -> Optional[LearningRecord]:
        """
        Never raises: a denied role or unknown record_id both return
        None. Only `level`/`confidence`/`notes` are ever updatable --
        `user_id`/`topic`/`source` are immutable after `create()`,
        the same narrow-scope convention
        `ai/trade_journal/journal_runtime.py`'s own `update_notes()`
        already established.
        """
        if not is_learning_intelligence_enabled_for(role, self._flags):
            return None

        existing = self._records.get(record_id)
        if existing is None:
            return None

        updated = dataclasses.replace(
            existing,
            level=level if level is not None else existing.level,
            confidence=confidence if confidence is not None else existing.confidence,
            notes=notes if notes is not None else existing.notes,
        )
        self._records[record_id] = updated
        return updated

    def archive(self, record_id: str, role: AIRole) -> Optional[LearningRecord]:
        """Never raises: sets status to ARCHIVED only -- never deletes a record (append-only-in-memory posture, no real database anywhere in this package)."""
        if not is_learning_intelligence_enabled_for(role, self._flags):
            return None

        existing = self._records.get(record_id)
        if existing is None:
            return None

        archived = dataclasses.replace(existing, status=LearningStatus.ARCHIVED)
        self._records[record_id] = archived
        return archived
