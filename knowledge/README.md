# knowledge/

## Purpose
A static, queryable knowledge base — not a live data source, not a
detector, not a strategy. Restates facts this codebase already
documented elsewhere (`docs/*.md`, `context/*.py`, `risk/README.md`)
in a structured, lookup-by-key shape a future AI consumer can retrieve
without re-deriving them from prose on every call. Added Phase 61.3
(AI Intelligence Layer), TASK 3.

## Flow
```
knowledge/registry.py   -- get_entry() / entries_by_category() / search()
      |
      v
(future) ai/tools/education_tool.py, ai/explanation/  -- not wired this phase
```

## Structure
Flat files per category, not literal subdirectories (see
`docs/PHASE61_3_INTELLIGENCE_AUDIT.md`'s "Structural adaptation"
section for why) — `smc.py`, `wyckoff.py`, `risk.py`, `psychology.py`,
`examples.py`, `faq.py`, each exporting one `*_ENTRIES` tuple of
`KnowledgeEntry`. `registry.py` composes all six into one lookup.
`knowledge_manager.py` (Phase 63.2, TASK 4) is a class-based facade
over `registry.py`, matching the Manager-over-Registry shape
`ai/persona/persona_manager.py` already established.

## Responsibilities
- `models.py` — `KnowledgeCategory` enum + `KnowledgeEntry` (frozen
  dataclass: `key`, `category`, `title`, `summary`, `tags`, and
  `source` — optional free-text provenance, Phase 63.2 TASK 2,
  `None` on every pre-existing entry).
- `knowledge_manager.py` — `KnowledgeManager`: `lookup(key)`,
  `search(query)`, `by_category(category)`, `filter(predicate)`,
  `list_all()`. Every dependency (its own entry set) is injectable;
  zero AI reasoning, zero LLM/network call, same read-only posture as
  `registry.py`'s own module-level functions it wraps.
- `smc.py` / `wyckoff.py` / `risk.py` — content traced directly to
  `context_layer/market_structure/bos.py`, `context_layer/market_structure/choch.py`, `context_layer/liquidity/liquidity.py`,
  `context_layer/order_block/order_block.py`, `context_layer/fair_value_gap/fvg.py`, `context_layer/amd/amd.py`,
  `context_layer/wyckoff/wyckoff.py`, `docs/WYCKOFF.md`, and `risk/README.md`.
- `psychology.py` — general, widely-established trading-discipline
  concepts (FOMO, revenge trading, overtrading, patience). GoldBot
  detects none of these states — no psychology-scoring code exists
  anywhere in this codebase; these entries are educational content
  only.
- `examples.py` — the exact worked examples `docs/MARKET_REGIME.md`
  and `docs/EXPLAINABILITY.md` already committed to, restated as
  queryable entries.
- `faq.py` — GoldBot's own documented behavior (advisory-only AI,
  Risk Manager as final gate, no broker execution, no volume data),
  traced to `CLAUDE.md` and `ai/README.md`.
- `registry.py` — `get_entry(key)`, `entries_by_category(category)`,
  `search(query)` (case-insensitive substring over title/summary/
  tags), `all_entries()`. Raises at import time on a duplicate key.

## Input
None — every entry is a static string decided at commit time.

## Output
`KnowledgeEntry` (single) or `Sequence[KnowledgeEntry]`.

## Dependencies
None outside the standard library. `knowledge/` does not import
`ai/`, `context/`, `decision/`, `risk/`, `execution/`, `strategies/`,
`database/`, or `telegram/` — it is pure static data, safe for any
future layer to depend on without creating a new inbound edge into
those layers.

## Future Roadmap
Not wired into any live handler or the pipeline this phase — a future
`ai/tools/education_tool.py` (TASK 4) or Explanation Engine (TASK 7)
reading through `registry.py`/`knowledge_manager.py` is the natural
next step, not done here. Phase 63.2 documented (not wired) one
concrete integration point: `ai/explanation/explanation_input.py`'s
`ExplanationInput.technical_reason`/`concept`/`example`/`lesson`
fields are natural landing spots for a future caller's
`KnowledgeManager.lookup()`/`.search()` result — see
`docs/PHASE63_2_AUDIT.md`.
