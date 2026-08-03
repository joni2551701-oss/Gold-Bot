# Market Regime Engine Foundation (Phase A7)

## Purpose

Classifies overall market character — `TRENDING` / `RANGE` /
`ACCUMULATION` / `DISTRIBUTION` / `HIGH_VOLATILITY` /
`LOW_VOLATILITY` / `UNKNOWN` — from data already computed elsewhere in
the Context Engine plus HTF Bias. **Market Regime is context, not a
decision.** It does not switch strategies, does not generate a signal,
and is not consumed by any strategy, `AIAnalyzer`, `DecisionEngine`,
or `RiskManager` in this phase.

This phase exists because GoldBot already knew *where* price is
(Structure), *when* it is (Session), and *what pattern* just happened
(Wyckoff) — but nothing summarized *what character* the market is
currently in. That's a distinct, higher-level question the individual
detectors don't answer on their own.

## Model

```python
class MarketRegime(Enum):
    TRENDING = "TRENDING"
    RANGE = "RANGE"
    ACCUMULATION = "ACCUMULATION"
    DISTRIBUTION = "DISTRIBUTION"
    HIGH_VOLATILITY = "HIGH_VOLATILITY"
    LOW_VOLATILITY = "LOW_VOLATILITY"
    UNKNOWN = "UNKNOWN"

class RegimeDirection(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"

@dataclass(frozen=True)
class MarketRegimeResult:
    regime: MarketRegime
    direction: RegimeDirection
    confidence: float   # 0-100
    reasons: Sequence[str]
```

Example output (matching the brief's own worked example, verified by
`tests/context/test_market_regime.py::test_bullish_trend_confirmed_by_htf`):

```json
{
  "regime": "TRENDING",
  "direction": "BULLISH",
  "confidence": 85.0,
  "reasons": ["HTF bullish bias", "HH/HL structure"]
}
```

`confidence` is 0-100, matching `HTFBiasResult.confidence`'s
convention — **not** `DecisionEngine`'s 0.0-1.0 scale, since
`MarketRegimeResult` is never blended into that formula in this
phase.

## Logic

No new indicator was introduced — every signal `compute_market_regime()`
reads is already detected elsewhere:

| Input | Source |
|---|---|
| Execution-timeframe structure direction | `context.market_structure.most_recent_bias()` (the same shared helper HTF Bias and Signal Quality Score already use) |
| Higher-timeframe direction | `context.htf_bias.HTFBiasResult` (Phase A2) — passed in externally, see "Architecture" below |
| Accumulation/Distribution phase evidence | `context.wyckoff.WyckoffEvent` (Phase A5) |
| Volatility comparison | `context.session.compute_session_volatility()` (Phase A6) |

**Priority order** (regime is a single label, not a combination —
when more than one signal could apply, the most specific wins):

1. **A recent Wyckoff Spring/Upthrust** → `ACCUMULATION`/`DISTRIBUTION`.
   The most concrete, highest-information signal available.
2. **Execution-timeframe structure + HTF Bias**:
   - Both agree (structure `BULLISH`/`BEARISH`, HTF Bias the same) →
     `TRENDING`, confidence `85.0`.
   - Structure has a clear bias but HTF Bias is unavailable
     (`None`) or `NEUTRAL`/`UNKNOWN` → `TRENDING` anyway, confidence
     `55.0` (lower — no higher-timeframe confirmation).
   - Structure and HTF Bias actively **disagree** (e.g. structure
     `BULLISH`, HTF Bias `BEARISH`) → `RANGE`, not `TRENDING` — a
     confident trend label isn't justified when the two best
     directional signals contradict each other.
3. **Volatility extremes**: the current session's average range
   (`compute_session_volatility()`) compared against the whole
   window's average range. `>= 1.5x` → `HIGH_VOLATILITY`; `<= 0.5x` →
   `LOW_VOLATILITY`. Both real ratios of real, already-computed data —
   not a historical or cross-window claim, only "unusual for *this*
   window."
