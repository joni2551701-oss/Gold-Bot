# GoldBot — Architecture Master

Governed by `docs/constitution/CONSTITUTION.md` Article 1 (Core
Principle) and Article 2 (Dependency Law). This document is the
practical expression of both: the real system layer diagram, and
what each layer CAN and CANNOT do.

## System Overview

Two parallel tracks. The Trading Engine decides. The AI Layer
explains. They meet only at the Telegram delivery boundary, never
inside the decision itself.

```
 Market Data → Context Engine → Strategy Engine → Signal Engine
      → Decision Engine → Risk Manager → Execution → Trade Monitor
                              |
                       (delivery boundary)
                              |
                          Telegram
                              |
                    AI Layer (parallel, advisory only)
      AI Infrastructure → AI Runtime → AI Intelligence
              → AI Product → AI Broadcast
```

Real modules behind each box:

| Diagram box       | Real module(s) |
|--------------------|----------------|
| Market Data        | `data/` |
| Context Engine      | `context_layer/context_engine/context_orchestrator.py` |
| Strategy Engine     | `strategy_layer/strategy_manager/strategy_manager.py` |
| Signal Engine       | `signal_layer/signal_engine/signal_engine.py` |
| Decision Engine     | `decision_layer/decision_engine/decision_engine.py` |
| Risk Manager        | `risk_layer/risk_engine/risk_manager.py` |
| Execution           | `execution_layer/execution_engine/execution_engine.py` (intentionally inert — no MT5 order calls exist yet) |
| Trade Monitor       | `lifecycle/paper_trade_monitor.py` |
| Telegram            | `telegram/handlers.py` → `telegram/*_service.py` → `database/*_repository.py` |
| AI Infrastructure   | `ai/providers/`, `ai/router/`, `ai/capabilities/` |
| AI Runtime          | `ai/runtime/` (`AIService`, `RuntimeManager`, `EventBus`) |
| AI Intelligence     | `ai/analyzer/` / `ai/ai_analyzer.py`, `ai/context/`, `ai/explanation/` |
| AI Product          | `ai/session/`, `ai/conversation/`, `ai/prompts/` |
| AI Broadcast        | `broadcast/`, `media/`, `translation/`, `ai/persona/` (Phase 63.0 — foundation/contract only, no real channel/media/translation call; see `docs/AI_BROADCAST_FOUNDATION.md`), plus `telegram/owner/runtime_commands.py`/`broadcast_commands.py` for Owner-facing surfacing (not wired to a live process loop) |

## Per-Layer Responsibility

Each entry follows the Director's own worked format: CAN / CANNOT /
depends-on.

### Context Engine (`context/`)
- **CAN**: build market context snapshots from raw data, feed the
  Strategy Engine a consistent view of current conditions.
- **CANNOT**: generate a trading signal, evaluate risk, talk to
  Telegram.
- **Depends on**: `data/` only.

### Strategy Engine (`strategies/`)
- **CAN**: apply strategy rules to context and produce candidate
  signal input.
- **CANNOT**: approve/reject a trade, size a position, send a
  Telegram message.
- **Depends on**: `context/`, `data/`.

### Signal Engine (`signals/`)
- **CAN**: assemble and validate a `SignalCandidate`/`SignalSchema`
  from strategy output.
- **CANNOT**: make the final approve/reject call, touch risk
  geometry.
- **Depends on**: `strategies/`, `context/`.

