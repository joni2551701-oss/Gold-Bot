"""
AI Layer — Portfolio Runtime (Phase 66.7: AI Portfolio Intelligence
Foundation, TASK 3).

`PortfolioRuntime` is CRUD-only Foundation, exactly as TASK 3/Rule 5
require ("Foundation. CRUD only."):
`create()`/`get()`/`list()`/`update()`/`update_notes()`/`archive()`,
nothing else. No portfolio evaluation, no optimization, no allocation
decision, no Risk Manager replacement, no Trading Core interaction of
any kind, no LLM/GPT/Claude/Gemini/reasoning/inference of any kind
(Rule 4).

In-memory only (Rule 3: "Database ishlatilmaydi") -- a private dict,
the same "Foundation, not a real persistence layer" convention
`ai/strategy/strategy_runtime.py`'s own `_records` dict already
established. No SQLite/Postgres/Redis import anywhere in this file.

Owner-gated: every method re-checks
`ai.portfolio.access.is_portfolio_intelligence_enabled_for()` itself,
the same "each method re-checks independently" posture every other
`65.x`/`66.x` Runtime already uses.
"""

import dataclasses
from datetime import datetime, timezone
from typing import Dict, Optional, Sequence

from ai.access.permissions import AIRole
from ai.portfolio.access import is_portfolio_intelligence_enabled_for
from ai.portfolio.models import (
    PortfolioHealth,
    PortfolioRecord,
    PortfolioRiskLevel,
    PortfolioStatus,
    generate_portfolio_id,
)
from configuration.feature_flags import DEFAULT_FLAGS, FeatureFlags


class PortfolioRuntime:
    """Every dependency is injectable, same convention as every other Phase 61.x-66.6 runtime/manager."""

    def __init__(self, flags: FeatureFlags = DEFAULT_FLAGS) -> None:
        self._flags = flags
        self._records: Dict[str, PortfolioRecord] = {}

    def create(
        self,
        portfolio_name: str,
        role: AIRole,
        status: PortfolioStatus = PortfolioStatus.ACTIVE,
        risk_level: Optional[PortfolioRiskLevel] = None,
        health: Optional[PortfolioHealth] = None,
        strategy_count: int = 0,
        active_strategy_count: int = 0,
        notes: Optional[str] = None,
    ) -> Optional[PortfolioRecord]:
        """Never raises: a denied role returns None before any record is constructed. Every field is relayed exactly as supplied -- never computed or graded here (Rule 5)."""
        if not is_portfolio_intelligence_enabled_for(role, self._flags):
            return None

        record = PortfolioRecord(
            portfolio_id=generate_portfolio_id(),
            portfolio_name=portfolio_name,
            status=status,
            risk_level=risk_level,
            health=health,
            strategy_count=strategy_count,
            active_strategy_count=active_strategy_count,
            notes=notes,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._records[record.portfolio_id] = record
        return record

    def get(self, portfolio_id: str, role: AIRole) -> Optional[PortfolioRecord]:
        """Never raises: an unknown portfolio_id or a denied role both return None."""
        if not is_portfolio_intelligence_enabled_for(role, self._flags):
            return None
        return self._records.get(portfolio_id)

    def list(self, role: AIRole) -> Sequence[PortfolioRecord]:
        """Never raises: a denied role returns an empty tuple, never a partial or fabricated list."""
        if not is_portfolio_intelligence_enabled_for(role, self._flags):
            return ()
        return tuple(self._records.values())

    def update(
        self,
        portfolio_id: str,
        role: AIRole,
        status: Optional[PortfolioStatus] = None,
        risk_level: Optional[PortfolioRiskLevel] = None,
        health: Optional[PortfolioHealth] = None,
        strategy_count: Optional[int] = None,
        active_strategy_count: Optional[int] = None,
    ) -> Optional[PortfolioRecord]:
        """
        Never raises: a denied role or unknown portfolio_id both return
        None. Only `status`/`risk_level`/`health`/`strategy_count`/
        `active_strategy_count` are ever updated by this method (each
        left unchanged when its argument is None) --
        `portfolio_id`/`portfolio_name`/`created_at` are immutable
        after `create()`.
        """
        if not is_portfolio_intelligence_enabled_for(role, self._flags):
            return None

        existing = self._records.get(portfolio_id)
        if existing is None:
            return None

        updates = {}
        if status is not None:
            updates["status"] = status
        if risk_level is not None:
            updates["risk_level"] = risk_level
        if health is not None:
            updates["health"] = health
        if strategy_count is not None:
            updates["strategy_count"] = strategy_count
        if active_strategy_count is not None:
            updates["active_strategy_count"] = active_strategy_count

        updated = dataclasses.replace(existing, **updates)
        self._records[portfolio_id] = updated
        return updated

    def update_notes(self, portfolio_id: str, role: AIRole, notes: str) -> Optional[PortfolioRecord]:
        """
        Never raises: a denied role or unknown portfolio_id both return
        None. Only `notes` is ever updated by this method, the same
        narrow-scope convention `ai/strategy/strategy_runtime.py`'s own
        `update_notes()` already established.
        """
        if not is_portfolio_intelligence_enabled_for(role, self._flags):
            return None

        existing = self._records.get(portfolio_id)
        if existing is None:
            return None

        updated = dataclasses.replace(existing, notes=notes)
        self._records[portfolio_id] = updated
        return updated

    def archive(self, portfolio_id: str, role: AIRole) -> Optional[PortfolioRecord]:
        """Never raises: sets `status=PortfolioStatus.ARCHIVED` only -- never deletes a record (append-only-in-memory posture, no real database anywhere in this package)."""
        if not is_portfolio_intelligence_enabled_for(role, self._flags):
            return None

        existing = self._records.get(portfolio_id)
        if existing is None:
            return None

        archived = dataclasses.replace(existing, status=PortfolioStatus.ARCHIVED)
        self._records[portfolio_id] = archived
        return archived
