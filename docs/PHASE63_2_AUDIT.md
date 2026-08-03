# Phase 63.2 — AI Knowledge Intelligence Foundation: TASK 0 Audit

Per Constitution Article 11 (Foundation Reuse Law): every Worker
Brief's TASK 0 answers, for the capability about to be built —
Foundation / Manager / Contract / Model / Capability / Registry — does
it already exist? This audit answers that for Knowledge before any
code is written.

## Foundation Reuse Audit

| Component | Exists? | Real file(s) |
|---|---|---|
| Knowledge Foundation | ✅ Yes — **not** `ai/knowledge/`, see finding below | `knowledge/` (top-level package, Phase 61.3) |
| Knowledge Manager | ❌ No | none — `registry.py` exposes module-level functions, not a class |
| Knowledge Registry | ✅ Yes | `ai_layer/knowledge_ai/knowledge_base/registry.py` — `get_entry()`, `entries_by_category()`, `search()`, `all_entries()` |
| Knowledge Contract/Model | ✅ Yes (mostly) | `ai_layer/knowledge_ai/knowledge_base/models.py` — `KnowledgeCategory` (enum), `KnowledgeEntry` (frozen dataclass: `key`, `category`, `title`, `summary`, `tags`) — no `source` field yet |
| Knowledge Capability | ➖ Partial | `ai/capabilities/capability.py`'s `Capability.EDUCATION` is the closest existing member; no dedicated `KNOWLEDGE` member |
| `ai/persona/` (referenced for pattern) | ✅ Yes | `Persona`, `PersonaManager`, `persona_registry.py` (Phase 63.0) — the Manager-over-Registry pattern this phase's Manager follows |
| `ai/content/` (referenced for pattern) | ✅ Yes | `ContentRequest`/`ContentResult`/`ContentType` (Phase 61.5) — untouched this phase |
| `ai/explanation/` (referenced for integration) | ✅ Yes | `ExplanationBuilder`/`ExplanationInput`/`ExplanationOutput` (Phase 63.1) — untouched this phase, TASK 5 documents only |
| `ai/runtime/` (referenced for pattern) | ✅ Yes | `AIService`, `RuntimeManager` (Phase 61.2/61.6) — not touched; Knowledge has no runtime/provider dependency |

**Rule applied**: Foundation, Registry, and (mostly) Contract already
exist. Per Article 11, a new module is forbidden for any of those three
concerns — only the one real gap (Manager) may be added, as a new file
inside the existing package. No new top-level package, no `ai/knowledge/`
package, no duplicate registry or contract.

## Critical finding — factual correction, not a Constitution conflict

**The brief's `ai/knowledge/` does not exist and is not the real
package.** Verified by directory listing: `ai/knowledge/` — no such
directory. The real, current Knowledge Foundation is `knowledge/`, a
**top-level package**, a sibling of `ai/`, built Phase 61.3 TASK 3.
This is already documented in three places prior to this phase:

- `docs/ai/AI_ARCHITECTURE.md`'s "Note on the brief's assumption" —
  "There is no dedicated `ai/security/` folder... `knowledge/` is a
  separate, top-level package."
- `docs/ai/AI_KNOWLEDGE.md` — its own opening line states this
  explicitly, with a pointer to `docs/architecture/NAMING_CONVENTIONS.md`.
- `docs/PHASE63_1_AUDIT.md` (previous phase) — the same correction,
  made independently when Phase 63.1 audited the same package.

This is the same category of finding as Phase 62.1b/62.1c's own
corrections (the real pipeline stage order, the real provider roster)
— a factual sketch discrepancy, not a Constitution Article 3 boundary
violation (compare Phase 63.1's `TradeContext`/`DecisionResult` finding,
which *was* a hard violation requiring STOP → Director Decision). No
pause is required here; per `docs/architecture/NAMING_CONVENTIONS.md`'s
own package-naming rule, this Worker proceeds by building inside the
real `knowledge/` package and documents the correction, exactly as the
two prior audits already did.

**This brief also names files that already exist under different
names.** TASK 1 asks for `knowledge_manager.py` / `knowledge_registry.py`
/ `knowledge_models.py` / `README.md`. Mapped against the real package:

