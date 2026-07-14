# Feature Engineering Foundation (Phase A10)

## Purpose

Builds one standard `MarketFeatures` snapshot per pipeline cycle —
`atr`, `volatility`, `trend_strength`, `session`, `regime`,
`htf_bias`, `liquidity_distance`, `volume` — entirely from data
already computed elsewhere in the pipeline. **This is a data-shaping
layer, not a new analysis.** No new indicator, no ML model, no
strategy logic, no signal-scoring change.

This phase exists because a future AI Analyzer, backtester, or ML
dataset exporter each need the same underlying market context, but
without a standard shape, each would independently re-derive its own
subset from raw `ContextSnapshot` fields — the same "everyone re-reads
raw candles" problem HTF Bias (Phase A2) and Signal Quality Score
(Phase A4) already solved for their own narrower questions.
`MarketFeatures` is the flat, documented, single answer to "what does
the market look like right now," reusable by all three future
consumers without any of them touching `context/` directly.

## Model

```python
@dataclass(frozen=True)
class MarketFeatures:
    atr: Optional[float]
    volatility: str              # "HIGH"/"LOW"/"NORMAL"/"UNKNOWN"
    trend_strength: float        # 0.0-1.0
    session: str                 # e.g. "LONDON"
    regime: str                  # e.g. "TRENDING"
    htf_bias: str                # e.g. "BULLISH"
    liquidity_distance: Optional[float]
    volume: Optional[float] = None
```

## How each field is computed (all reused, none re-derived)

| Field | Source | Notes |
|---|---|---|
| `atr` | `context.session.compute_session_volatility()` (Phase A6), current session only | **Not a textbook Wilder ATR** — see "Why `atr` isn't a real ATR" below. `None` if no candles. |
| `volatility` | `context.market_regime.MarketRegimeResult.regime` (Phase A7) | Direct read: `HIGH_VOLATILITY`→`"HIGH"`, `LOW_VOLATILITY`→`"LOW"`, `UNKNOWN`→`"UNKNOWN"`, anything else→`"NORMAL"`. No new volatility calculation. |
| `trend_strength` | `context.market_regime.MarketRegimeResult.confidence` (Phase A7) | `confidence / 100.0` when `regime == TRENDING`, else `0.0`. The exact same HTF+structure-agreement signal Market Regime already computed — not a new trend calculation. |
| `session` | `context.session_events[-1].session` (Phase A6) | The most recent session transition's session. `"UNKNOWN"` if no session data. |
| `regime` | `context.market_regime.MarketRegimeResult.regime` (Phase A7) | Direct `.value` read. |
| `htf_bias` | `HTFBiasResult.bias` (Phase A2, passed in externally, same pattern as Decision Engine v2/Market Regime) | `"UNKNOWN"` if no `HTFBiasResult` was supplied. |
| `liquidity_distance` | `context.liquidity_zones` (unchanged) | Absolute distance from the most recent candle's close to the nearest zone's price. `None` if no candles or no zones. |
| `volume` | — | Always `None` — see "Volume hook" below. |

### Why `atr` isn't a real ATR

A textbook Average True Range uses `max(high-low, |high-prev_close|,
|low-prev_close|)` averaged (typically Wilder-smoothed) over a fixed
period (conventionally 14). This phase does not implement that
formula — it reuses `context.session.compute_session_volatility()`'s
already-computed "average `(high-low)` range for the current session,"
the exact same real, honest statistic Market Regime's own
`HIGH_VOLATILITY`/`LOW_VOLATILITY` check already relies on. Calling
this field `atr` follows the roadmap's own naming, but this document
states plainly what it actually is: a real, computed range proxy, not
a specific named indicator formula. A future phase implementing a real
Wilder ATR would be a genuinely new indicator, out of this
foundation-only phase's scope.

### Volume hook

`volume` is always `None`. This codebase has no volume data source at
all — `data/twelve_data_client.py`'s `Candle` is OHLC-only, confirmed
repeatedly since Phase A1's architecture audit. Per this phase's
explicit instruction ("Fake qiymat berilmaydi" — no fake value is
given), `volume` is an honest, named hook, never a fabricated number.
Wiring in a real volume source is a future, separately-approved phase;
only `feature_engine.py`'s `volume=None` line would need to change.

## Pipeline position

```
Context Engine
      |
      v
Feature Engineering (features/feature_engine.py, Phase A10)
      |         compute_market_features(context, htf_bias)
      |         -> MarketFeatures, one per cycle (not per-candidate)
      v
Strategy Engine   -- unchanged; does not read MarketFeatures
```

One new `core/pipeline.py` stage, immediately after `context` (before
`signal`). `MarketFeatures` is computed once per cycle — unlike Signal
Quality Score or Explainability (one result per candidate), Feature
Engineering describes the overall market context at this point in
time, matching HTF Bias's and Market Regime's own once-per-cycle
shape. `TradingPipeline.run()`'s result dict gains one new key,
`"features"`.

## What this does NOT do

- Does not train, run, or reference any ML model.
- Does not change `strategies/*.py`, `signals/signal_engine.py`,
  `signals/signal_quality.py`'s scoring, `ai/`, or
  `decision/decision_engine.py` — none read `MarketFeatures` in this
  phase.
- Does not fabricate a volume value.
- Does not persist `MarketFeatures` anywhere — no schema change, no
  new table.
- Does not implement backtesting or a research harness — `features/`
  only produces the standard shape a future one would consume.

## Significance for AI

`ai/ai_analyzer.py`'s `AIAnalyzer.analyze()` is still a permanent-
reject heuristic stub (`docs/AI_ARCHITECTURE.md`). `MarketFeatures` is
exactly the flat, numeric/categorical shape a future real AI
provider's prompt or feature vector would want — a single object
instead of re-deriving trend/volatility/session/regime from raw
`ContextSnapshot` on every call. It is already sitting in `run()`'s
result dict, alongside `context.market_regime`
(`docs/MARKET_REGIME.md`) and `SignalExplanation`
(`docs/EXPLAINABILITY.md`) — the same "available, not yet consumed"
posture all three foundation layers share.

## Future ML usage

- **Backtesting**: `compute_market_features()` is a pure function over
  a `ContextSnapshot` — a future backtest harness could replay
  historical candles through the existing `context/` detectors and
  call this function identically to how `core/pipeline.py` does live,
  producing a consistent feature history without new code here.
- **ML dataset export**: `MarketFeatures`'s flat, dataclass shape
  (verified stable via `dataclasses.fields()` in
  `tests/features/test_feature_engine.py`) is directly serializable
  (e.g. to a CSV/Parquet row) for a future training dataset — not
  implemented in this phase.
- **A real ATR / real volume**: both named above as the two
  deliberate simplifications this phase carries forward, each with an
  explicit, minimal path to becoming real once the underlying data
  source or scope decision exists.
