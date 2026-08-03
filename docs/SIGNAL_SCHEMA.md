# Signal Schema Standard Foundation (Phase A15)

## Purpose

Builds one standard, cross-module data contract — `SignalSchema` — for
"how does GoldBot store and pass a signal between modules." **This is
a standardization layer, not a new signal source.** No new signal
strategy, no new entry logic, no `DecisionEngine` change, and no AI
logic change are introduced in this phase.

Today, each module effectively has its own private view of what a
"signal" looks like: a strategy produces a `SignalCandidate`
(`direction`/`entry`/`sl`/`tp`), the AI layer produces an
`AIAnalysisResult` (`confidence`/`explanation`), Decision Engine
produces a `TradeDecision`, and a future Analytics module would want
`result`/`rr` — each a different shape, answering a different
question. `SignalSchema` is the single, documented shape all of them
can describe themselves in terms of:

```
SignalCandidate
        |
        v
   SignalSchema
        |
        +-- Decision
        +-- Risk
        +-- Telegram
        +-- Analytics
        +-- AI
```

## Design Rules

1. `SignalSchema` does not compute anything — every field is either a
   direct copy of an already-computed value, or an explicit `None`
   placeholder for a reference that doesn't exist yet.
2. `validate_signal()` never raises — an invalid `SignalSchema`
   produces a structured `ValidationResult(valid=False, errors=[...])`,
   the same fail-safe posture every other Phase A foundation module
   uses.
3. Existing signal creation (`strategies/*.py`, `signal_layer/signal_engine/signal_engine.py`,
   `signal_layer/signal_builder/models.py`) is untouched. `SignalSchema` is purely
   additive, bridged via `signal_layer/signal_builder/adapter.py`.
4. Not wired into `core/pipeline.py` in this phase (Phase A15) — pipeline
   logic is unchanged. **Update (Pre-Phase 59 Architecture Readiness
   Review, AC-03)**: `core/pipeline.py` now calls
   `from_signal_candidate()` in a new `signal_history` stage; see
   "Integration" below for the current, real wiring.

## Pre-implementation audit

Before writing any code, `signals/` and everything that already
produces or references a signal ID/timestamp were read in full, to
reuse rather than invent:

| Found | Location | Reused as |
|---|---|---|
| `SignalCandidate(signal_type, entry, stop_loss, take_profit, strategy_name, confidence, reasons)` | `signal_layer/signal_builder/models.py` | The adapter's required input — untouched. |
| `SignalType.BUY/SELL/NONE` | `signal_layer/signal_builder/models.py` | `SignalSchema.direction`'s exact allowed vocabulary (`ALLOWED_DIRECTIONS`) — read as plain literals, not imported as the enum type (see "Why fields are plain strings" below). |
| `SignalQualityResult(grade: QualityGrade, score, ...)` | `signal_layer/signal_scoring/signal_quality.py` | `SignalSchema.quality_grade`/`.confidence_score`, relayed via `grade.value`/`score` in the adapter, never recomputed. |
| `SignalRecord(signal_id: str, created_at: datetime, ...)`, `create_signal_record()`'s `signal_id=str(uuid.uuid4())`, `created_at=datetime.now(timezone.utc)` | `database_layer/trade_repository/signal_record.py` (untouched) | `SignalSchema.signal_id`/`.created_at`'s exact generation convention (`generate_signal_id()`), not a new counter-based scheme. See "Relationship to SignalRecord" below for why `SignalSchema` is a distinct model, not a duplicate. |
| `DecisionAction.APPROVE/REJECT/NO_TRADE` | `decision_layer/decision_engine/models.py` | Confirmed **not** the same vocabulary as this phase's `SignalSchema.decision` (`APPROVED`/`REJECTED`/`PENDING`) — see "Decision status mapping" below for why, and the explicit, documented mapping. |
| `RiskResult(approved, lot_size, risk_amount, risk_reward, reason)` — no `id` field | `risk_layer/risk_engine/risk_manager.py` | Confirmed `risk_id` has no real source anywhere today — stays an honest `None` hook, never fabricated. |
| `SignalExplanation(direction, reasons, quality, confidence)` — no `id` field | `signal_layer/signal_scoring/explainability.py` | Confirmed `explanation_id` has no real source anywhere today — stays an honest `None` hook. |
| `main.py`'s `symbol="XAUUSD"`, `interval="M15"`; `assets/profiles/gold.py`'s `AssetType.GOLD.value == "GOLD"` | `main.py`, `assets/` | `signal_layer/signal_builder/adapter.py`'s default `symbol`/`timeframe`/`asset_type` — real, already-established values, not new inventions (the same real-value-reuse pattern Phase A11/A12/A13 followed). `asset_type`'s default is the literal `"GOLD"` string, not an `assets/` import — see "Why no `assets/` import" below. |

