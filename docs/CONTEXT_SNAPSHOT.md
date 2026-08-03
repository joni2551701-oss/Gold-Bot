# Context Snapshot Foundation (Phase A16)

## Purpose

Builds one standard, flat, JSON-serializable summary of market
context — `ContextSnapshotSchema` — for a future AI provider,
Analytics, Replay, or Education consumer. **This is a
standardization layer, not a new analysis.** No new strategy, no
BOS/CHoCH algorithm change, no liquidity logic change, no FVG logic
change, no AI integration, no pipeline redesign, and no database
migration are introduced in this phase.

Today, the real, internal `context.context_orchestrator.ContextSnapshot`
(12 fields: `candles`, `structure`, `bos_events`, `choch_events`,
`liquidity_zones`, `liquidity_sweeps`, `order_blocks`,
`fair_value_gaps`, `amd_events`, `wyckoff_events`, `session_events`,
`market_regime`) is exactly what the live pipeline needs — every
strategy, Signal Quality Score, Explainability, and Feature
Engineering already consume it directly. It is **not**, however,
JSON-serializable, versioned, identity-bearing, or immutable-by-
design in a way a future backtest replay or training dataset export
could rely on across process boundaries. `ContextSnapshotSchema`
exists to answer a different question than the real `ContextSnapshot`
does: not "what does a live pipeline cycle need to run a strategy,"
but "what does a permanent, portable record of *this moment's*
context look like."

## A critical naming note

`context_layer.context_engine.context_orchestrator` already defines a class named
`ContextSnapshot` — untouched by this phase, and it stays the name
every existing detector/strategy/signal-quality/explainability/
feature-engineering module already imports and consumes. This
phase's new class is deliberately named **`ContextSnapshotSchema`**,
not `ContextSnapshot`, specifically to avoid a same-name collision
between two structurally unrelated types in the same top-level
package. This mirrors Phase A15's own naming: `signal_layer/signal_builder/schema.py`
defines `SignalSchema`, not a second `SignalCandidate`, to stay
distinct from `signal_layer/signal_builder/models.py`'s real `SignalCandidate`. Anyone
searching this codebase for "ContextSnapshot" should be aware there
are now two distinct concepts:

| | `context.context_orchestrator.ContextSnapshot` | `context.snapshot.ContextSnapshotSchema` |
|---|---|---|
| Since | Phase A2 (extended through A7) | Phase A16 |
| Shape | 12 fields, each a full sequence of detector-result objects (`Sequence[StructurePoint]`, `Sequence[BosEvent]`, etc.) | ~12 fields, flat/nested primitives only (`bool`, `str`, `Optional[str]`, `Optional[datetime]`) |
| Consumers | Every strategy, `signal_quality.py`, `explainability.py`, `feature_engine.py`, `core/pipeline.py` | None in this phase — a future AI/Analytics/Replay/Education consumer |
| JSON-serializable | No | Yes (`to_dict()`/`to_json()`) |
| Identity/versioning | None | `snapshot_id`, `created_at`, `version` |
| Wired into the live pipeline | Yes — `core/pipeline.py`'s `context = build_context_snapshot(...)` | No — not in this phase |

## Architecture

```
Market Data
      |
      v
Context Engine
      |
      v
Context Snapshot (real, internal -- context.context_orchestrator.ContextSnapshot)
      |
      v
     (Strategy Engine consumes it exactly as before -- unchanged)
```

```
ContextSnapshotSchema (this phase, standalone)
      |
      v
AI / Analytics / Replay / Education   -- not wired to any of these in this phase
```

`context_layer/context_engine/snapshot.py`'s `from_context_snapshot()` adapts an existing,
already-built `context.context_orchestrator.ContextSnapshot` into a
`ContextSnapshotSchema` — it is not itself part of the live pipeline
flow. `core/pipeline.py` does not call it anywhere in this phase.

## Pre-implementation audit

