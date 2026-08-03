# GoldBot Core Owner Monitoring Alpha — Foundation Reuse Audit (TASK 0)

Governed by `docs/constitution/CONSTITUTION.md` Article 11 (Foundation
Reuse Law). This is the mandatory TASK 0 audit for the "GoldBot Core
Owner Monitoring Alpha" Worker Brief — a V1 pre-production observation
phase, not part of the `66.x` AI Trading Intelligence sub-sequence.
Every package the brief names (`monitoring/`, `logs/`, `database/`,
`telegram/`, `core/`, `signals/`) is audited before any new module is
created. Findings below are exhaustive; conclusions state exactly what
is reused, what is extended, and what is genuinely new.

## `monitoring/` (top-level package)

Three files already exist:

- **`core_layer/health_monitor/signal_monitor.py`** — `SignalMonitor`/`MonitorConfig`/
  `MonitorResult`. A dead placeholder: `monitor()` takes no parameters
  and always returns `MonitorResult(monitored=False, reason="Not
  implemented")`. Confirmed **zero callers anywhere in the codebase**
  (grep for `SignalMonitor`/`MonitorConfig`/`MonitorResult` outside
  this file itself returns nothing). Different shape from what this
  brief's own TASK 4 (`total_signals`/`buy_count`/`sell_count`/
  `none_count`/`average_confidence`) needs. **Decision**: this file is
  extended in place — the dead placeholder classes are left untouched
  (Article 9 discipline even though nothing calls them), and the real
  `get_signal_health()`/`SignalHealth` implementation is added
  alongside.
- **`core_layer/health_monitor/provider_health.py`** — real, live logic:
  `check_provider_health()`/`check_registry_health()`/
  `ProviderHealthReport`/`ProviderHealthStatus` (ONLINE/DEGRADED/
  OFFLINE), measuring how long each registered `DataProvider`'s
  `get_market_status()` call takes. **Genuinely reusable** for this
  brief's TASK 3 (Market Data Monitor) `data_source_status`/latency —
  composed, not duplicated.
- **`core_layer/health_monitor/performance.py`** — real `PerformanceTracker`/
  `PerformanceResult` computing win-rate/strategy-breakdown from
  `SignalRepository`'s closed signals. A **different concern**
  (historical trade-outcome performance) from this brief's
  `SignalHealth` (today's activity counts: buy/sell/none + average
  confidence) — not reused, not touched.

## `telegram/owner/` (22 existing files)

Five files reviewed in full per TASK 0's own list:

- **`telegram/owner/status_commands.py`** — real `get_system_status()`
  composing `AdminService().get_system_status()` + provider registry +
  `core_layer.system_state.system_state.SystemState` + `SignalRepository.get_latest_signal()`
  into a "GoldBot Status" text block. **Not live-wired** to any
  command. Close in spirit to this brief's `/status`, but a different
  structured shape (no uptime/last_scan/last_error fields) — not
  reused directly; the new `SystemHealth` model composes the same
  underlying sources independently to get those additional fields.
- **`telegram/owner/system_commands.py`** — real `get_system_health()`
  composing `AdminService().get_system_status()` +
  `check_registry_health()` into a full diagnostic block; also
  `count_online_providers()`. **Not live-wired.** **This is a direct,
  strong match for this brief's `/health` ("To'liq diagnostika")** —
  reused as-is, only wired to a live command. No new "full diagnostics"
  function is written.
- **`telegram/owner/dashboard.py`** — `get_owner_summary()` (the real,
  **live** `/owner` command) and `get_doctor_report()` (the real,
  **live** `/doctor` command) already surface system/AI/provider/
  signals-today/win-rate/emergency status. Reviewed to avoid
  duplicating their content; the new `/status`/`/health`/`/market`/
  `/signals`/`/errors`/`/pipeline`/`/report` commands are additive,
  narrower, and monitoring-specific — none of their command names
  collide with `/owner`/`/doctor`.
