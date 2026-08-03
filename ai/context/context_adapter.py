"""
AI Layer — AI Context Adapter (Phase 61.0: AI Infrastructure
Foundation, TASK 5; extended Phase 61.3: AI Intelligence Layer,
TASK 2).

A defensive boundary, not a data source: `sanitize_market_context()`
exists so "AI hech qachon raw market data olmaydi" (AI never receives
raw market data) is enforced structurally, not just by convention --
it rejects a `MarketContext` whose `metadata` carries the kind of
bulk/raw keys a candle-series dump would use, rather than trusting
every future caller to remember not to pass one.

`market_context_from_snapshot()` (TASK 2) is the
`context.snapshot.ContextSnapshotSchema -> MarketContext` adapter
`docs/PHASE61_3_INTELLIGENCE_AUDIT.md` TASK 1 found missing. It takes
an *already-built* `ContextSnapshotSchema` (`context_layer/context_engine/snapshot.py`'s
`from_context_snapshot()` output) rather than calling that function or
importing `context.context_orchestrator.ContextSnapshot` itself --
`ai/` never holds a runtime dependency on `context/` (the same
TYPE_CHECKING-only pattern `ai/prompts/prompt_manager.py`'s
`get_fundamental_analysis_prompt()` already uses for
`context.fundamental_context.FundamentalContextSnapshot`, Phase 60.5).
A future caller (`core/pipeline.py`, which already legitimately calls
`from_context_snapshot()`) builds the schema; this function only
formats its already-computed fields -- `ContextSnapshotSchema` itself
carries no raw candle data at all, so there is nothing to sanitize
away here, only to format.
"""

from typing import Optional, TYPE_CHECKING

from ai.interfaces import MarketContext

if TYPE_CHECKING:
    from context_layer.context_engine.snapshot import ContextSnapshotSchema

# Metadata keys that would indicate a caller accidentally attached raw
# market data (a candle series, a full OHLCV dump) instead of the
# already-summarized text MarketContext.summary is meant to carry.
_FORBIDDEN_METADATA_KEYS = frozenset({"candles", "raw_candles", "ohlcv", "raw_data"})


def sanitize_market_context(market_context: Optional[MarketContext]) -> Optional[MarketContext]:
    """
    Returns `market_context` unchanged if it carries no forbidden raw
    key, or a copy with those keys stripped from `metadata` otherwise.
    Never raises -- a violation is corrected, not fatal, matching this
    codebase's fail-safe posture for foundation modules.
    """
    if market_context is None:
        return None

    offending = _FORBIDDEN_METADATA_KEYS.intersection(market_context.metadata.keys())
    if not offending:
        return market_context

    cleaned_metadata = {
        key: value for key, value in market_context.metadata.items()
        if key not in _FORBIDDEN_METADATA_KEYS
    }
    return MarketContext(
        symbol=market_context.symbol,
        timeframe=market_context.timeframe,
        summary=market_context.summary,
        metadata=cleaned_metadata,
    )


def market_context_from_snapshot(schema: "ContextSnapshotSchema") -> MarketContext:
    """
    Formats an already-built `ContextSnapshotSchema`'s fields into a
    `MarketContext` -- never recomputes trend/liquidity/regime, only
    reads what `from_context_snapshot()` already derived. `symbol`/
    `timeframe` fall back to `"UNKNOWN"` if the schema left them
    `None` (an empty-candle snapshot, per `from_context_snapshot()`'s
    own docstring) -- `MarketContext.symbol`/`timeframe` are required,
    non-optional fields, so this never raises even for a degenerate
    input schema.
    """
    structure = schema.structure
    liquidity = schema.liquidity
    zones = schema.zones

    summary_parts = [
        f"Regime: {schema.regime}",
        f"Trend: {structure.trend or 'UNKNOWN'}",
    ]
    if structure.bos:
        summary_parts.append("BOS detected")
    if structure.choch:
        summary_parts.append("CHoCH detected")
    if structure.swing_state:
        summary_parts.append(f"Swing state: {structure.swing_state}")
    if liquidity.sweep_detected:
        summary_parts.append(f"Liquidity sweep: {liquidity.liquidity_type or 'unspecified'}")
    if zones.order_block:
        summary_parts.append("Order block present")
    if zones.fvg:
        summary_parts.append("Fair value gap present")
    if schema.session.current_session:
        summary_parts.append(f"Session: {schema.session.current_session}")

    return MarketContext(
        symbol=schema.symbol or "UNKNOWN",
        timeframe=schema.timeframe or "UNKNOWN",
        summary=", ".join(summary_parts),
        metadata={"snapshot_id": schema.snapshot_id, "regime": schema.regime},
    )
