# GoldBot — Module Dependencies

Governed by `docs/constitution/CONSTITUTION.md` Article 2 (Dependency
Law) and Article 3 (Import Rules). This document is the living proof
those Articles hold today — it lists the real, current per-module
dependency structure, not an aspirational one.

## Dependency diagram

```
        Telegram
           |
     Command Layer          (telegram/command_router.py, commands.py, permissions.py)
           |
     Service Layer           (telegram/*_service.py, telegram/owner/*.py)
           |
      AI / Product Layer      (ai/session, ai/conversation, ai/prompts)
           |
        AI Core               (ai/runtime, ai/router, ai/providers, ai/analyzer, ...)
           |
      Data Context            (context/, signals/ [type-only], data/)
           |
        Database               (database/*_repository.py)
```

`core/` sits beneath everything and is depended on by every layer
above; it depends on nothing in this diagram.

## Real per-module dependencies

### Trading pipeline (unchanged this phase — documentation only)

| Module | Depends on |
|---|---|
| `data/` | external market data sources, `core/` |
| `context_layer/context_engine/context_orchestrator.py` | `data/`, `core/` |
| `strategies/strategy_manager.py` | `context/`, `data/`, `core/` |
| `signals/signal_engine.py` | `strategies/`, `context/`, `core/` |
| `decision/decision_engine.py`, `decision/models.py` | `signals/`, `context/`, `core/`, plus `ai.ai_analyzer.AIAnalysisResult` (**type only** — the one sanctioned `decision/ → ai/` import, see Constitution Article 1/3) |
| `risk/risk_manager.py` | `decision/`, `core/` |
| `execution/execution_engine.py` | `risk/`, `core/` (inert — no live order calls) |
| `lifecycle/paper_trade_monitor.py` | `decision/`, `risk/`, `core/` |
| `core/pipeline.py` | orchestrates all of the above, top to bottom |

### Telegram layer

| Module | Depends on |
|---|---|
| `telegram/handlers.py` | `telegram/*_service.py` only — never `database.*` or `core.pipeline` directly |
| `telegram/command_router.py` | `telegram/commands.py`, `telegram/permissions.py`, `telegram/handlers.py` |
| `telegram/*_service.py` (admin/feedback/notification/signal/subscription/user) | `database/*_repository.py` |
| `telegram/owner/*.py` (19 files: ai/backtest/control/dashboard/dataset/emergency/execution/feature/fundamental/learning/performance/provider/replay/report/runtime/security/status/system/validation) | corresponding service/repository layer for their domain; `runtime_commands.py` additionally depends on `ai/runtime/` (`AIService`, `RuntimeManager`, `self_check`) |

### Database layer

| Module | Depends on |
|---|---|
| `database/*_repository.py` (19 repositories) | `database/*_models.py`, `database/database.py` — SQL only, no business logic |

### AI layer — 21 real subpackages under `ai/`

