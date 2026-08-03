# AI Learning Intelligence (`ai/learning/`)

Phase 66.3 (AI Learning Intelligence Foundation). Genuine new
subpackage inside the already-existing `ai/` top-level package,
confirmed by `docs/PHASE66_3_AUDIT.md`'s TASK 0 audit — the fourth
phase in the `66.x` AI Trading Intelligence sub-sequence, sitting
immediately after `ai/trade_journal/` (Phase 66.2). Per the Director's
own framing: this is the first phase in GoldBot's history where AI
infrastructure begins preparing to learn *from the user*, not just
narrate the Trading Core's own output — but this phase itself does
**not** learn, evaluate, coach, or teach anything yet. It only builds
the Foundation those future capabilities will stand on.

## Position in the pipeline

The brief's own diagram:

```
Trading Analyst → Chart Intelligence → Trade Journal
   → Learning Intelligence → Coaching
```

Learning Intelligence never evaluates a trade, never computes a win
rate or any performance metric, never coaches, and never generates a
lesson or quiz (Rules 6-9). It never touches `decision/`, `risk/`,
`execution/`, `signals/`, `telegram/`, `database/`, `monitoring/`, or
`strategies/` (Rule 2), makes no LLM call and no network call
(Rule 4/5), and performs no real AI inference of any kind (Rule 10).

## `learning/` (top-level) and `ai_layer/knowledge_ai/learning_context.py` already exist
## — reviewed, not reused

`ai_layer/knowledge_ai/learning_loop/models.py`'s own `LearningRecord` (Phase 60.6/60.7) is a
**trade-outcome pattern-statistics record** (`trade_id`, `signal_id`,
`failure_type`, `success_pattern`, `htf_bias`, etc.), real-DB-persisted
via `database_layer/journal_repository/learning_repository.py` — a fundamentally different
concept from this phase's own per-user, topic-mastery record, and
reusing it would violate Rule 3 (no database) by association.
`ai_layer/knowledge_ai/learning_context.py`'s `LearningContext` (Phase 60.6/60.7) is a
read-only aggregation bundle for a future AI explainer, built *from*
that same trade-outcome system — also not reused. See
`docs/PHASE66_3_AUDIT.md` for the full reasoning behind why neither
was extended.

## Model

- `models.py` — `LearningTopic` (TASK 2's own 12-value vocabulary:
  DISCIPLINE/ENTRY/EXIT/RISK/PATIENCE/STRUCTURE/FVG/OB/LIQUIDITY/
  TREND/SESSION/PSYCHOLOGY), `LearningLevel` (UNKNOWN/BEGINNER/
  INTERMEDIATE/ADVANCED/MASTERED — always caller-supplied, never
  graded by this package), `LearningSource` (TASK 7 — TRADE/JOURNAL/
  CHART/MANUAL/SIMULATION), `LearningStatus` (TASK 7 — ACTIVE/
  ARCHIVED/PENDING). `LearningRecord` (TASK 2's own exact contract:
  `id`, `user_id`, `topic`, `level`, `confidence`, `notes`, `created_at`,
  extended with `source`/`status` from TASK 7's own vocabulary so
  every record carries its origin and lifecycle state without a second
  contract). `generate_learning_id()` — a stateless uuid4 generator.

## Runtime (TASK 3)

`learning_runtime.py`'s `LearningRuntime` is CRUD-only, exactly as
Rule 10 requires: `create()`/`get()`/`list()`/`update()`/`archive()`,
nothing else. In-memory only (Rule 3 — no SQLite/Postgres/Redis
anywhere in this package): a private dict, the same "Foundation, not a
real persistence layer" convention `ai/trade_journal/journal_runtime.py`'s
own `_entries` dict already established. `update()` only ever updates
`level`/`confidence`/`notes` — `user_id`/`topic`/`source` are immutable
after `create()`. `archive()` sets `status` to `ARCHIVED`, never
deletes a record. Owner-gated: every method re-checks
`ai_layer.knowledge_ai.learning_engine.access.is_learning_intelligence_enabled_for()` itself.

