# AI_REFACTOR_RECOMMENDATIONS.md — TASK-AI-000 Phase 7 (Future Architecture) + Refactor Recommendations

Status: **AUDIT ONLY — recommendations, not implementation**. Unlike
`docs/CONSTITUTION_V2_AUDIT.md`'s Open Questions (which the Director
explicitly said not to answer), the Director's Phase 7 instruction for
*this* task explicitly says "Worker quyidagi savollarga javob bersin"
— Worker should answer. The answers below are recommendations for
Director review, not applied changes; no code was written.

## Phase 7 — Future Architecture: answers

**AI Foundation qanday bo'lishi kerak? (What should the AI Foundation look like?)**
Not a rewrite — a thin composition layer over what already exists.
`AI_FOUNDATION_READINESS.md` found 4 of 7 core components already
fully functional (Session, Context, Lifecycle, Interfaces) and the
remaining 3 (Manager, Registry, Factory) missing only in *name*, not
in underlying capability. Recommend: introduce one `AIManager` facade
class in `ai/` (new file, e.g. `ai_layer/ai_engine/foundation.py` or extend
`ai_layer/ai_engine/intelligence_runtime.py` — per the Module Reuse Principle, extend
before creating) that composes `ProviderManager` + `CapabilityManager`
+ `SessionManager` + `RuntimeManager` behind one entry point, without
changing any of their internals. This closes the naming gap cheaply
and gives future subpackages one obvious place to register against.

