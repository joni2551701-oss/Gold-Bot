# Signal Quality Score (Phase A4)

## Purpose

Grades how well a `SignalCandidate` aligns with existing SMC context
— HTF Bias, Structure, Liquidity, Order Blocks, Fair Value Gaps —
into a letter grade (`A+`/`A`/`B`/`C`). **Signal Quality Score is
context alignment, not a decision.** It never generates a signal,
never approves/rejects a trade, and (in this phase) is not consumed
by `AIAnalyzer`, `DecisionEngine`, or `RiskManager` — it produces one
`SignalQualityResult` per signal candidate per pipeline cycle that
currently goes nowhere except `TradingPipeline.run()`'s result dict,
for a later, separately-approved phase to consume — the same posture
HTF Bias (Phase A2) had before Decision Engine v2 (Phase A3) connected
it.

This phase exists because Decision Engine v2 (Phase A3) answers "how
strong is this signal?" (a weighted confidence blend) but nothing
answered "how clean is this signal's setup?" — a distinct question a
strength score alone doesn't capture (a high-confidence signal can
still be a mediocre setup with no liquidity sweep, no order block, no
FVG reaction behind it).

## Architecture

```
Signal Candidates (signals/signal_engine.py, unchanged)
      |
      v
signals/signal_quality.py
      |  compute_signal_quality(signal, context, htf_bias) -> SignalQualityResult
      v
TradingPipeline.run()'s result dict ("quality_results", Phase A4)
      |
      v
(nothing consumes it yet -- a future, separately-approved phase
 is where a real consumer, e.g. Decision Engine v3, would be added)
```

Computed once per signal candidate, independent of the AI/Decision/
Risk stages — it needs only the candidate itself, the already-built
`ContextSnapshot`, and the already-computed `HTFBiasResult` (Phase
A2), all of which exist in `core/pipeline.py`'s `run()` before this
stage runs. A failure or missing input degrades gracefully (an unmet
criterion, never an exception) — see "What this does NOT do" below.

**Reuse, not duplication** (per `CLAUDE.md`'s "No duplicate logic"
rule):
- `context.market_structure.most_recent_bias()` — extracted in this
  phase from `context_layer/trend/htf_bias.py`'s per-timeframe classification
  (which had this exact walk-backward-through-structure logic
  inline). Both `htf_bias.py` and `signal_quality.py` now call the
  same, single definition; `context_layer/trend/htf_bias.py`'s own 9 tests were
  re-run after the extraction and confirmed byte-for-byte unchanged
  behavior.
- `ContextSnapshot.structure`/`.liquidity_sweeps`/`.order_blocks`/
  `.fair_value_gaps` — already computed by `context_orchestrator.py`
  for every pipeline cycle; no new detection logic was added anywhere
  in `context/`.
- `HTFBiasResult` (Phase A2) — already computed every cycle; not
  recomputed here.

No detector was rewritten or copied to produce this feature.

## Inputs

`compute_signal_quality(signal, context, htf_bias=None)`:
- `signal: SignalCandidate` (from `signals/models.py`) — needs
  `signal_type` (BUY/SELL/NONE) and `entry` (price).
- `context: ContextSnapshot` (from `context/`) — reads `.structure`,
  `.liquidity_sweeps`, `.order_blocks`, `.fair_value_gaps`.
- `htf_bias: Optional[HTFBiasResult]` (from `context_layer/trend/htf_bias.py`,
  Phase A2) — defaults to `None` (treated as "not aligned," never an
  error).

## Outputs

`SignalQualityResult` (immutable dataclass):

| Field | Type | Meaning |
|---|---|---|
| `grade` | `QualityGrade` enum | `A+` / `A` / `B` / `C` — see "Grading" below. |
| `score` | `float`, 0–100 | `criteria_met_count / criteria_total * 100`. |
| `criteria_met` | `Sequence[str]` | Names of the criteria that passed (e.g. `("HTF_ALIGNED", "LIQUIDITY_SWEPT")`) — explainability, not used by the grading itself. |
| `criteria_total` | `int` | Always `5` today — see "Supported criteria" below. Exposed explicitly (not hardcoded `5` in a caller) so a future phase adding a real criterion doesn't silently change what "100%" means without every caller noticing the total moved. |

## Grading