## Journal Adapter (TASK 4)

`journal_adapter.py`'s `journal_entry_to_learning_input()` is a pure
mapping — TASK 4's own instruction: "Hech qanday AI yo'q. Faqat
mapping" (no AI, mapping only). It reads an existing `TradeJournalEntry`
(`ai/trade_journal/`, Phase 66.2) type-only and returns a plain dict of
keyword arguments `LearningRuntime.create()` accepts. It never calls
`LearningRuntime.create()` itself, and it never returns `topic`/`level`
— inferring those from a journal entry's own text would be real AI
inference, forbidden by Rule 10; a caller supplies them explicitly.
The one file in `ai/learning/` permitted to import
`ai_layer.knowledge_ai.knowledge_base.trade_journal.models`.

## Memory Reference (TASK 5)

`memory_adapter.py`'s `memory_reference_key()` is a pure string-format
function (`"learning:{id}"`) — this package never imports `ai_layer.knowledge_ai.memory_manager`
at all (TASK 5: "Memory Runtime chaqirilmaydi"). Mirrors
`ai/trade_journal/memory_adapter.py`'s own precedent exactly (Phase
66.2, TASK 6).

## Owner Mode (TASK 6)

`access.py`'s `is_learning_intelligence_enabled_for(role, flags)`
requires **both**
`configuration.feature_flags.FeatureFlags.enable_learning_intelligence`
(default `False`) **and** `role == AIRole.OWNER`. Mirrors
`ai/trade_journal/access.py`'s shape exactly.

## Future Compatibility (TASK 8)

No implementation exists for Quiz, Lesson, Exercise, Homework, Video,
Replay, Practice, Progress, or Certificate — only the architecture
(this Foundation's own `LearningTopic`/`LearningLevel`/`LearningSource`
vocabulary and CRUD surface) is ready for a future, separately-approved
phase to build on top of. `tests/ai/learning/test_ai_learning_compatibility.py`
permanently confirms none of these nine concepts exists as a module,
class, or method anywhere in this package.

## What it is not

- No trade evaluation, no win rate/profit/performance computation of
  any kind (Rule 6).
- No coaching (Rule 7), no lesson generation (Rule 8), no quiz
  generation (Rule 9).
- No real AI inference — `level`/`confidence` are always
  caller-supplied (Rule 10).
- No database (Rule 3) — `LearningRuntime` is in-memory only.
- No LLM, no network call (Rule 4/5).
- No new top-level package — lives inside the existing `ai/`.
- Never imports `decision/`, `risk/`, `execution/`, `signals/`,
  `telegram/`, `database/`, `monitoring/`, `strategies/`, `context/`,
  `learning/` (the pre-existing, unrelated top-level package),
  `analytics/`, `ai_layer.knowledge_ai.memory_manager`, `ai_layer.ai_engine.reasoning`, `knowledge/`,
  `ai_layer.vision_ai`, `ai_layer.ai_engine.trading_analyst`, `ai.content/`,
  `media/`, `broadcast/`, `assistant/`, or `voice/` — zero exceptions,
  permanently enforced by
  `tests/ai/learning/test_ai_learning_isolation.py`.
- Not wired into `core/pipeline.py` or any Telegram command this
  phase — foundation only.

## Related

- `docs/PHASE66_3_AUDIT.md`, `docs/PHASE66_3_FREEZE.md` — full
  documentation of this phase.
- `ai/learning/README.md` — the package's own top-level README.
- `ai/trade_journal/` — the sibling package this phase's
  `journal_adapter.py` reads from (type-only).
- `learning/`, `ai_layer/knowledge_ai/learning_context.py` — the pre-existing, unrelated
  trade-outcome-statistics types reviewed but not reused.
- `docs/ai/AI_TRADE_JOURNAL.md` — the immediately preceding phase's
  own documentation.