| Subpackage | Real responsibility | Depends on |
|---|---|---|
| `ai/access/` | capability/permission gating for AI requests | `core/` |
| `ai/analyzer/` | Phase 55 compat entry point → re-exports canonical `ai/ai_analyzer.py` | `ai/ai_analyzer.py` |
| `ai/audit/` | provider stats / call auditing (`provider_stats.py`) | `core/` |
| `ai/cache/` | response caching | `core/` |
| `ai/capabilities/` | capability enum + permission matrix | `core/` |
| `ai/content/` | `ContentEngine`'s two surfaces: `generate()` (real `AIService.ask()`, Phase 61.5), extended Phase 63.6 with a deterministic `create`/`format`/`preview`/`validate`/`history` surface; `content_schema.py`/`content_types.py` (`ContentRequest`/`ContentResult`/`ContentType`, Phase 61.5/63.0); `models.py`/`content_adapters.py` (Phase 63.6) | `ai/runtime/`, `ai/capabilities/`, `ai/explanation/` (type-only), `ai/conversation/` (type-only), `core/` — never `translation/`/`media/`/`broadcast/` (Intelligence Dependency Principle) |
| `ai/context/` | `context_snapshot.py`/`context_builder.py` — reads `signals/`/`context/` types only | `signals/` (type-only), `context/` (type-only), `core/` |
| `ai/conversation/` | `ConversationEngine`'s two surfaces: `start_session()`/`ask()` (real `AIService.ask()`, Phase 61.3), extended Phase 63.5 with a deterministic `append`/`summarize`/`history`/`context`/`reset`/`close` surface | `ai/session/`, `ai/runtime/`, `knowledge/` (type-only), `ai/memory/` (type-only), `ai/reasoning/` (type-only), `core/` — never `ai/explanation/`/`ai/content/`/`broadcast/`/`media/`/`translation/` (Intelligence Dependency Principle) |
| `ai/explanation/` | `explanation_engine.py` — reads `signals/` types only; Phase 63.1 added `explanation_input.py`/`explanation_output.py`/`explanation_templates.py`/`explanation_builder.py`/`explanation_content_adapter.py` — deterministic, template-based, primitive-values-only (`ExplanationInput`), never imports `decision/`/`risk/` | `signals/` (type-only), `ai/persona/` (`PersonaManager`, Phase 63.1), `ai/content/` (`BroadcastReadyContent`, Phase 63.1 adapter only), `core/` |
| `ai/journal/` | `trade_journal.py` (canonical) — reads `signals/` types only | `signals/` (type-only), `core/` |
| `ai/memory/` | long-term AI memory storage; Phase 63.3 added `models.py`/`memory_registry.py` (`MemoryEntry` contract, `MemoryScope` catalog) and extended `MemoryRuntime` with a structured `store`/`recall`/`search`/`filter` surface | `core/` |
| `ai/persona/` | `Persona`, `PersonaManager`, `persona_registry.py` (Phase 63.0; only `SENIOR_TRADING_AI` registered as of Phase 63.1) | `core/` |
| `ai/profiles/` | `RuntimeProfile` definitions | `core/` |
| `ai/prompts/` | prompt templates | `core/` |
| `ai/providers/` | `BaseAIProvider`, vendor implementations, `circuit_breaker.py` | `core/` only — no vendor name leaks above this package |
| `ai/reasoning/` | `ReasoningRuntime` (deterministic `ReasoningResult` store, Phase 63.4) | `knowledge/` (type-only), `ai/memory/` (type-only), `core/` — never `ai/explanation/`/`ai/content/`/`ai/conversation/`/`broadcast/`/`media/`/`translation/` (Intelligence Dependency Principle, `docs/policies/DIRECTOR_POLICY.md`) |
| `ai/router/` | `AIRouter`, `routing_rules.py` | `ai/providers/`, `ai/capabilities/`, `core/` |
| `ai/runtime/` | `AIService`, `RuntimeManager`, `EventBus`, `self_check.py` — the orchestration point | `ai/router/`, `ai/providers/`, `ai/cache/`, `ai/audit/`, `ai/profiles/`, `core/` |
| `ai/session/` | session/user context for AI product surfaces | `core/` |
| `ai/tools/` | AI-callable tool definitions (advisory only) | `core/` |
| `ai/validation/` | response validation, `safety.py` | `core/` |

`ai/intelligence_runtime.py` (Phase 64.0) — a single top-level file,
not a subpackage — is the one deliberate exception to the per-layer
dependency table above: it is the Intelligence layer's composition
root, so it legitimately imports all eight layers it orchestrates
(`knowledge/`, `ai/memory/`, `ai/reasoning/`, `ai/conversation/`,
`ai/explanation/`, `ai/content/`, `media/`, `broadcast/`) — the same
role `core/pipeline.py` already plays for the Trading layer. It never
imports `decision/`/`risk/`/`execution/`/`strategies/`/`signals/`/
`database/`/`telegram/`.

Two top-level compat shims, documented so they are not mistaken for
new modules: `ai/ai_analyzer.py` and `ai/trade_journal.py` are the
canonical files; `ai/analyzer/ai_analyzer.py` and
`ai/journal/trade_journal.py` are the Phase 55-restructure entry
points that re-export them.

**Note on the brief's assumption**: `knowledge/` is a separate
**top-level** package (`knowledge/`, a sibling of `ai/`, not
`ai/knowledge/`), and there is no dedicated `ai/security/` folder —
AI-relevant safety logic lives in `ai/validation/safety.py`, and
Telegram-side security lives in `telegram/owner/security.py`. This
document records the real structure rather than the assumed one, per
Constitution Article 7 (Reuse Principle — audit before asserting).
`media/` is the same shape — a separate **top-level** package, a
sibling of `ai/`, not `ai/media/` (a Phase 63.7 brief assumed the
latter; see `docs/PHASE63_7_AUDIT.md`). `broadcast/` is the same shape
a third time — not `ai/broadcast/` (a Phase 63.8 brief assumed the
latter; see `docs/PHASE63_8_AUDIT.md`). `voice/` (Phase 65.0) is also a
separate top-level package, not `ai/voice/` — but unlike the three
corrections above, this is not a naming discrepancy: neither path
existed before Phase 65.0 (see `docs/PHASE65_0_AUDIT.md`).

