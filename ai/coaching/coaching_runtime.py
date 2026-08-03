"""
AI Layer — Coaching Runtime (Phase 66.4: AI Coaching Intelligence
Foundation, TASK 3).

`CoachingRuntime` is CRUD-only Foundation, exactly as the brief
requires ("LLM yo'q. Reasoning yo'q. Inference yo'q." -- no LLM, no
reasoning, no inference): `create()`/`get()`/`list()`/`archive()`/
`update_status()`, nothing else. No trade evaluation, no BUY/SELL
decision, no Risk computation, no Trading Core interaction of any kind.

In-memory only (isolation list, TASK 8: no `database/` import) -- a
private dict, the same "Foundation, not a real persistence layer"
convention `ai/learning/learning_runtime.py`'s own `_records` dict
already established. No SQLite/Postgres/Redis import anywhere in this
file.

Owner-gated: every method re-checks
`ai.coaching.access.is_coaching_intelligence_enabled_for()` itself, the
same "each method re-checks independently" posture every other
`65.x`/`66.x` Runtime already uses.
"""

import dataclasses
from datetime import datetime, timezone
from typing import Dict, Mapping, Optional, Sequence

from ai.access.permissions import AIRole
from ai.coaching.access import is_coaching_intelligence_enabled_for
from ai.coaching.models import (
    CoachingPriority,
    CoachingRecommendation,
    CoachingStatus,
    CoachingTopic,
    CoachingType,
    generate_coach_id,
)
from core_layer.configuration.feature_flags import DEFAULT_FLAGS, FeatureFlags


class CoachingRuntime:
    """Every dependency is injectable, same convention as every other Phase 61.x-66.3 runtime/manager."""

    def __init__(self, flags: FeatureFlags = DEFAULT_FLAGS) -> None:
        self._flags = flags
        self._records: Dict[str, CoachingRecommendation] = {}

    def create(
        self,
        user_id: str,
        topic: CoachingTopic,
        message: str,
        role: AIRole,
        learning_id: Optional[str] = None,
        journal_id: Optional[str] = None,
        priority: CoachingPriority = CoachingPriority.MEDIUM,
        type: CoachingType = CoachingType.RECOMMENDATION,
        recommendation: Optional[str] = None,
        metadata: Optional[Mapping[str, str]] = None,
    ) -> Optional[CoachingRecommendation]:
        """Never raises: a denied role returns None before any record is constructed. `message`/`recommendation`/`topic`/`priority`/`type` are relayed exactly as supplied -- never generated or graded here."""
        if not is_coaching_intelligence_enabled_for(role, self._flags):
            return None

        record = CoachingRecommendation(
            coach_id=generate_coach_id(),
            user_id=user_id,
            topic=topic,
            message=message,
            learning_id=learning_id,
            journal_id=journal_id,
            priority=priority,
            type=type,
            recommendation=recommendation,
            status=CoachingStatus.PENDING,
            created_at=datetime.now(timezone.utc).isoformat(),
            metadata=dict(metadata) if metadata is not None else {},
        )
        self._records[record.coach_id] = record
        return record

    def get(self, coach_id: str, role: AIRole) -> Optional[CoachingRecommendation]:
        """Never raises: an unknown coach_id or a denied role both return None."""
        if not is_coaching_intelligence_enabled_for(role, self._flags):
            return None
        return self._records.get(coach_id)

    def list(self, role: AIRole) -> Sequence[CoachingRecommendation]:
        """Never raises: a denied role returns an empty tuple, never a partial or fabricated list."""
        if not is_coaching_intelligence_enabled_for(role, self._flags):
            return ()
        return tuple(self._records.values())

    def update_status(
        self, coach_id: str, role: AIRole, status: CoachingStatus
    ) -> Optional[CoachingRecommendation]:
        """
        Never raises: a denied role or unknown coach_id both return
        None. Only `status` is ever updated by this method -- every
        other field is immutable after `create()`, the same
        narrow-scope convention `ai/learning/learning_runtime.py`'s
        own `update()` already established. `status=ARCHIVED` is
        rejected here -- archiving is a dedicated, one-way action via
        `archive()` only.
        """
        if not is_coaching_intelligence_enabled_for(role, self._flags):
            return None
        if status == CoachingStatus.ARCHIVED:
            return None

        existing = self._records.get(coach_id)
        if existing is None:
            return None

        updated = dataclasses.replace(existing, status=status)
        self._records[coach_id] = updated
        return updated

    def archive(self, coach_id: str, role: AIRole) -> Optional[CoachingRecommendation]:
        """Never raises: sets status to ARCHIVED only -- never deletes a record (append-only-in-memory posture, no real database anywhere in this package)."""
        if not is_coaching_intelligence_enabled_for(role, self._flags):
            return None

        existing = self._records.get(coach_id)
        if existing is None:
            return None

        archived = dataclasses.replace(existing, status=CoachingStatus.ARCHIVED)
        self._records[coach_id] = archived
        return archived
