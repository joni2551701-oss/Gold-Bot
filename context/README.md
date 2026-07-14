# context/

## Purpose
Pure Smart Money Concepts (SMC) market-structure detection for the
execution timeframe (including Wyckoff Spring/Upthrust detection,
`wyckoff.py`, Phase A5; session classification, `session.py`, Phase
A6; and market regime classification, `market_regime.py`, Phase A7),
plus HTF Bias (`htf_bias.py`, Phase A2) — a separate, higher-timeframe
market-context classification. All stateless, read-only detection
code; none makes a trading decision. `snapshot.py` (Phase A16)
additionally standardizes an already-built `ContextSnapshot` into a
flat, JSON-serializable `ContextSnapshotSchema`, now wired into
`core/pipeline.py`'s `signal_history` stage (Pre-Phase 59 Architecture
Readiness Review, AC-03). `market_phase.py` (AC-02) adds a wired,
advisory `MarketPhase` classification (`ACCUMULATION`/`MANIPULATION`/
`DISTRIBUTION`/`MARKUP`/`MARKDOWN`/`UNKNOWN`) reusing already-detected
Wyckoff/AMD/Market Regime data — no new detection.

## Flow
```
Market Data
      |
      |-- get_candles() (execution timeframe)      -- get_snapshot() (Daily/H4/H1)
      |         |                                             |
      v         |                                             v
Context Engine <-----------------------------------------htf_bias.py
      |  swings, BOS/CHoCH, liquidity, OB, FVG,               |
      |  AMD, Wyckoff (A5), Session (A6),                     |
      |  Market Regime (A7 -- the only detector               |
      |  that also reads htf_bias, passed into                |
      |  build_context_snapshot()) -- all in ContextSnapshot   |
      v                                                        v
Strategies                          TradingPipeline.run()'s result dict
                                     ("htf_bias") -> decision/'s
                                     DecisionEngine.evaluate() (Phase
                                     A3, see docs/HTF_BIAS.md)
```

## Responsibilities
Swing points, BOS/CHoCH, liquidity sweeps, order blocks, fair value
gaps, AMD (Accumulation-Manipulation-Distribution) cycle detection,
Wyckoff Spring/Upthrust detection (`wyckoff.py`, Phase A5), session
classification (`session.py`, Phase A6), and market regime
classification (`market_regime.py`, Phase A7) — all as stateless
functions, all part of `ContextSnapshot`. `htf_bias.py` additionally
classifies Daily/H4/H1 direction using the same swing/structure
functions, independently of `ContextSnapshot` (a different timeframe
than everything else in this package operates on) — `market_regime.py`
is the one exception that reads both `ContextSnapshot`-shaped data
*and* an externally-supplied `HTFBiasResult`, see below.

### Why Wyckoff exists
Phase A1's architecture audit found zero Wyckoff code anywhere —
`amd.py`'s Accumulation-Manipulation-Distribution detector uses
overlapping vocabulary but is a distinct, narrower concept. Phase A5
adds Spring/Upthrust detection (the "test of support/resistance"
events Wyckoff theory is most identified by), correlating already-
detected liquidity sweeps with the nearest subsequent same-direction
structural break — no new sweep or break detection. See
`docs/WYCKOFF.md` for the full detection rule, the "Relationship to
AMD" explanation (why `amd.py` was deliberately not touched or
reused), and the volume-confirmation hook (always `None` — no volume
data source exists in this codebase).

### What Wyckoff does NOT do
- Does not generate a `BUY`/`SELL` signal, and is not itself a
  strategy — no `strategies/*.py` file reads `WyckoffEvent`.
- Does not implement full Wyckoff phase theory (A/B/C/D/E boundaries)
  — only the Spring/Upthrust test events.
- Does not modify `amd.py`, `order_block.py`, or any other existing
  detector.