### Top-level Intelligence packages (siblings of `ai/`)

| Module | Real responsibility | Depends on |
|---|---|---|
| `media/` | `MediaManager`'s two surfaces: Owner ENABLED/DISABLED intent per `MediaType` (Phase 63.0), extended Phase 63.7 with a deterministic `MediaAsset` surface (`create_asset`/`validate_asset`/`prepare_asset`/`get_asset`); `media_registry.py` (`MediaDescriptor`, `get`/`exists`, Phase 63.0/63.7); `models.py`/`media_adapter.py`/`media_pipeline.py` (Phase 63.7) | `ai/content/` (type-only), `core/` — never `broadcast/`/`translation/` (Intelligence Dependency Principle) |
| `broadcast/` | `BroadcastManager`'s two surfaces: `would_broadcast`/`prepare` (real `BroadcastRequest` builder, Phase 63.0), extended Phase 63.8 with a deterministic `BroadcastAsset` surface (`create_broadcast`/`validate_broadcast`/`prepare_broadcast`/`get_broadcast`/`list_broadcasts`); `provider_manager.py`/`trigger_manager.py`/`models.py` (Phase 63.0, extended 63.8 with `TELEGRAM`/`MINI_APP`/`BroadcastTriggerType`); `broadcast_adapter.py` (Phase 63.8) | `media/` (type-only), `ai/content/` (type-only), `ai/persona/` (type-only), `core/` — never `decision/`/`risk/`/`execution/`/`strategies/`/`signals/` |
| `voice/` | `VoiceManager`'s deterministic surface: profile ops delegated to `VoiceProfileRegistry`, provider ENABLED/DISABLED intent tracking, `validate`/`prepare` request lifecycle (Phase 65.0), extended Phase 65.1 with a real adapter registry (`register_adapter`/`get_adapter`) and per-profile provider selection (`set_provider_for_profile`/`provider_for_profile`); `models.py` (`VoiceProvider`/`VoiceProfile`/`VoiceSettings`/`VoiceRequest`/`VoiceResult`); `profiles.py`/`providers.py` (static catalogs, LOCKed); `registry.py` (`VoiceProfileRegistry`); `provider_contract.py` (`VoiceProviderContract`, Phase 65.1); `provider_adapters/` (real OpenAI/ElevenLabs TTS + Local/Custom skeletons, Phase 65.1); `adapter.py` (`content_result_to_voice_request` Phase 65.0, `media_asset_to_voice_request`/`broadcast_asset_to_voice_request`/`conversation_turn_to_voice_request` Phase 65.1); `runtime.py` (`VoiceRuntime`, thin façade, extended Phase 65.1 with `generate_audio`/`generate_with_fallback`); `stt/` (`STTProviderContract`/`STTManager`/real OpenAI Whisper + Local/Custom skeletons, Phase 65.2); `intents/` (`VoiceIntent`/`detect_intent()`, Phase 65.2); `session/` (`VoiceSession`/`VoiceSessionManager`, Phase 65.2); `conversation_bridge.py` (`handle_voice_turn()`, the real STT→Conversation→TTS composition root, Phase 65.2) | `ai/content/` (type-only), `media/` (type-only, Phase 65.1), `broadcast/` (type-only, Phase 65.1), `ai.session`/`ai.conversation` (type-only in `adapter.py`; `conversation_bridge.py` alone calls the real `ai.conversation.conversation_engine.ConversationEngine.ask()`, Phase 65.1/65.2), `core/` — never `translation/`/`decision/`/`risk/`/`execution/`/`strategies/`/`signals/`/`ai.memory`/`ai.reasoning`/`ai.explanation`/`knowledge` (Phase 65.2 Rule 2, zero exemptions) |

## Related documents

- `docs/architecture/ARCHITECTURE_MASTER.md` — the layer diagram and
  per-layer CAN/CANNOT this document's dependencies serve.
- `docs/architecture/IMPORT_RULES.md` — the allowed/forbidden import
  table this document's dependencies are checked against.