Before writing any code, `context_layer/context_engine/context_orchestrator.py` and every
detector module it orchestrates were read in full, to reuse rather
than invent:

| Found | Location | Reused as |
|---|---|---|
| `most_recent_bias(structure) -> Optional[str]` ("BULLISH"/"BEARISH"/`None`) | `context_layer/market_structure/market_structure.py` (Phase A4/A5 shared helper) | `StructureInfo.trend` — the exact same value Signal Quality Score and HTF Bias already compute, not a new calculation. |
| `StructureType.HIGHER_HIGH.value == "HH"` (and `HL`/`LH`/`LL`/`UNKNOWN`) | `context_layer/market_structure/market_structure.py` | `StructureInfo.swing_state` — the most recent `StructurePoint.structure.value`, a single already-classified label (not a new combined "last-high + last-low" walk — see "A deliberate simplification" below). |
| `MarketRegime.TRENDING/RANGE/ACCUMULATION/DISTRIBUTION/HIGH_VOLATILITY/LOW_VOLATILITY/UNKNOWN` | `context_layer/trend/market_regime.py` (Phase A7) | `ContextSnapshotSchema.regime` — the real 7-value vocabulary, relayed via `.regime.value` (see "A deliberate deviation" below). |
| `LiquidityType.BSL.value == "BUY_SIDE_LIQUIDITY"`, `SSL.value == "SELL_SIDE_LIQUIDITY"` | `context_layer/liquidity/liquidity.py` | `LiquidityInfo.liquidity_type` — the real value, not the roadmap's shortened illustrative `"SELL_SIDE"` label. |
| `Session.LONDON.value == "LONDON"` (and every other session) | `context_layer/session/session.py` (Phase A6) | `SessionInfo.current_session` — the latest `SessionEvent.session.value`, same pattern `features/feature_engine.py` (Phase A10) already used. |
| `setup_logger("ContextEngine")` | `context_layer/context_engine/context_orchestrator.py` | `SnapshotMetadata.source` default — the real logger name this module already uses, not an invented label. |
| No `premium_discount`/premium-discount-zone detector anywhere; `context_layer/context_engine/context_config.py`'s own docstring names it as a future detector | `context_layer/context_engine/context_config.py` | Confirms `ZonesInfo.premium_discount` has no real source today — stays an honest `None` hook, never fabricated. |
| `signal_layer/signal_builder/schema.py`'s `generate_signal_id()` (`str(uuid.uuid4())`), `ValidationResult(valid, errors)` shape (Phase A15) | `signal_layer/signal_builder/schema.py` | The exact same identity-generation convention (`generate_snapshot_id()`) and result-shape convention, independently re-declared (not imported — see "Why not import from `signals/`" below), not invented. |

## Model

```python
@dataclass(frozen=True)
class ContextSnapshotSchema:
    snapshot_id: str
    created_at: datetime
    version: str = "1.0"
    symbol: Optional[str] = None
    timeframe: Optional[str] = None
    timestamp: Optional[datetime] = None
    structure: StructureInfo = field(default_factory=StructureInfo)
    liquidity: LiquidityInfo = field(default_factory=LiquidityInfo)
    zones: ZonesInfo = field(default_factory=ZonesInfo)
    session: SessionInfo = field(default_factory=SessionInfo)
    regime: str = "UNKNOWN"
    metadata: SnapshotMetadata = field(default_factory=SnapshotMetadata)
```

