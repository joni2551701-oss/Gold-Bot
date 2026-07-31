# GoldBot Ecosystem Architecture — Application Services

Part of the Senior Trading AI Ecosystem architecture set. Governed by
`docs/constitution/CONSTITUTION.md` (supreme) and scoped under
`01_Ecosystem_Architecture.md` (the ecosystem's high-level map — see
its "Division of authority" section). This file is the Application Services
detail split out of that document's own former Section (TASK-GOV-004,
Owner-directed restructure, Option A: ecosystem-level summary, not a
duplicate of the Trading-Core/AI/Telegram mechanical detail already
owned by `ARCHITECTURE_MASTER.md`/`LAYER_CONTRACT.md`/
`MODULE_DEPENDENCIES.md`/`DATA_FLOW.md` where this layer overlaps them
— this file cross-references those, it does not restate them).

**Status: mostly not built.** The diagram's Application Services layer
(Signal/Chart/AI/Notification/Replay/Analytics/Portfolio/Gateway
Service, behind an API/WebSocket Gateway) is the boundary between Core
and every product surface. Real findings:

| Service | Status |
|---|---|
| Signal Service | Not a standalone service — signal output is currently formatted and delivered directly by `telegram/signal_formatter.py`/`notifier.py` inside the pipeline, not through a separate service boundary. |
| Chart Service | Partial — `ai/chart_intelligence/` exists but is AI-vision-oriented (chart image analysis), not a chart-rendering/serving service. |
| AI Service | Real and substantial — `ai/runtime/ai_service.py` is production-wired (Phase 62.2; see `docs/PHASE62_2_RUNTIME_FREEZE.md`) with lifecycle gating, circuit-breaker failover, response validation, audit logging, and cost protection. This is the one Application Service that is genuinely real. |
| Notification Service | Real, beyond `telegram/notifier.py` — `telegram/notification_service.py`, `telegram/owner/runtime_notifications.py`, plus a `broadcast/` package for multi-channel delivery (contract-only, Phase 63.0). |
| Replay Service | Real as foundation — `data/replay/` (module 8), plus `telegram/owner/replay_commands.py`. Not wired into the live pipeline. |
| Analytics Service | Real as an internal reporting package — `analytics/` (benchmark, equity curve, execution/gap/performance/signal/strategy reports). Internal, not a customer-facing service. |
| Portfolio Service | Partial — `ai/portfolio/` exists but is scoped inside the AI layer (feeds AI reasoning), not a standalone user-facing service. |
| API / WebSocket Gateway | `core/gateway/` (Module 10) exists as an internal Core Gateway — single entry point into Core services (auth, rate limiting, circuit breaking, dependency graph). It is **not** a public-facing API/WebSocket server; no such server exists in the repository. |

