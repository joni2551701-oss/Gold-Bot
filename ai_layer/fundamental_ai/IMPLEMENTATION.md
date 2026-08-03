# AI Research Intelligence (`ai/research/`)

Phase 66.8 (AI Research Intelligence Foundation). **Final phase of the
`66.x` AI Trading Intelligence sub-sequence.** Genuine new subpackage
inside the already-existing `ai/` top-level package, confirmed by
`docs/PHASE66_8_AUDIT.md`'s TASK 0 audit — sitting immediately after
`ai/portfolio/` (Phase 66.7).

## What this package is

A Foundation that accepts data from every prior `66.x` Foundation
module in a standard format, creating a single scientific layer for
future AI Research, Analytics, and Academy work. It never opens a
trade, never gives a signal, never computes risk, never selects a
strategy, and never touches Trading Core — GoldBot's Trading Core
remains the only source of any BUY/SELL/NO_TRADE decision. This phase
builds the contract and CRUD runtime only; it does not evaluate,
grade, mine, or draw conclusions itself.

### TASK 9 — Future Compatibility (architecture only, no code)

The brief's own eleven future directions are recorded here as
Foundation-level compatibility notes, not implemented:

- **Research Dataset** — `ResearchRuntime` stores individual records
  only; no bulk-dataset export exists.
- **Pattern Mining** — no pattern-detection algorithm exists over
  `ResearchRecord`s.
- **Market Regime Detection** — no regime classification exists;
  `ResearchCategory.MARKET` is a plain caller-supplied tag, not a
  computed regime.
- **Knowledge Graph Integration** — no linkage to `knowledge/`'s own
  SMC/Wyckoff/risk/psychology content exists.
- **Paper Generator** — no AI-authored research paper generation
  exists; `summary`/`notes` are always caller-supplied.
- **Backtest Dataset** — no wiring to `backtesting/`'s own replay
  engine exists (a separate, already-existing Trading Core module,
  untouched by this phase).
- **AI Dataset Builder** — no training-dataset assembly exists.
- **Research Report** — no report-rendering surface exists.
- **Research Versioning** — no version-history tracking exists;
  `ResearchRecord` carries no version field.
- **Research Export** — no export-to-file/external-system mechanism
  exists.
- **Research Archive** (beyond `archive()`'s own status flip) — no
  bulk-archival or cold-storage mechanism exists.

`tests/ai/research/test_ai_research_compatibility.py` permanently
confirms none of these eleven concepts exists as a module, class, or
method anywhere in this package.

## What this package is not

- No BUY/SELL, no signal generation, no risk computation, no strategy
  selection, no Trading Core interaction of any kind.
- No LLM call, no Reasoning, no real inference anywhere — `title`/
  `summary`/`notes`/`source_count` are always caller-supplied, never
  generated or graded by this package; each sibling-Foundation
  adapter's `category` value is a fixed structural constant of that
  adapter, never inferred from record content.
- No database — SQLite/Postgres/Redis, none anywhere in this package.
  `ResearchRuntime` stores records in an in-memory dict.
- No network call.
- No new top-level package — lives inside the existing `ai/`.
- Never imports `decision/`, `risk/`, `execution/`, `strategies/`,
  `signals/`, `context/`, `monitoring/`, `telegram/`, `database/`,
  `voice/`, `assistant/`, `core.`, or `ai_layer.knowledge_ai.memory_manager` — zero exceptions,
  permanently enforced by
  `tests/ai/research/test_ai_research_isolation.py`.
- Not wired into `core/pipeline.py` or any Telegram command this
  phase — foundation only.

## Related

- `docs/PHASE66_8_AUDIT.md`, `docs/PHASE66_8_FREEZE.md` — full
  documentation of this phase.
- `docs/ai/AI_RESEARCH.md` — the full subsystem documentation.
- `ai/performance/`, `ai/strategy/`, `ai/portfolio/` — the three
  sibling packages this phase's own adapters read from (type-only, no
  Runtime imports).
- This phase closes the `66.x` AI Trading Intelligence sub-sequence
  entirely — see `docs/roadmap/AI_EVOLUTION.md` for the full roadmap
  and the Director's own next-steps notes (GoldBot Core Owner
  Monitoring Alpha, Track B).
