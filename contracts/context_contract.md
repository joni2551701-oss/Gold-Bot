# Context Engine

## Responsibility
Determines the market's current structural state from raw candles —
swing points, structure (HH/HL/LH/LL), BOS/CHoCH, liquidity zones and
sweeps, order blocks, fair value gaps, AMD cycles, Wyckoff
Spring/Upthrust, session classification, and market regime. Pure,
stateless, read-only detection — it never decides whether to trade.

## Input
`Sequence[data_layer.providers.twelve_data_client.Candle]` — the execution-timeframe
candle series (`context.context_orchestrator.ContextEngine.build()`/
`build_context_snapshot()`). `context.htf_bias.compute_htf_bias()`
takes a `data_layer.live_data.market_data.MarketSnapshot` (from
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
flat/JSON-serializable *standardized* representation of the same
context, built via `from_context_snapshot()` — still not what
`strategies/`, Signal Quality Score, Explainability, or Feature
Engineering receive from Context Engine (they all read the real
`ContextSnapshot` directly, unaffected). As of the Pre-Phase 59
Architecture Readiness Review (AC-03), `core/pipeline.py` does build
one `ContextSnapshotSchema` per cycle (in its `signal_history` stage)
to obtain a `snapshot_id` for linking `SignalSchema.context_id` — see
`docs/CONTEXT_SNAPSHOT.md`'s naming note and
`docs/SIGNAL_SCHEMA.md`'s "AC-03 update" section. Use `ContextSnapshot`
when describing what the live pipeline passes to Strategy/Signal
Quality/Explainability/Feature Engineering; use `ContextSnapshotSchema`
when describing the serialized/historical record.

`context.market_phase.MarketPhaseResult` (AC-02) is a separate,
advisory output — `phase` (`ACCUMULATION`/`MANIPULATION`/
`DISTRIBUTION`/`MARKUP`/`MARKDOWN`/`UNKNOWN`) and `reason` — built via
`compute_market_phase(context)` from already-detected
`wyckoff_events`/`amd_events`/`market_regime`; not a `ContextSnapshot`
field. Computed once per cycle by `core/pipeline.py`'s new
`market_phase` stage, logged, and returned in `run()`'s result dict
only — not consumed by `strategies/`, `signals/`, `ai/`, `decision/`,
or `risk/`.

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
