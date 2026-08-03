# Phase 60.0 — Architecture Audit

Director-assigned formal task (Phase 60.0, before any Phase 60.1+ code
is written): six-part audit — Module Dependency Graph, Dead Code,
Duplicate Logic, Database Audit, Owner Audit, Pipeline Audit. Every
finding below was re-verified directly against the current source
(`ast`-based import graph, grep-verified reference counts, direct file
reads) as of commit `49df5cf`, not assumed from
`docs/PHASE59_ARCHITECTURE_FREEZE.md` or any earlier doc. Design/
documentation only — no code was changed to produce this audit.

## 1. Module Dependency Graph

Real, `ast`-parsed, top-level-package import graph (every
`import X`/`from X import Y` where `X` is another top-level package in
this repo, third-party and stdlib imports excluded):

```
ai          -> context, core, signals
analytics   -> data, database, lifecycle, signals
configuration -> core, database
context     -> core, data
core        -> ai, context, data, database, decision, features, risk, signals, telegram   (pipeline.py's own orchestration import)
data        -> core, database
database    -> configuration, core, data, decision, risk, signals
decision    -> ai, context, signals
execution   -> risk
features    -> context, signals
lifecycle   -> data, signals
monitoring  -> core, data, database
performance -> core
risk        -> decision, signals
scripts     -> core, database
signals     -> context, core, decision, strategies
strategies  -> context, signals
telegram    -> ai, analytics, configuration, core, data, database, decision, monitoring, risk, signals
```

Every edge was individually checked for direction correctness against
`CLAUDE.md`'s `data → context → strategies → signals → ai → decision →
risk → telegram → database` chain:

- **`database → decision/risk/signals`**: real, but expected —
  `database_layer/trade_repository/signal_record.py`'s `SignalRecord` wraps a
  `(SignalCandidate, TradeDecision, RiskResult)` triple for
  persistence-identity. `database/` sits at the *end* of the chain; it
  is supposed to import upstream result types to store them. Not a
  violation.
- **`risk → decision`**: real — `risk_layer/risk_engine/risk_manager.py` imports
  `decision_layer.decision_engine.models.TradeDecision`/`DecisionAction` because
  `RiskManager.evaluate()` *consumes* a `TradeDecision` as input (the
  Decision Engine's output is Risk's input, exactly the documented
  order). `decision/` does **not** import `risk/` anywhere — confirmed
  via grep, zero matches — so this is one-directional, not circular.
- **`signals → decision`**: `signal_layer/signal_builder/adapter.py`'s only reference to
  `decision_layer.decision_engine.models.TradeDecision` is inside an `if TYPE_CHECKING:`
  block — never a real runtime import.
- **`telegram → risk/decision/ai`**: real, but confined to
  `telegram/signal_formatter.py`, which formats the same
  `(SignalCandidate, TradeDecision, RiskResult, AIAnalysisResult)`
  tuple for a Telegram message — the same "downstream formats
  upstream's output" pattern as `database_layer/trade_repository/signal_record.py` above.
- **`core → ai/context/data/database/decision/features/risk/signals/telegram`**:
  all from `core/pipeline.py`, the orchestrator — expected to import
  every layer it sequences.

**Zero circular imports; zero backward-flow violations.** The CI
import sweep (re-run this pass) confirms 195/195 modules import
cleanly.

## 2. Dead Code

Script-assisted (parse every top-level `class`/public `def` in every
tracked `.py` file, then grep-count real references anywhere in the
repo including `tests/`) pass, manually verified to exclude pytest's
`test_*` naming-convention discovery (not a real "unused" signal) and
any `TYPE_CHECKING`-only reference. Six genuine findings — all
**pre-existing** (none introduced by any Phase 59.x work in this
session), all self-consistent with their own "not yet wired"
docstrings rather than accidental orphans:

| Item | File | Status |
|---|---|---|
| `class DecisionResult` | `decision_layer/decision_engine/decision_engine.py:24` | Superseded — `DecisionEngine.decide()` actually returns `TradeDecision` (from `decision_layer/decision_engine/models.py`), never `DecisionResult`. Zero references anywhere. |
| `class SignalMonitor` | `core_layer/health_monitor/signal_monitor.py:16` | Self-documented placeholder ("Currently a placeholder... Signal ID, state, and timestamp will arrive via a future event contract"). Never constructed anywhere. |
| `def build_prompt()` | `ai/ai_prompt.py:40` | `ai/ai_analyzer.py` (the real, live AI analyzer) never imports `ai_prompt` — this is a disconnected, earlier-generation prompt builder. |
| `def evaluate_confidence()` | `ai/confidence_model.py:23` | Same disconnection — `ai_analyzer.py` never imports `confidence_model`. Its own docstring already says it's a no-op until a future phase populates `SignalCandidate.context_refs`. |
| `def is_doji()`, `body_ratio()`, `upper_wick()`, `lower_wick()` | `context_layer/context_engine/candle.py:23,33,36,42` | Candle-shape helper functions with zero callers anywhere (sibling functions `direction()`/`is_bullish()`/`is_bearish()`/`body_size()`/`range_size()` in the same file *are* used elsewhere and were correctly not flagged). |
| `def is_user()` | `telegram/permissions.py:59` | `get_permission_level()` in the same file falls through to `PermissionLevel.USER` directly without calling `is_user()` — the function exists but nothing calls it. |

**No action taken** — `decision_layer/decision_engine/decision_engine.py` and `ai/` are
both under `CLAUDE.md`'s "Trading Safety" explicit-approval
restriction, and `context_layer/context_engine/candle.py`/`monitoring/`/`telegram/permissions.py`
changes should go through the same review discipline as everything
else. This audit reports; it does not delete. A future, explicitly-approved
cleanup task should decide per item (delete `DecisionResult`/`SignalMonitor`
outright, or wire `build_prompt()`/`evaluate_confidence()` into `ai_analyzer.py`
if they were meant to be used — that decision needs the AI layer's
owner, not this audit).

## 3. Duplicate Logic

Checked the Director's own named candidate first — `feature_registry`
vs `runtime_feature` vs `feature_flags` — by reading all three source
files directly. **Confirmed layered, not duplicated:**

```
configuration/feature_flags.py (Phase A13)
  -- FeatureFlags: a static dataclass, every field defaults False,
     no runtime behavior, no persistence.
        |
        v  (read as one of two sources)