## Relationship to `SignalRecord` (`database_layer/trade_repository/signal_record.py`)

`SignalRecord` already exists and is untouched by this phase. It is
**not** the same thing as `SignalSchema`:

| | `SignalRecord` (pre-existing) | `SignalSchema` (Phase A15) |
|---|---|---|
| When it can exist | Only once a full `(SignalCandidate, TradeDecision, RiskResult)` triple already exists — the end of a pipeline cycle. | Right after Strategy Engine — before Decision Engine or Risk Manager have run. |
| `decision`/`risk_result` | Required, non-optional dataclass fields. | Optional references (`decision` defaults `"PENDING"`, `risk_id` defaults `None`). |
| Shape | Persistence-display-oriented (`rr_ratio`, `ai_decision`, `risk_status`, `signal_status` — flattened for the `signals` SQL table). | Cross-module contract-oriented (`asset_type`, `session`, `quality_grade`, `confidence_score`, `context_id`, `explanation_id` — fields `SignalRecord` has no equivalent for). |
| Consumer | `database_layer/trade_repository/signal_repository.py` only. | A future AI provider, Analytics, Replay, Education — never the database in this phase. |
| Written to the database? | Yes — that's its purpose. | No — not in this phase. |

Both independently reuse the same `str(uuid.uuid4())`/
`datetime.now(timezone.utc)` convention because both need a real
identity/timestamp and neither should invent a second scheme.

## Model

```python
@dataclass(frozen=True)
class SignalSchema:
    signal_id: str
    created_at: datetime
    symbol: str
    timeframe: str
    direction: str
    version: str = "1.0"
    asset_type: Optional[str] = None
    session: Optional[str] = None
    entry_price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    context_id: Optional[str] = None
    strategy_name: Optional[str] = None
    strategy_version: Optional[str] = None
    quality_grade: Optional[str] = None
    confidence_score: Optional[float] = None
    explanation_id: Optional[str] = None
    decision: str = "PENDING"
    decision_score: Optional[float] = None
    decision_id: Optional[str] = None
    risk_id: Optional[str] = None
```

`decision_id` was added in the Pre-Phase 59 Architecture Readiness
Review (AC-03) — see "AC-03 update" below.

### Field groups

| Group | Fields | Notes |
|---|---|---|
| Identity | `signal_id`, `created_at`, `version` | `signal_id` via `generate_signal_id()` (`str(uuid.uuid4())`). `version` is the *schema* version (`"1.0"` today), not a strategy version. |
| Market | `symbol`, `asset_type`, `timeframe`, `session`, `market_phase` | `symbol`/`timeframe` required; `asset_type`/`session`/`market_phase` optional. `market_phase` added Phase 59 Real Market Validation Foundation (TASK 2) — `core/pipeline.py`'s `signal_history` stage relays it from the same cycle's already-computed `MarketPhaseResult.phase.value` (AC-02); never recomputed here. |
| Direction | `direction` | One of `"BUY"`/`"SELL"`/`"NONE"` — validated, not enum-typed (see below). |
| Price | `entry_price`, `stop_loss`, `take_profit` | Required for `BUY`/`SELL` (validated), meaningless for `NONE`. |
| Context reference | `context_id` | A reference only, never the `ContextSnapshot` itself. Phase A16 (Context Snapshot Foundation) is the named next phase. |
| Strategy | `strategy_name`, `strategy_version` | `strategy_name` is the real `SignalCandidate.strategy_name` value (e.g. `"LIQUIDITY_SWEEP_STRATEGY"`), not a human label — see "A deliberate deviation" below. `strategy_version` has no source today; an honest hook. |
| Quality | `quality_grade`, `confidence_score` | Relayed from an already-computed `SignalQualityResult` — never recomputed. |
| Explainability reference | `explanation_id` | A reference only; `SignalExplanation` has no id field today. |
| Decision | `decision`, `decision_score`, `decision_id` | `decision` defaults `"PENDING"`; see "Decision status mapping" below. `decision_id` (added AC-03) is a freshly generated `str(uuid.uuid4())` per `TradeDecision`, since `decision_layer.decision_engine.models.TradeDecision` itself has no id field — generated by `core/pipeline.py` at the point it builds the historical record, not by the adapter or `TradeDecision`. |
| Risk reference | `risk_id` | A reference only; `RiskResult` has no id field today. |

