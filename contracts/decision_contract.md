# Decision Engine

## Responsibility
Blends every already-computed score into one final verdict. The only
place a `TradeDecision` is produced. Never generates a new signal and
never re-analyzes the market itself — see
`docs/DECISION_PRINCIPLES.md`'s "Why this matters" section for the
"whose read wins" framing this whole document follows.

## Input
`signals.models.SignalCandidate`, `ai.ai_analyzer.AIAnalysisResult`,
and an optional `context.htf_bias.HTFBiasResult`
(`decision.decision_engine.DecisionEngine.evaluate(signal, ai_analysis, htf_bias=None)`).

**A deliberate correction to the brief's own example**: the brief
lists Decision Engine's input as "Signal, AI Analysis, Risk
Assessment." That is not the real pipeline order — Risk Manager runs
*after* Decision Engine (see `core/pipeline.py`'s stage order and
`docs/ARCHITECTURE.md`'s Decision Engine v2 section: "`risk.risk_manager.RiskResult`
is **not** one of the four inputs — Risk Manager runs after Decision
Engine in the pipeline and cannot supply an input to a decision that
precedes it"). This document states the real input set; the "Risk"
component `DecisionWeights` blends is `AIAnalysisResult.risk_score`
(already computed by the AI layer before Decision Engine runs),
inverted so higher always means better — not a `RiskResult`.

## Output
`decision.models.TradeDecision` — `action` (`DecisionAction.APPROVE`/
`REJECT`/`NO_TRADE`), `confidence`, `reason`, the originating `signal`
and `ai_analysis`, plus `signal_score`/`htf_score`/`risk_score`/
`ai_score`/`final_score` (Phase A3's weighted-formula components,
exposed for explainability).

## Allowed Dependencies
✅ `ai/` (`AIAnalysisResult`) — one of the weighted inputs.
✅ `signals/` (`SignalCandidate`) — the candidate being decided on.
✅ `context/` (`HTFBias`, as of Phase A3 — a real runtime import,
used as a dict key; `HTFBiasResult` itself stays `TYPE_CHECKING`-only).

## Forbidden Dependencies
❌ `strategies/` — Decision Engine never generates a new signal or
calls a strategy.
❌ Re-analyzing market structure/liquidity/etc. itself — every input
is already computed; `decision/` never re-derives what `context/`
already determined.
❌ `risk/` — the dependency runs the other way; `risk/` imports
`decision/`, never the reverse (would create a cycle, and would
violate the real pipeline order above).
❌ `database/`, `telegram/`, `execution/` — Decision Engine never
persists, messages, or dispatches anything itself.

## Error Contract
`evaluate()` never raises — every input (a `SignalType.NONE`
candidate, a missing `HTFBiasResult`, an unapproved `AIAnalysisResult`)
produces a well-formed `TradeDecision` (typically `REJECT`/`NO_TRADE`
with a `reason` string), never an exception. The AI-approval hard gate
(`if not ai_analysis.approved: REJECT`, checked before any threshold)
is itself part of the documented contract, not an error path — see
`decision/README.md`'s "Decision v2" section for the full weighted
formula and threshold logic.

## Future Extension
`docs/DECISION_PRINCIPLES.md`'s Principle 1 names the boundary this
module must keep even as inputs grow (e.g. a future real AI provider
still cannot become the decision-maker itself). No new weighted input
is planned without a task explicitly requesting a
`DecisionEngine.evaluate()` signature change — protected under
`CLAUDE.md`'s Trading Safety rules.