| Group | Fields | Notes |
|---|---|---|
| Identity | `snapshot_id`, `created_at`, `version` | `snapshot_id` via `generate_snapshot_id()`. `version` is the *schema* version (`"1.0"` today). |
| Market | `symbol`, `timeframe`, `timestamp` | All `Optional` — an empty-candle context has no real `timestamp` to report; `validate_snapshot()`, not the constructor, is where that becomes an error. |
| `structure: StructureInfo` | `trend`, `bos`, `choch`, `swing_state` | `bos`/`choch` are presence checks (`bool(context.bos_events)`/`bool(context.choch_events)`), not direction or count. |
| `liquidity: LiquidityInfo` | `sweep_detected`, `liquidity_type` | `liquidity_type` is the most recent sweep's real `LiquidityType.value`. |
| `zones: ZonesInfo` | `order_block`, `fvg`, `premium_discount` | `order_block`/`fvg` are presence checks. `premium_discount` is always `None` (no detector exists). |
| `session: SessionInfo` | `current_session` | The latest `SessionEvent.session.value`. |
| `regime` | — | One of `ALLOWED_REGIMES` (the real 7-value `MarketRegime` vocabulary). |
| `metadata: SnapshotMetadata` | `source`, `engine_version` | `source` defaults `"ContextEngine"`. `engine_version` is always `None` — no versioning scheme exists for the detection engine itself today. |

### A deliberate deviation: `regime`'s vocabulary

The brief's own illustrative example listed a 5-value `regime`
vocabulary (`TREND`/`RANGE`/`REVERSAL`/`VOLATILITY`/`UNKNOWN`) — not
what `context_layer/trend/market_regime.py`'s real `MarketRegime` enum produces
(`TRENDING`/`RANGE`/`ACCUMULATION`/`DISTRIBUTION`/`HIGH_VOLATILITY`/
`LOW_VOLATILITY`/`UNKNOWN`, 7 values). Collapsing the real 7 values
down to the illustrative 5 would require inventing a new mapping rule
— e.g., deciding whether `ACCUMULATION` means `"REVERSAL"` or
something else — which is itself a new piece of analysis logic this
phase's explicit scope forbids ("Yangi analiz logikasi yozilmaydi").
`ContextSnapshotSchema.regime` therefore relays
`MarketRegimeResult.regime.value` directly, using the real,
already-computed 7-value vocabulary — the same
real-value-over-illustrative-example choice Phase A11/A12/A15 each
made when a brief's example conflicted with an already-real value.

### A deliberate simplification: `swing_state`

The brief's own illustrative example showed `"swing_state":"HH_HL"` —
a combined pair (most recent classified high type + most recent
classified low type). Computing that pair would require a new
backward walk over `context.structure` tracking the last high-type
and low-type classifications independently — a small but genuinely
new piece of aggregation logic. `StructureInfo.swing_state` instead
uses the single most recent `StructurePoint.structure.value` (e.g.
`"HH"` alone) — a direct read of already-classified data, zero new
walk logic. Documented here rather than silently narrowed, matching
Phase A10's own disclosure that `MarketFeatures.atr` is a range
proxy, not a textbook ATR.

### Why not import from `signals/`

