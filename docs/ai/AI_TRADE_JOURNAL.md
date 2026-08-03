# AI Trade Journal Intelligence (`ai/trade_journal/`)

Phase 66.2 (AI Trade Journal Intelligence Foundation). Genuine new
subpackage inside the already-existing `ai/` top-level package,
confirmed by `docs/PHASE66_2_AUDIT.md`'s TASK 0 audit — the third
phase in the `66.x` AI Trading Intelligence sub-sequence, sitting
immediately after `ai/chart_intelligence/` (Phase 66.1).

## Position in the pipeline

The brief's own diagram:

```
Market → Trading Core → Trading Analyst → Chart Intelligence
   → Trade Journal → Learning → Coaching → Performance
```

Trade Journal never decides — it writes a professional, narrative
record of an already-decided trade and links it to its originating
chart (`chart_id`) and trade (`trade_id`), preparing historical ground
truth for the future Learning (66.3), Coaching (66.4), and Performance
(66.5) layers to *read* (READ ONLY — Rule 2). It never produces a
BUY/SELL/NO_TRADE verdict, never opens a trade, and never touches
`decision/`, `risk/`, `execution/`, `strategies/`, `signals/`,
`context/`, or `monitoring/` (Rule 1).

## `ai/journal/` already exists — reviewed, not reused

`ai/journal/trade_journal.py`'s own `TradeJournalEntry` (Phase 55) is
a different, Trading-Core-coupled type (imports
`signal_layer.signal_builder.models.SignalType`, predates Constitution Article 3) —
structurally different from this phase's own contract and left
untouched. `ai/journal/failure_analysis.py`'s `FailureAnalysisEntry`
(Phase 59) is narrower (failure-only). `ai_layer/knowledge_ai/learning_loop/models.py`'s
`LearningRecord` (Phase 60.6/60.7) is DB-persisted and
pattern-analysis-shaped, not narrative. See `docs/PHASE66_2_AUDIT.md`
for the full reasoning behind why none of these three was extended.

## Model

- `models.py` — `TradeJournalEntry` (TASK 2's own exact contract:
  `journal_id`, `chart_id`, `trade_id`, `symbol`, `timeframe`,
  `direction`, `entry`, `sl`, `tp`, `result`, `confidence`, `reason`,
  `lesson`, `mistakes`, `created_at`). `chart_id`/`trade_id` are
  mandatory links (Director Note 4) — no default value. `confidence`
  is relayed exactly as supplied, with no scale conversion (Rule 4 —
  Journal never transforms). `ReplayContext` (TASK 3 — `trade_id`,
  `chart_id`, `snapshot_id`, `comment`, `sequence`; metadata only, no
  video/image/binary field of any kind, Director Note 3).
  `generate_journal_id()` — a stateless uuid4 generator.

## Chart ID extension (Phase 66.1 LOCK-permitted)

`ai/chart_intelligence/models.py`'s `ChartAnalysis` (Phase 66.1,
Director LOCKed) gained one new, additive, trailing-defaulted field —
`chart_id: str = ""` — plus `generate_chart_id()`. This realizes both
the Phase 66.1 LOCK review's own Director Note 1 ("Kelajakda har
ChartAnalysis ichida chart_id bo'lishi foydali bo'ladi... Bu Journal
va Replay tizimida kerak bo'ladi") and this phase's own Director Note
4. Permitted under the Phase 66.1 LOCK's own "✅ extension" allowance;
no existing `ChartAnalysis(...)` call site uses positional arguments,
so nothing breaks (Article 9). See `docs/PHASE66_2_AUDIT.md`'s "Chart
ID extension" section for the full reasoning.

## Runtime (TASK 4)

`journal_runtime.py`'s `TradeJournalRuntime` is CRUD-only, exactly as
Rule 4 requires: `create()`/`get()`/`list()`/`update_notes()`, nothing
else — no Replay logic, no Analytics, no Learning/Coaching/Performance
computation. In-memory only (Rule 3 — no SQLite/Postgres/Redis
anywhere in this package): a private dict, the same "Foundation, not a
real persistence layer" convention `ai/content/content_adapter.py`'s
own `_history` list already established. `update_notes()` only ever
updates the three narrative fields (`reason`/`lesson`/`mistakes`) —
`chart_id`/`trade_id`/`direction`/`entry`/`sl`/`tp`/`result` are
immutable after `create()`. Owner-gated: every method re-checks
`ai_layer.knowledge_ai.knowledge_base.trade_journal.access.is_trade_journal_enabled_for()` itself.

