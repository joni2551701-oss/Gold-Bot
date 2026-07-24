# ai/memory/

## Purpose
The AI layer's in-process memory foundation — not a live data source,
not a trading record, not a database. Two coexisting surfaces over the
same package: a raw, layer-keyed key/value store (Phase 55/61.3) and a
structured, queryable `MemoryEntry` catalog (Phase 63.3). Neither
persists anything to disk or a database — both are foundation-only,
in-memory contracts, the same "compute now, connect later" posture
every other Phase 61.x/63.x foundation module has used.

## Structure
```
ai/memory/
  context_memory.py   ContextMemory -- Phase 55, the underlying raw key/value store
  memory_runtime.py   MemoryRuntime -- Phase 61.3's 5-layer facade over
                       ContextMemory (save/load/clear/clear_all), extended
                       Phase 63.3 with a structured MemoryEntry surface
                       (store/recall/search/filter/list_all/short_term/
                       long_term/forget)
  models.py            MemoryType/MemoryPriority/MemoryScope/MemoryEntry
                       (Phase 63.3)
  memory_registry.py   MemoryScopeDescriptor catalog, build_memory_scope_registry()/
                       describe() (Phase 63.3)
```

## Responsibilities
- `context_memory.py` — `ContextMemory`: a minimal per-key in-memory
  store (`save`/`load`/`clear`). Not modified since before Phase 61.3.
- `memory_runtime.py` — `MemoryRuntime`, `MemoryLayer`. Original
  surface (`save`/`load`/`clear`/`clear_all` over five fixed layers:
  `CONVERSATION`/`USER`/`TRADE`/`LEARNING`/`MARKET`) is LOCKed since
  Phase 61.3 and unchanged. Phase 63.3 added a second, structured
  surface on the same class: `store(entry)`, `recall(key)`,
  `search(query)`, `filter(predicate)`, `list_all()`, `short_term()`,
  `long_term()`, `forget(key)` — operating over `MemoryEntry` records,
  not raw values.
- `models.py` — `MemoryType` (`SHORT_TERM`/`LONG_TERM`),
  `MemoryPriority` (`LOW`/`NORMAL`/`HIGH`), `MemoryScope`
  (`CONVERSATION`/`MARKET`/`EDUCATION`/`USER_PREFERENCE`/
  `EXPLANATION_HISTORY`/`KNOWLEDGE_REFERENCE`), `MemoryEntry` (frozen
  dataclass: `key`, `scope`, `memory_type`, `value`, `priority`).
- `memory_registry.py` — a static, six-entry catalog describing each
  `MemoryScope` (label, description, default `MemoryType`). Metadata
  only, zero AI reasoning, zero LLM/network call.

## Input
None — `MemoryEntry.value` accepts whatever a caller passes; `ai/memory/`
itself never reads live market data, a database, or a trading-layer
object (verified by a permanent AST regression test).

## Output
`Optional[Any]` (`load`/`recall`), `Sequence[MemoryEntry]`
(`search`/`filter`/`short_term`/`long_term`), `List[MemoryEntry]`
(`list_all`), `Sequence[MemoryScopeDescriptor]`
(`build_memory_scope_registry`).

## Dependencies
`core/` only, at the standard-library level. `ai/memory/` does not
import `decision/`, `risk/`, `execution/`, `strategies/`, `database/`,
or `telegram/` — verified by grep sweep at the close of every
AI-touching phase (Constitution Article 3).

## Future Roadmap
Not wired into `core/pipeline.py`, `ai/conversation/`, `ai/explanation/`,
or `knowledge/` this phase — foundation only. Two integration points
are documented (not implemented) in `docs/PHASE63_3_AUDIT.md`: a
future `MemoryScope.KNOWLEDGE_REFERENCE` entry pointing back to a
`knowledge/` entry key, and a future caller populating
`ExplanationInput`'s free-text fields from a `MemoryRuntime.recall()`/
`.short_term()` result before calling `ExplanationBuilder.build()`.

## Related
- `docs/ai/AI_MEMORY.md` — the full, current documentation of this
  package.
- `docs/PHASE61_3_INTELLIGENCE_FREEZE.md` — where `MemoryRuntime` was
  first LOCKed.
- `docs/PHASE63_3_AUDIT.md`, `docs/PHASE63_3_FREEZE.md` — the phase
  that added `models.py`/`memory_registry.py` and extended
  `MemoryRuntime`.
