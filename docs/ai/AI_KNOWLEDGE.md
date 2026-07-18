# GoldBot — AI Knowledge

Governed by `docs/constitution/CONSTITUTION.md` Article 7. `knowledge/`
(Phase 61.3 TASK 3) is a **top-level package**, a sibling of `ai/`, not
`ai/knowledge/` — confirmed by directory listing, the same correction
`docs/architecture/MODULE_DEPENDENCIES.md` and `docs/ai/AI_ARCHITECTURE.md`
already both state. It has zero dependencies — a pure static catalog.

## The six categories

```
knowledge/
  examples.py     worked examples
  faq.py          frequently-asked-question entries
  psychology.py   trading psychology reference
  risk.py         risk-management reference
  smc.py          Smart Money Concepts reference
  wyckoff.py      Wyckoff method reference
  registry.py     lookup / category-filter / search over all six
  models.py       the entry shape every category returns
```

26 entries across the six categories as of Phase 61.3. `registry.py`
is the only way any other module reads this package — `lookup()`,
filtering by category, and free-text `search()`.

## Knowledge Manager (Phase 63.2, TASK 4)

`knowledge_manager.py`'s `KnowledgeManager` is a class-based facade
over `registry.py`, the same Manager-over-Registry shape
`ai/persona/persona_manager.py` already established over
`persona_registry.py`. Its dependency (the entry set) is injectable —
a caller/test never needs the real static registry to exercise it.

```
KnowledgeManager(entries=None)   # defaults to registry.all_entries()
  .lookup(key) -> Optional[KnowledgeEntry]
  .search(query) -> Sequence[KnowledgeEntry]
  .by_category(category) -> Sequence[KnowledgeEntry]
  .filter(predicate) -> Sequence[KnowledgeEntry]
  .list_all() -> List[KnowledgeEntry]
```

Zero AI reasoning, zero LLM/network call — every method is a read over
data already in memory, exactly like the module-level functions it
wraps. Nothing in this codebase calls it yet this phase; it is built
and tested standalone, same "foundation first, wiring is separately
approved" posture every Phase 61.x/63.x module has used.

`KnowledgeEntry` (Phase 63.2, TASK 2) also gained one new optional
field: `source: Optional[str] = None` — free-text provenance (e.g.
`"context/bos.py"`, `"docs/WYCKOFF.md"`) for where an entry's content
was traced from. Unset (`None`) on all 26 pre-existing entries; this
phase does not backfill them, only adds the capability for future
entries to record it.

## What it is not

Not AI-generated — every entry is static, authored content, the same
posture `ContentType.EDUCATION` (Phase 63.0) will eventually draw on
when a future phase wires content generation to a real source. This
package is that source's most likely first input, not itself a
generator.

## Related

- `docs/PHASE61_3_INTELLIGENCE_FREEZE.md` — TASK 3, where this was
  built.
- `docs/architecture/NAMING_CONVENTIONS.md` — why this is a new
  top-level package rather than `ai/knowledge/`.
- `docs/PHASE63_2_AUDIT.md`, `docs/PHASE63_2_FREEZE.md` — the phase
  that added `KnowledgeManager` and `KnowledgeEntry.source`, and its
  own correction of a second Worker Brief that assumed `ai/knowledge/`.
