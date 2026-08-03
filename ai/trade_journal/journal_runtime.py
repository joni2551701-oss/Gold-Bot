"""
AI Layer — Trade Journal Runtime (Phase 66.2: AI Trade Journal
Intelligence Foundation, TASK 4).

`TradeJournalRuntime` is CRUD-only Foundation, exactly as Rule 4 and
Director Note 5 require: `create()`/`get()`/`list()`/`update_notes()`,
nothing else. No Replay logic, no Analytics, no Learning/Coaching/
Performance computation of any kind -- this Runtime never reads
`self._entries` back into a statistic, a pattern, or a verdict. A
future `66.3`-`66.5` phase may *read* this Runtime's own `list()`
output (Director Note 5: "Bu qatlam kelajakdagi 66.3-66.5
bosqichlari tomonidan faqat o'qiladi (READ ONLY)"), but this Runtime
itself never calls into any of those future layers.

In-memory only (Rule 3: "Journal database emas") -- a private dict,
the same convention `ai/content/content_adapter.py`'s own
`_history` list already established for "Foundation, not a real
persistence layer" storage. No SQLite/Postgres/Redis import anywhere
in this file.

Owner-gated: every method re-checks
`ai.trade_journal.access.is_trade_journal_enabled_for()` itself, the
same "each method re-checks independently" posture every other
`65.x`/`66.x` Runtime already uses.
"""

import dataclasses
from datetime import datetime, timezone
from typing import Dict, Optional, Sequence

from ai.access.permissions import AIRole
from ai.trade_journal.access import is_trade_journal_enabled_for
from ai.trade_journal.models import TradeJournalEntry, generate_journal_id
from core_layer.configuration.feature_flags import DEFAULT_FLAGS, FeatureFlags


class TradeJournalRuntime:
    """Every dependency is injectable, same convention as every other Phase 61.x-66.1 runtime/manager."""

    def __init__(self, flags: FeatureFlags = DEFAULT_FLAGS) -> None:
        self._flags = flags
        self._entries: Dict[str, TradeJournalEntry] = {}

    def create(
        self,
        chart_id: str,
        trade_id: str,
        symbol: str,
        timeframe: str,
        direction: str,
        role: AIRole,
        entry: Optional[float] = None,
        sl: Optional[float] = None,
        tp: Optional[float] = None,
        result: Optional[str] = None,
        confidence: Optional[float] = None,
        reason: Optional[str] = None,
        lesson: Optional[str] = None,
        mistakes: Sequence[str] = (),
    ) -> Optional[TradeJournalEntry]:
        """Never raises: a denied role returns None before any entry is constructed. `direction`/`result` are relayed exactly as supplied -- never computed or validated here (Rule 2/4)."""
        if not is_trade_journal_enabled_for(role, self._flags):
            return None

        journal_entry = TradeJournalEntry(
            journal_id=generate_journal_id(),
            chart_id=chart_id,
            trade_id=trade_id,
            symbol=symbol,
            timeframe=timeframe,
            direction=direction,
            entry=entry,
            sl=sl,
            tp=tp,
            result=result,
            confidence=confidence,
            reason=reason,
            lesson=lesson,
            mistakes=tuple(mistakes),
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._entries[journal_entry.journal_id] = journal_entry
        return journal_entry

    def get(self, journal_id: str, role: AIRole) -> Optional[TradeJournalEntry]:
        """Never raises: an unknown journal_id or a denied role both return None."""
        if not is_trade_journal_enabled_for(role, self._flags):
            return None
        return self._entries.get(journal_id)

    def list(self, role: AIRole) -> Sequence[TradeJournalEntry]:
        """Never raises: a denied role returns an empty tuple, never a partial or fabricated list."""
        if not is_trade_journal_enabled_for(role, self._flags):
            return ()
        return tuple(self._entries.values())

    def update_notes(
        self,
        journal_id: str,
        role: AIRole,
        reason: Optional[str] = None,
        lesson: Optional[str] = None,
        mistakes: Optional[Sequence[str]] = None,
    ) -> Optional[TradeJournalEntry]:
        """
        Never raises: a denied role or unknown journal_id both return
        None. Only the three narrative fields (`reason`/`lesson`/
        `mistakes`) are ever updatable -- every other field
        (`chart_id`/`trade_id`/`direction`/`entry`/`sl`/`tp`/`result`)
        is immutable after `create()`, since this method's own name is
        "update_notes," not "update_entry" (TASK 4's own narrow scope).
        """
        if not is_trade_journal_enabled_for(role, self._flags):
            return None

        existing = self._entries.get(journal_id)
        if existing is None:
            return None

        updated = dataclasses.replace(
            existing,
            reason=reason if reason is not None else existing.reason,
            lesson=lesson if lesson is not None else existing.lesson,
            mistakes=tuple(mistakes) if mistakes is not None else existing.mistakes,
        )
        self._entries[journal_id] = updated
        return updated
