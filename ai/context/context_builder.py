"""
AI Layer — AI Context Builder (Phase 61.0: AI Infrastructure
Foundation, TASK 5; extended Phase 61.1.1: AI Foundation Corrections,
TASK 2).

Pure composition: `build_ai_context()` bundles five already-computed
inputs into one `AIContext`. It never fetches, computes, or derives
any of them itself -- `ai/learning_context.py`'s own docstring
precedent ("reuses... directly", "does NOT itself generate") is
followed here for every input, not just learning data.

Phase 61.1.1 TASK 2: this is the one and only place `AIContext.snapshot_id`
is ever computed. It is a deterministic SHA-256 (via
`ai.cache.cache_policy.compute_context_hash()`, reused, not
reimplemented) over this exact `AIContext`'s own `to_dict()` output
with `built_at` removed first -- `built_at` is the only field that
would otherwise make two calls with byte-identical inputs produce
different ids, which is exactly the "har safar cache miss" failure
mode the Director's brief forbids. Identical inputs at different real
times -> identical `snapshot_id` (a legitimate cache hit is possible);
different inputs -> different `snapshot_id` (a stale answer can never
be served for genuinely different content). No `datetime.now()` or
`uuid.uuid4()` call is used to produce this value, per the brief's own
explicit prohibition -- freshness is content-derived, not
time-derived; `CachePolicy`'s TTL (see `ai/cache/cache_policy.py`) is
what still bounds how long an identical-content cache hit may be
served, layered on top of this identity check.
"""

from dataclasses import replace
from datetime import datetime, timezone
from typing import List, Optional

from ai.cache.cache_policy import compute_context_hash
from ai.context.context_adapter import sanitize_market_context
from ai.context.context_snapshot import AIContext
from ai.interfaces import MarketContext
from ai.journal.trade_journal import TradeJournalRecord
from ai.learning_context import LearningContext
from ai.profiles.user_profile import AIUserProfile
from signals.schema import SignalSchema


def build_ai_context(
    market_context: Optional[MarketContext] = None,
    signal: Optional[SignalSchema] = None,
    user_profile: Optional[AIUserProfile] = None,
    trade_history: Optional[List[TradeJournalRecord]] = None,
    learning_context: Optional[LearningContext] = None,
    context_version: str = "1.0",
) -> AIContext:
    """Never raises: every input is optional, an all-None call returns an AIContext with every field empty/None except built_at/schema_version/context_version/snapshot_id. `schema_version` is not a parameter -- it names this function's own AIContext shape, not something a caller chooses per call (Phase 61.1 TASK 7)."""
    context_without_snapshot_id = AIContext(
        market_context=sanitize_market_context(market_context),
        signal=signal,
        user_profile=user_profile,
        trade_history=list(trade_history) if trade_history is not None else [],
        learning_context=learning_context,
        built_at=datetime.now(timezone.utc),
        context_version=context_version,
    )

    canonical_payload = context_without_snapshot_id.to_dict()
    canonical_payload.pop("built_at", None)
    snapshot_id = compute_context_hash(canonical_payload)

    return replace(context_without_snapshot_id, snapshot_id=snapshot_id)
