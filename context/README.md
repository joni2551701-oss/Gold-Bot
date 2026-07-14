# context/

## Purpose
Pure Smart Money Concepts (SMC) market-structure detection for the
execution timeframe (including Wyckoff Spring/Upthrust detection,
`wyckoff.py`, Phase A5, and session classification, `session.py`,
Phase A6), plus HTF Bias (`htf_bias.py`, Phase A2) — a separate,
higher-timeframe market-context classification. All stateless,
read-only detection code; none makes a trading decision.

## Flow
```
Market Data
      |
      |-- get_candles() (execution timeframe)      -- get_snapshot() (Daily/H4/H1)
      |         |                                             |
      v         |                                             v
Context Engine <-'                                       htf_bias.py
      |  swings, BOS/CHoCH, liquidity, OB, FVG,               |
      |  AMD, Wyckoff (A5), Session (A6, in ContextSnapshot)   |
      v                                                        v
Strategies                          TradingPipeline.run()'s result dict
                                     ("htf_bias") -> decision/'s
                                     DecisionEngine.evaluate() (Phase
                                     A3, see docs/HTF_BIAS.md)
```

## Responsibilities
Swing points, BOS/CHoCH, liquidity sweeps, order blocks, fair value
gaps, AMD (Accumulation-Manipulation-Distribution) cycle detection,
Wyckoff Spring/Upthrust detection (`wyckoff.py`, Phase A5), and
session classification (`session.py`, Phase A6) — all as stateless
functions over a candle sequence, all part of `ContextSnapshot`.
`htf_bias.py` additionally classifies Daily/H4/H1 direction using the
same swing/structure functions, independently of `ContextSnapshot` (a
different timeframe than everything else in this package operates
on).

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

## Input
`Sequence[Candle]` (from `data/`) for the execution-timeframe
detectors. `htf_bias.py`'s `compute_htf_bias()` takes a
`data.market_data.MarketSnapshot` (from `get_snapshot()`) instead.

## Output
`ContextSnapshot` (`context_orchestrator.py`) — an immutable, fully
resolved snapshot of every detector's output for one candle series,
11 fields as of Phase A6 (`wyckoff_events` added in A5,
`session_events` added in A6; every pre-existing field's name and
meaning is unchanged). `htf_bias.py`'s
`compute_htf_bias()` returns a separate `HTFBiasResult` (`bias`,
`confidence`, `timeframes`, `quality_score`) — not part of
`ContextSnapshot`, since it operates on different timeframes than
everything else in this package.

## Dependencies
`data/` (for the `Candle`/`MarketSnapshot` types) only. No dependency
on `strategies/`, `signals/`, `ai/`, `database/`, or `telegram/` —
`htf_bias.py` follows the same isolation as every other file in this
package.

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
boundaries all remain unimplemented.
