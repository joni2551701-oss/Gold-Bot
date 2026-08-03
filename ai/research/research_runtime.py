"""
AI Layer — Research Runtime (Phase 66.8: AI Research Intelligence
Foundation, TASK 3). Final phase of the `66.x` AI Trading Intelligence
sub-sequence.

`ResearchRuntime` is CRUD-only Foundation, exactly as TASK 3/Rule 5
require ("CRUD only."): `create()`/`get()`/`list()`/`update()`/
`update_notes()`/`archive()`, nothing else. No BUY/SELL, no signal, no
risk computation, no strategy selection, no Trading Core interaction
of any kind, no GPT/Claude/Gemini/OpenAI/AI-inference/reasoning of any
kind (Rule 4).

In-memory only (Rule 3: "Database ishlatilmaydi") -- a private dict,
the same "Foundation, not a real persistence layer" convention
`ai/portfolio/portfolio_runtime.py`'s own `_records` dict already
established. No SQLite/Postgres/Redis import anywhere in this file.

Owner-gated: every method re-checks
`ai.research.access.is_research_intelligence_enabled_for()` itself,
the same "each method re-checks independently" posture every other
`65.x`/`66.x` Runtime already uses.
"""

import dataclasses
from datetime import datetime, timezone
from typing import Dict, Optional, Sequence

from ai.access.permissions import AIRole
from ai.research.access import is_research_intelligence_enabled_for
from ai.research.models import (
    ResearchCategory,
    ResearchPriority,
    ResearchRecord,
    ResearchStatus,
    generate_research_id,
)
from goldbot.core_layer.configuration.feature_flags import DEFAULT_FLAGS, FeatureFlags


class ResearchRuntime:
    """Every dependency is injectable, same convention as every other Phase 61.x-66.7 runtime/manager."""

    def __init__(self, flags: FeatureFlags = DEFAULT_FLAGS) -> None:
        self._flags = flags
        self._records: Dict[str, ResearchRecord] = {}

    def create(
        self,
        title: str,
        category: ResearchCategory,
        role: AIRole,
        priority: ResearchPriority = ResearchPriority.MEDIUM,
        status: ResearchStatus = ResearchStatus.ACTIVE,
        summary: Optional[str] = None,
        source_count: int = 0,
        notes: Optional[str] = None,
    ) -> Optional[ResearchRecord]:
        """Never raises: a denied role returns None before any record is constructed. Every field is relayed exactly as supplied -- never computed or graded here (Rule 5)."""
        if not is_research_intelligence_enabled_for(role, self._flags):
            return None

        record = ResearchRecord(
            research_id=generate_research_id(),
            title=title,
            category=category,
            priority=priority,
            status=status,
            summary=summary,
            source_count=source_count,
            notes=notes,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._records[record.research_id] = record
        return record

    def get(self, research_id: str, role: AIRole) -> Optional[ResearchRecord]:
        """Never raises: an unknown research_id or a denied role both return None."""
        if not is_research_intelligence_enabled_for(role, self._flags):
            return None
        return self._records.get(research_id)

    def list(self, role: AIRole) -> Sequence[ResearchRecord]:
        """Never raises: a denied role returns an empty tuple, never a partial or fabricated list."""
        if not is_research_intelligence_enabled_for(role, self._flags):
            return ()
        return tuple(self._records.values())

    def update(
        self,
        research_id: str,
        role: AIRole,
        priority: Optional[ResearchPriority] = None,
        status: Optional[ResearchStatus] = None,
        summary: Optional[str] = None,
        source_count: Optional[int] = None,
    ) -> Optional[ResearchRecord]:
        """
        Never raises: a denied role or unknown research_id both return
        None. Only `priority`/`status`/`summary`/`source_count` are
        ever updated by this method (each left unchanged when its
        argument is None) -- `research_id`/`title`/`category`/
        `created_at` are immutable after `create()`.
        """
        if not is_research_intelligence_enabled_for(role, self._flags):
            return None

        existing = self._records.get(research_id)
        if existing is None:
            return None

        updates = {}
        if priority is not None:
            updates["priority"] = priority
        if status is not None:
            updates["status"] = status
        if summary is not None:
            updates["summary"] = summary
        if source_count is not None:
            updates["source_count"] = source_count

        updated = dataclasses.replace(existing, **updates)
        self._records[research_id] = updated
        return updated

    def update_notes(self, research_id: str, role: AIRole, notes: str) -> Optional[ResearchRecord]:
        """
        Never raises: a denied role or unknown research_id both return
        None. Only `notes` is ever updated by this method, the same
        narrow-scope convention `ai/portfolio/portfolio_runtime.py`'s
        own `update_notes()` already established.
        """
        if not is_research_intelligence_enabled_for(role, self._flags):
            return None

        existing = self._records.get(research_id)
        if existing is None:
            return None

        updated = dataclasses.replace(existing, notes=notes)
        self._records[research_id] = updated
        return updated

    def archive(self, research_id: str, role: AIRole) -> Optional[ResearchRecord]:
        """Never raises: sets `status=ResearchStatus.ARCHIVED` only -- never deletes a record (append-only-in-memory posture, no real database anywhere in this package)."""
        if not is_research_intelligence_enabled_for(role, self._flags):
            return None

        existing = self._records.get(research_id)
        if existing is None:
            return None

        archived = dataclasses.replace(existing, status=ResearchStatus.ARCHIVED)
        self._records[research_id] = archived
        return archived