Each of the 5 supported criteria is a boolean (met/not met) — this is
a **checklist model**, not a weighted average like Decision Engine
v2's, matching the roadmap's own worked example ("H4 trend aligned +
Liquidity sweep + FVG reaction + ... = A+"):

| Criteria met | Score | Grade |
|---|---|---|
| 5 or 4 of 5 | 100 or 80 | `A+` |
| 3 of 5 | 60 | `A` |
| 2 of 5 | 40 | `B` |
| 0 or 1 of 5 | 0 or 20 | `C` |

## Supported criteria

All 5 are direction-specific — a BUY and a SELL candidate check for
opposite conditions:

| Criterion | Met when (BUY) | Met when (SELL) |
|---|---|---|
| `HTF_ALIGNED` | `htf_bias.bias == BULLISH` | `htf_bias.bias == BEARISH` |
| `STRUCTURE_ALIGNED` | Most recent confirmed structure point is HH/HL | Most recent confirmed point is LH/LL |
| `LIQUIDITY_SWEPT` | A sell-side liquidity (`SSL`) sweep exists in context | A buy-side liquidity (`BSL`) sweep exists in context |
| `ORDER_BLOCK_ALIGNED` | `signal.entry` falls inside a `BULLISH` Order Block's `[low, high]` zone | `signal.entry` falls inside a `BEARISH` Order Block's zone |
| `FVG_ALIGNED` | `signal.entry` falls inside a `BULLISH` Fair Value Gap's `[bottom, top]` zone | `signal.entry` falls inside a `BEARISH` FVG's zone |

A `signal_type` of `NONE` (or a missing `htf_bias`, or an empty
`context`) fails every criterion it touches — never raises, never
crashes the pipeline.

### Deliberately not included: Session and Volume

The Phase A4 roadmap sketch named **Session** and **Volume** as two
additional inputs. Neither is included in this phase, by explicit
Director decision when this ambiguity was raised before implementation:

- **Session**: at the time of Phase A4, no session classification
  existed anywhere in this codebase (only `data_layer/live_data/session_filter.py`'s
  binary trading-hours gate, not a session classifier). **Phase A6
  built `context_layer/session/session.py`'s `classify_session()`/`Session` enum**,
  so a real session criterion is now buildable — but wiring it into
  this module's `_CRITERIA` tuple was not part of Phase A6's scope
  either (that phase built Session Intelligence standalone, the same
  "compute now, connect later" posture HTF Bias had between Phase A2
  and Phase A3). `criteria_total` is still `5` as of Phase A6; adding
  `SESSION_ALIGNED` remains a distinct, not-yet-done future step (see
  below), now unblocked rather than blocked on missing data.
- **Volume**: this codebase still has **no volume data source at
  all** — `data_layer/providers/twelve_data_client.py`'s `Candle` dataclass is
  OHLC-only; Twelve Data's response is never asked for volume.
  Unchanged since Phase A4.

Neither was faked with a placeholder/neutral score when this module
was built — `criteria_total` stayed `5` until a real criterion exists
to add, and still does.

## What this does NOT do

- Does not generate a `BUY`/`SELL` signal, and is not itself a
  strategy — `signals/signal_engine.py` and every `strategies/*.py`
  file are unchanged.
- Does not approve, reject, or size a trade.
- Is not consumed by `AIAnalyzer`, `DecisionEngine`, or `RiskManager`
  in this phase — it travels only as far as `TradingPipeline.run()`'s
  result dict (`"quality_results"`). A future, separately-approved
  phase is where a real consumer would be added — the same pattern
  Phase A2's HTF Bias followed before Phase A3 connected it.
- Does not change `SignalCandidate`, `ContextSnapshot`,
  `AIAnalysisResult`, `TradeDecision`, or `RiskResult`'s fields, or
  any existing function signature.
- Does not write to the database — no schema change, no new table, no
  persistence of `SignalQualityResult` anywhere.
- Does not block, delay-gate, or filter the existing pipeline in any
  way — a candidate with grade `C` is still passed to
  `AIAnalyzer`/`DecisionEngine`/`RiskManager` exactly as before this
  phase; grading is purely observational.

## Future expansion

- **Session criterion**: Session Intelligence exists as of Phase A6
  (`context_layer/session/session.py`) — add a `SESSION_ALIGNED` entry to
  `signals/signal_quality.py`'s `_CRITERIA` tuple (the single place a
  new criterion needs to be registered) and bump `criteria_total`
  accordingly. Still not done — a distinct future step, not implied by
  Session Intelligence existing.
- **Volume criterion**: same mechanism, once a volume data source
  exists in `data/`.
- **Decision Engine v3**: a future, separately-approved phase could
  add `SignalQualityResult` as a fifth weighted input to
  `DecisionEngine.evaluate()`, following the exact pattern Phase A3
  used for HTF Bias (see `decision/README.md`).
- **Persistence**: if quality-grade history becomes valuable for
  analytics, persisting `SignalQualityResult` alongside a
  `SignalRecord` is a natural, separate schema-change proposal — not
  part of this phase.
