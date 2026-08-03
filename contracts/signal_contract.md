# Signal Layer

## Responsibility
Defines the standard shape a signal is described in, at two levels:
`SignalCandidate` (the live, in-pipeline proposal every strategy
produces) and `SignalSchema` (Phase A15's standardized, cross-module,
JSON-serializable record built from one). Grades a candidate's
context alignment (Signal Quality Score) and turns that grade into
human-readable reasons (Explainability) — computing nothing new
itself in either case.

```
SignalCandidate
        |
        v
   SignalSchema
```

## Input
`signal_layer.signal_engine.signal_engine.SignalEngine` takes a `ContextSnapshot` (routes
to `strategies.StrategyManager`).
`signal_layer.signal_scoring.signal_quality.compute_signal_quality()` takes a
`SignalCandidate`, a `ContextSnapshot`, and an optional
`HTFBiasResult`.
`signal_layer.signal_scoring.explainability.explain_signal()` takes a `SignalCandidate`, a
`ContextSnapshot`, and an already-computed `SignalQualityResult`.
`signal_layer.signal_builder.adapter.from_signal_candidate()` (Phase A15) takes a
`SignalCandidate` (required) plus optional `SignalQualityResult`/
`TradeDecision`/reference strings.

## Output
`List[SignalCandidate]` (`signal_engine.py`).
`SignalQualityResult` (`grade`, `score`, `criteria_met`,
`criteria_total`) — one per candidate.
`SignalExplanation` (`direction`, `reasons`, `quality`, `confidence`)
— one per candidate.
`signal_layer.signal_builder.schema.SignalSchema` — the standard record: identity
(`signal_id`, `created_at`, `version`), `symbol`, `timeframe`,
`direction`, price (`entry_price`, `stop_loss`, `take_profit`), a
`context_id` reference, strategy info (`strategy_name`,
`strategy_version`), quality info (`quality_grade`,
`confidence_score`), an `explanation_id` reference, decision info
(`decision`, `decision_score`, `decision_id`), and a `risk_id`
reference. See `docs/SIGNAL_SCHEMA.md` for the full field table.

## Allowed Dependencies
✅ `context/` — the `ContextSnapshot` every function here reads.
✅ `strategies/` — `signal_engine.py` routes to `StrategyManager`.

## Forbidden Dependencies
❌ `ai/`, `decision/`, `risk/` — Signal Quality Score and
Explainability are advisory only; neither is consumed by these layers
in this phase (`"quality_results"`/`"explanations"` travel only as
far as `TradingPipeline.run()`'s result dict).
❌ `database/`, `telegram/` — `signal_layer/signal_builder/schema.py` imports only the
standard library; `signal_layer/signal_builder/adapter.py` adds `TYPE_CHECKING`-only
`decision_layer.decision_engine.models` for a type hint, never a runtime dependency (would
otherwise invert `decision/`'s own existing `signals/` import and
create a cycle).

## Error Contract
`compute_signal_quality()`/`explain_signal()` never raise — a missing
`HTFBiasResult`, an empty context, or a `SignalType.NONE` candidate
all simply produce fewer criteria/reasons, never an exception.
`validate_signal(schema)` (Phase A15) returns a structured
`ValidationResult(valid, errors)` — never raises — for a malformed
`SignalSchema` (missing required field, invalid direction, inverted
BUY/SELL price ordering). Per `contracts/error_contract.md`, this is
the model every module's own validation should follow: a
`ValidationError` is a *result*, not a thrown exception, unless the
caller explicitly needs a hard-fail lookup (see
`assets.asset_registry.DuplicateAssetSymbolError`/
`strategy_layer.strategy_manager.lifecycle.strategy_registry.DuplicateStrategyIdError` for
the one legitimate raise-worthy case: a genuine programmer error,
duplicate registration, not a data-quality issue).

## Future Extension
`SignalSchema.explanation_id`/`risk_id` remain `None` hooks —
Explainability and Risk have no id field of their own yet.
`context_id` and `decision_id` are **no longer hooks**: as of the
Pre-Phase 59 Architecture Readiness Review (AC-03), `core/pipeline.py`
calls `from_signal_candidate()` in its new `signal_history` stage,
setting `context_id` to that cycle's real
`ContextSnapshotSchema.snapshot_id` and `decision_id` to a freshly
generated `str(uuid.uuid4())` per `TradeDecision` — see
`docs/SIGNAL_SCHEMA.md`'s "AC-03 update" section for the exact wiring.