configuration/feature_registry.py (Phase 59.6)
  -- build_feature_registry(): unifies feature_flags.DEFAULT_FLAGS +
     config.Config's real ENABLE_* constants into one catalog.
     Read-only; no new logic, no gating.
        |
        v  (seeds the in-memory cache on load())
configuration/runtime_feature_manager.py (Phase 59.7)
  -- RuntimeFeatureManager: the only one of the three that is
     actually mutable/persisted/audited -- layers runtime overrides
     on top of feature_registry's static defaults.
```

Each layer adds something the one below it doesn't have (a unified
catalog view; then runtime mutability) — none re-implements the one
below it. No action needed.

**One real duplicate found, not previously flagged**: `telegram/owner/validation_commands.py`'s
`get_validation_report(signals, performances, period_start, period_end)`
(Phase 59 Real Market Validation Foundation) and
`telegram/owner/report_commands.py`'s `get_validation_summary(signals,
performances, period_start, period_end)` (Phase 59.8) share an
**identical call signature** and both explicitly target the same
future command name — `get_validation_summary()`'s own docstring says
"the future `/validation_report` command's payload." They differ only
in which builder they wrap (`analytics.validation_report.build_validation_report()`
vs `analytics.strategy_report.build_strategy_report()` +
`compute_win_rate()`), producing two different text formats for what
is meant to become the same one command. Unlike the
`list_features()`/`get_feature_states()` pair (deliberately different
questions: static vs. runtime), this pair answers the *same* question
twice. **Recommendation**: a future wiring phase must pick exactly one
for the live `/validation_report` command, same resolution pattern
already used for `/features` — flagged here, not resolved, since
picking one is a product decision (which report format the Director
wants), not an architecture one.

## 4. Database Audit

12 tables, 12 repositories, 1:1 — verified by cross-referencing every
`CREATE TABLE IF NOT EXISTS` in `database_layer/database_manager/models.py` against
`database/*_repository.py`:

| Table | Repository | Purpose |
|---|---|---|
| `signals` | `signal_repository.py` | Every signal sent to a user (pre-Phase-59, live) |
| `users` | `user_repository.py` | Registered Telegram users (pre-Phase-59, live) |
| `subscriptions` | `subscription_repository.py` | FREE/PREMIUM/VIP plan state (pre-Phase-59, live) |
| `feedback` | `feedback_repository.py` | User feedback messages (pre-Phase-59, live) |
| `admins` | `admin_repository.py` | ADMIN-tier Telegram IDs (pre-Phase-59, live) |
| `raw_candles` | `raw_candle_repository.py` | Per-provider OHLC storage (Phase 59.3) |
| `market_snapshots` | `market_snapshot_repository.py` | Computed HTF/context snapshots (Phase 59.3) |
| `sync_state` | `sync_state_repository.py` | Historical collector's per-`(provider,symbol,timeframe)` resume watermark (Phase 59.5) |
| `audit_log` | `audit_log_repository.py` | Append-only owner/system action trail (Phase 59.6) |
| `config_snapshots` | `config_snapshot_repository.py` | Rollback-capture on every runtime toggle (Phase 59.6/59.7) |
| `runtime_features` | `runtime_feature_repository.py` | One row per feature name, upserted (Phase 59.7) |
| `emergency_states` | `emergency_repository.py` | Append-only emergency state transition history (Phase 59.9) |

No duplicate tables, no unused tables — every table has exactly one
owning repository and at least one real caller (`RuntimeFeatureManager`,
`EmergencyManager`, the historical collector, or a live pre-Phase-59
service). `audit_log`/`config_snapshots` are only written to by
`RuntimeFeatureManager`/`EmergencyManager` today (no owner command's
real Telegram invocation exists yet to trigger a write in production)
— a live-wiring gap, not a schema problem.

## 5. Owner Audit

13 modules in `telegram/owner/`, mapped to the Director's 7 command
categories (`owner_roles.py`/`security.py` are cross-cutting support,
not a category of their own):

| Category | Module(s) | Functions |
|---|---|---|
| Status | `status_commands.py`, `system_commands.py` | `get_system_status()`, `get_system_health()`, `count_online_providers()` |
| Report | `report_commands.py` | `format_daily_stats()`, `get_validation_summary()`, `pick_best_strategy()` |
| Validation | `validation_commands.py` | `get_validation_status()`, `get_today_signals()`, `get_validation_report()` |
| Emergency | `emergency_commands.py` | `kill_system()`, `pause_system()`, `maintenance_on()`, `restore_system()`, `get_emergency_status()` |
| Dataset | `dataset_commands.py` | `get_dataset_status()`, `get_history_status()`, `get_sync_status()`, `get_provider_compare()` |
| Provider | `provider_commands.py` | `list_providers()`, `get_data_status()`, `enable_provider()`, `disable_provider()` |
| Control | `control_commands.py`, `feature_commands.py` | `get_feature_states()`, `enable_feature()`, `disable_feature()`, `list_features()` |

A second real overlap, beyond the validation-report pair in section 3:
`status_commands.get_system_status()` (Phase 59.8) and
`system_commands.get_system_health()` (Phase 59.3) both call
`AdminService().get_system_status()` and both derive
provider-availability information from `build_default_registry()`.
`system_commands.py`'s own docstring already calls itself "a superset,
not a replacement" of the plain `/system` command, but relative to
`status_commands.get_system_status()` specifically, the two now
genuinely compete for the same future `/system_status` command rather
than answering clearly different questions.

**Dashboard consolidation plan** — `telegram/owner/dashboard.py`
(Phase 59.8) today composes exactly 3 of these 7 categories (Status
via `status_commands`, Control via `control_commands`, Provider via
`provider_commands`). A future, separately-approved wiring phase
extending it to all 7 should, in order:

1. Resolve the two same-question overlaps first (`get_system_status()`
   vs `get_system_health()`; `get_validation_report()` vs
   `get_validation_summary()`) — extending the dashboard before
   resolving them would bake both into the single consolidated view.
2. Add Report, Validation, Dataset, Emergency sections to
   `get_dashboard()`, following the existing "each section catches its
   own errors, one failure degrades only that section" pattern already
   established for the first 3.
3. Gate the whole dashboard (and every individual command once live)
   with `security.py`'s `require_role()` — not called by anything yet.
4. Only then register commands into `telegram/commands.py`, per
   `docs/OWNER_COMMANDS.md`'s existing Roadmap section.

## 6. Pipeline Audit

The **real, live** pipeline (`core/pipeline.py`'s `run()`, re-read
this pass, every `self._log_stage(...)` call in call order) — this is
ground truth, not the aspirational full diagram:

```
market_data → data_quality → htf_bias → context → market_phase →
signal → signal_quality → explainability → features → ai →
decision → risk → signal_history → telegram_format →
telegram_delivery → database
```

This matches `CLAUDE.md`'s `data → context → strategies → signals →
ai → decision → risk → telegram → database` chain exactly, at finer
granularity (`strategies` isn't its own pipeline stage name because
`signal_layer/signal_engine/signal_engine.py` calls into `strategies/` internally during
the `signal` stage, not as a separate top-level phase).

The Director's requested full diagram adds four stages beyond what's
live today — **all confirmed foundation-only, not wired**:

```
... risk → [Execution] → [Paper] → [Analytics] → [Journal]
```

- **Execution**: `execution_layer/execution_engine/execution_engine.py` — confirmed inert,
  zero `order_send`/MT5 calls anywhere in `execution/` (re-grepped
  this pass), per `CLAUDE.md`'s own statement.
- **Paper**: `trade_monitoring_layer/paper_trading/paper_trade.py` + `trade_monitoring_layer/paper_trading/paper_trade_monitor.py`
  (Phase 59.4) — `PaperTradeMonitor` is never constructed anywhere
  outside `tests/` (re-grepped this pass); no cron/scheduler/pipeline
  call site exists.
- **Analytics**: `analytics/*.py` (`strategy_report`, `signal_performance`,
  `validation_report`, `dataset_report`, `gap_report`, `context_report`)
  — all consumer-side, computed on demand from already-persisted data
  via an owner command or a test, never as a per-cycle pipeline stage.
- **Journal**: `ai/journal/failure_analysis.py`/`trade_journal.py` —
  same posture, standalone/on-demand.

None of these four should be added as literal `_log_stage()` calls
inside `core/pipeline.py`'s `run()` without a separate, explicit
approval per `CLAUDE.md`'s Trading Safety rules — `run()` executes
every cycle in production; Execution specifically must stay inert
until MT5 order wiring is itself an explicitly-approved phase.

## Summary of actionable findings

1. **`get_validation_report()` vs `get_validation_summary()`** —
   real duplicate, same signature, same target command. Needs a
   product decision on which format to keep (section 3).
2. **`get_system_status()` vs `get_system_health()`** — real overlap,
   both targeting `/system_status`. Needs the same kind of decision
   (section 5).
3. **Six dead-code items** (section 2) — reported, not touched;
   `decision_layer/decision_engine/decision_engine.py`'s `DecisionResult` and `ai/`'s
   `build_prompt()`/`evaluate_confidence()` need the Trading
   Safety/AI-layer owner's explicit sign-off before any removal or
   wiring.

Everything else audited (dependency graph, the `feature_registry`
trio, all 12 database tables, the live pipeline's 16 real stages) is
clean — no circular imports, no schema duplication, no accidental
reimplementation.

## Director decisions (post-audit, APPROVED)

The audit itself was approved as-is. Six explicit decisions were made
on top of it — recorded here as the resolution of record; **none is
implemented yet**, each is a target shape for a future, separately-approved
wiring/consolidation phase, not an instruction to refactor
`telegram/owner/` in this pass:

1. **Validation Report duplicate (finding 1)** — `report_commands.get_validation_summary()`
   is kept; `validation_commands.get_validation_report()` is
   deprecated in favor of it, because validation is a kind of report,
   not a separate category. Target future shape for
   `report_commands.py`: `get_validation_summary()`,
   `get_strategy_report()`, `get_context_report()`,
   `get_dataset_report()`, `get_daily_report()`, `get_weekly_report()`,
   `get_monthly_report()` — one report module, not one module per
   report type.
2. **System Status duplicate (finding 2)** — `status_commands.get_system_status()`
   is kept as the Owner Dashboard's primary Status module;
   `system_commands.get_system_health()` folds into it as one section
   among several. Target future shape for `status_commands.py`:
   System, Database, Providers, Pipeline, Emergency, Features,
   Validation, Performance, Health, Resources — all visible from one
   place.
3. **Dead code (section 2)** — untouched. Rule: never remove trading
   code without a separate, dedicated audit.
4. **AI module (`build_prompt()`/`evaluate_confidence()`)** — left as
   is. Re-audit when v0.4 AI Intelligence work begins.
5. **`SignalMonitor` placeholder** — kept; reserved for a future Live
   Monitoring feature.
6. **Module Reuse Principle** — promoted from this doc's companion
   (`docs/PHASE59_ARCHITECTURE_FREEZE.md`'s "Design principle"
   section) to a mandatory rule in `CLAUDE.md` itself (this repo's own
   governance file), under "Restrictions." Applies to all new module
   creation from this point forward.

Phase 60.1+ implementation work should not start on findings 1–2 until
a separately-approved wiring phase is assigned for each; this audit
records the decision, not the change.
