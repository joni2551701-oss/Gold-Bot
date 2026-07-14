# Context Engine

## Responsibility
Determines the market's current structural state from raw candles —
swing points, structure (HH/HL/LH/LL), BOS/CHoCH, liquidity zones and
sweeps, order blocks, fair value gaps, AMD cycles, Wyckoff
Spring/Upthrust, session classification, and market regime. Pure,
stateless, read-only detection — it never decides whether to trade.

## Input
`Sequence[data.twelve_data_client.Candle]` — the execution-timeframe
candle series (`context.context_orchestrator.ContextEngine.build()`/
`build_context_snapshot()`). `context.htf_bias.compute_htf_bias()`
takes a `data.market_data.MarketSnapshot` (from
`MarketDataNormalizer.get_snapshot()`) instead — a separate,
multi-timeframe input, not `ContextSnapshot`-shaped. Both are read-only:
neither writes to, mutates, or re-fetches its input.

## Output
`context.context_orchestrator.ContextSnapshot` — the real, internal,
12-field structure every downstream module already consumes
(`candles`, `structure`, `bos_events`, `choch_events`,
`liquidity_zones`, `liquidity_sweeps`, `order_blocks`,
`fair_value_gaps`, `amd_events`, `wyckoff_events`, `session_events`,
`market_regime`). `context.htf_bias.HTFBiasResult` is a separate
output, not part of `ContextSnapshot`.

`context.snapshot.ContextSnapshotSchema` (Phase A16) is a distinct,
optional, flat/JSON-serializable *standardized* representation of the
same context, built via `from_context_snapshot()` — not what
`core/pipeline.py` actually receives from Context Engine today (see
`docs/CONTEXT_SNAPSHOT.md`'s naming note). Use `ContextSnapshot` when
describing what the live pipeline passes downstream; use
`ContextSnapshotSchema` when describing a serialized/historical
record.

## Allowed Dependencies
✅ `data/` (`Candle`, `MarketSnapshot`) — market data only.

## Forbidden Dependencies
❌ `strategies/` — Context Engine does not generate a candidate.
❌ `ai/` — no AI interpretation happens here.
❌ `telegram/` — no user-facing output.
❌ `risk/` — no risk computation.
❌ `decision/`, `execution/`, `database/` — same reasoning; Context
Engine is the lowest layer in the pipeline and must never reach
upward. See `docs/ARCHITECTURE_RULES.md`'s Context Engine section.

## Error Contract
Never raises for bad/insufficient market data — every detector
degrades to an empty sequence or an `UNKNOWN`-shaped result (e.g.
`MarketRegime.UNKNOWN`, `HTFBias.UNKNOWN`) rather than throwing.
`ContextEngine._validate_candle_order()` logs a warning (never raises,
never reorders) if candles arrive out of chronological order. Per
`contracts/error_contract.md`, any future exception this layer does
raise (e.g. a malformed `Candle`) should be a `DataError`, never a
bare `Exception`/`ValueError` — not yet implemented in this phase.

## Future Extension
Premium/discount zoning (named, not built — see
`context/context_config.py`'s own docstring and
`docs/CONTEXT_SNAPSHOT.md`'s `ZonesInfo.premium_discount`). Real
volume confirmation once a volume data source exists (Wyckoff's
`_volume_confirms()` hook). `ContextSnapshotSchema` persistence (Phase
A16 names this as a future, not-yet-approved step).
