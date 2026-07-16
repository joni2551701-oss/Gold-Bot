# ai/

## Purpose
Advisory-only AI evaluation layer. As of Phase 55, this is a
**foundation** for a future AI Assistant Core — no real AI/LLM call
happens anywhere in this directory.

## Flow
```
Signal Candidate + Context
      |
      v
AI Layer   -- advisory only, never approves/rejects itself
      |
      v
Decision Engine
```

## Responsibilities
- `ai_analyzer.py` — the production entry point `core/pipeline.py`
  calls. Currently a permanent-reject heuristic stub (documented,
  intentional — see the README's top-level Environment Variables
  table and `docs/AI_ARCHITECTURE.md`).
- `interfaces.py` — `AIAnalyzerInterface`/`MarketContext`/
  `UserContext`/`AIResponse`: the contract a future provider
  implements.
- `memory/`, `prompts/`, `profiles/`, `journal/`, `analyzer/` —
  Phase 55 foundation subpackages (memory, prompt templates, user
  profile model, trade journal, and a re-export of the canonical
  analyzer respectively). None are wired into the production pipeline.
- `learning_context.py` (Phase 60.6: Learning Loop Foundation, TASK 7;
  extended Phase 60.7: Adaptive Intelligence Layer Foundation, TASK 6)
  — `LearningContext` + `build_learning_context()`: bundles
  already-computed `learning/` data (`recent_failures`/
  `successful_patterns`/`strategy_stats`, plus Phase 60.7's
  `patterns`/`failures`/`regimes`/`confidence`) into the Director's own
  AI-facing JSON shape. Generates no explanation/recommendation text
  itself — that is left to a future AI consumer, still bound by
  `AIAnalyzerInterface`'s advisory-only contract. See
  `docs/LEARNING_LOOP.md`.

## Input
`SignalCandidate` + `ContextSnapshot` (production `AIAnalyzer`); the
new foundation types (`MarketContext`/`UserContext`) for anything
built against `interfaces.py` in a future phase; an already-built
`Sequence[learning.models.LearningRecord]` for `learning_context.py`.

## Output
`AIAnalysisResult` (production); `AIResponse` (future interface
shape); `LearningContext` (`learning_context.py`).

## Dependencies
`context/` and `signals/` for the production/interface path. No
dependency on `database/` or `telegram/` — an AI provider must never
reach either directly (see `CLAUDE.md`'s Trading Safety rules).
`learning_context.py` (Phase 60.6, extended 60.7) additionally imports
`analytics.strategy_report.compute_win_rate`,
`learning.models`/`learning.pattern_detector`, and
`learning.confidence.compute_pattern_confidence` — read-only, no
trading-decision logic, and still no `database/`/`telegram/`
dependency.

## AI Infrastructure Foundation (Phase 61.0)

Eight new subpackages, built on top of the frozen Foundation Layer,
none wired into the production pipeline — see `docs/AI_INFRASTRUCTURE.md`
for the full picture and `docs/PHASE61_AI_FOUNDATION_AUDIT.md` for the
reuse audit that justified each one:

- `capabilities/` — `Capability` enum + `CapabilityManager`: what the
  AI layer can be asked to do, independently toggleable, never
  provider-aware.
- `providers/` — `BaseAIProvider` contract + five placeholder vendor
  stubs (OpenAI/Gemini/Claude/Grok/Local LLM, no real API call) +
  `ProviderManager`'s Preferred/Fallback/Disabled selection.
- `router/` — `AIRouter`: Capability -> Provider -> Return, via a
  data-driven `routing_rules.py` table, never a hardcoded branch.
- `context/` — `AIContext` + `build_ai_context()`: composes Market
  Context/Signal Schema/User Profile/Trade History/Learning Context
  into one bundle; AI never receives raw market data.
- `access/` — `AIRole` (OWNER/ADMIN/VIP/PREMIUM/FREE) x `Capability`
  permission matrix (`AccessControl`) + `UsageLimiter` daily ceilings.
- `session/` — `SessionManager`/`ConversationState`/`ContextWindow`: a
  temporary conversation, distinct from `memory/`'s longer-lived store.
- `tools/` — `BaseAITool` + four placeholder tools (market/news/
  analytics/education), interface only, no database/pipeline call.
- `audit/` — `RequestLog`/`ResponseLog`/`provider_stats`: in-memory AI
  call audit trail (provider/latency/token/cost/status/capability).

## AI Provider Reliability Foundation (Phase 61.1)

A narrower "Provider Foundation" pass over five Phase 61.0 packages,
plus a new `ai/cache/` package — see `docs/AI_PROVIDER_FOUNDATION.md`
and `docs/PHASE61_1_PROVIDER_AUDIT.md` (reuse audit):

- `providers/provider_health.py` + `provider_status.py` +
  `provider_failover.py` — observed health (ONLINE/DEGRADED/
  RATE_LIMITED/OFFLINE/DISABLED), separate from `ProviderManager`'s
  owner-intent status; `select_available()` picks the first healthy
  candidate.
- `providers/provider_capabilities.py` — which `Capability` each
  provider actually declares support for; the router now checks this
  before selecting.
- `router/router.py` — extended selection order (capability matrix ->
  provider status -> health) + read-only `provider_metrics()` reusing
  `audit/provider_stats.py` (no new metrics module).
- `prompts/prompt_registry.py` — Version/Active/Rollback over
  `PromptManager`'s existing templates; `PromptManager` itself
  unmodified.
- `access/tool_permissions.py` — Role x Tool matrix, a second axis
  beside the existing Role x Capability matrix.
- `context/context_snapshot.py` — `+schema_version`/`context_version`,
  additive, backwards compatible.
- `cache/` (new) — `response_cache.py` + `cache_policy.py`: a TTL
  cache whose key structurally requires Capability + Context Version +
  Provider + Prompt Version + Context Hash (never bare prompt text).

## Future Roadmap
Full audit and folder-structure rationale in `docs/AI_ARCHITECTURE.md`.
The real work — replacing the permanent-reject stub with actual
heuristic/model scoring, and wiring a real provider into `ai/providers/` —
is explicitly out of Phase 61.0/61.1's scope. Phase 61.2 (deferred by
Phase 61.1's own brief) covers the Workflow Engine, real Provider API
integration, streaming, Conversation Engine, AI Explanation Runtime,
and traffic-based provider auto-selection.
