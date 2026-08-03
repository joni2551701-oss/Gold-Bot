# AI Strategy Intelligence (`ai/strategy/`)

Phase 66.6 (AI Strategy Intelligence Foundation). Genuine new
subpackage inside the already-existing `ai/` top-level package,
confirmed by `docs/PHASE66_6_AUDIT.md`'s TASK 0 audit — the seventh
phase in the `66.x` AI Trading Intelligence sub-sequence, sitting
immediately after `ai/performance/` (Phase 66.5). Per the brief's own
framing: this phase's job is to answer one question — "Qaysi
strategiya qanday ishlayapti?" (Which strategy is performing how?) —
while AI still never opens a trade, gives a signal, manages risk, or
affects the Decision Engine; GoldBot's Trading Core remains the only
source of any BUY/SELL/NO_TRADE decision.

## Position in the pipeline

Trading Core → Trade Journal (66.2) → Learning (66.3) → Coaching
(66.4) → Performance Intelligence (66.5) → **Strategy Intelligence
(66.6)** → Portfolio Intelligence (66.7, future).

Strategy Intelligence never evaluates a trade, never computes a win
rate or performance metric itself, and performs no real AI inference
of any kind (Rule 4: "GPT/Claude/Gemini/Reasoning/Inference YO'Q"). It
never touches `decision/`, `risk/`, `execution/`, `strategies/`,
`signals/`, `context/`, `monitoring/`, `telegram/`, `database/`,
`voice/`, `assistant/`, `media/`, `broadcast/`, `academy/`,
`portfolio/`, `research/`, `core.`, or `ai.memory` (TASK 9's own
isolation list).

## Model (TASK 2)

- `models.py` — `StrategyType` (8-value vocabulary: LIQUIDITY_SWEEP/
  FVG/AMD/TREND_BREAKOUT/ORDER_BLOCK/WYCKOFF/SMC/CUSTOM),
  `StrategyStatus` (ACTIVE/TESTING/DISABLED/ARCHIVED),
  `StrategyConfidence` (LOW/MEDIUM/HIGH/VERY_HIGH). `StrategyRecord`
  (TASK 2's own exact field list: `strategy_id`, `strategy_name`,
  `strategy_type`, `strategy_version`, `confidence`, `notes`,
  `status`, `created_at`). `generate_strategy_id()` — a stateless
  uuid4 generator.

### Naming note: `StrategyStatus` vs the Trading Core one

Documented in `docs/PHASE66_6_AUDIT.md`, not a defect, and stricter
than every prior `66.x` naming collision: `strategy_layer.strategy_manager.lifecycle.strategy_status.StrategyStatus`
(`TESTING`/`ACTIVE`/`DISABLED`/`DEPRECATED`) is a genuine, mature
Trading Core Strategy metadata contract — but this brief's own Rule 1
bans `ai/` from importing `strategies/` at all, making reuse
architecturally impossible rather than merely impractical. This
package's own `StrategyStatus` (`ACTIVE`/`TESTING`/`DISABLED`/
`ARCHIVED`, a different value set) is a distinct, non-colliding
fully-qualified path, never imported alongside the Trading Core one —
confirmed permanently by
`tests/ai/strategy/test_ai_strategy_isolation.py`'s ban on any
`strategies` import.

## Runtime (TASK 3)

`strategy_runtime.py`'s `StrategyRuntime` is CRUD-only, exactly as
Rule 5 requires ("Bu Foundation. Faqat CRUD."):
`create()`/`get()`/`list()`/`update()`/`update_notes()`/`archive()`,
nothing else. In-memory only (Rule 3) — a private dict, the same
"Foundation, not a real persistence layer" convention
`ai/performance/performance_runtime.py`'s own `_records` dict already
established. `update()` mutates only `strategy_version`/`confidence`/
`status`, each left unchanged when its argument is `None`;
`update_notes()` only ever mutates `notes`. `archive()` sets
`status=StrategyStatus.ARCHIVED` and never deletes a record.
Owner-gated: every method re-checks
`ai.strategy.access.is_strategy_intelligence_enabled_for()` itself.

## Performance Adapter (TASK 4)