- **`telegram/owner/security.py`** / **`telegram/owner/owner_roles.py`**
  — a foundation-only, four-tier `OwnerRole` (OWNER/SUPER_ADMIN/ADMIN/
  VIEWER) + `require_role()`/`log_owner_action()`, explicitly
  documented as not enforced anywhere. This is a **separate hierarchy**
  from the live gate (see "Security" section below) — not extended
  this phase; this brief's own TASK 8 says "Hozir: faqat OWNER
  ishlaydi" (only OWNER works for now), which the live gate already
  satisfies exactly.
- **`telegram/owner/report_commands.py`** — `format_daily_stats()`/
  `get_validation_summary()` take pre-fetched `SignalSchema`/
  `SignalPerformance` lists as parameters; nothing in the codebase
  persists those shapes yet, so these functions cannot be called from
  a real handler without new data-sourcing work first (per their own
  docstrings). Not reused for `/report` — the new `/report` command
  instead composes this phase's own new monitoring functions.

## Security — access control

**No `telegram/access_control.py` (or anything shaped like it) exists
anywhere** — the only `access_control.py` in the repo is
`ai/access/access_control.py`, a different subsystem (AI capability
tier gating, not Telegram owner/admin command gating).

The **live, already-enforced** mechanism is:
`telegram/permissions.py`'s `PermissionLevel` (OWNER/ADMIN/USER) +
`is_owner()` (sourced from `core.secrets.Secrets.TELEGRAM_OWNER_ID`,
one env var, singular — no `OWNER_IDS` list exists anywhere) +
`telegram/command_router.py`'s `_required_level()`, which ranks a
command as OWNER-only by checking membership in
`telegram.commands.OWNER_COMMANDS`. Every existing Owner-only command
(`/owner`, `/doctor`, `/runtime`, etc.) is gated this exact way.
**Decision**: this brief's TASK 8 ("mavjud tizim" — existing system)
is fully satisfied by this live mechanism. No new `access_control.py`
is created; the new commands are registered in `OWNER_COMMANDS` only
(never dual-listed in `ADMIN_COMMANDS`), the same convention `/doctor`
already uses.

## `core/`

- **`core_layer/logger/logger.py`** — `setup_logger()` is a bare stdlib
  `logging.Logger` (stdout only, no file handler, no persistence, no
  structured event object). Confirmed via repo-wide grep: **no
  `ErrorEvent`, no `error_monitor`, no `severity` field, no
  error-capture/persistence mechanism of any kind exists anywhere in
  this codebase.** This is a genuine gap — `core_layer/health_monitor/error_monitor.py`
  and its persistence are new.
- **`core_layer/system_state/system_state.py`** — `SystemState` enum + `SystemStateRecord`
  (one immutable transition record). Explicitly documented as having
  **no live singleton/holder anywhere** — nothing mutates or reads a
  "current state." Not useful for uptime tracking (a running-process
  concept); reused only as `status_commands.py` already does, as a
  display label sourced from `Config.VALIDATION_MODE`.
- **`core/pipeline.py`** — confirmed (read-only) that
  `persist_signals=True` writes a `SignalRecord` per evaluation cycle,
  including REJECT/NO_TRADE candidates, via
  `SignalRepository.save_signal_record()`. Not modified (Strict Rule).

## `database/`

Every `*_repository.py` reviewed. None stores `SystemHealth`
(status/uptime/last_scan/last_error/data_connection/database_status),
`MarketHealth` (symbol/last_price/last_update/latency/
data_source_status), or `ErrorEvent` (timestamp/module/error_type/
message/severity) in that shape — genuine gaps for those three.
`SignalRepository` already has `count_signals_today()`/
`get_closed_signals_today()`/`get_open_signals()`/`get_closed_signals()`
but no "all of today's signals, any status" read — a minimal, additive
`get_signals_today()` method is added (mirrors the existing
`count_signals_today()`/`get_closed_signals_today()` pattern exactly).
`MarketSnapshotRepository` stores candle-window *provenance*
(symbol/timeframe/candle_count/provider/data_quality), not live
price/latency — a different concern, not reused.

