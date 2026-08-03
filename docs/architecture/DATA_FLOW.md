# GoldBot — Data Flow

Governed by `docs/constitution/CONSTITUTION.md` Article 2 (Dependency
Law). This is the real, per-cycle stage order `core/pipeline.py` runs,
verified directly against `TradingPipeline._log_stage()`'s sixteen
call sites — not a simplified sketch. Every stage name below is the
exact string that appears in the pipeline's own log output.

## The real stage order

```
market_data
    ↓
data_quality
    ↓
htf_bias
    ↓
context
    ↓
market_phase
    ↓
signal
    ↓
signal_quality
    ↓
explainability
    ↓
features
    ↓
ai                    ← AI Analysis runs here, BEFORE decision/risk
    ↓
decision
    ↓
risk
    ↓
signal_history
    ↓
telegram_format
    ↓
telegram_delivery
    ↓
database
```

## Correction note

An earlier draft of this document (matching the Director's own
higher-level sketch) placed "AI Analysis" after Trade Monitor/Journal
and just before Telegram delivery. The real, mechanically-verified
order places `ai` **before** `decision` and `risk` — matching
`CLAUDE.md`'s own stated pipeline order
(`signals/ -> ai/ -> decision/ -> risk/ -> telegram/ -> database/`)
and Constitution Article 1/2 exactly: the Decision Engine receives the
AI's `AIAnalysisResult` as one advisory input *before* it decides,
not a summary generated *after* risk/execution has already run. This
document states the real order per Constitution Article 7's "document
reality, not assumption" precedent (the same correction
`docs/architecture/MODULE_DEPENDENCIES.md` made once already, for
`knowledge/`'s real location).

There is no dedicated `journal` pipeline stage — `ai/journal/trade_journal.py`
exists as a standalone module (used by learning/analytics reporting)
but is not called from `core/pipeline.py`. The nearest real pipeline
stage to "Journal" is `signal_history`, which persists the signal's
lifecycle record, not an AI-authored journal entry.

## Stage-by-stage responsibility

| Stage | What happens | Real module |
|---|---|---|
| `market_data` | Fetch and normalize candles | `data/` |
| `data_quality` | Score data completeness/validity | `data/` |
| `htf_bias` | Higher-timeframe bias computation | `context/` |
| `context` | Build the market context snapshot | `context_layer/context_engine/context_orchestrator.py` |
| `market_phase` | Classify market phase (Wyckoff/AMD/trend) | `context/` |
| `signal` | Generate candidate signal(s) | `strategies/`, `signal_layer/signal_engine/signal_engine.py` |
| `signal_quality` | Score/filter candidate signals | `signals/` |
| `explainability` | Build the explainability payload for the signal | `signals/`, `ai/explanation/` (type-only) |
| `features` | Assemble feature values for AI context | `context/`, `signals/` |
| `ai` | `AIAnalyzer.analyze()` — produces `AIAnalysisResult` | `ai_layer/ai_engine/ai_analyzer.py` |
| `decision` | Blend confidence, APPROVE/REJECT/NO_TRADE | `decision_layer/decision_engine/decision_engine.py` |
| `risk` | Geometry/stop-loss validation, sizing | `risk_layer/risk_engine/risk_manager.py` |
| `signal_history` | Persist the signal's lifecycle record | `lifecycle/` |
| `telegram_format` | Format the Telegram message | `telegram/` |
| `telegram_delivery` | Send eligible messages | `telegram/` |
| `database` | Persist the final signal record | `database/*_repository.py` |

## The one AI/Decision rule this diagram exists to protect

The AI layer produces a *value* (`AIAnalysisResult`) at the `ai` stage.
It never calls `decision/`, `risk/`, or `execution/` itself — the
pipeline orchestrator (`core/pipeline.py`) is the only caller of both
`AIAnalyzer.analyze()` and `DecisionEngine`, and it calls them in this
fixed order. See Constitution Article 1 ("AI yordam beradi. AI qaror
bermaydi.") and `docs/architecture/IMPORT_RULES.md`'s Forbidden table.

## Related

- `docs/architecture/SYSTEM_LAYERS.md` — the layer-cluster view this
  flow passes through.
- `docs/architecture/AI_FLOW.md` — what happens *inside* the `ai` stage.
- `docs/ARCHITECTURE.md` — the original full pipeline diagram this
  document supersedes as the stage-accurate reference.