### Why fields are plain strings, not enums

`SignalSchema.direction`/`.quality_grade`/`.decision` are plain `str`,
not `SignalType`/`QualityGrade`/a new enum. `SignalSchema` is meant to
be JSON-native and dependency-light — a future AI/Analytics/Replay/
Education consumer should not need to import internal pipeline enum
types just to read a signal record. `validate_signal()` still checks
each field against the real vocabulary (`ALLOWED_DIRECTIONS`
mirrors `SignalType`'s real values exactly), so the vocabulary is
never invented independently of its source of truth — only the
*field's Python type* is simplified.

### A deliberate deviation from the brief's own example

The brief's example used `strategy_name="Liquidity Sweep"` (a human
label). The adapter uses `signal.strategy_name` directly — the real
value every `strategies/*.py` file already produces (e.g.
`"LIQUIDITY_SWEEP_STRATEGY"`) — not a human-readable rename, since
that requires zero new mapping and stays exactly joinable against
`SignalRecord.strategy`/`StrategyDefinition.id` (Phase A11), which use
the same real value. The same real-value-over-illustrative-label
choice Phase A11 made for `supported_assets=["XAUUSD"]` over the
brief's `["GOLD"]`.

### Decision status mapping

`SignalSchema.decision`'s vocabulary (`APPROVED`/`REJECTED`/`PENDING`)
is deliberately **not** the same as `decision_layer.decision_engine.models.DecisionAction`'s
real values (`APPROVE`/`REJECT`/`NO_TRADE`) — `SignalSchema` can exist
before Decision Engine has run at all, so `"PENDING"` is a real,
necessary third state `DecisionAction` has no equivalent for.
`signal_layer/signal_builder/adapter.py`'s `_DECISION_ACTION_TO_STATUS` is the one place
the translation happens, when a `TradeDecision` is supplied:

| `DecisionAction` | `SignalSchema.decision` |
|---|---|
| `APPROVE` | `"APPROVED"` |
| `REJECT` | `"REJECTED"` |
| `NO_TRADE` | `"REJECTED"` (collapsed — both mean "no signal reaches the user") |
| *(not supplied)* | `"PENDING"` |

### Why no `assets/` import

`SignalSchema.asset_type` defaults to the literal `"GOLD"` string in
`signal_layer/signal_builder/adapter.py`, matching `assets.asset_type.AssetType.GOLD.value`
exactly — but `signal_layer/signal_builder/adapter.py` does not import `assets/` to get
it. Each Phase A foundation module (Strategy Lifecycle, Asset
Intelligence, Configuration) has deliberately stayed unwired from the
others in its own phase (see e.g. `docs/ASSET_INTELLIGENCE.md`'s
"Strategy Lifecycle relationship (documentation only)") — a real
cross-package import here would be new wiring beyond this phase's
"minimal integration" scope, for a single string constant a comment
can equally well document.

## Validation Rules

`validate_signal(signal: SignalSchema) -> ValidationResult` checks, in
order:

1. **Required fields** — `signal_id`, `symbol`, `timeframe`,
   `direction`, `created_at` must all be truthy.
2. **Direction** — must be one of `"BUY"`/`"SELL"`/`"NONE"`.
3. **Price ordering** — for `BUY`: `stop_loss < entry_price <
   take_profit`. For `SELL`: `take_profit < entry_price <
   stop_loss`. For `NONE`: not checked. A `BUY`/`SELL` direction
   missing any of the three price fields is itself an error.
