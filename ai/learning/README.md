# AI Learning Intelligence (`ai/learning/`)

Phase 66.3 (AI Learning Intelligence Foundation). Genuine new
subpackage inside the already-existing `ai/` top-level package,
confirmed by `docs/PHASE66_3_AUDIT.md`'s TASK 0 audit — the fourth
phase in the `66.x` AI Trading Intelligence sub-sequence, sitting
immediately after `ai/trade_journal/` (Phase 66.2).

## What this package is

A Foundation for tracking a trader's own per-topic mastery level
(`LearningTopic` × `LearningLevel`) — the first phase in this
codebase's history where AI infrastructure begins preparing to learn
*from the user*, not just narrate the Trading Core's own output. This
phase builds the contract and CRUD runtime only; it does not evaluate
trades, does not compute win rate/performance, does not coach, and
does not generate a lesson or quiz.

## What this package is not

- No trade evaluation, no win rate/profit/performance computation of
  any kind (Rule 6).
- No coaching (Rule 7), no lesson generation (Rule 8), no quiz
  generation (Rule 9).
- No real AI inference anywhere (Rule 10) — `level`/`confidence` are
  always caller-supplied, never graded or classified by this package.
- No database — SQLite/Postgres/Redis, none anywhere in this package
  (Rule 3). `LearningRuntime` stores records in an in-memory dict.
- No LLM, no network call (Rule 4/5).
- No new top-level package (Rule 1's own "Trading Core ZERO TOUCH"
  spirit extends to "no new engine") — lives inside the existing `ai/`.
- Never imports `decision/`, `risk/`, `execution/`, `signals/`,
  `telegram/`, `database/`, `monitoring/`, `strategies/`, `learning/`
  (the pre-existing, unrelated top-level package), or `ai.memory` —
  zero exceptions, permanently enforced by
  `tests/ai/learning/test_ai_learning_isolation.py`.
- Not wired into `core/pipeline.py` or any Telegram command this
  phase — foundation only.

## Related

- `docs/PHASE66_3_AUDIT.md`, `docs/PHASE66_3_FREEZE.md` — full
  documentation of this phase.
- `docs/ai/AI_LEARNING.md` — the full subsystem documentation.
- `ai/trade_journal/` — the sibling package this phase's
  `journal_adapter.py` reads from (type-only).
- `learning/` — the pre-existing, unrelated top-level package
  (trade-outcome pattern statistics, DB-persisted) reviewed but not
  reused (see `docs/PHASE66_3_AUDIT.md`).
