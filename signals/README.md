# signals/

## Purpose
Defines the signal candidate data contract, routes context to
strategies for candidate generation, and (Phase A4) grades each
candidate's context alignment into a letter-grade Signal Quality
Score.

## Flow
```
Strategies
      |
      v
Signal Engine   -- aggregates candidates
      |     |
      |     '-- signal_quality.py (Phase A4, per candidate)
      v          grades HTF/Structure/Liquidity/OB/FVG alignment
AI Layer          -> A+/A/B/C, advisory only (see below)
```

## Responsibilities
- `models.py` — `SignalCandidate`, the immutable contract every
  strategy produces and every downstream layer (AI/Decision/Risk/
  Telegram) consumes.
- `signal_engine.py` — thin router to `strategies.StrategyManager`.
- `signal_quality.py` (Phase A4) — `compute_signal_quality()`, a
  read-only, advisory grading function. Does **not** change how
  candidates are generated or aggregated — `signal_engine.py` and
  every `strategies/*.py` file are untouched by this addition.

### Why Signal Quality Score exists
Decision Engine v2 (Phase A3) answers "how strong is this signal?" (a
weighted confidence blend); nothing answered "how clean is this
signal's setup?" — a checklist-style grade over the same SMC context
already detected upstream (Structure, Liquidity, Order Blocks, FVG)
plus HTF Bias (Phase A2). See `docs/SIGNAL_QUALITY.md` for the full
grading table and criteria definitions.

### What Signal Quality Score does NOT do
- Does not generate a `BUY`/`SELL` signal and is not itself a
  strategy.
- Is not consumed by `ai/`, `decision/`, or `risk/` in this phase —
  it travels only as far as `TradingPipeline.run()`'s result dict
  (`"quality_results"`). A future, separately-approved phase (e.g.
  Decision Engine v3) is where a real consumer would be added — the
  same pattern HTF Bias followed between Phase A2 and Phase A3.
- Does not block, filter, or reorder candidates — a `C`-graded
  candidate still reaches AI/Decision/Risk exactly as before this
  phase.
- Does not include a Session or Volume criterion. Session Intelligence
  now exists (`context/session.py`, Phase A6) but wiring a
  `SESSION_ALIGNED` criterion here is a distinct, not-yet-done future
  step; Volume still has no data source anywhere in `data/`. Both
  remain named, explicit future-extension points in
  `docs/SIGNAL_QUALITY.md`, not faked.

## Input
`ContextSnapshot` (from `context/`) for `signal_engine.py`.
`compute_signal_quality()` additionally takes the `SignalCandidate`
being graded and an optional `HTFBiasResult` (from `context/htf_bias.py`).

## Output
`List[SignalCandidate]` from `signal_engine.py`, unchanged.
`SignalQualityResult` (`grade`, `score`, `criteria_met`,
`criteria_total`) from `compute_signal_quality()` — one per candidate.

## Dependencies
`context/` and `strategies/`, unchanged. `signal_quality.py`
additionally imports `context.htf_bias` (for `HTFBias`) and
`context.market_structure`/`context.liquidity`/`context.order_block`/
`context.fvg` (for their result types and the shared
`most_recent_bias()` helper) — all still within `context/`, no new
package dependency. No dependency on `ai/`, `decision/`, `risk/`,
`database/`, or `telegram/`.

## Future Roadmap
Candidate filtering/ranking (single-best-candidate selection)
intentionally lives in `core/pipeline.py`, not here — see
`docs/AUDIT_REPORT.md` for why. For Signal Quality Score specifically,
see `docs/SIGNAL_QUALITY.md`'s Future Expansion section (Session/
Volume criteria once their data sources exist, Decision Engine v3
consumption, optional persistence — none implemented in this phase).