**Decision on TASK 9's "Saqlash: health snapshots, error events,
signal statistics"**: `SystemHealth`/`MarketHealth`/`SignalHealth` are
computed live, on demand, from already-existing sources — matching the
established house convention every comparable module already follows
(`AdminService.get_system_status()`, `system_commands.get_system_health()`,
`PerformanceTracker.calculate()` are all computed-on-demand, none
persist a redundant "snapshot" row, and nothing in the brief's own
worked examples implies historical trending is needed yet). Only
**error events** (genuinely no existing capture mechanism) and
**decision pipeline entries** (TASK 5 explicitly names these as a
future `66.5`/`66.6` datasource, which must survive process restarts
to accumulate) get new tables — `database_layer/audit_log/monitoring_models.py` +
`database_layer/audit_log/monitoring_repository.py` (new, minimal, two tables).
Signal statistics reuse `SignalRepository` — no new storage.

## `signals/` and `context/` — structured evaluation trace

`decision_layer/decision_engine/decision_engine.py` only exposes a **weighted blend score**
(`signal_score`/`htf_score`/`risk_score`/`ai_score`/`final_score`, all
continuous floats) — not a Market Structure/Liquidity/FVG pass-fail
trace. The actual structured, already-computed, per-criterion trace
the brief describes lives in **`signal_layer/signal_scoring/signal_quality.py`**:
`SignalQualityResult` (`grade`, `score`, `criteria_met: Sequence[str]`
— e.g. `("HTF_ALIGNED", "LIQUIDITY_SWEPT")`, `criteria_total`), built
from `context.context_orchestrator.ContextSnapshot`'s own structure/
liquidity/order-block/FVG detector output. Nothing currently logs or
persists a `SignalQualityResult`. **Decision**: `decision_layer/decision_logger/decision_logger.py`
accepts **primitive fields only** (`criteria_met: Sequence[str]`,
`criteria_total: int`, `decision: str`, `reason: str`) rather than
importing `SignalQualityResult`/`signal_layer.signal_scoring.signal_quality` directly —
the same "primitive contract, no upstream object import" discipline
this codebase's `ai/*/models.py` Foundation contracts already
established for observability boundaries. This keeps `monitoring/`
free of any `signals`/`context` import, satisfying TASK 8's isolation
list conservatively (which names only `decision`/`risk`/`execution` as
forbidden imports, but this is a stricter, safer choice).

## `data_layer/providers/`

`ProviderRegistry`/`build_default_registry()` confirmed as the plain
catalog `core_layer/health_monitor/provider_health.py` already composes. No existing
"last candle received" / data-freshness concept anywhere — only
`ProviderHealthReport.latency_ms` (API-call latency) and `.checked_at`
(when the health check ran) exist; `ProviderStatus` itself carries no
price or last-update timestamp. **Decision**: `MarketHealth.last_price`/
`.last_update` are `Optional`, populated only via an injectable
snapshot parameter — `None` (never fabricated) when the caller
supplies nothing, consistent with this codebase's "never invent data"
discipline.

## Conclusion — genuine gaps, TASK 1's package decision

Per Constitution Article 11 step 2: two functions (`get_system_health()`,
provider health) are reused outright; `SignalRepository` and
`core_layer/health_monitor/signal_monitor.py` are extended in place; the live
`telegram/permissions.py` + `command_router.py` gate is reused
unchanged. The genuine new surface is: `core_layer/health_monitor/models.py`,
`core_layer/health_monitor/system_monitor.py`, `core_layer/health_monitor/market_monitor.py`,
`decision_layer/decision_logger/decision_logger.py`, `core_layer/health_monitor/error_monitor.py`,
`telegram/owner/monitoring_commands.py` (the brief names
`telegram/owner_commands.py`; the existing, established convention is
one file per feature inside the already-existing `telegram/owner/`
package — e.g. `report_commands.py`, `performance_commands.py` — so
`telegram/owner/monitoring_commands.py` follows that convention rather
than creating a same-named top-level file), and
`database_layer/audit_log/monitoring_models.py`/`database_layer/audit_log/monitoring_repository.py`.
No new top-level package.

## Related documents

- `docs/PHASE_CORE_MONITORING_FREEZE.md` — this phase's own freeze.
- `docs/architecture/MONITORING.md` — the full subsystem documentation
  (TASK 11).