`context_layer/context_engine/snapshot.py` defines its own tiny `ValidationResult(valid,
errors)` rather than importing `signal_layer.signal_builder.schema.ValidationResult`
(Phase A15), even though the shape is identical. `context/` must
never depend on `signals/` — `docs/ARCHITECTURE_RULES.md`'s Context
Engine rule states this explicitly ("❌ signal yaratish" extends to
not importing the signal layer's own types). The two-field
`(valid, errors)` shape recurring independently across
`SignalQualityResult`-adjacent code, `DataQualityResult`,
`RiskResult.approved`, `signal_layer.signal_builder.schema.ValidationResult`, and now
`context.snapshot.ValidationResult` is a *convention*, not shared
code — the same reasoning Phase A5's Wyckoff module used for not
reusing `amd.py`'s sweep-correlation logic.

## Design Rules

`ContextSnapshotSchema`:

**Does**
- ✅ Store context information (already-computed values only).
- ✅ Serialize (`to_dict()`/`to_json()`) and deserialize
  (`from_dict()`/`from_json()`).
- ✅ Validate (`validate_snapshot()`).

**Does NOT**
- ❌ Generate a signal.
- ❌ Produce a `BUY`/`SELL` decision.
- ❌ Call a strategy.
- ❌ Call the AI layer.
- ❌ Write to the database.

## Immutability

`ContextSnapshotSchema` and every nested `*Info`/`SnapshotMetadata`
group are `@dataclass(frozen=True)` — a snapshot cannot be edited
after creation. This matters specifically because a future backtest,
AI training run, or replay needs historical accuracy: a 10:00
snapshot correctly read `BULLISH`, and a later 10:30 snapshot
correctly reads `BEARISH` — two separate, both-correct
`ContextSnapshotSchema` objects, never one object silently overwritten
in place. `dataclasses.FrozenInstanceError` is raised on any
attribute-assignment attempt (verified in
`tests/context/test_snapshot.py`).

## Serialization

`to_dict()` returns a JSON-safe, nested `dict` (`created_at`/
`timestamp` rendered as ISO-8601 strings via `.isoformat()`, `None`
`timestamp` stays `None`, not a string; every other field is already
a JSON-native primitive, including the nested `structure`/
`liquidity`/`zones`/`session`/`metadata` groups). `to_json()` wraps it
in `json.dumps()`. `from_dict()`/`from_json()` are the exact inverse
— reconstructing every nested group and parsing ISO-8601 strings back
into `datetime`. `tests/context/test_serialization.py` verifies the
full round trip (`Python object -> JSON -> object`) produces an equal
object.

## Validation

`validate_snapshot(snapshot) -> ValidationResult` checks that
`symbol`, `timeframe`, `timestamp`, and `version` are all present
(the roadmap's own explicit requirement), plus that `regime` (when
set) is one of the real `MarketRegime` values. Never raises — an
invalid `ContextSnapshotSchema` (e.g. `symbol=None`) produces
`ValidationResult(valid=False, errors=[...])`, the same fail-safe
posture every other Phase A foundation module uses.

## Versioning

`version: str = "1.0"` — the schema's own version, distinct from
`SnapshotMetadata.engine_version` (the detection engine's version,
always `None` today — no such scheme exists) and distinct from
`strategies/lifecycle/`'s `StrategyDefinition.version` (a different
concept entirely). Exists so a future `ContextSnapshotSchema v2` can
be distinguished from `v1` once this schema's shape needs to change —
not implemented in this phase.

## Existing code — untouched

`context_layer/market_structure/market_structure.py`, `context_layer/liquidity/liquidity.py`,
`context_layer/order_block/order_block.py`, `context_layer/fair_value_gap/fvg.py`,
`context_layer/context_engine/context_orchestrator.py`, and every other existing
`context/*.py` detector are read-only inputs to this phase — none is
modified. `context_layer/context_engine/snapshot.py` is a new, additive file; nothing it
does changes any existing detection algorithm, and
`context.context_orchestrator.ContextSnapshot` (the real, internal
type) is unaffected.

## Future usage

- **AI**: `Signal + ContextSnapshotSchema = Explanation` — a future
  real AI provider reading a specific signal's `SignalSchema` (Phase
  A15) alongside the `ContextSnapshotSchema` its `context_id` would
  reference, to produce a richer explanation than either alone. Not
  implemented in this phase — `SignalSchema.context_id` stays `None`
  until a future phase wires the two together.
- **Analytics**: `Historical Context + Result = Pattern discovery` —
  a future module joining a sequence of `ContextSnapshotSchema`
  records against real trade outcomes to discover which market states
  preceded which results. Not implemented in this phase.
- **Replay**: `from_context_snapshot()` is a pure function over an
  already-built `ContextSnapshot` — a future backtest harness could
  replay historical candles through the existing `context/` detectors
  and call it identically to how a live consumer would, producing a
  consistent, serializable context history without new detection code.
- **Education**: `Past Market Context + Outcome = Lesson` — a stable,
  JSON-native shape simple enough to export for a teaching dataset or
  explain to a non-technical trader, without requiring the internal
  `context.context_orchestrator.ContextSnapshot`'s full detector-object
  graph.
