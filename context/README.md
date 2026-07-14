# context/

## Purpose
Pure Smart Money Concepts (SMC) market-structure detection for the
execution timeframe, plus HTF Bias (`htf_bias.py`, Phase A2) — a
separate, higher-timeframe market-context classification. Both are
stateless, read-only detection code; neither makes a trading decision.

## Flow
```
Market Data
      |
      |-- get_candles() (execution timeframe)      -- get_snapshot() (Daily/H4/H1)
      |         |                                             |
      v         |                                             v
Context Engine <-'                                       htf_bias.py
      |  swings, BOS/CHoCH, liquidity, OB, FVG, AMD            |
      v                                                        v
Strategies                          TradingPipeline.run()'s result dict
                                     ("htf_bias") -> decision/'s
                                     DecisionEngine.evaluate() (Phase
                                     A3, see docs/HTF_BIAS.md)
```

## Responsibilities
Swing points, BOS/CHoCH, liquidity sweeps, order blocks, fair value
gaps, and AMD (Accumulation-Manipulation-Distribution) cycle
detection — all as stateless functions over a candle sequence.
`htf_bias.py` additionally classifies Daily/H4/H1 direction using the
same swing/structure functions, independently of `ContextSnapshot`.

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
resolved snapshot of every detector's output for one candle series.
`htf_bias.py`'s `compute_htf_bias()` returns a separate
`HTFBiasResult` (`bias`, `confidence`, `timeframes`, `quality_score`)
— not part of `ContextSnapshot`.

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
persistence and per-timeframe weighting remain unimplemented.