| Brief's name | Real file | Status |
|---|---|---|
| `knowledge_models.py` | `ai_layer/knowledge_ai/knowledge_base/models.py` | Exists — Article 9 LOCKed (Phase 61.3 frozen), not renamed |
| `knowledge_registry.py` | `ai_layer/knowledge_ai/knowledge_base/registry.py` | Exists — Article 9 LOCKed, not renamed |
| `README.md` | `knowledge/README.md` | Exists — extended, not rewritten |
| `knowledge_manager.py` | *(none)* | **Genuine gap** — the one file this phase actually creates |

Renaming `models.py`/`registry.py` to `knowledge_models.py`/
`knowledge_registry.py` would violate Article 9 (a LOCKed module's file
path does not move). The package name itself already carries
"knowledge" (`ai_layer.knowledge_ai.knowledge_base.models`, `ai_layer.knowledge_ai.knowledge_base.registry`), so the prefix
the brief's literal filenames imply is redundant, not missing.

## TASK 2's contract naming ("KnowledgeItem, KnowledgeCategory,
KnowledgeSource") — reuse mapping

- **`KnowledgeCategory`** — exact match, already exists, unchanged.
- **`KnowledgeItem`** — conceptually identical to the existing
  `KnowledgeEntry` (same shape: key/category/title/summary/tags). Per
  Article 7/11, this is a naming difference, not a functional gap — no
  parallel `KnowledgeItem` class is created (same resolution Phase 63.1
  applied to `TradeContext`/`DecisionResult`: the brief's name was
  conceptual, the real type already covers the concept).
- **`KnowledgeSource`** — the one real, if small, gap: no existing
  field records where an entry's content is traced from. Today that
  provenance lives only in prose, inside each category module's own
  docstring (e.g. `smc.py`: "Restates `context_layer/market_structure/bos.py`... docstrings").
  Resolution: extend `KnowledgeEntry` (Article 9's allowed shape — a
  new **optional** field with a safe default) with `source: Optional[str]
  = None`, rather than create a new `KnowledgeSource` class. A free-text
  provenance string satisfies the brief's ask without introducing a
  second enum this phase's own "no AI logic, minimal Foundation" scope
  does not call for.

## TASK 6 — Capability Audit (pre-answered here, confirmed at TASK 6)

`ai/capabilities/capability.py`'s `Capability` enum enumerates *what
the AI layer can be asked to do* (its own docstring: "names what the
AI layer can be asked to do, never how or which vendor answers it").
Knowledge lookup itself is not an AI request — it is deterministic,
non-AI, zero-LLM static data access, the same category `context/`/
`signals/` occupy (neither has a `Capability` member either).
`Capability.EDUCATION` already exists and is the closest semantic
match for a *future* AI-facing consumer of `knowledge/` content (e.g. a
future `ai/tools/education_tool.py`, already named as the natural next
step in `knowledge/README.md`'s own "Future Roadmap" section). No new
`Capability` member is added this phase — full detail at TASK 6 below.

## TASK 5's integration point (documented, not wired)

`ai/explanation/explanation_input.py`'s `ExplanationInput` already
carries free-text fields a knowledge lookup could one day populate:
`technical_reason`/`fundamental_reason`/`risk_reason` (TRADE mode) and
`concept`/`example`/`lesson` (EDUCATION mode). A future phase's most
direct integration would be a caller (not `ai/explanation/` itself)
reading `KnowledgeManager.lookup(key)` or `.search(query)` and passing
`entry.summary` into one of those fields before calling
`ExplanationBuilder.build()` — the same "caller assembles primitive
values, the builder never reaches into another package's internals"
shape Phase 63.1 already established for `core/pipeline.py` →
`ExplanationInput`. `ai/explanation/explanation_builder.py` is not
modified this phase.

## Requesting no Director Decision

Unlike Phase 63.1's TASK 0, this audit found no Constitution Article 3
(or any other Article) conflict — only naming corrections already
precedented twice in this repository's own history. TASK 1 through
TASK 10 proceed without a pause.

## Related

- `docs/constitution/CONSTITUTION.md` Article 7, 9, 11, 12.
- `docs/architecture/NAMING_CONVENTIONS.md` — the package-naming rule
  this finding applies.
- `docs/ai/AI_KNOWLEDGE.md` — the existing, real documentation of
  `knowledge/` this phase extends rather than replaces.
- `docs/PHASE63_1_AUDIT.md` — the prior phase's own audit, the model
  this document follows.