### Decision Engine (`decision_layer/decision_engine/decision_engine.py`)
- **CAN**: blend confidence (including the `AIAnalysisResult` value
  `core/pipeline.py` hands it — `ai_confidence` on `DecisionResult`),
  apply APPROVE/REJECT/NO_TRADE thresholds, decide whether a signal
  proceeds. Accepting the AI's analysis as one input value is real and
  intended (`CLAUDE.md`'s own `signals/ -> ai/ -> decision/` order).
- **CANNOT**: call into `ai/router/`, `ai/providers/`, or `ai/runtime/`
  itself, trigger an AI request, or let the AI layer make the
  decision for it (Constitution Article 1/3 — the AI answers, it does
  not act); be bypassed by any shortcut path to Telegram delivery.
- **Depends on**: `signals/`, `context/`, and `ai.ai_analyzer.AIAnalysisResult`
  (type only — see `docs/architecture/IMPORT_RULES.md`).

### Risk Manager (`risk_layer/risk_engine/risk_manager.py`)
- **CAN**: evaluate a signal's geometry/stop-loss validity, size a
  position, reject on risk-limit violation via `evaluate()`.
- **CANNOT**: be skipped for any signal reaching a user (`CLAUDE.md`
  Trading Safety hard rule — "Never bypass Risk Manager"); consult
  the AI layer.
- **Depends on**: `decision/`.

### Execution (`execution/`)
- **CAN**: exist as the designated future home for order placement.
- **CANNOT**: place a real order today — intentionally inert, no MT5
  order calls exist yet; wiring it up requires explicit approval, not
  a routine addition.
- **Depends on**: `risk/`.

### Trade Monitor (`lifecycle/paper_trade_monitor.py`)
- **CAN**: track the lifecycle of an approved/paper trade after
  delivery.
- **CANNOT**: originate a new signal, alter a risk decision already
  made.
- **Depends on**: `decision/`, `risk/`.

### Telegram (`telegram/`)
- **CAN**: present pipeline output and AI explanations to users,
  route Owner commands to services.
- **CANNOT**: touch the database directly from a handler (Constitution
  Article 4) — handlers call services, services call repositories.
- **Depends on**: `telegram/*_service.py` → `database/*_repository.py`;
  reads AI output for explanation surfacing only, never triggers an
  AI call that feeds back into a trading decision.

### AI Layer (`ai/`) — all five tracks (Infrastructure/Runtime/Intelligence/Product/Broadcast)
- **CAN**: explain, analyze, summarize, educate, assist a human
  reading pipeline output.
- **CANNOT**: approve a trade, execute an order, modify a risk
  parameter, call the Risk Manager, or trigger a Telegram send that
  bypasses the pipeline's own eligibility filter (Constitution
  Article 1 and 3; `CLAUDE.md` Trading Safety — "Never allow AI direct
  execution").
- **Depends on**: `core/` only, plus the narrow, audited
  `signals/`/`context/` type-only import exception listed in
  Constitution Article 3.
- **Production status** (Phase 62.2): the AI Runtime track
  (`ai/runtime/ai_service.py`) is now the real, production-wired
  orchestration point — runtime lifecycle gating, circuit breaker
  failover with backoff, response validation, audit logging (including
  the runtime-unhealthy path), and AI Cost Protection (daily cost/token
  ceiling → `RuntimeState.DEGRADED` + Owner alert) all run for real on
  every `AIService.ask()` call, not standalone-but-unused foundation
  pieces. See `docs/PHASE62_2_RUNTIME_FREEZE.md` for the full flow and
  what remains explicitly out of scope (streaming, voice, broadcast,
  autonomous trading decisions, memory learning).

### Senior Trading AI Foundation (`ai/persona/`, `broadcast/`, `media/`, `translation/`) — Phase 63.0
- **CAN**: hold identity data (`Persona`), hold channel/media-type/
  language *intent* (Owner-set ENABLED/DISABLED/armed flags), build a
  `BroadcastRequest`/`ExplanationOutput` *value* — pure data, never
  sent or generated.
- **CANNOT**: build a prompt, call `AIService` or any provider, call a
  YouTube/OBS/RTMP/Twitch/Kick client, synthesize voice/image/video,
  call a translation backend, or touch `decision/`/`risk/`/
  `execution/`/`database/`/`telegram.handlers` directly. Every one of
  these packages is contract-first — see `docs/PHASE63_0_FREEZE.md`.
- **Depends on**: `core/`, `ai/content/` (for `BroadcastReadyContent`/
  `ContentType`) — `broadcast/`/`media/`/`translation/` are top-level
  packages (not under `ai/`), the same reasoning that keeps
  `execution/` separate from `decision/` (see
  `docs/PHASE63_0_FOUNDATION_AUDIT.md`).

## Related documents

- `docs/constitution/CONSTITUTION.md` — the governing Articles this
  document expresses concretely.
- `docs/architecture/MODULE_DEPENDENCIES.md` — the real per-module
  dependency map.
- `docs/architecture/IMPORT_RULES.md` — the allowed/forbidden import
  table.
- `docs/ARCHITECTURE.md` — the original, still-current full pipeline
  and AI Runtime data-flow diagrams this document summarizes at the
  system level.
