"""
AI Layer — Strategy Runtime (Phase 66.6: AI Strategy Intelligence
Foundation, TASK 3).

`StrategyRuntime` is CRUD-only Foundation, exactly as TASK 3/Rule 5
require ("Bu Foundation. Faqat CRUD."):
`create()`/`get()`/`list()`/`archive()`/`update()`/`update_notes()`,
nothing else. No strategy evaluation, no BUY/SELL decision, no Risk
computation, no Trading Core interaction of any kind, no LLM/GPT/Claude/
Gemini/reasoning/inference of any kind (Rule 4).

In-memory only (Rule 3: "Database ishlatilmaydi") -- a private dict,
the same "Foundation, not a real persistence layer" convention
`ai/performance/performance_runtime.py`'s own `_records` dict already
established. No SQLite/Postgres/Redis import anywhere in this file.

Owner-gated: every method re-checks
`ai_layer.ai_engine.strategy.access.is_strategy_intelligence_enabled_for()` itself, the
same "each method re-checks independently" posture every other
`65.x`/`66.x` Runtime already uses.
"""

import dataclasses
from datetime import datetime, timezone
from typing import Dict, Optional, Sequence

from ai_layer.ai_service.access.permissions import AIRole
from ai_layer.ai_engine.strategy.access import is_strategy_intelligence_enabled_for
from ai_layer.ai_engine.strategy.models import (
    StrategyRecord,
    StrategyStatus,
    StrategyType,
    generate_strategy_id,
)
from core_layer.configuration.feature_flags import DEFAULT_FLAGS, FeatureFlags


class StrategyRuntime:
    """Every dependency is injectable, same convention as every other Phase 61.x-66.5 runtime/manager."""

    def __init__(self, flags: FeatureFlags = DEFAULT_FLAGS) -> None:
        self._flags = flags
        self._records: Dict[str, StrategyRecord] = {}

    def create(
        self,
        strategy_name: str,
        strategy_type: StrategyType,
        role: AIRole,
        strategy_version: Optional[str] = None,
        confidence: Optional[str] = None,
        notes: Optional[str] = None,
        status: StrategyStatus = StrategyStatus.TESTING,
    ) -> Optional[StrategyRecord]:
        """Never raises: a denied role returns None before any record is constructed. Every field is relayed exactly as supplied -- never computed or graded here (Rule 5)."""
        if not is_strategy_intelligence_enabled_for(role, self._flags):
            return None

        record = StrategyRecord(
            strategy_id=generate_strategy_id(),
            strategy_name=strategy_name,
            strategy_type=strategy_type,
            strategy_version=strategy_version,
            confidence=confidence,
            notes=notes,
            status=status,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._records[record.strategy_id] = record
        return record

    def get(self, strategy_id: str, role: AIRole) -> Optional[StrategyRecord]:
        """Never raises: an unknown strategy_id or a denied role both return None."""
        if not is_strategy_intelligence_enabled_for(role, self._flags):
            return None
        return self._records.get(strategy_id)

    def list(self, role: AIRole) -> Sequence[StrategyRecord]:
        """Never raises: a denied role returns an empty tuple, never a partial or fabricated list."""
        if not is_strategy_intelligence_enabled_for(role, self._flags):
            return ()
        return tuple(self._records.values())

    def update(
        self,
        strategy_id: str,
        role: AIRole,
        strategy_version: Optional[str] = None,
        confidence: Optional[str] = None,
        status: Optional[StrategyStatus] = None,
    ) -> Optional[StrategyRecord]:
        """
        Never raises: a denied role or unknown strategy_id both return
        None. Only `strategy_version`/`confidence`/`status` are ever
        updated by this method (each left unchanged when its argument
        is None) -- `strategy_id`/`strategy_name`/`strategy_type`/
        `created_at` are immutable after `create()`.
        """
        if not is_strategy_intelligence_enabled_for(role, self._flags):
            return None

        existing = self._records.get(strategy_id)
        if existing is None:
            return None

        updates = {}
        if strategy_version is not None:
            updates["strategy_version"] = strategy_version
        if confidence is not None:
            updates["confidence"] = confidence
        if status is not None:
            updates["status"] = status

        updated = dataclasses.replace(existing, **updates)
        self._records[strategy_id] = updated
        return updated

    def update_notes(self, strategy_id: str, role: AIRole, notes: str) -> Optional[StrategyRecord]:
        """
        Never raises: a denied role or unknown strategy_id both return
        None. Only `notes` is ever updated by this method, the same
        narrow-scope convention `ai/performance/performance_runtime.py`'s
        own `update_notes()` already established.
        """
        if not is_strategy_intelligence_enabled_for(role, self._flags):
            return None

        existing = self._records.get(strategy_id)
        if existing is None:
            return None

        updated = dataclasses.replace(existing, notes=notes)
        self._records[strategy_id] = updated
        return updated

    def archive(self, strategy_id: str, role: AIRole) -> Optional[StrategyRecord]:
        """Never raises: sets `status=StrategyStatus.ARCHIVED` only -- never deletes a record (append-only-in-memory posture, no real database anywhere in this package)."""
        if not is_strategy_intelligence_enabled_for(role, self._flags):
            return None

        existing = self._records.get(strategy_id)
        if existing is None:
            return None

        archived = dataclasses.replace(existing, status=StrategyStatus.ARCHIVED)
        self._records[strategy_id] = archived
        return archived