4. **Decision status** — if set, must be one of `"APPROVED"`/
   `"REJECTED"`/`"PENDING"`.

`ValidationResult(valid: bool, errors: List[str])` — never raises,
same convention as `SignalQualityResult`/`DataQualityResult`/
`RiskResult.approved` elsewhere in this codebase.

## Serialization

`SignalSchema.to_dict()` returns a JSON-safe `dict` (`created_at`
rendered as an ISO-8601 string via `.isoformat()`, every other field
already a JSON-native primitive). `SignalSchema.to_json()` wraps it in
`json.dumps()`.

## Backward compatibility

```
Existing SignalCandidate
        |
        v
   Adapter (signal_layer/signal_builder/adapter.py)
        |
        v
     SignalSchema
```

`signal_layer/signal_builder/adapter.py`'s `from_signal_candidate(signal, ...)` is the one
adapter — the minimum input is an existing `SignalCandidate`
(unmodified). Every other parameter (`quality`, `decision`,
`context_id`, `explanation_id`, `risk_id`, `strategy_version`,
`session`) is optional, letting a caller supply more already-computed
objects when available without ever requiring them.

## Integration

Minimal in Phase A15 — not wired into `core/pipeline.py` at the time:

```
Strategy Output (SignalCandidate)
        |
        v
SignalSchema Adapter (signal_layer/signal_builder/adapter.py)
        |
        v
   Existing Pipeline (unchanged)
```

`ai/`, `decision/`, `risk/`, `telegram/`, `database/`, `execution/`,
and `strategies/` were all untouched by Phase A15.

### AC-03 update (Pre-Phase 59 Architecture Readiness Review)

`core/pipeline.py` now calls `from_signal_candidate()` for real, in a
new `signal_history` stage immediately after `risk`, once per candidate
that reached Risk Manager:

```
context_snapshot = from_context_snapshot(context, symbol, timeframe)  # context_layer/context_engine/snapshot.py

signal_history = [
    from_signal_candidate(
        candidate, symbol=symbol, timeframe=timeframe,
        session=context_snapshot.session.current_session,
        context_id=context_snapshot.snapshot_id,   # links this signal to this cycle's context
        quality=quality, decision=decision,
        decision_id=str(uuid.uuid4()),              # fresh per TradeDecision
    )
    for candidate, quality, decision in zip(signal_candidates, quality_results, decisions)
]
```

`context_id` on every resulting `SignalSchema` equals
`context_snapshot.snapshot_id` — the same value viewed from the two
sides of the link (see `docs/ARCHITECTURE_READINESS_REVIEW.md`'s AC-03
section for the full diagram). `strategy_id` needed no new field:
`strategy_name` already equals `StrategyDefinition.id` (Phase A11).
`"context_snapshot"` and `"signal_history"` are new keys in `run()`'s
result dict. This wiring does **not** persist either object to the
database — no migration, no new repository — the records are simply
now genuinely linked and `to_json()`-ready for a future persistence
step. `ai/`, `decision_layer/decision_engine/decision_engine.py`, `risk_layer/risk_engine/risk_manager.py`,
`telegram/`, and `strategies/` remain untouched — `core/pipeline.py`
only reads their already-computed output to build these two records.

## Future usage

- **AI**: a future real AI provider reading a flat, JSON-native
  `SignalSchema` instead of assembling context from several separate
  objects.
- **Replay**: `SignalSchema.to_json()`/`to_dict()` makes a signal
  trivially loggable and replayable outside a live pipeline run — not
  implemented in this phase.
- **Backtesting**: the same standard shape a future backtest harness
  would produce per historical signal, joinable against
  `SignalRecord`/`StrategyDefinition` via `strategy_name` and
  `signal_id`.
- **Education**: a stable, documented shape simple enough to explain
  to a non-technical user or export for a tutorial dataset.
- **Analytics**: `context_id`/`explanation_id`/`risk_id` become real,
  joinable references once Phase A16 (Context Snapshot Foundation)
  and any future Explainability/Risk persistence exist — not
  implemented in this phase.
