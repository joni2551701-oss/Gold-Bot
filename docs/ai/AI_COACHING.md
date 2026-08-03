# AI Coaching Intelligence (`ai/coaching/`)

Phase 66.4 (AI Coaching Intelligence Foundation). Genuine new
subpackage inside the already-existing `ai/` top-level package,
confirmed by `docs/PHASE66_4_AUDIT.md`'s TASK 0 audit — the fifth
phase in the `66.x` AI Trading Intelligence sub-sequence, sitting
immediately after `ai/learning/` (Phase 66.3). Per the Director's own
framing: this phase's job is to build the AI Coach's *foundation* —
explaining a trader's own mistakes, surfacing weaknesses, and carrying
a study/action suggestion — while AI still never decides a trade;
GoldBot's Trading Core and AI Analyst remain the only source of any
BUY/SELL/NO_TRADE decision.

## Position in the pipeline

The brief's own diagram:

```
Trading Analyst → Chart Intelligence → Trade Journal
   → Learning Intelligence → Coaching
```

Coaching Intelligence never evaluates a trade, never computes a win
rate or any performance metric, and performs no real AI inference of
any kind. It never touches `decision/`, `risk/`, `execution/`,
`strategies/`, `signals/`, `context/`, `telegram/`, `database/`,
`voice/`, `assistant/`, `media/`, `broadcast/`, `academy/`,
`performance/`, `portfolio/`, `research/`, or `core.` (TASK 8's own
isolation list).

## Model

- `models.py` — `CoachingTopic` (12-value vocabulary, mirroring
  `ai_layer.knowledge_ai.learning_engine.models.LearningTopic`'s own value set for coherence but
  defined as a separate, local enum — no cross-package import in
  `models.py`), `CoachingPriority` (LOW/MEDIUM/HIGH/CRITICAL),
  `CoachingType` (FEEDBACK/RECOMMENDATION/WARNING/MOTIVATION/REMINDER),
  `CoachingStatus` (PENDING/ACTIVE/ACKNOWLEDGED/ARCHIVED).
  `CoachingRecommendation` (TASK 2's own exact contract: `coach_id`,
  `user_id`, `learning_id`, `journal_id`, `topic`, `priority`, `type`,
  `message`, `recommendation`, `status`, `created_at`, `metadata`).
  `generate_coach_id()` — a stateless uuid4 generator.

## Runtime (TASK 3)

`coaching_runtime.py`'s `CoachingRuntime` is CRUD-only, exactly as the
brief requires ("LLM yo'q. Reasoning yo'q. Inference yo'q."):
`create()`/`get()`/`list()`/`archive()`/`update_status()`, nothing
else. In-memory only — a private dict, the same "Foundation, not a
real persistence layer" convention `ai/learning/learning_runtime.py`'s
own `_records` dict already established. `update_status()` moves a
record between PENDING/ACTIVE/ACKNOWLEDGED but rejects ARCHIVED —
archiving is a dedicated, one-way action reachable only via
`archive()`. Owner-gated: every method re-checks
`ai_layer.personal_ai.senior.access.is_coaching_intelligence_enabled_for()` itself.

## Learning Adapter (TASK 4)

`learning_adapter.py`'s `learning_record_to_coaching_input()` is a
pure mapping — TASK 4's own instruction: "Hech qanday yangi AI analiz
qilmaydi. Mapping only." It reads an existing `LearningRecord`
(`ai/learning/`, Phase 66.3) type-only and returns a plain dict of
keyword arguments `CoachingRuntime.create()` accepts. Unlike the
Journal Adapter, this one *can* relay `topic` directly —
`LearningRecord.topic` is already an explicit, caller-supplied
classification, so copying it is a direct relay, not an inference. The
one file in `ai/coaching/` permitted to import `ai_layer.knowledge_ai.learning_engine.models`.

## Journal Adapter (TASK 5)

`journal_adapter.py`'s `journal_entry_to_coaching_input()` is a pure
mapping — TASK 5's own instruction: "Mapping only. Inference
taqiqlanadi." It reads an existing `TradeJournalEntry`
(`ai/trade_journal/`, Phase 66.2) type-only. `topic` is deliberately
absent from the returned mapping — `TradeJournalEntry` has no
topic-shaped field, so choosing one would require real inference,
mirroring `ai_layer.knowledge_ai.learning_engine.journal_adapter`'s own "topic/level deliberately
omitted" precedent. The one file in `ai/coaching/` permitted to import
`ai_layer.knowledge_ai.knowledge_base.trade_journal.models`.

## Owner Mode (TASK 6)

`access.py`'s `is_coaching_intelligence_enabled_for(role, flags)`
requires **both**
`configuration.feature_flags.FeatureFlags.enable_coaching_intelligence`
(default `False`) **and** `role == AIRole.OWNER`. Mirrors
`ai/learning/access.py`'s shape exactly.

## Future Compatibility (TASK 7)

No implementation exists for AI Coach (as an independently-reasoning
entity), Lesson, Exercise, Homework, Daily Plan, Weekly Plan, Monthly
Goal, Certification, Academy, or Voice Coach — only the architecture
(this Foundation's own `CoachingTopic`/`CoachingPriority`/
`CoachingType`/`CoachingStatus` vocabulary and CRUD surface) is ready
for a future, separately-approved phase to build on top of. The
Director's own notes for this phase name five specific future
directions the Foundation is designed to support without implementing
any of them yet: a Skill Tree view over `CoachingTopic`, per-user
Weakness Tracking, Adaptive Coaching (reading `ai/learning/` per user),
a Learning History chain (Lesson → Exercise → Quiz → Replay → Exam →
Certificate), and eventual Academy integration.
`tests/ai/coaching/test_ai_coaching_compatibility.py` permanently
confirms none of the nine named future concepts exists as a module,
class, or method anywhere in this package.

## What it is not

- No signal generation, no BUY/SELL/NO_TRADE decision of any kind —
  `CoachingRecommendation` has no verdict-shaped field.
- No Risk computation, no Trading Core interaction of any kind.
- No real AI inference — `message`/`recommendation`/`topic`/
  `priority`/`type` are always caller-supplied, never generated or
  graded by this package.
- No database — `CoachingRuntime` is in-memory only.
- No LLM, no network call.
- No new top-level package — lives inside the existing `ai/`.
- Never imports `decision/`, `risk/`, `execution/`, `strategies/`,
  `signals/`, `context/`, `telegram/`, `database/`, `voice/`,
  `assistant/`, `media/`, `broadcast/`, `academy/`, `performance/`,
  `portfolio/`, `research/`, `core.`, the pre-existing top-level
  `learning/` package, or `analytics/` — zero exceptions, permanently
  enforced by `tests/ai/coaching/test_ai_coaching_isolation.py`.
- Not wired into `core/pipeline.py` or any Telegram command this
  phase — foundation only.

## Related

- `docs/PHASE66_4_AUDIT.md`, `docs/PHASE66_4_FREEZE.md` — full
  documentation of this phase.
- `ai/coaching/README.md` — the package's own top-level README.
- `ai/learning/` — the sibling package this phase's
  `learning_adapter.py` reads from (type-only).
- `ai/trade_journal/` — the sibling package this phase's
  `journal_adapter.py` reads from (type-only).
- `docs/ai/AI_LEARNING.md` — the immediately preceding phase's own
  documentation.
