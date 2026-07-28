# AI_CLEANUP_REPORT.md — TASK-AI-000A: AI Architecture Cleanup

Status: **IMPLEMENTED**. This document records what TASK-AI-000A
actually changed. Scope was `ai/` architecture cleanup only —
circular-dependency removal, duplicate-class resolution, naming
consistency, import cleanup, dependency direction. No new AI feature
was added. Dead files were **not** touched (deferred to TASK-AI-000B
per the Director's own instruction). Trading Core is zero-diff.

All changes were made with the Director's approved Stage-1 strategy
priority — (1) shared-abstraction extraction, (2) neutral module,
(3) dependency injection, (4) EventBus only if needed — and **no lazy
import and no temporary hack** were used anywhere.

## Stage 1 — Circular Dependency Cleanup

The TASK-AI-000 audit found **4 real circular subpackage
dependencies**. All 4 are now removed. Post-cleanup cycle count
(AST-based detector over `ai/`, `if TYPE_CHECKING:` blocks excluded):
**0 cycles, acyclic, 39 nodes / 88 edges.**

### Cycles 1–3 (the runtime/providers/router/audit cluster) — one fix

- `ai.runtime ↔ ai.providers`
- `ai.audit ↔ ai.runtime`
- `ai.audit → ai.runtime → ai.router → ai.audit` (3-node)

**Root cause:** all three back-edges existed only because the shared
event-bus primitive (`EventBus`/`EventType`/`RuntimeEvent`) lived
*inside* `ai/runtime/`, so `ai/providers/circuit_breaker.py` and
`ai/audit/provider_stats.py` had to import *up* into `ai/runtime/`
while `ai/runtime/` imported *down* into providers/audit/router.

**Fix (approved strategy #1/#2):** the event bus was relocated to a
neutral top-level module, `ai/runtime/event_bus.py` → **`ai/event_bus.py`**.
`event_bus.py` depends only on `core.logger` + stdlib (no `ai/`
dependency), so every consumer now depends on it *downward*. The three
cycles vanish at once — the minimal cut that breaks all of them. The
`EventBus`/`EventType`/`RuntimeEvent` public classes are byte-for-byte
unchanged; only the module's import path moved. 14 code files (7
source, 7 test) updated from `ai.runtime.event_bus` → `ai.event_bus`.

### Cycle 4 (`ai.explanation ↔ ai.content`) — HIGH priority, two fixes

This cycle also violated the documented **Intelligence Dependency
Principle** (`docs/policies/DIRECTOR_POLICY.md`: Explanation sits
strictly *upstream* of Content). Two explanation→content edges were
the violation; the one content→explanation edge is the correct
direction and was kept.

- **Edge B** — `ai/explanation/explanation_content_adapter.py` imported
  `ai.content.broadcast_output.BroadcastReadyContent`. **Fix:** the
  adapter (which bridges an upstream `ExplanationOutput` into a
  content-package type) was moved **into `ai/content/`**, the
  downstream package that is legitimately allowed to import
  `ai/explanation/`. No production code called it (foundation-only per
  its own docstring); its single test moved with it
  (`tests/ai/explanation/` → `tests/ai/content/`).
- **Edge A** — `ai/explanation/explanation_output.py` imported
  `ai.content.content_types.ContentType`, because `ExplanationOutput`
  has a public, test-locked `content_type: Optional[ContentType]`
  field. **Fix (approved strategy #1):** `ContentType` was extracted
  to a neutral top-level module, **`ai/content_types.py`**. It is a
  genuinely cross-cutting vocabulary used by 5 packages across the
  pipeline (`ai/explanation/`, `ai/trading_analyst/`,
  `ai/chart_intelligence/`, `ai/content/`, `broadcast/`), so a neutral
  home is architecturally correct, not just cycle-breaking. Only the
  enum moved; the content-service-internal, `Capability`-based helpers
  (`CONTENT_CAPABILITIES`, `is_content_capability()`, `content_title()`)
  stay in `ai/content/content_types.py`. 21 files updated (19
  ContentType-only imports via exact-line replace, 2 mixed imports
  split by hand); 5 docstring path references updated.

The Intelligence Dependency Principle is now restored:
`ai/content/content_adapters.py` imports `ai/explanation/`
(content downstream of explanation) and nothing in `ai/explanation/`
imports `ai/content/`.

## Stage 2 — Duplicate Class Resolution

Two unrelated classes were both named `TradeJournalEntry`:
`ai.journal.trade_journal.TradeJournalEntry` (Phase 55, a
`signals.SignalType`-coupled completed-trade record) and
`ai.trade_journal.models.TradeJournalEntry` (Phase 66.2, a narrative
journal entry). The name is now unique.

**Approved decision applied:** the older, Trading-Core-coupled
*record* was renamed **`TradeJournalEntry` → `TradeJournalRecord`**
(the newer *narrative entry* keeps `TradeJournalEntry`, since it is
the more actively extended of the two and already carried a
disambiguating docstring). This was the lower-blast-radius choice: the
old class had only 3 real code importers vs. ~20 for the new one.
Fields and the `create_journal_entry()` factory are unchanged — only
the class name. Consumers updated: `ai/context/context_builder.py`,
`ai/context/context_snapshot.py`, `ai/trade_journal.py` (the shim's
re-export), plus a docstring in `ai/journal/failure_analysis.py`.

Public API stability: no external caller passed a `TradeJournalEntry`
by name to a public signature (the class was consumed as a type
annotation and via the unchanged factory); the rename is documented in
`COMPATIBILITY_REPORT.md`. No backward-compat alias was added — an
alias would reintroduce the exact duplicate name this stage removes.

## Stage 3 — Naming Consistency

The two Stage-1/Stage-2 moves already improved naming materially: the
event bus and content-type vocabulary now sit at honest neutral paths,
and the trade-journal class name is unique. Remaining naming findings
from the TASK-AI-000 audit were assessed:

- **`*_registry.py` two-shape inconsistency** (class-based
  `PromptRegistry`/`ToolRegistry` vs. function-based
  `build_x_registry()`): **deferred**, not changed. "Registry" is
  explicitly a TASK-AI-001 concept on this task's Forbidden list, and
  standardizing the registry shape is Foundation-Activation work, not
  cleanup. Recorded here for TASK-AI-001's Phase B (Registry).
- **File-name shorten outliers** (`chart_runtime.py`,
  `analyst_runtime.py`, `journal_runtime.py`) and **compound
  subpackage names** (`chart_intelligence`, `trade_journal`,
  `trading_analyst`): left as-is. Renaming them is pure churn with no
  correctness or dependency benefit, and each keeps its full,
  descriptive class name; changing them would risk regressions for a
  cosmetic gain the Director's "no unnecessary refactor" rule
  discourages.

## Stage 4 — Import Cleanup

- `pyflakes` over every tracked `.py`: **reports nothing** — zero
  unused imports, zero redefinitions, including all 46 changed files.
- **Zero wildcard imports** anywhere in `ai/` or `broadcast/`
  (verified with an anchored `^\s*from \S+ import \*` grep).
- No duplicate imports were introduced; the two mixed-import splits
  (`ai/content/content_adapter.py`, `tests/ai/content/test_content_types.py`)
  produce two clean, distinct import lines each.

## Stage 5 — Dependency Direction

The corrected graph is acyclic and flows in one direction. The neutral
primitives (`ai/event_bus.py`, `ai/content_types.py`) sit at the
foundation level with no `ai/` dependencies of their own; the
runtime/provider/router/audit cluster and the content/explanation
cluster now have strictly one-directional edges. See
`UPDATED_DEPENDENCY_GRAPH.md` and `IMPORT_GRAPH.md` for the full
before/after graph.

## Validation summary (all green)

| Check | Result |
|---|---|
| Circular dependencies (AST, TYPE_CHECKING-excluded) | **0** (was 4) |
| Duplicate class-name conflicts | **0** (`TradeJournalEntry` now unique) |
| Wildcard imports (`ai/`, `broadcast/`) | **0** |
| pyflakes | clean |
| compileall | pass |
| pytest | **4609 passed** |
| python main.py smoke | OK, baseline log shape |
| Trading Core diff (`core/decision/risk/execution/strategies/signals/context/data/lifecycle/database`) | **zero** |
| Files changed | 46 (all under `ai/`, `broadcast/`, `telegram/owner/`, `tests/`) |
