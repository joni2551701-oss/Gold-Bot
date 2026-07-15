# Phase 59 Architecture Freeze Audit

Director-requested full-project re-audit after Phase 59.9 (Emergency
Safety Layer Foundation), CI run #52 (commit `94a7177`) green — before
Phase 60 (real trading intelligence) begins. Scope: excess/redundant
modules, duplicate logic, wrong dependencies, a consolidated wiring
plan, and the v1.0 roadmap. Every claim below was re-verified against
the actual source this pass (grep/import sweep re-run, `telegram/commands.py`
read directly), not assumed from earlier phases' own docs.

This supersedes nothing — `docs/ARCHITECTURE_AUDIT.md`/`DEPENDENCY_MAP.md`/
`FOUNDATION_GAP_ANALYSIS.md` (Phase A1, pre-`v0.3.5`) remain valid
historical snapshots of that earlier state. This document is the
Phase 59 milestone's own audit, current as of `94a7177`.

## Phase 59 status

| Phase | Scope | Status |
|---|---|---|
| 59.1 | Provider Foundation | ✅ |
| 59.2 | Provider Registry | ✅ |
| 59.3 | Raw Storage | ✅ |
| 59.4 | Paper Validation | ✅ |
| 59.5 | Historical Dataset | ✅ |
| 59.6 | Audit & Observability | ✅ |
| 59.7 | Runtime Feature Toggle | ✅ |
| 59.8 | Owner Dashboard Foundation | ✅ |
| 59.9 | Emergency Layer Foundation | ✅ (CI run #52, commit `94a7177`, success) |

195 non-test modules, 116 test files, 1164 tests passing, 0 circular
imports (re-confirmed this pass via the same import-sweep CI runs —
see "Dependency direction audit" below).

## 1. Redundant/parallel module audit

Five deliberate parallel hierarchies exist in the codebase. All were
disclosed explicitly at the phase that introduced the newer half of
each pair; none is an accidental duplicate — each pair answers a
different question or serves a different layer. Re-confirmed here,
in one place, for the freeze:

| Pair | Difference | Reconcile before v1.0? |
|---|---|---|
| `core.system_state.SystemState` (Phase 59.6) vs `core.emergency.emergency_state.EmergencyState` (Phase 59.9) | `SystemState` is a coarse, unheld display-label enum (`RUNNING`/`VALIDATION`/`MAINTENANCE`/`PANIC`/`READ_ONLY`); `EmergencyState` is the actual runtime-controlled, persisted, audited state machine (`NORMAL`/`WARNING`/`PAUSED`/`KILLED`/`MAINTENANCE`) with a manager. `SystemState`'s own docstring reserved `PANIC`/`MAINTENANCE` "for a future Phase 59.9" but `EmergencyState` ended up a separate, finer enum instead (needed `WARNING`/`PAUSED`, which `SystemState` has no equivalent of). | **Yes** — a future wiring phase should decide whether `SystemState` becomes a thin display view derived from `EmergencyManager.get_status()`, or is retired in favor of `EmergencyState` everywhere. Two sources of truth for "is the bot OK" is the one loose end this freeze surfaces. |
| `telegram.owner.owner_roles.OwnerRole` (Phase 59.6) vs `telegram.permissions.PermissionLevel` (pre-Phase-59, live) | `PermissionLevel` (`OWNER`/`ADMIN`/`USER`) is the real enum `telegram/command_router.py`'s `_PERMISSION_RANK` gates the live 26 commands with today. `OwnerRole` (`OWNER`/`SUPER_ADMIN`/`ADMIN`/`VIEWER`) is a finer, not-yet-wired hierarchy for the future Owner Dashboard. | No — by design, documented in `docs/OWNER_PERMISSIONS.md` since Phase 59.6. A live-wiring phase for `telegram/owner/` will make `OwnerRole` real; `PermissionLevel` keeps gating the existing 26 commands unchanged either way. |
| `telegram.owner.feature_commands.list_features()` (Phase 59.3, static `Config`/`FeatureFlags` view) vs `telegram.owner.control_commands.get_feature_states()` (Phase 59.8, runtime `RuntimeFeatureManager` view) | Answer different questions: "what does this flag default to" vs "what has an owner actually toggled right now." | **Yes** — `docs/OWNER_COMMANDS.md` already flags this: a future `/features` wiring step must pick exactly one. Both stay until that step. |
| `configuration.feature_registry.FeatureDescriptor` / `configuration.runtime_state.FeatureRuntimeState` / `database.runtime_feature_models.RuntimeFeatureRecord` (Phase 59.6/59.7) — and the equivalent triad `core.emergency.emergency_state.EmergencyStateRecord` / `database.emergency_models.EmergencyStateEntry` (Phase 59.9) | Consistent "static declaration → in-memory runtime view → DB row" split repeated twice, once for features and once for emergency state. Same pattern both times, not a duplication of each other (`FeatureDescriptor` and `EmergencyStateRecord` describe unrelated things). | No — this is the codebase's own established modeling convention (declared in `configuration/README.md`/`database/README.md`), applied consistently. Nothing to reconcile. |
| `core.emergency.maintenance.MaintenanceMode` (Phase 59.9) vs `EmergencyState.MAINTENANCE` (same phase) | Enum value vs. detail record — same "enum value vs. detail record" split as `FeatureDescriptor` vs `FeatureRuntimeState` above. | No — intentional, same convention. |

No accidental duplicate function names were found: a repo-wide scan
of every `def` in `telegram/owner/`, `core/emergency/`, and
`configuration/` shows zero name collisions outside the pairs above,
all of which are deliberately, differently named
(`list_features`/`get_feature_states`, `enable`/`enable_feature`
aliases documented in `runtime_feature_manager.py`'s own docstring,
etc.).

## 2. Duplicate logic check

- `python -m pyflakes $(git ls-files '*.py')` — clean (0 findings) as
  of `94a7177`.
- No two repositories implement the same table's CRUD twice; no two
  services recompute the same metric with different formulas (every
  win-rate figure in `telegram/owner/report_commands.py` — daily
  stats, validation summary — routes through the single
  `analytics.strategy_report.compute_win_rate()`).
- The one place two *different* upsert conventions coexist
  (`runtime_features`: one row per name, upsert; `emergency_states`:
  append-only) is intentional and documented in both tables' own
  schema docstrings (`database/models.py`) — a feature has one current
  value to overwrite, an emergency transition is a historical event
  that must never be overwritten.

## 3. Dependency direction audit

Re-ran the exact import-sweep CI uses
(`.github/workflows/ci.yml`'s "Smoke import" step, every `.py` file
in the repo except `tests/`): **195 modules, 0 import failures, 0
circular imports.**

Confirmed directly by reading `core/pipeline.py`'s own import list and
grepping `core/pipeline.py`, `decision/`, `risk/risk_manager.py`,
`execution/`, `telegram/handlers.py`, `telegram/command_router.py`,
`telegram/commands.py`, `telegram/permissions.py` for any reference to
a Phase 59.x foundation module (`runtime_feature`, `emergency_manager`,
`emergency_state`, `audit_log_repository`, `config_snapshot`,
`owner_roles`, `feature_registry`, `feature_dependency_validator`,
`runtime_api`, `runtime_state`): **zero matches.** The live trading
path (`data → context → strategies → signals → ai → decision → risk →
telegram → database`, per `CLAUDE.md`) is unchanged and untouched by
any Phase 59 foundation module, exactly as every phase's own
validation report claimed.

Every new one-directional cross-layer edge introduced since Phase 59.3
remains one-directional, never reversed (re-confirmed by reading the
importing side of each):

- `data/` → `database/` (Phase 59.5: historical collector persists what it fetches)
- `monitoring/` → `data/providers/` (Phase 59.2: provider health reads the registry)
- `configuration/` → `database/` (Phase 59.7: `RuntimeFeatureManager` persists toggles)
- `core/emergency/` → `database/` (Phase 59.9: `EmergencyManager` persists transitions)
- `telegram/owner/` → `configuration/`, `database/`, `core/emergency/`, `core.system_state` (every Owner Mode module composes lower-layer pieces, never the reverse)

## 4. Consolidated wiring plan

Ground truth, read directly from `telegram/commands.py` this pass —
**the live bot's actual command surface today is exactly 26 commands**:
17 in `COMMANDS`, 5 in `OWNER_COMMANDS`, 8 in `ADMIN_COMMANDS`
(`admin`/`system`/`broadcast` counted once each, shared between the
latter two). None of Phase 59.1–59.9's work appears in any of the
three dicts.

**Foundation-only (real code, tested, not wired into the live bot):**

| Package | What it is | What wiring it into `core/pipeline.py`/`telegram/` would require |
|---|---|---|
| `telegram/owner/` (all 13 modules) | Every owner-facing view/control built across Phase 59.1–59.9 | New entries in `telegram/commands.py`'s `OWNER_COMMANDS`, routing in `telegram/command_router.py` using `telegram/owner/security.py`'s `require_role()`, new handlers in `telegram/handlers.py` calling these functions |
| `configuration/runtime_feature_manager.py` | Real, working runtime toggle (validated/persisted/audited/snapshotted) | Nothing in `core/pipeline.py` currently constructs a `RuntimeFeatureManager` or checks a feature's runtime value before running a stage |
| `core/emergency/emergency_manager.py` | Real, working kill/pause/maintenance/restore controller | Nothing in `core/pipeline.py`/`risk/risk_manager.py`/`execution/` reads `EmergencyManager.get_status()` before running; `core/emergency/circuit_breaker.py`'s `evaluate_circuit()` is never fed live loss/drawdown/api data |
| `core/system_state.py` | A pure enum + record, no holder | No singleton exists anywhere holding "the" current `SystemState` |
| `database/audit_log_repository.py` | Real, append-only audit trail | Only written to by `RuntimeFeatureManager`/`EmergencyManager` today — no owner command's real invocation exists yet to trigger those writes in production |
| `database/config_snapshot_repository.py` | Real rollback-capture mechanism | Only written to by `RuntimeFeatureManager` today; nothing reads a snapshot back to actually roll back a config yet |

**Live and protected (the real trading path, untouched by any Phase
59 work):** `data/` → `context/` → `strategies/`/`signals/` → `ai/`
→ `decision/decision_engine.py` → `risk/risk_manager.py` →
`telegram/notifier.py` → `database/signal_repository.py`. Every
signal that reaches a user still passes through
`RiskManager.evaluate()` with no shortcut, per `CLAUDE.md`'s own
"Never bypass Risk Manager" rule — confirmed unchanged this pass.

## 5. v1.0 roadmap (Phase 60, Director's reordering)

Per the Director's stated reasoning — the bot should prove itself
against historical data before an AI/Fundamental layer is built on
top of it:

```
Phase 60
│
├── 60.1 Multi-Provider Live Integration
├── 60.2 Backtesting Engine
├── 60.3 Market Replay
├── 60.4 Historical Validation           <- reordered ahead of Fundamental
├── 60.5 Fundamental Intelligence
├── 60.6 Economic Calendar
├── 60.7 News Engine
└── 60.8 Learning Loop
```

Largest remaining blocks, still foundation-only or entirely missing:

1. **Backtesting Engine** — history replay, tick/candle simulation,
   fill model, slippage model, spread simulation. Nothing in this
   codebase does this yet; Phase 59.5's `data/historical_data_collector.py`/
   `RawCandleRepository` is the dataset this phase would consume.
2. **Fundamental Intelligence** — economic calendar, manual weekly
   plan, news result processing, FRED integration (Phase 59.2's
   `FredProvider` is a stub only), macro scoring.
3. **Learning Loop** — trade outcome analysis (Phase 59.4's
   `analytics/`/`lifecycle/paper_trade.py` is the data source),
   strategy performance weighting, AI knowledge updates, context
   learning.
4. **Live wiring** — per the table in section 4 above: Runtime
   Features → Pipeline, Owner Commands → Telegram, Emergency Layer →
   Execution, Validation → Analytics, Historical Dataset →
   Backtesting. Each is a separate, explicit approval per
   `CLAUDE.md`'s "Trading Safety" rules — none should be bundled into
   a single "wire everything" change.

## Recommendation

No urgent fixes are needed before Phase 60 starts. Every parallel
hierarchy found is intentional and already documented at its point of
origin; this audit's only new finding is the `SystemState` vs
`EmergencyState` overlap (section 1), which is a **future** wiring
decision, not a defect — nothing currently reads either enum's value
to make a real decision, so there is no live inconsistency to fix
today. The architecture is safe to freeze as-is. Backtesting (60.2)
is the natural first consumer of the Historical Dataset work
(Phase 59.5) already built, and should not require touching any
Phase 59 foundation module to get started.

## Design principle (in force from this freeze forward)

Before any new module (new file, new package, or a new top-level
class/function in an existing file) is written, its author must
answer, in order, and stop at the first "yes":

```
1. Does this already exist somewhere in the repo?
       |
       v (no)
2. Can an existing module be extended to cover this
   (a new method, a new optional field, a new function
   in an existing file) without breaking its current
   contract?
       |
       v (no)
3. Is a genuinely new module required?
       |
       v (yes)
   Create it — and document, in the new module's own
   docstring, why steps 1 and 2 were both "no".
```

"Reuse" (step 1 or 2) is the default outcome, not the exception —
every parallel hierarchy in section 1 above exists because a real,
narrow difference in *meaning* justified a new name (a static default
vs. a runtime value; a coarse display label vs. an audited, persisted
state machine), never because reuse was merely inconvenient. A new
top-level package (`core/emergency/`, `configuration/`, `lifecycle/`,
etc.) is the highest-cost option on this list and should be rare —
Phase 59's own history shows most work landed as a new file inside an
*existing* package (`telegram/owner/*.py`, `database/*_repository.py`)
rather than a new package, and that ratio should hold going forward.
This rule governs Phase 60 onward; it does not require revisiting any
already-shipped Phase 59.x decision.