### Why Session Intelligence exists
GoldBot already knew Structure, Liquidity, Wyckoff phase, and HTF
trend, but nothing described which part of the trading day a candle
belonged to. Phase A6 adds a five-way session classification
(`ASIA`/`LONDON`/`LONDON_NEW_YORK_OVERLAP`/`NEW_YORK`/`OFF_HOURS`, by
UTC hour) plus two real, data-backed statistics per session (average
range, liquidity-sweep count) — not fabricated placeholders. See
`docs/SESSION_INTELLIGENCE.md` for the full session-boundary table and
an explicit account of what was named in the roadmap but deliberately
NOT built ("liquidity probability" needs historical aggregation this
phase doesn't have; "setup quality" per session is
`signals/signal_quality.py`'s job, not wired here).

### What Session Intelligence does NOT do
- Does not generate a `BUY`/`SELL` signal, and is not itself a
  strategy — no `strategies/*.py` file reads `Session`/`SessionEvent`.
- Does not add a `SESSION_ALIGNED` criterion to
  `signals/signal_quality.py` — a distinct, separate, not-yet-done
  future step.
- Does not read, call, or duplicate `data/session_filter.py`'s
  `is_trading_time()` — different purpose (wall-clock trading-hours
  gate vs. per-candle session classification), different time
  convention (Tashkent vs. UTC).
- Does not fabricate "liquidity probability" or cross-window
  statistics — `compute_session_volatility()`/
  `compute_session_liquidity_activity()` report only what the
  provided candle window actually contains.

### Why Market Regime exists
GoldBot already knew *where* price is (Structure), *when* it is
(Session), and *what pattern* just happened (Wyckoff), but nothing
summarized *what character* the market is currently in — a distinct,
higher-level question. Phase A7 adds a 7-way classification
(`TRENDING`/`RANGE`/`ACCUMULATION`/`DISTRIBUTION`/`HIGH_VOLATILITY`/
`LOW_VOLATILITY`/`UNKNOWN`) with a clear priority order (Wyckoff
Spring/Upthrust > confirmed HTF+structure trend > volatility extreme >
default `RANGE` > `UNKNOWN` for no data) — no new indicator. See
`docs/MARKET_REGIME.md` for the full priority table, the exact
confidence values, and why this required a small, backward-compatible
`build_context_snapshot()`/`ContextEngine.build()` signature extension
(the only detector in this package that also needs `HTFBiasResult`,
which lives outside `ContextSnapshot`'s own data).

### What Market Regime does NOT do
- Does not generate a `BUY`/`SELL` signal, and is not itself a
  strategy — no `strategies/*.py` file reads `MarketRegimeResult`.
- Does not switch or route between strategies ("Strategy Router" is
  explicitly out of scope for this phase).
- Does not change `AIAnalyzer`, `DecisionEngine`, or `RiskManager` —
  all three are unmodified.
- Does not persist regime history — no schema change, no new table.

### Why HTF Bias exists
Phase A1's architecture audit found `data/market_data.py`'s
`MarketDataNormalizer.get_snapshot()` — a fully-built multi-timeframe
fetch with per-timeframe data-quality flags — already existed but was
never called by `core/pipeline.py`. Phase A2 wires that connection and
adds the one missing piece: an actual Daily/H4/H1 bias classification,
reusing `market_structure.py`'s existing swing/structure functions
rather than duplicating them. See `docs/HTF_BIAS.md` for the full
architecture and confidence-scoring explanation.

### What HTF Bias does NOT do
- Does not generate a `BUY`/`SELL` signal, and is not itself a
  strategy or a decision.
- Is not a field on `ContextSnapshot`, and is not passed into
  `strategies/`, `signals/`, `ai/`, or `risk/`. As of Phase A3, it
  *is* passed into `decision.decision_engine.DecisionEngine.evaluate()`
  as one weighted input among four (`decision/README.md`'s "Decision
  v2" section) — it still never approves/rejects anything itself, and
  `context/htf_bias.py` was not modified to make this connection (the
  consuming code lives in `decision/`, not here).
- Does not block or alter the execution-timeframe pipeline in any
  way — an HTF fetch/compute failure degrades to `HTFBias.UNKNOWN`
  and is logged, never raised; Decision Engine v2 treats that as a
  neutral contribution, not an error.

### Why Context Snapshot exists
The real `ContextSnapshot` (`context_orchestrator.py`) is exactly
what the live pipeline needs — every strategy and Signal Quality
Score/Explainability/Feature Engineering module already consumes it
directly — but it is not JSON-serializable, versioned, or
identity-bearing in a way a future backtest replay, AI training
export, or Analytics dataset could rely on. Phase A16 adds
`ContextSnapshotSchema` — deliberately not named `ContextSnapshot`,
to avoid a same-name collision with the real type in this same
package; mirrors `signals/schema.py`'s `SignalSchema` naming for the
identical reason. See `docs/CONTEXT_SNAPSHOT.md` for the full field
table, the "critical naming note" explaining the two types' relationship in detail, and two deliberate, disclosed
deviations from the roadmap's own illustrative example (`regime`
using the real 7-value `MarketRegime` vocabulary instead of an
invented 5-value one; `swing_state` reading a single already-classified
label instead of a new combined "last-high + last-low" walk).

### What Context Snapshot does NOT do
- Does not generate a `BUY`/`SELL` signal, call a strategy, or call
  the AI layer.
- Does not modify `market_structure.py`, `liquidity.py`,
  `order_block.py`, `fvg.py`, `context_orchestrator.py`, or any other
  existing detector — `snapshot.py` only reads their already-computed
  output via `from_context_snapshot()`.
- Does not write to the database — no schema change, no new table.
- Was not consumed by `core/pipeline.py`, `strategies/`, `signals/`,
  `ai/`, `decision/`, or `risk/` in Phase A16. **Update (AC-03)**:
  `core/pipeline.py` now calls `from_context_snapshot()` once per
  cycle in its `signal_history` stage, to obtain the `snapshot_id`
  every `SignalSchema` links back to via `context_id` —
  `strategies/`, `ai/`, `decision/`, and `risk/` still never import
  `snapshot.py`.
- Does not raise on an invalid snapshot — `validate_snapshot()`
  returns a structured `ValidationResult`, matching every other Phase
  A foundation module's fail-safe posture.

### Why Market Phase exists (AC-02)
A Pre-Phase 59 Architecture Readiness Review found `wyckoff.py`'s own
2-state `WyckoffPhase` (`ACCUMULATION`/`DISTRIBUTION`) didn't cover the
5-state Wyckoff/AMD cycle (`ACCUMULATION`/`MANIPULATION`/
`DISTRIBUTION`/`MARKUP`/`MARKDOWN`) a signal explanation would ideally
reference. `market_phase.py` adds `compute_market_phase(context)`,
classifying by priority order (most recent Wyckoff Spring/Upthrust >
most recent AMD event > confirmed `TRENDING` `MarketRegime` direction >
`UNKNOWN`) — the same priority-order pattern `market_regime.py`
already established. No new detection: reads only
`context.wyckoff_events`, `context.amd_events`, and
`context.market_regime`, all pre-existing `ContextSnapshot` fields.

### What Market Phase does NOT do
- Does not generate a `BUY`/`SELL` signal, and is not itself a
  strategy — no `strategies/*.py` file reads `MarketPhaseResult`.
- Does not add a new field to `ContextSnapshot` — all three inputs
  already existed.
- Is not consumed by `signals/`, `ai/`, `decision/`, or `risk/` — the
  new `core/pipeline.py` `market_phase` stage only logs it and returns
  it in `run()`'s result dict (`"market_phase"`), advisory only.

## Input
`Sequence[Candle]` (from `data/`) for the execution-timeframe
detectors. `htf_bias.py`'s `compute_htf_bias()` takes a
`data.market_data.MarketSnapshot` (from `get_snapshot()`) instead.
`market_regime.py`'s `compute_market_regime()` additionally takes an
optional `HTFBiasResult` (defaults to `None`). `snapshot.py`'s
`from_context_snapshot()` takes an already-built `ContextSnapshot`
(required) plus optional `symbol`/`timeframe`/`engine_version`
overrides. `market_phase.py`'s `compute_market_phase()` takes an
already-built `ContextSnapshot` (required) only.

## Output
`ContextSnapshot` (`context_orchestrator.py`) — an immutable, fully
resolved snapshot of every detector's output for one candle series,
12 fields as of Phase A7 (`wyckoff_events` added in A5,
`session_events` added in A6, `market_regime` added in A7; every
pre-existing field's name and meaning is unchanged).
`market_regime: MarketRegimeResult` is the one field that is a single
result object rather than a `Sequence[...]` — a regime is a state of
the whole window, not a sparse event list. `htf_bias.py`'s
`compute_htf_bias()` returns a separate `HTFBiasResult` (`bias`,
`confidence`, `timeframes`, `quality_score`) — not part of
`ContextSnapshot`, since it operates on different timeframes than
everything else in this package. `snapshot.py`'s
`from_context_snapshot()` returns a `ContextSnapshotSchema` — flat,
JSON-serializable (`to_dict()`/`to_json()`), immutable.
`market_phase.py`'s `compute_market_phase()` returns a
`MarketPhaseResult` (`phase`, `reason`) — immutable, not part of
`ContextSnapshot`.

## Dependencies
`data/` (for the `Candle`/`MarketSnapshot` types) only. No dependency
on `strategies/`, `signals/`, `ai/`, `database/`, or `telegram/` —
`htf_bias.py` and `market_regime.py` both follow the same isolation as
every other file in this package (`market_regime.py`'s
`HTFBiasResult` parameter is `TYPE_CHECKING`-only; `HTFBias` the enum
is a real runtime import, used for equality comparison). `snapshot.py`
imports only the standard library plus `context.context_orchestrator`
and `context.market_structure` (same package) — deliberately does
**not** import `signals/` (see `docs/CONTEXT_SNAPSHOT.md`'s "Why not
import from signals/" section for why its `ValidationResult` is a
separate, independent definition, not shared code). `market_phase.py`
imports `context.amd`, `context.market_regime`, and `context.wyckoff`
(same package) plus, `TYPE_CHECKING`-only, `context.context_orchestrator`
— no dependency on `strategies/`, `signals/`, `ai/`, `database/`, or
`telegram/`.

## Future Roadmap
The execution-timeframe SMC formulas remain stable and explicitly out
of scope for casual change (see `CLAUDE.md`'s Trading Safety rules).
For HTF Bias specifically, see `docs/HTF_BIAS.md`'s Future Expansion
section — Decision Engine v2 consumption is done (Phase A3); optional
persistence and per-timeframe weighting remain unimplemented. For
Wyckoff specifically, see `docs/WYCKOFF.md`'s Future Expansion
section — a `strategies/wyckoff_strategy.py`, real volume confirmation
(once a volume data source exists), and a shared sweep-then-break
helper (a minor, known duplication across `order_block.py`, `amd.py`,
and `wyckoff.py`, deliberately not refactored in this foundation-only
phase) all remain unimplemented. For Session Intelligence
specifically, see `docs/SESSION_INTELLIGENCE.md`'s Future Expansion
section — a `SESSION_ALIGNED` Signal Quality Score criterion,
historical liquidity-probability aggregation, and DST-aware session
boundaries all remain unimplemented. For Market Regime specifically,
see `docs/MARKET_REGIME.md`'s Future Usage section — a Strategy Router
and a Signal Quality Score / Decision Engine v3 input both remain
unimplemented. For Context Snapshot specifically, see
`docs/CONTEXT_SNAPSHOT.md`'s "Future usage" section — AI (`Signal +
ContextSnapshotSchema = Explanation`, joinable via `SignalSchema`'s
`context_id` once a future phase wires the two together), Analytics,
Replay, and Education all remain unimplemented. For Market Phase
specifically, see `docs/ARCHITECTURE_READINESS_REVIEW.md`'s AC-02
section — full Wyckoff phase theory boundaries (A/B/C/D/E) and any
future consumer beyond logging remain unimplemented.
