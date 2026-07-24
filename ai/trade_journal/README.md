# AI Trade Journal Intelligence (`ai/trade_journal/`)

Phase 66.2 (AI Trade Journal Intelligence Foundation). Genuine new
subpackage inside the already-existing `ai/` top-level package,
confirmed by `docs/PHASE66_2_AUDIT.md`'s TASK 0 audit — the third
phase in the `66.x` AI Trading Intelligence sub-sequence, sitting
immediately after `ai/chart_intelligence/` (Phase 66.1).

## What this package is

A professional, per-trade narrative journal — records what happened,
links it to its originating chart (`chart_id`) and trade (`trade_id`),
and prepares historical ground truth for the future Learning (66.3),
Coaching (66.4), and Performance (66.5) layers to *read* (never write
to this package back).

## What this package is not

- No statistics, no win rate/Sharpe/profit factor/drawdown computation
  (Director Note 1 — that belongs to 66.5).
- No BUY/SELL/NO_TRADE verdict of any kind (Rule 2 — READ ONLY, only
  ever narrates an already-decided `direction`).
- No database — SQLite/Postgres/Redis, none anywhere in this package
  (Rule 3). `TradeJournalRuntime` stores entries in an in-memory dict.
- No Replay video/screenshot/animation — `ReplayContext` is metadata
  only (Director Note 3).
- No Analytics, Coaching, or Performance logic (Rule 4 — Journal only
  writes).
- No new top-level package — lives inside the existing `ai/`.
- Never imports `decision/`, `risk/`, `execution/`, `strategies/`,
  `signals/`, `context/`, `monitoring/`, `database/`, `telegram/`,
  `assistant/`, `voice/`, or `ai.memory` — zero exceptions, permanently
  enforced by `tests/ai/trade_journal/test_trade_journal_isolation.py`.
- Not wired into `core/pipeline.py` or any Telegram command this
  phase — foundation only.

## Related

- `docs/PHASE66_2_AUDIT.md`, `docs/PHASE66_2_FREEZE.md` — full
  documentation of this phase.
- `docs/ai/AI_TRADE_JOURNAL.md` — the full subsystem documentation.
- `ai/trading_analyst/`, `ai/chart_intelligence/` — the two sibling
  packages this phase's `trading_analyst_adapter.py` composes with
  (type-only reads).
- `ai/journal/` — the pre-existing, unrelated Phase 55/59 journal
  types reviewed but not reused (see `docs/PHASE66_2_AUDIT.md`).