`performance_adapter.py`'s `performance_record_to_strategy_input()` is
a pure mapping — TASK 4's own instruction: "Type-only. Runtime import
emas." It reads an existing `ai.performance.models.PerformanceRecord`
(Phase 66.5, LOCKed) type-only and relays `confidence_score` →
`confidence` and `notes` → `notes`. `strategy_name`/`strategy_type`/
`strategy_version` are deliberately absent — `PerformanceRecord`
carries no field shaped for any of the three. Never imports
`ai.performance.performance_runtime` — confirmed by
`test_performance_adapter_never_imports_performance_runtime()`. The
one file in `ai/strategy/` permitted to import `ai.performance.models`.

## Journal Adapter (TASK 5)

`journal_adapter.py`'s `journal_entry_to_strategy_input()` is a pure
mapping — TASK 5's own instruction: "Hech qanday inference yo'q." It
reads an existing `ai.trade_journal.models.TradeJournalEntry` (Phase
66.2) type-only, relaying `lesson` (falling back to `reason`) into
`notes`. `strategy_name`/`strategy_type`/`strategy_version` are
deliberately absent (no field to relay), and `confidence` is also
deliberately absent — `TradeJournalEntry.confidence` is a per-trade
value, not a per-strategy one, so relaying it would be inference. The
one file in `ai/strategy/` permitted to import `ai.trade_journal.models`.

## Owner Mode (TASK 7)

`access.py`'s `is_strategy_intelligence_enabled_for(role, flags)`
requires **both**
`configuration.feature_flags.FeatureFlags.enable_strategy_intelligence`
(default `False`) **and** `role == AIRole.OWNER`. Mirrors
`ai/performance/access.py`'s shape exactly.

## Memory Preparation (TASK 6)

`memory_adapter.py`'s `strategy_reference_key(record) -> str` builds a
plain string key (`"strategy:{strategy_id}"`) for a future,
separately-approved phase to use once real Memory storage is wired —
this module never imports `ai.memory` at all. Mirrors
`ai.performance.memory_adapter.performance_memory_key()`'s own
precedent exactly.

## Future Compatibility (TASK 8)

No implementation exists for Strategy Versioning history, Market
Regime classification, Strategy Evolution History, A/B Strategy
Testing, Optimization Hooks, Auto Benchmark, Simulation,
Recommendation, or Correlation — only the architecture (this
Foundation's own `StrategyRecord.strategy_version`/`StrategyType`/
`StrategyStatus` vocabulary and CRUD surface) is ready for a future,
separately-approved phase to build on top of. The Director's own notes
for this phase name these nine directions explicitly, plus the
Performance → Strategy → Portfolio chain for Phase 66.7 and Strategy
Intelligence as a research datasource for Phase 66.8.
`tests/ai/strategy/test_ai_strategy_compatibility.py` permanently
confirms none of the nine named future concepts exists as a module,
class, or method anywhere in this package.

## What it is not

- No signal generation, no BUY/SELL/NO_TRADE decision of any kind.
- No Risk computation, no Trading Core interaction of any kind.
- No real AI inference — `strategy_name`/`strategy_type`/
  `strategy_version`/`confidence`/`notes`/`status` are always
  caller-supplied, never generated or graded by this package.
- No database — `StrategyRuntime` is in-memory only.
- No LLM, no network call.
- No new top-level package — lives inside the existing `ai/`.
- Never imports `decision/`, `risk/`, `execution/`, `strategies/`,
  `signals/`, `context/`, `monitoring/`, `telegram/`, `database/`,
  `voice/`, `assistant/`, `media/`, `broadcast/`, `academy/`,
  `portfolio/`, `research/`, `core.`, or `ai.memory` — zero
  exceptions, permanently enforced by
  `tests/ai/strategy/test_ai_strategy_isolation.py`.
- Not wired into `core/pipeline.py` or any Telegram command this
  phase — foundation only.

## Related

- `docs/PHASE66_6_AUDIT.md`, `docs/PHASE66_6_FREEZE.md` — full
  documentation of this phase.
- `ai/strategy/README.md` — the package's own top-level README.
- `ai/performance/` — the sibling package this phase's
  `performance_adapter.py` reads from (type-only, no Runtime import).
- `ai/trade_journal/` — the sibling package this phase's
  `journal_adapter.py` reads from (type-only).
- `strategies/lifecycle/` — the pre-existing Trading Core Strategy
  metadata contract this package's own models are deliberately
  independent from (import forbidden by Rule 1).
- `docs/ai/AI_PERFORMANCE.md` — the immediately preceding phase's own
  documentation.
