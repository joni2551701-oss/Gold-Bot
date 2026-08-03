# AI Intelligence Layer (Phase 61.3)

The fourth v0.4 AI Core phase. Where 61.0/61.1/61.1.1 built foundation
pieces and 61.2 built the first real end-to-end request lifecycle
(`AIService.ask()`), 61.3 makes that lifecycle *usable* — a context
adapter, a static knowledge base, real (read-only) tool logic, a
conversation loop, a memory facade, an explanation wrapper, request
tracing, and a provider ranking function. Full reuse audit:
`docs/PHASE61_3_INTELLIGENCE_AUDIT.md` (TASK 1).

**Still AI Runtime, not AI Trading.** Every module below inherits
`AIService.ask()`'s own isolation guarantee — see "Isolation
re-verification" below for the closing AST sweep.

## TASK 2 — AI Context Intelligence

`ai/context/context_adapter.py` gained `market_context_from_snapshot(schema)`
— the `context.snapshot.ContextSnapshotSchema -> ai.interfaces.MarketContext`
adapter TASK 1's audit found missing. Takes an *already-built* schema
(`context.snapshot.from_context_snapshot()`'s own output) via a
`TYPE_CHECKING`-only reference, never a real import of `context/` —
the same pattern `ai/prompts/prompt_manager.py`'s
`get_fundamental_analysis_prompt()` established in Phase 60.5 for
`FundamentalContextSnapshot`. Formats `structure`/`liquidity`/`zones`/
`session`/`regime` into `MarketContext.summary`; never recomputes any
of them. Verified via a fresh-process `sys.modules` check that
importing this module never pulls in `context`/`context_layer.context_engine.snapshot`.

## TASK 3 — AI Knowledge Foundation

`knowledge/` (new top-level package, zero dependencies): six flat
category files (not literal subdirectories — see
`docs/PHASE61_3_INTELLIGENCE_AUDIT.md`'s "Structural adaptation")
— `smc.py`, `wyckoff.py`, `risk.py` (traced to `context/*.py`'s own
detection rules, `docs/WYCKOFF.md`, `risk/README.md`), `psychology.py`
(general, non-proprietary trading-discipline concepts — GoldBot itself
detects none of these states), `examples.py` (the exact worked
examples `docs/MARKET_REGIME.md`/`docs/EXPLAINABILITY.md` already
committed to), `faq.py` (GoldBot's own documented behavior, traced to
`CLAUDE.md`/`ai/README.md`). `registry.py` composes all six into
`get_entry(key)` / `entries_by_category(category)` / `search(query)` /
`all_entries()`, raising at import time on a duplicate key. 26 entries,
14 tests (`tests/knowledge/test_knowledge_registry.py`), including an
AST-based isolation test confirming `knowledge/` never imports
`decision/`/`risk/`/`execution/`/`strategies/`/`database/`/`telegram/`.

## TASK 4 — Real AI Tool Calling

All five `ai/tools/*.py` tools (`market_tool`, `news_tool`,
`analytics_tool`, `education_tool`, and a new `learning_tool`) replaced
their placeholder stub bodies with real, read-only formatting logic —
`ai/tools/tool_registry.py`'s `BaseAITool`/`ToolRegistry` contract is
unchanged. **Architecture correction from TASK 1's own audit**: the
audit's initial plan (tools reading `database/*_repository.py`
directly) was rejected before implementation — zero precedent exists
anywhere in `ai/` for a direct `database/` import (confirmed by grep),
and `ai/README.md`'s own Dependencies section already states "an AI
provider must never reach [database/] directly." Instead, every tool
now accepts an **already-built** input object via `run(**kwargs)`,
matching this codebase's existing dependency-injection convention:

| Tool | Accepts | Reuses |
|---|---|---|
| `market_tool` | `market_context: MarketContext` | `ai.interfaces.MarketContext` |
| `news_tool` | `fundamental: FundamentalContextSnapshot` (`TYPE_CHECKING`-only) | same pattern as TASK 2 |
| `analytics_tool` | `performances: Sequence[SignalPerformance]` | `analytics.strategy_report.build_strategy_report()` (the same `ai/` → `analytics/` import `ai/learning_context.py` already established, Phase 60.6) |
| `education_tool` | `key` or `query` | `knowledge/registry.py` (TASK 3) |
| `learning_tool` (new) | `learning_context: LearningContext` | `ai.learning_context.LearningContext` (unmodified, Phase 60.6/60.7) |

No tool fetches its own data; every one formats data a caller already
legitimately built. 15 tests (`tests/ai/tools/test_tool_registry.py`).

## TASK 5 — Conversation Engine

`ai/conversation/conversation_engine.py`'s `ConversationEngine` — the
first real caller of two foundation packages built but never used:
`ai/session/` (Phase 61.0 TASK 7) and `ai/runtime/ai_service.py`
(Phase 61.2), both unmodified in shape. Flow: get-or-create
`ConversationState` (`SessionManager`) → record the user's turn →
`ContextWindow`-trim recent history into a prompt → `RuntimeRequest`
(`capability=CHAT`) → `AIService.ask()` → on acceptance, record the
assistant's turn → return the `RuntimeResponse` plus `session_id`.
Requires an already-built `AIContext` from the caller (via
`build_ai_context()`) rather than constructing one itself — a raw
`AIContext()` leaves `snapshot_id=None`, which the cache-key builder
rejects.

**Necessary correctness fix to `ai/runtime/ai_service.py`** (the one
non-additive change this phase makes to Phase 61.2 code): the cache
key's `context_hash` previously defaulted to `ai_context.snapshot_id`
alone, which never varies with `request.prompt` — meaning two
different explicit CHAT messages against the same market snapshot
would have collided on one cache entry and silently returned the first
question's answer to the second. Fixed by hashing the *resolved*
prompt text instead, via `build_cache_key_from_context()`'s existing
(Phase 61.1.1) `context_hash` override parameter — no new parameter, no
`CacheKey` field change. Still produces an identical key for two calls
with an identical resolved prompt (the market-analysis-template path,
where `PromptManager` templates are a pure function of `MarketContext`
with no timestamp interpolation), so every pre-existing cache-hit test
still passes. 6 tests (`tests/ai/conversation/test_conversation_engine.py`).

## TASK 6 — Memory Runtime

`ai/memory/memory_runtime.py`'s `MemoryRuntime` — a thin facade over
five namespaced `ai.memory.context_memory.ContextMemory` instances
(`MemoryLayer.CONVERSATION`/`USER`/`TRADE`/`LEARNING`/`MARKET`), not
five new storage implementations. `ContextMemory` (Phase 55, confirmed
unused in production by TASK 1's audit) is unmodified — still
in-process, in-memory only, no persistence. 7 tests
(`tests/ai/memory/test_memory_runtime.py`).

## TASK 7 — Explanation Engine

`ai/explanation/explanation_engine.py`'s `ExplanationEngine` wraps
`AIService.ask()` (unmodified) for four capability-shaped questions:

- `explain_signal(SignalExplanation, ...)` — `Capability.EXPLANATION`,
  the only one of the four with a real `BaseAIProvider` method mapping
  today. Reuses `signal_layer/signal_scoring/explainability.py`'s already-computed
  `SignalExplanation` (`ai/` → `signals/` is the one sanctioned
  cross-layer import; `explanation_engine.py` never recomputes signal
  reasoning).
- `summarize_report(report_text, ...)` — `Capability.SUMMARY`.
- `explain_topic(key, ...)` — `Capability.EDUCATION`, looks up a
  `knowledge/registry.py` entry (TASK 3) first.
- `analyze_market(...)` — `Capability.ANALYSIS`, a thin passthrough
  (`AIService` already derives the prompt from `market_context`).

SUMMARY and EDUCATION are always cleanly rejected by `AIService.ask()`
itself ("no runtime method mapping yet") — a pre-existing gap from
Phase 61.2 this module does not attempt to close; the request shape is
built correctly so a future phase only needs to add a provider-side
method, not touch this engine. 7 tests
(`tests/ai/explanation/test_explanation_engine.py`).

## TASK 8 — Runtime Trace

`RuntimeResponse` gained `request_id: Optional[str] = None` (additive).
`AIService.ask()` now surfaces the `AIRequestLogEntry.request_id`
(already-generated UUID, `ai/audit/request_log.py`, no new ID scheme)
on the two return paths where exactly one request-log entry
corresponds to the response (validation-rejected, success). `None` on
every other path: an early rejection before a provider was attempted
(access/capability/prompt), a cache hit (no provider call happened, so
nothing was logged as a request), and the final "every provider
failed" rejection (multiple attempts logged, no single one to point
to).

`ai/audit/trace.py` (new file inside the existing `ai/audit/`
package): `trace_request(request_log, response_log, request_id) ->
RuntimeTrace` — a read-only join over `RequestLog.all()`/
`ResponseLog.all()`, neither log class modified. Never raises: an
unknown `request_id` returns a `RuntimeTrace` with `request=None` and
an empty `responses` list. 5 tests
(`tests/ai/audit/test_runtime_trace.py`).

## TASK 9 — Provider Benchmark

`ai/audit/provider_stats.py` extended in place (no new module):
`rank_providers(stats: Dict[str, ProviderStats]) -> List[ProviderStats]`
— best-first, primary key `success_rate` descending, tiebreaker 1
`avg_latency_ms` ascending, tiebreaker 2 `total_cost` ascending. Over
`ProviderStats`'s existing, unmodified fields — no new metric. Still
observability only: nothing in `ai/router/` or `ai/runtime/` calls this
function. 5 tests (in `tests/ai/audit/test_ai_audit.py`).

## Isolation re-verification (TASK 10, matching Phase 61.2's own closing step)

AST-based import sweep (`ast.walk()` over every `.py` file under
`ai/`), re-run at the end of this phase:

| Target | Import sites found |
|---|---|
| `decision/` | **0** |
| `risk/` | **0** |
| `execution/` | **0** |
| `strategies/` | **0** |
| `signals/` | 7 (6 pre-existing + `ai/explanation/explanation_engine.py`, new this phase — `signal_layer.signal_scoring.explainability`, the layer immediately below `ai/`) |
| `database/` | **0** |
| `telegram/` | **0** |

`context/` appears in 6 `ImportFrom` nodes total, but a second sweep
distinguishing `TYPE_CHECKING`-guarded imports from runtime ones shows
only 3 are real runtime imports — and all 3 (`ai/ai_analyzer.py`,
`ai/ai_prompt.py`, `ai/confidence_model.py`) predate this entire v0.4
AI Core arc (the pre-existing, separately-documented production
`ai_analyzer.py` path — see `ai/README.md`'s own "Dependencies"
section). The other 3 (`ai/context/context_adapter.py`,
`ai/prompts/prompt_manager.py`, `ai/tools/news_tool.py`) are all
`TYPE_CHECKING`-only, zero runtime dependency on `context/` — no new
runtime `ai/` → `context/` edge was introduced this phase.

`knowledge/` was checked separately (it sits outside the `ai/` → ...
chain entirely): zero imports of `decision/`/`risk/`/`execution/`/
`strategies/`/`database/`/`telegram/` anywhere in the package.

## Not wired

`ai/conversation/`, `ai/explanation/`, `ai/memory/memory_runtime.py`,
`ai/audit/trace.py`, and `knowledge/` are not called from
`core/pipeline.py`, any live Telegram handler, or
`platform_layer/telegram/command_router.py` — foundation only, same posture as every
prior Phase 61.x module. `platform_layer/telegram/command_router.py`'s
`_parse_command()` still requires a leading `/`; no free-text/
conversational handling exists anywhere in `telegram/` (confirmed by
TASK 1's own audit).

## Tests

342 tests across `tests/ai/` and `tests/knowledge/` (up from 291 at
the start of this phase), zero regressions in the pre-existing suite.

## Deliberately out of scope (Director's own unnumbered material)

AI Identity Layer (`identity/persona.py`/`behavior.py`/`style.py`/
`rules.py`), Broadcast Foundation (`broadcast/`), Media Capability enum
additions (TEXT/IMAGE/VIDEO/VOICE/VISION/DOCUMENT/LIVE/BROADCAST),
Owner Command Foundation for future commands, and the v0.6 Telegram
Ecosystem roadmap were all presented as forward-looking vision in the
Phase 61.3 brief but never given their own numbered TASK — treated as
context for a future phase, not commissioned work, matching this
session's established discipline of only executing explicitly-numbered
TASK items from a formal brief.