4. **`RANGE`** (confidence `50.0`): data exists but none of the above
   triggered — the default non-trending, non-extreme state.
5. **`UNKNOWN`** (confidence `0.0`): no candle data at all. Reserved
   for genuinely missing/insufficient input, not a low-confidence
   guess.

This ordering is a foundation-phase judgment call, not a claim that
(e.g.) a trending market can never simultaneously be highly volatile —
a future phase could combine signals into a richer, multi-dimensional
result if that becomes valuable; this phase deliberately keeps the
output to one clear label per cycle.

## Architecture

Unlike Wyckoff and Session (Phase A5/A6), which compute purely from
`candles`, Market Regime needs `HTFBiasResult` — computed *outside*
`ContextEngine.build()` (a separate multi-timeframe fetch). Since
`core/pipeline.py` already computes `htf_bias` *before* building
`context` (`market_data → htf_bias → context → ...`), the fix was a
minimal, backward-compatible signature extension:

```python
def build_context_snapshot(candles, htf_bias=None) -> ContextSnapshot: ...
def ContextEngine.build(self, candles, htf_bias=None) -> ContextSnapshot: ...
```

`htf_bias` defaults to `None` — every pre-Phase-A7 caller (both real
production code before this phase, and every existing test) keeps
working unchanged; only `core/pipeline.py`'s one call site was updated
to pass the `htf_bias` it already had computed. `market_regime`
becomes the 12th `ContextSnapshot` field (8th `ContextEngine.build()`
stage) — the only field on `ContextSnapshot` that is a single result
object rather than a `Sequence[...]`, since a regime is a state of the
whole window, not a sparse list of events (matching
`context.htf_bias.HTFBiasResult`'s own single-aggregate-result shape,
not Wyckoff/Session's event-list shape).

## What this does NOT do

- Does not generate a `BUY`/`SELL` signal and is not itself a
  strategy — no `strategies/*.py` file reads `MarketRegimeResult`.
- Does not switch, select, or route between strategies — "Strategy
  Router" is explicitly out of scope for this phase.
- Does not change `AIAnalyzer`, `DecisionEngine`, or `RiskManager` —
  all three are completely unmodified.
- Does not add a backtest, historical regime tracking, or any
  persistence — no database schema change, no new table.
- Does not block, delay-gate, or filter the pipeline in any way.

## Future usage

- **A Strategy Router** (a future, separately-approved phase) could
  use `context.market_regime.regime` to weight or select which
  strategy's candidates are trusted more — e.g. trend-following setups
  (BOS + FVG continuation) in `TRENDING`, mean-reversion/liquidity-
  sweep setups in `RANGE`. Not implemented here.
- **Signal Quality Score / Decision Engine v3**: `MarketRegimeResult`
  is a natural fifth or sixth weighted input alongside HTF Bias and
  Session, following the exact extension pattern
  `docs/SIGNAL_QUALITY.md` and `decision/README.md` already document.

## Significance for AI

`ai_layer/ai_engine/ai_analyzer.py`'s `AIAnalyzer.analyze()` is still a permanent-
reject heuristic stub (`docs/AI_ARCHITECTURE.md`) — this phase does
not connect Market Regime to it. But regime context is exactly the
kind of structured, human-readable signal a future real AI provider
would benefit from having available without re-deriving it from raw
candles on every call: "the market is currently TRENDING BULLISH with
85% confidence because HTF bias and execution-timeframe structure
agree" is a far more useful prompt input than a bare OHLC series. When
`ai_layer/ai_service/interfaces.py`'s `AIAnalyzerInterface` gains a real implementation
(v0.4 AI Assistant Core, per `docs/v0.3_RELEASE_NOTES.md`'s Known
Limitations), `ContextSnapshot.market_regime` is already sitting in
the same `ContextSnapshot` object `AIAnalyzer.analyze()` already
receives — no new plumbing needed to make it available, only a
decision (out of this phase's scope) to actually read it.
