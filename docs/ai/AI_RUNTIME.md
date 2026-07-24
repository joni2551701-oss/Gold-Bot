# GoldBot — AI Runtime

Governed by `docs/constitution/CONSTITUTION.md` Article 1/5. This is a
one-page current-state summary — the full request sequence diagram
already lives in `docs/AI_RUNTIME_FLOW.md` (Phase 61.7) and the
production-wiring detail in `docs/PHASE62_2_RUNTIME_FREEZE.md`
(Phase 62.2). Per Constitution Article 7/11, this document points to
both rather than re-deriving them.

## Current real state (as of Phase 62.2, still frozen)

```
Telegram/User → Permission → Capability → AIService → RuntimeManager
    → Cache → Circuit Breaker → Provider → Validation → Audit → Response
```

- **Runtime Manager** (`ai/runtime/runtime_manager.py`) — the AI
  runtime process's own health: INITIALIZING/READY/BUSY/DEGRADED/
  FAILED/SHUTDOWN. Gates every `AIService.ask()` call via
  `is_healthy()`.
- **Provider Health** (`ai/providers/provider_health.py`) — per-provider
  ONLINE/DEGRADED/RATE_LIMITED/OFFLINE/DISABLED, independent of the
  Runtime's own state.
- **Circuit Breaker** (`ai/providers/circuit_breaker.py`) — per-provider
  CLOSED/OPEN/HALF_OPEN, opens on the 5th consecutive failure, exponential
  backoff (`2 ** attempt` seconds) between same-request retry attempts.
- **Event Bus** (`ai/runtime/event_bus.py`) — decoupled pub/sub; every
  lifecycle moment (request started/completed/failed, provider
  failed/recovered, runtime state changed) is a published `EventType`,
  never a direct call between producer and subscriber.
- **Metrics** (`ai/audit/provider_stats.py`) — per-provider latency/
  success/requests/tokens/cost, plus `DailyUsage`/cost-protection
  functions (Phase 62.2).
- **Cost Protection** — a daily cost/token ceiling check after every
  successful response; a breach transitions the Runtime to `DEGRADED`
  and queues an Owner alert. Real and tested; not yet live-triggering
  from real traffic because every `response_log` entry today logs
  `cost=0.0, tokens=0` (no provider reports usage back yet).

## What is explicitly frozen (Phase 62.2)

No further work lands on `ai/runtime/ai_service.py`'s orchestration
shape, `ai/providers/circuit_breaker.py`'s retry/backoff behavior, or
`ai/audit/provider_stats.py`'s cost-protection functions before the
next formally-numbered Worker Brief — see
`docs/PHASE62_2_RUNTIME_FREEZE.md`'s own "What this freeze means"
section.

## Related

- `docs/AI_RUNTIME_FLOW.md` — the full request-sequence diagram.
- `docs/PHASE62_2_RUNTIME_FREEZE.md` — the production-wiring freeze.
- `docs/AI_RUNTIME_OPERATIONS.md` — Owner-facing runtime operations
  (`/runtime_status`, `/runtime_restart`, `/runtime_provider`).
- `docs/policies/FOUNDATION_POLICY.md` — why this module is LOCKed.