**Persona Engine qayerda bo'lishi kerak? (Where should the Persona Engine live?)**
Stay exactly where it is: `ai/persona/`. It is correctly scoped today
(pure identity data, no prompt-building, no `AIService` calls) and is
already structurally separated from `assistant/`'s `AssistantIdentity`
by design (`ai_layer/ai_service/assistant/identity.py`'s explicit "never imports
`ai/persona/`" rule) — this is the one boundary in the whole audited
surface that needs no change.

**Senior qayerda yashaydi? (Where does "Senior" live?)**
No code for a "Senior AI" concept exists anywhere in `ai/` today (zero
grep hits). Recommend it follow the same pattern every 66.x
subpackage already uses successfully: a new `ai/senior/` subpackage
with `access.py` + `models.py` + `*_runtime.py`, consuming
`ai_layer.ai_engine.reasoning`/`ai_layer.knowledge_ai.memory_manager`/`ai.knowledge` the same way
`ai_layer.ai_engine.trading_analyst` does — not a new top-level package, not a
rewrite of an existing one.

**Seniorita qayerda yashaydi? (Where does "Seniorita" live?)**
Same answer and same reasoning as Senior — a sibling `ai/seniorita/`
subpackage following the proven 66.x template, if and when this
concept is formally scoped. Until a concrete responsibility is
defined for it (distinct from Senior's), no subpackage should be
created — this recommendation is placement guidance, not an
implementation request.

**Media qanday ulanadi? (How does Media connect?)**
Exactly as it already does for the existing 66.x subpackages:
transitively, through `ai_layer.ai_engine.intelligence_runtime.IntelligenceRuntime.run()`
and each subpackage's own `content_adapter.py` /
`*_to_content_body()` functions — never a direct
`ai/<subpackage>/ → media` import. `ai/chart_intelligence/` and
`ai/trading_analyst/` both already follow this pattern; it should
stay the template for Senior/Seniorita/any future subpackage.

**Platform qanday ulanadi? (How does Platform/Telegram connect?)**
It doesn't, and shouldn't, connect directly to `ai/` at all — this is
already a hard, correctly-enforced rule (`AI_DEPENDENCY_GRAPH.md`
confirms zero `telegram` imports anywhere in `ai/`). Platform reaches
AI capability only through `platform_layer/telegram/owner/ai_commands.py` (outside
this audit's scope) calling into `ai_layer.ai_engine.runtime.ai_service.AIService`,
never the reverse.

**Memory qayerga ulanadi? (Where does Memory connect?)**
Stays exactly as it is: `ai_layer.knowledge_ai.memory_manager.memory_runtime.MemoryRuntime`, a
5-layer facade, consumed directly by `ai_layer.personal_ai.interaction_manager` and
`ai_layer.ai_engine.reasoning`, and by exactly one external consumer,
`ai_layer/ai_service/assistant/runtime_adapter.py`, through a single confined import. This
one-writer-many-readers shape (per `AI_ARCHITECTURE_REVIEW.md`'s
Personal AI Review) is healthy and should be the template any future
Senior/Seniorita/Voice memory access follows — a single named adapter
file, never a direct scatter of `ai_layer.knowledge_ai.memory_manager` imports across many files.

**Voice qayerda bo'ladi? (Where does Voice live?)**
Stays outside `ai/` in the existing top-level `voice/` package — it
is out of this audit's scope by the Director's own instruction ("Audit
faqat ai/ moduli uchun"), and `docs/CONSTITUTION_V2_AUDIT.md` already
flagged a real, separate tension (`voice/`'s independent OpenAI
integration vs. Article 5's Provider Rule) that needs Director
resolution before any further Voice work — see that document's Section
5.2 and Open Question 2. Not re-litigated here.

**Vision qayerda bo'ladi? (Where does Vision live?)**
Inside `ai/chart_intelligence/`, which already reserves exactly this
role: `vision_provider_types.py`'s `ChartVisionProviderType` enum is
explicitly documented as "future vendor-choice vocabulary only," and
the subpackage's own README states "no Vision API, LLM, or image
recognition model is wired" yet. No new subpackage is needed — Vision
is Extension Point work inside an existing, already-reserved module,
consistent with the Module Reuse Principle.

**Agent System qayerda bo'ladi? (Where does an Agent System live?)**
No code for this exists anywhere in `ai/` today. If "Agent System"
means autonomous multi-step tool-calling, the foundation it would
build on already exists in `ai_layer.ai_service.tools` (`BaseAITool`/`ToolRegistry`,
5 tools registered) — recommend any future Agent System extend
`ai_layer.ai_service.tools` rather than create a new top-level orchestration package,
since the tool-calling contract is already there. This is explicitly
**not** a request to build one now — Trading Core rules (Constitution
Article 1, this repo's own CLAUDE.md) require any agentic system to
remain advisory-only, same as every other AI-layer component audited
here.

---

## Refactor recommendations (not applied — for Director approval)

These map directly to `AI_GAP_ANALYSIS.md`'s High/Medium items.

1. **Break the 4 circular dependencies** (AI_DEPENDENCY_GRAPH.md
   Section 3). For `runtime↔providers` and `audit↔runtime`: extract
   the shared piece (`EventBus`/`EventType`/`RuntimeEvent`) each side
   needs into a module neither `ai_layer.ai_engine.runtime` nor its counterpart owns,
   or accept the dependency as one-directional by having
   `circuit_breaker.py`/`provider_stats.py` take an `EventBus`
   instance as a constructor argument instead of importing it. For
   `explanation↔content`: since `content_adapters.py`'s own docstring
   already states the intended direction (Explanation upstream of
   Content), move `ExplanationOutput`/`BroadcastReadyContent`'s
   cross-references to use dependency injection or move the two
   colliding functions into a third, neutral module.

2. **Resolve the `TradeJournalEntry` name collision.** Rename
   `ai/journal/trade_journal.py`'s class (the older, Phase-55 one) to
   something disambiguating (e.g. `SignalTradeJournalEntry`), since
   the newer `ai/trade_journal/models.py` version already carries
   self-documentation acknowledging the collision and is the more
   actively-extended of the two. Update its ~6 known consumers
   (`database_layer/audit_log/audit_log_models.py`, `ai_layer/knowledge_ai/learning_loop/regime_memory.py`,
   `ai_layer/knowledge_ai/learning_loop/pattern_detector.py`, `ai_layer/knowledge_ai/learning_loop/models.py`,
   `core_layer/system_state/system_state.py`, `ai/context/`).

3. **Delete the 4 confirmed-dead files**: `ai_layer/knowledge_ai/knowledge_base/trade_journal.py`
   (permanently unreachable shim), `ai/analyzer/ai_analyzer.py`,
   `ai_layer/ai_engine/ai_prompt.py`, `ai_layer/confidence_ai/confidence_model.py`. Each has zero real
   callers and zero test coverage; deletion is zero-risk per the
   evidence in `AI_RISK_REPORT.md`.

4. **Standardize the `*_registry.py` pattern** on one shape (either
   always a stateful `XRegistry` class, or always a `build_x_registry()`
   free function) across `ai_layer.ai_engine.prompts`, `ai_layer.ai_service.tools`, `ai_layer.knowledge_ai.memory_manager`,
   `ai_layer.personal_ai.persona_manager`, `ai_layer.ai_engine.capabilities`, `ai_layer.ai_engine.reasoning` — internal-only
   change, no external callers per each subpackage's empty
   `__init__.py`.

5. **Write a short internal layering document** (extend
   `docs/ai/AI_ARCHITECTURE.md` rather than create a new file) stating
   the intended `ai/` subpackage dependency order explicitly, once
   recommendation 1 has actually made that order true.

6. **Do not touch `assistant/`'s boundary to `ai/`.** It is the
   healthiest coupling pattern found in this audit (single confined
   adapter file, externally enforced by an isolation test) — explicitly
   recommended as the template for any future Senior/Seniorita/Agent
   System integration, not as something needing its own fix.

None of the above is implemented by this audit, per the Director's
"Kod o'zgartirilmasin. Faqat audit." instruction.
