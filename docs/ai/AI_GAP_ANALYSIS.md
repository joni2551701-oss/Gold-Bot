# AI_GAP_ANALYSIS.md — TASK-AI-000 Phase 8: Gap Analysis

Status: **AUDIT ONLY**. No code changed. "Today's AI" is
`AI_FILE_TREE.md`/`AI_DEPENDENCY_GRAPH.md`/`AI_FOUNDATION_READINESS.md`'s
findings; "Ideal AI" is the Director's own Phase 5/7 vocabulary
(Manager/Registry/Factory/Lifecycle/Interfaces; Persona/Senior/
Seniorita/Media/Platform/Memory/Voice/Vision/Agent placement — answered
in `AI_REFACTOR_RECOMMENDATIONS.md`'s Phase 7 section).

| # | Gap | Current | Target | Priority | Est. Complexity | Risk | Dependency |
|---|---|---|---|---|---|---|---|
| 1 | No unified `AIManager` | 7+ domain-scoped managers (`ProviderManager`, `CapabilityManager`, `SessionManager`, etc.) + 2 composition roots (`IntelligenceRuntime`, `AIService`), no single top-level entry point | A thin `AIManager` facade composing the existing managers — not a rewrite, a wrapper | Medium | Low (facade only; every underlying piece already exists) | Low — additive, no existing contract changes | None of the pieces it wraps need to change first |
| 2 | No unified `AI Registry` | 6 per-subsystem registries with 2 incompatible shapes (`XRegistry` class vs. `build_x_registry()` function) | Standardize on one shape, then optionally compose into one registry-of-registries | Low | Medium (touches 6 files, all internal, no external callers per README) | Low — internal-only APIs, no `__init__.py` exports to break | Should follow, not precede, resolving the `*_registry.py` naming inconsistency in AI_RISK_REPORT.md |
| 3 | No `Factory` class | `build_provider_registry()`/`build_default_tool_registry()` fill the role functionally | Formalize as `ProviderFactory`/`ToolFactory` if the codebase ever needs runtime (not just import-time) construction | Low | Low | Low | None — cosmetic naming, not a functional gap |
| 4 | 4 real circular dependencies | `runtime↔providers`, `audit↔runtime`, `audit→runtime→router→audit`, `explanation↔content` | Acyclic subpackage graph | **High** (esp. the `explanation↔content` cycle, which contradicts a documented rule) | Medium (each cycle needs an extracted shared module or an inverted dependency) | Medium — current cycles are stable but fragile; a careless future edit could break imports | None — can be tackled independently per cycle |
| 5 | Duplicate `TradeJournalEntry` class name | Two unrelated classes, same name, different modules, both live | Rename one (likely the older `ai/journal/trade_journal.py` one, since the newer one already carries a disambiguating docstring) | **High** | Low (rename + update ~10 call sites per AI_DEPENDENCY_GRAPH.md) | Medium — silent wrong-import risk today | None |
| 6 | `ai/trade_journal.py` shim permanently unreachable | Dead file, shadowed by `ai/trade_journal/` package | Delete the shim (it can never be imported by any interpreter) | Medium | Trivial | Low — confirmed zero real-world callers | Should happen alongside gap 5 to avoid two passes over the same area |
| 7 | 3 additional dead files (`ai/analyzer/ai_analyzer.py`, `ai/ai_prompt.py`, `ai/confidence_model.py`) | Zero callers, zero test coverage | Delete or document as intentionally-reserved | Low | Trivial | Low | None |
| 8 | Every `__init__.py` empty — no enforced public API surface | Convention-only isolation | Add `__all__`/re-exports to the highest-traffic subpackages (`ai.runtime`, `ai.providers`, `ai.access`) first | Low | Medium (touches every consumer's import path if done repo-wide; safe if additive-only) | Low if additive, Medium if it changes existing import paths | Should follow cycle resolution (gap 4), since a real `__init__.py` export makes accidental cross-cycle imports easier to introduce, not harder, without also fixing the cycles first |
| 9 | `assistant/` (Personal AI) has only one narrow, well-tested seam into `ai/` | `runtime_adapter.py` is the sole importer of `ai.memory`/`ai.conversation`/`ai.intelligence_runtime`, enforced by an isolation test | No gap — this is the healthiest boundary in the audit (see AI_ARCHITECTURE_REVIEW.md) | — | — | — | — |
| 10 | No formal internal layering document for `ai/` (unlike Trading Core's documented pipeline) | One informal rule stated in a single file's docstring (`content_adapters.py`'s "Intelligence Dependency Principle"), and it's violated by gap 4 | A short `ai/ARCHITECTURE.md` (or extend `docs/ai/AI_ARCHITECTURE.md`) stating the intended subpackage layering explicitly | Medium | Low (documentation only) | Low | Should be written only after gap 4 is resolved, so it describes the true state rather than an aspirational one |
| 11 | Vision/Voice/Senior/Seniorita/Agent System have no placement decision in `ai/` | `ai/chart_intelligence/` has a placeholder `ChartVisionProviderType` enum only; Voice lives entirely outside `ai/` in the separate `voice/` package (out of this audit's scope, but flagged in `docs/CONSTITUTION_V2_AUDIT.md`); no Senior/Seniorita/Agent System code exists anywhere | See `AI_REFACTOR_RECOMMENDATIONS.md` Phase 7 for the Director's requested placement answers | Medium (architecture decision, not urgent) | N/A — decision, not implementation | Low (no code exists yet to be at risk) | Should be decided before any of these are implemented, to avoid a fifth full subpackage rewrite |

## Priority summary

| Priority | Gaps |
|---|---|
| High | #4 (circular dependencies), #5 (duplicate class name) |
| Medium | #1 (AIManager facade), #6 (dead shim), #10 (layering doc), #11 (Vision/Voice/Senior/Seniorita/Agent placement) |
| Low | #2 (registry unification), #3 (Factory naming), #7 (3 dead files), #8 (`__init__.py` exports), #9 (no gap) |

No implementation is proposed by this audit — see
`AI_REFACTOR_RECOMMENDATIONS.md` for concrete (still unapplied)
remediation shapes, and `AI_FOUNDATION_READINESS.md`/`WORKER_REPORT.md`
for the overall readiness verdict this feeds into.
