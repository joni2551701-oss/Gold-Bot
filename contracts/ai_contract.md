# AI Layer

## Responsibility
Advisory interpretation only. **AI does not create a trade.** It
reads a candidate and its context, and returns a confidence/risk read
plus an explanation — never a `BUY`/`SELL` decision, never the final
word. See `docs/DECISION_PRINCIPLES.md`'s Principle 1 and
`ai_layer/ai_service/interfaces.py`'s `AIAnalyzerInterface` docstring, which states
this contract in code, not just in this document.

## Input
`signal_layer.signal_builder.models.SignalCandidate` and `context.context_orchestrator.ContextSnapshot`
(`ai_layer.ai_engine.ai_analyzer.AIAnalyzer.analyze(signal, context)`).

A future real AI provider could additionally read
`signal_layer.signal_builder.schema.SignalSchema`/`context.snapshot.ContextSnapshotSchema`
(Phase A15/A16's standardized, JSON-serializable shapes) instead of
the live pipeline objects — not implemented in this phase; both are
named in `docs/SIGNAL_SCHEMA.md`'s and `docs/CONTEXT_SNAPSHOT.md`'s
own "Future usage"/"Significance for AI" sections as the intended
future input shape.

## Output
`ai_layer.ai_engine.ai_analyzer.AIAnalysisResult` — the real fields are `approved`
(`bool`), `confidence` (`float`, 0.0–1.0), `risk_score` (`float`,
0.0–1.0, higher means riskier), `explanation` (`str`).

**A deliberate deviation from the brief's own example**: the brief's
illustrative output shape (`{confidence: 82, risk_note: "medium",
explanation: "..."}`) does not match `AIAnalysisResult`'s real field
names or types — there is no `risk_note` field, `risk_score` is a
0.0–1.0 float, not a `"low"/"medium"/"high"` label, and `approved` is
not shown in the brief's example at all despite being the field
`decision_layer/decision_engine/decision_engine.py`'s hard-gate check
(`if not ai_analysis.approved: REJECT`) actually reads. This document
describes the real, already-implemented type — see
`docs/AI_ARCHITECTURE.md` for why `AIAnalyzer.analyze()` is currently
a heuristic stub (permanent-reject today) rather than a real model.

## Allowed Dependencies
✅ `signals/` (`SignalCandidate`) — the candidate being evaluated.
✅ `context/` (`ContextSnapshot`) — the market context around it.

## Forbidden Dependencies
❌ Producing a `BUY`/`SELL` value itself — `AIAnalysisResult` has no
`signal_type`/`direction` field; AI never re-states or overrides the
candidate's own direction.
❌ `decision/` — AI never calls `DecisionEngine.evaluate()`; the
dependency runs the other way (`decision/` imports `ai/`, never the
reverse).
❌ `risk/`, `execution/`, `telegram/`, `database/` — AI never sizes a
position, dispatches an order, messages a user, or persists anything.

## Error Contract
`analyze()` never raises today — the current heuristic stub always
returns a well-formed `AIAnalysisResult` (currently
`approved=False`, a fixed high `risk_score`, and an explanation
string), never an exception, regardless of input. A future real AI
provider integration (an external API call) would need to map any
provider failure (timeout, malformed response, rate limit) to
`contracts/error_contract.md`'s `ExternalAPIError` — never let a
provider outage propagate as a bare exception that could crash a
pipeline cycle. Not yet implemented; `docs/AI_ARCHITECTURE.md` is the
specification for what that integration should look like.

## Future Extension
v0.4 "AI Assistant" (see `docs/SYSTEM_OVERVIEW.md`'s version roadmap)
is the named future phase that replaces the heuristic stub with a
real provider. `configuration/feature_flags.py`'s `enable_ai` flag
(Phase A13, always `False` today) is the reserved gate for that
future capability — not wired to anything yet.
