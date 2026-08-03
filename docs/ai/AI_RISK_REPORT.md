# AI_RISK_REPORT.md — TASK-AI-000 Validation Findings

Status: **AUDIT ONLY**. No code changed. Covers the Director's
explicit Validation checklist: import errors, circular dependency,
duplicate modules, duplicate services, dead code, unused files, unused
classes, unused imports, naming consistency, package consistency.
Each finding rated Severity (High/Medium/Low) and Likelihood of causing
a real problem if left unaddressed.

## Import errors

**None found.** No file under `ai/` fails to import; the 4 real
cycles (below) do not currently raise `ImportError` because no two
cycle-participating modules import each other's *importer* module
directly — but this is fragile, not structurally guaranteed. Severity:
Low today, Medium as latent risk (see Circular dependency below).

## Circular dependency — 4 real cycles

| Cycle | Severity | Likelihood | Note |
|---|---|---|---|
| `ai_layer.ai_engine.runtime ↔ ai.providers` | Medium | Low (currently stable) | A future refactor to either file that adds one more cross-import could trip a real `ImportError` with no warning today |
| `ai_layer.ai_service.audit ↔ ai.runtime` | Medium | Low | Same class of latent risk |
| `ai_layer.ai_service.audit → ai.runtime → ai.router → ai.audit` (3-node) | Medium | Low | Same class of latent risk, larger blast radius (3 subpackages) |
| `ai_layer.explanation_ai ↔ ai.content` | **High** | Medium | Directly contradicts a **documented** architectural rule (`ai/content/content_adapters.py`'s own "Intelligence Dependency Principle" states Explanation sits upstream of Content) — this is a real, self-acknowledged design violation, not just a structural tangle |

Full evidence in `AI_DEPENDENCY_GRAPH.md` Section 3. No fix is
proposed here — see `AI_REFACTOR_RECOMMENDATIONS.md`.

## Duplicate modules / services

| Finding | Severity | Detail |
|---|---|---|
| Two unrelated classes both named `TradeJournalEntry` | **High** | `ai/journal/trade_journal.py:20` (Phase 55, `SignalType`-coupled) vs `ai/trade_journal/models.py:38` (Phase 66.2, primitive-only). Both are live and imported by multiple other subpackages/top-level packages. The collision is self-documented in `ai/trade_journal/models.py:13-20`'s own comment, but self-documentation doesn't prevent a future engineer from importing the wrong one by name-only reasoning. |
| `ai_layer/knowledge_ai/knowledge_base/trade_journal.py` (shim) permanently shadowed by `ai/trade_journal/` (package) | **Medium** | Same import name, same parent directory — Python always resolves the package over the sibling module, so the shim is unreachable by any interpreter, confirmed empirically. Not a runtime bug (nothing calls it), but dead, misleading code that looks load-bearing from its docstring. |
| `ai/content/content_adapter.py` vs `ai/content/content_adapters.py` | Low | Not a functional duplicate — singular defines `ContentEngine`, plural defines two unrelated adapter functions — but the near-identical filenames in the same directory are a readability/maintenance hazard. |
| `ai/analyzer/ai_analyzer.py` vs `ai_layer/ai_engine/ai_analyzer.py` | Low | Re-export shim in the opposite direction of the `trade_journal` case; unlike that case this one is not shadowed (it's importable), it is simply unused (see Dead code below). |
| `*_registry.py` naming inconsistency | Medium | `prompt_registry.py`/`tool_registry.py` implement a stateful `XRegistry` class; `memory_registry.py`/`persona_registry.py`/`capability_registry.py`/`reasoning_registry.py` implement no class at all, just a `build_x_registry()` free function. Same filename suffix, two incompatible architectural patterns — increases onboarding cost and risks a future subpackage picking the "wrong" one inconsistently. |

## Dead code / unused files

| File | Severity | Evidence |
|---|---|---|
| `ai/analyzer/ai_analyzer.py` | Low | Zero references anywhere in the repo to `ai_layer.ai_engine.ai_analyzer` or `ai_layer.ai_engine` outside its own docstring; zero test coverage in `tests/`. |
| `ai_layer/knowledge_ai/knowledge_base/trade_journal.py` (top-level shim) | Low (unreachable, not harmful) | Permanently shadowed by the `ai/trade_journal/` package — see Duplicate modules above. |
| `ai_layer/ai_engine/ai_prompt.py` | Low | No file anywhere imports it (`from ai.ai_prompt import`/`from ai import ai_prompt`/`import ai.ai_prompt` all return 0 hits); only comment/docstring mentions exist. |
| `ai_layer/confidence_ai/confidence_model.py` | Low | Only consumer is the also-dead `ai_layer/ai_engine/ai_prompt.py`; no other file references `confidence_model` or `ConfidenceResult`. |

All four are transitively dead — nothing exercises them at runtime,
none appear in any test file. Severity is Low individually (no runtime
impact, since nothing calls them), but collectively they are a
maintenance-burden and a "looks-official-but-isn't" trap for a future
engineer skimming `ai/` for a starting point.

## Unused classes

Checked all ~185 top-level class definitions. **Zero** classes have
literally zero references anywhere in the repo. Restricting to
"referenced only within their own defining file" surfaces 15 classes
(`RuntimeStateRecord`, `ReasoningTypeDescriptor`, `ProviderHealthRecord`,
`CacheEntry`, `RuntimeTrace`, `RuntimeMetrics`, `TrialEligibilityResult`,
`TrialStatus`, `ProviderScore`, `PromptVersionRecord`,
`MemoryScopeDescriptor`, plus `PromptPayload`/`ScoringConfig` in the
two dead files above, and 2 intentionally-private
underscore-prefixed classes). Severity: **Low** — 13 of the 15 are
internal data-holder types actively used by other functions in the
same, actively-imported module; only `PromptPayload` and
`ScoringConfig` are genuinely dead (their containing files are dead,
see above).

## Unused imports

**None found** — `python -m pyflakes` (run as part of the standard
Commit Protocol, most recently confirmed clean on commit `3baae51`)
covers this class of issue across the whole repository including
`ai/`, and reported nothing.

## Naming consistency

| Finding | Severity |
|---|---|
| Strong `XRuntime`/`XEngine`/`XManager` per-subpackage class convention (25 of 30 subpackages) | — (strength, not a finding) |
| 3 subpackages shorten their file name relative to the package name (`chart_intelligence/chart_runtime.py`, `trading_analyst/analyst_runtime.py`, `trade_journal/journal_runtime.py`) while keeping the full class name | Low |
| 3 of 30 subpackages use compound `snake_case` names (`chart_intelligence`, `trade_journal`, `trading_analyst`) vs. 27 single-word names | Low |
| `*_registry.py` filename-vs-pattern inconsistency | Medium (repeated from Duplicate modules above) |
| `ai/analyzer/` is structurally unlike every other subpackage — a single file that only re-exports a top-level module | Low |

## Package consistency

| Finding | Severity |
|---|---|
| All 30 subpackages have an `__init__.py`, but every one is completely empty — no subpackage has a public API surface at the package level | **Medium** — this is an architecture-wide risk, not a per-package one; see `AI_ARCHITECTURE_REVIEW.md`'s Clean Architecture section |
| README coverage: 13 of 30 subpackages have one, 18 don't (`ai/analyzer` has none, appropriately, being dead) | Low — no consistent rule for when a subpackage gets a README |
| `ai/analyzer/`, `ai/profiles/`, `ai/prompts/` lack a dedicated `tests/ai/<name>/` directory | Low — `profiles`/`prompts` are still tested via flat files directly under `tests/ai/`; only `ai/analyzer/` has zero coverage, consistent with it being dead |

## Confirmed non-findings (explicitly checked, clean)

- **No file under `ai/` imports `decision/`, `risk/`, `execution/`,
  `database/`, `telegram/`, or `strategies/`.** Anchored greps
  returned zero real import statements for all six; the rule holds
  with no exceptions. This is the single most safety-relevant check
  in this report, and it passed cleanly.

## Severity summary

| Severity | Count | Items |
|---|---|---|
| High | 2 | `explanation ↔ content` cycle contradicting documented rule; duplicate `TradeJournalEntry` class name |
| Medium | 5 | 3 latent import cycles; shim/package name collision; `*_registry.py` pattern inconsistency; empty `__init__.py` architecture-wide |
| Low | remainder | dead files, unused-outside-own-file classes, filename/naming outliers, README coverage gap |

See `AI_REFACTOR_RECOMMENDATIONS.md` for proposed (not applied)
remediation of the High and Medium items.