## Trading Analyst / Chart Intelligence Integration (TASK 5)

`trading_analyst_adapter.py`'s `journal_entry_from_trading_and_chart()`
composes an existing `TradingAnalysis` (Phase 66.0) and an existing
`ChartAnalysis` (Phase 66.1) into a single `TradeJournalEntry` — the
pipeline's own "TradingAnalysis → ChartAnalysis → TradeJournal" order.
`direction` is relayed from `trading` unchanged (Rule 2); `reason`
relays `trading.recommendation` (falling back to `trading.summary`);
`lesson` relays `chart.notes`. `entry`/`sl`/`tp`/`result` are accepted
as optional pass-through parameters — neither upstream contract
carries price levels or a realized result in its own output, so this
Foundation-only adapter never fabricates them. The one file in
`ai/trade_journal/` permitted to import `ai_layer.ai_engine.trading_analyst.models`
and `ai_layer.vision_ai.models`.

## Memory Reference (TASK 6)

`memory_adapter.py`'s `memory_reference_key()` is a pure string-format
function (`"trade_journal:{journal_id}"`) — this package never imports
`ai_layer.knowledge_ai.memory_manager` at all (Rule 6: "Memory o'zgarmaydi"). `ai/memory/models.py`'s
`MemoryScope` enum has no member shaped for a trade journal entry, and
adding one would violate Rule 6; a future, separately-approved phase
would use this key as `ai_layer.knowledge_ai.memory_manager.models.MemoryEntry.key` when it
decides to wire real Memory storage.

## Owner Mode (TASK 7)

`access.py`'s `is_trade_journal_enabled_for(role, flags)` requires
**both** `configuration.feature_flags.FeatureFlags.enable_trade_journal`
(default `False`) **and** `role == AIRole.OWNER`. Mirrors
`ai/trading_analyst/access.py`'s and `ai/chart_intelligence/access.py`'s
shape exactly — a dedicated flag, distinct from `enable_ai_memory`
(whose own docstring references `ai/journal/trade_journal.py` but does
not govern it).

## Future Compatibility (TASK 8)

No new artifact was needed — `TradeJournalRuntime.list()`/`get()`'s
own READ ONLY surface is already the Foundation a future Learning
(66.3), Coaching (66.4), Performance (66.5), or Research (66.8) phase
would read from (Director Note 5: "Bu qatlam kelajakdagi 66.3-66.5
bosqichlari tomonidan faqat o'qiladi"). This phase itself never reads
from or writes to any of those future layers.

## What it is not

- No statistics, no win rate/Sharpe/profit factor/drawdown computation
  (Director Note 1 — that belongs to 66.5).
- No BUY/SELL/NO_TRADE verdict of any kind (Rule 2).
- No database of any kind (Rule 3) — `TradeJournalRuntime` is
  in-memory only.
- No Replay video/screenshot/animation — `ReplayContext` is metadata
  only (Director Note 3).
- No new top-level package — lives inside the existing `ai/`.
- Never imports `decision/`, `risk/`, `execution/`, `strategies/`,
  `signals/`, `context/`, `monitoring/`, `database/`, `telegram/`,
  `assistant/`, `voice/`, `ai_layer.knowledge_ai.memory_manager`, `ai_layer.ai_engine.reasoning`, `knowledge/`,
  `ai.content/`, `media/`, or `broadcast/` — zero exceptions,
  permanently enforced by
  `tests/ai/trade_journal/test_trade_journal_isolation.py`.
- Not wired into `core/pipeline.py` or any Telegram command this
  phase — foundation only.

## Related

- `docs/PHASE66_2_AUDIT.md`, `docs/PHASE66_2_FREEZE.md` — full
  documentation of this phase.
- `ai/trade_journal/README.md` — the package's own top-level README.
- `ai/trading_analyst/`, `ai/chart_intelligence/` — the two sibling
  packages this phase's `trading_analyst_adapter.py` composes with.
- `ai/journal/`, `learning/` — the pre-existing, unrelated journal/
  learning types reviewed but not reused.
- `docs/ai/AI_TRADING_ANALYST.md`, `docs/ai/AI_CHART_INTELLIGENCE.md` —
  the two immediately preceding phases in this sub-sequence.
