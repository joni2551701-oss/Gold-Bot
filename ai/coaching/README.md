# AI Coaching Intelligence (`ai/coaching/`)

Phase 66.4 (AI Coaching Intelligence Foundation). Genuine new
subpackage inside the already-existing `ai/` top-level package,
confirmed by `docs/PHASE66_4_AUDIT.md`'s TASK 0 audit — the fifth
phase in the `66.x` AI Trading Intelligence sub-sequence, sitting
immediately after `ai/learning/` (Phase 66.3).

## What this package is

A Foundation for structuring coaching-shaped recommendations
(`CoachingRecommendation`) derived from a trader's own Learning and
Trade Journal records — explaining mistakes, surfacing weaknesses, and
carrying a study/action suggestion. AI still never decides a trade:
GoldBot's Trading Core and AI Analyst continue to be the only source of
any BUY/SELL/NO_TRADE decision. This phase builds the contract and
CRUD runtime only; it does not reason, does not call an LLM, and does
not generate coaching text itself.

## What this package is not

- No signal generation, no BUY/SELL/NO_TRADE decision of any kind.
- No Risk computation, no Trading Core interaction of any kind.
- No LLM call, no Reasoning, no real inference anywhere — `message`/
  `recommendation`/`topic`/`priority`/`type` are always
  caller-supplied, never generated or graded by this package.
- No database — SQLite/Postgres/Redis, none anywhere in this package.
  `CoachingRuntime` stores records in an in-memory dict.
- No network call.
- No new top-level package — lives inside the existing `ai/`.
- No Daily/Weekly/Monthly coaching plans, no Lesson/Exercise/Homework/
  Certification/Academy/Voice Coach — Director Notes for a future,
  separately-briefed phase; this Foundation only classifies and stores
  individual coaching messages.
- Never imports `decision/`, `risk/`, `execution/`, `strategies/`,
  `signals/`, `context/`, `telegram/`, `database/`, `voice/`,
  `assistant/`, `media/`, `broadcast/`, `academy/`, `performance/`,
  `portfolio/`, `research/`, or `core.` — zero exceptions, permanently
  enforced by `tests/ai/coaching/test_ai_coaching_isolation.py`.
- Not wired into `core/pipeline.py` or any Telegram command this
  phase — foundation only.

## Related

- `docs/PHASE66_4_AUDIT.md`, `docs/PHASE66_4_FREEZE.md` — full
  documentation of this phase.
- `docs/ai/AI_COACHING.md` — the full subsystem documentation.
- `ai/learning/` — the sibling package this phase's
  `learning_adapter.py` reads from (type-only).
- `ai/trade_journal/` — the sibling package this phase's
  `journal_adapter.py` reads from (type-only).
