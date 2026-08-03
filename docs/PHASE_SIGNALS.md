# PHASE_SIGNALS — Canonical Signal Layer (STEP-08 / TASK-CORE-008)

The `signals/` layer is GoldBot's single **Canonical Signal Layer**: it
turns a setup-layer `StrategyResult` into ONE platform-independent signal
every consumer reads. It performs no analysis, no strategy selection, no risk
sizing, no decision, and touches no platform.

## 1. Position in the flow

```
config -> providers -> stream -> market -> context -> strategies
                                                          │
                                                    ┌─────┴─────┐
                                                    │  signals  │  ← STEP-08
                                                    └─────┬─────┘
                                                          │  Canonical Signal
        decision · telegram · mobile · mini app · desktop · ai · monitoring
```

## 2. Input / Output

- **Input (mandatory):** `StrategyResult` (read duck-typed), `ContextSnapshot`.
- **Input (optional):** MarketSnapshot / CurrentPrice / symbol + session
  metadata (passed as keyword args to `SignalManager.build`).
- **Output:** a `CanonicalSignalResult` whose `.signal` is the canonical
  `SignalSchema`, plus derived views (strength, enrichment, presentation,
  routes, lifecycle status) and a flat JSON payload via `.to_payload()`.
- signals/ does **not** talk to providers or stream directly.

## 3. Director decision — reuse-first

`signal_layer.signal_builder.schema.SignalSchema` (Phase A15) is ALREADY the cross-module,
platform-independent signal contract, with `validate_signal()`,
`to_dict()/to_json()`, and an `adapter.from_signal_candidate()`. STEP-08
therefore **reuses** it: `signal_layer.signal_builder.signal.CanonicalSignal is SignalSchema`.
No second signal model was created — this satisfies the task's own Refactor
Rules ("duplicate yozilmasin, mavjud kod reuse qilinsin") and CLAUDE.md's
"No duplicate logic".

### Field mapping (task spec → where it lives)

| Task CanonicalSignal field | Home |
|---|---|
| signal_id, symbol, direction, strategy, confidence, entry, stop_loss, take_profit, status(decision), created_at, session, timeframe | `SignalSchema` fields (reused verbatim) |
| quality | `signal_layer.signal_scoring.quality.SignalStrength` (STRONG/GOOD/NORMAL/WEAK/INVALID), on `CanonicalSignalResult.strength` |
| rr | derived in `manager` from the setup's own geometry (descriptive), carried on the result |
| reason | `SignalPresentation.short_reason` (from the StrategyResult reasons) |
| metadata | `SignalEnrichment` (price/spread/session/volatility/regime/build_version) |
| lifecycle status | `signal_layer.signal_engine.lifecycle.CanonicalSignalStatus` |

`SignalSchema` (frozen A15 contract) was **not** modified — the extra fields
live in the surrounding STEP-08 structures, kept additive.

## 4. File responsibilities

| File | Does | Does NOT |
|---|---|---|
| `signal.py` | re-export SignalSchema as CanonicalSignal + helpers | define a new model |
| `base.py` | `SignalContract` ABC (validate/build/serialize) | implement pipeline |
| `registry.py` | `SignalKind` (BUY/SELL/CLOSE/CANCEL/UPDATE/WATCHLIST) | trade |
| `validator.py` | reuse `validate_signal` + dedup + setup precheck | decide/approve |
| `quality.py` | strength label from confidence/rr, grade mapping | compute risk |
| `enricher.py` | attach env metadata, fill optional fields (non-mutating) | recompute structure/regime |
| `formatter.py` | neutral title/summary/description/reason/tags | write Telegram/UI markup |
| `serializer.py` | dict/JSON (reuses schema) + full payload | I/O |
| `router.py` | consumer route metadata | send anything |
| `manager.py` | orchestrate the pipeline | analyze / risk / decide |
| `lifecycle/` | `CanonicalSignalStatus` build/publish state machine | persist |

## 5. Three distinct signal-lifecycle concepts (disambiguated)

| Enum | Package | Tracks |
|---|---|---|
| `CanonicalSignalStatus` | `signals/lifecycle/` | signals/-layer **build/publish** (CREATED→VALIDATED→ENRICHED→READY→PUBLISHED/EXPIRED/CANCELLED) |
| `SignalLifecycleState` | `lifecycle/signal_state.py` | signal **analysis/decision** journey (CREATED→QUALITY_CHECKED→…→CLOSED) |
| `SignalState` | `execution_layer/execution_monitor/signal_lifecycle.py` | Telegram **message delivery** (inert) |

Three names, three packages, one concept each — the codebase's standing
disambiguation discipline.

## 6. Trading-safety / boundary guarantees

- Live path (`signal_engine.SignalEngine → SignalCandidate`, consumed by
  `core/pipeline.py` and `decision/`) is **FROZEN and untouched** — STEP-08
  imports it nowhere and modifies none of `models.py`, `signal_engine.py`,
  `schema.py`.
- signals/ imports no `risk/`, `decision/`, `execution/`, `telegram/`,
  `ai/`, `provider`, or `stream` runtime module; it reads a `StrategyResult`
  duck-typed and returns data.
- Every path is fail-safe: a None/empty/partial StrategyResult yields a
  defined INVALID `CanonicalSignalResult`, never a raise.

## 7. Tests

`tests/signals/test_canonical_*.py` cover: model + registry, validator,
quality, enricher, formatter, serializer, manager pipeline, lifecycle, and
the mandatory edge cases — empty StrategyResult, invalid signal, duplicate
signal, serialization. The pre-existing `tests/signals/` suite (adapter,
schema, quality, explainability) is unchanged and still green.

## 8. Upstream freeze

Per the STEP-08 directive, `config`, `data_layer/providers`, `stream`, `market`,
`context`, `strategies` are now formally FROZEN — see
`docs/STEP_08_UPSTREAM_FREEZE.md`. Changing any of them requires explicit
Director approval.
