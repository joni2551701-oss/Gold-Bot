# Emergency Safety Layer — Foundation (Phase 59.9)

**Not wired into the live bot.** Same posture as every Owner Mode
phase before it (Phase 59.3-59.8): real, tested, standalone modules
exist; nothing is registered into `telegram/commands.py`,
`telegram/command_router.py`, or `telegram/handlers.py`; nothing in
`core/pipeline.py`, `decision/`, `risk/risk_manager.py`, or
`execution/` reads or is blocked by any module in this phase. No real
order or signal is blocked by this phase's code.

## Modules

```
core/emergency/
├── emergency_state.py     -- EmergencyState enum + EmergencyStateRecord (domain model)
├── emergency_manager.py   -- EmergencyManager (the runtime controller)
├── circuit_breaker.py     -- evaluate_circuit() (pure decision function)
└── maintenance.py         -- MaintenanceMode (detail record for EmergencyState.MAINTENANCE)

database/
├── emergency_models.py      -- EmergencyStateEntry (DB row shape)
└── emergency_repository.py  -- EmergencyRepository (append-only history)

telegram/owner/
└── emergency_commands.py  -- kill_system()/pause_system()/maintenance_on()/restore_system()/get_emergency_status()
```

## State diagram

```
                    activate_pause()
        +-------------------------------+
        |                                v
   [NORMAL] <----restore_normal()---- [PAUSED]
        |                                ^
        | activate_kill()                | (owner/system decides to
        v                                |  step down from KILLED,
   [KILLED] ----restore_normal()---------+  via restore_normal())
        |
        | activate_maintenance() / restore_normal()
        v
   [MAINTENANCE] <---> [NORMAL]

   [WARNING] -- reachable only as a circuit_breaker.evaluate_circuit()
                CircuitDecision, not an EmergencyManager transition in
                this phase (see "Known gap" below).
```

Every transition (including a repeated `NORMAL -> NORMAL`) is recorded
as a **new row** in `emergency_states` — nothing is ever overwritten.
`EmergencyRepository.get_current_state()` derives "now" from the most
recent row; `get_history()` returns the full, never-lost sequence
(`NORMAL -> PAUSED -> NORMAL`, etc., per this phase's own acceptance
criteria).

## EmergencyState vs core.system_state.SystemState

Two deliberately separate vocabularies, same "two hierarchies for two
granularities" precedent as `telegram.owner.owner_roles.OwnerRole` vs
`telegram.permissions.PermissionLevel` (Phase 59.6/59.8).
`core.system_state.SystemState`'s own docstring reserved
`PANIC`/`MAINTENANCE` "for a future Phase 59.9" — this phase does not
reuse those two values because `SystemState` has no equivalent of
`WARNING`/`PAUSED` (a circuit-breaker-driven, less-severe posture,
distinct from a full `KILLED` stop), which `circuit_breaker.py` needs.
Reconciling the two enums (or having one wrap the other) is a future,
separately-approved decision — this phase does not touch
`core/system_state.py`.

## Safety rules

- **`EmergencyManager` never calls Risk Manager, Decision Engine, or
  any execution code** — it only persists a state transition and
  writes an audit entry. Blocking a real signal/order based on this
  state is a future, separately-approved wiring phase.
- **`evaluate_circuit()` is pure and stateless** — no database, no
  side effects, never called from `core/pipeline.py` or any pipeline
  stage in this phase. It returns a decision; it does not act on one.
- **Every transition is audited**, never silently applied:
  `KILL_ACTIVATED`, `PAUSE_ACTIVATED`, `MAINTENANCE_ENABLED`,
  `SYSTEM_RESTORED` (via `database.audit_log_repository.AuditLogRepository`,
  Phase 59.6) — one entry per call to `activate_kill()`/`activate_pause()`/
  `activate_maintenance()`/`restore_normal()`, `result="SUCCESS"`
  always (this phase has no rejection path — unlike Phase 59.7's
  dependency-validated feature toggles, there is no invalid emergency
  transition to reject).
- **History survives a restart** — `EmergencyManager()` constructed
  fresh (own `EmergencyRepository()`) reads the same current state and
  full history back from the same database file, same guarantee
  `RuntimeFeatureManager` already provides for feature toggles.

## Known gap: WARNING is not a manager transition in this phase

`EmergencyState.WARNING` exists in the enum and
`circuit_breaker.CircuitDecision.WARNING` can be produced by
`evaluate_circuit()`, but `EmergencyManager` exposes no
`activate_warning()` — this task's own brief lists only
`activate_pause()`/`activate_kill()`/`activate_maintenance()`/
`restore_normal()`/`get_status()`. A future wiring phase deciding how
a `CircuitDecision.WARNING` should affect the persisted
`EmergencyState` (raise a `WARNING` transition? just log it? require
two consecutive `WARNING`s before a real `PAUSED`?) is explicitly out
of scope here.

## Future wiring plan

```
docs/EMERGENCY_SYSTEM.md (Phase 59.9 -- foundation, this document)
        |
        v
core/emergency/*.py, database/emergency_*.py,
telegram/owner/emergency_commands.py (Phase 59.9 -- real logic, not wired)
        |
        v
Phase 60.8 (Safe Integration Layer) closed the first bullet below —
see its own section further down this document. The rest remain
future, separately-approved steps:
  - ~~core/pipeline.py: check EmergencyManager.get_status() before a
    stage runs (e.g. skip signal generation when PAUSED/KILLED)~~ —
    done, via `core/guards/pipeline_guard.py`'s `PipelineGuard`
  - risk/risk_manager.py or a stage ahead of it: feed live
    loss/drawdown/api/execution signals into
    circuit_breaker.evaluate_circuit(), and decide what a BLOCK/WARNING
    decision should do to EmergencyManager's state
  - execution/: an actual order-blocking check reading
    EmergencyManager.get_status() (execution/ is still intentionally
    inert today -- no MT5 order calls exist, per CLAUDE.md)
  - telegram/commands.py / telegram/command_router.py / telegram/handlers.py:
    register /panic, /pause, /maintenance, /restore, /emergency_status,
    using telegram/owner/security.py's require_role() (Phase 59.8) for
    the per-command minimum-OwnerRole gate, and
    telegram/owner/emergency_commands.py's functions as the payload
  - a decision on how EmergencyState reconciles (or doesn't) with
    core.system_state.SystemState -- both exist independently today
```

## Phase 60.8: Safe Integration Layer — Emergency Hook

`core/guards/pipeline_guard.py`'s `PipelineGuard` is the first real
caller of `EmergencyManager.get_status()` (previously zero callers
outside this module's own tests and `telegram/owner/emergency_commands.py`,
confirmed by `docs/PHASE60_8_INTEGRATION_AUDIT.md`'s TASK 1 audit).
Read-only: `PipelineGuard` never calls `activate_pause()`/
`activate_kill()`/`activate_maintenance()`/`restore_normal()` itself —
only an owner (once a future, separately-approved phase wires a
command) or the circuit breaker can actually transition
`EmergencyState`.

Mapping, checked at each of `core/pipeline.py`'s four guarded stage
boundaries (`signal`, `ai`, `telegram_delivery`, `database` — see
`docs/PIPELINE_GUARD.md` for the full stage diagram):

| `EmergencyState` | Effect |
|---|---|
| `NORMAL` | every stage proceeds normally |
| `WARNING` | every stage proceeds; one `logger.warning()` per guard check |
| `PAUSED` | `telegram_delivery` is skipped; `signal`/`ai`/`database` proceed |
| `MAINTENANCE` | all four stages skip (see `docs/PIPELINE_GUARD.md`'s Disclosed Finding 1 for the one honest gap — read-only context stages ahead of the first hook still run) |
| `KILLED` | the pipeline run aborts immediately at the first hook checked |

This is intentionally the minimum real behavior change this phase
makes: `EmergencyManager`'s own state machine, persistence, and audit
trail are entirely unmodified — `PipelineGuard` only reads the current
state and translates it into a proceed/skip/abort decision for
`core/pipeline.py` to act on. See `docs/PIPELINE_GUARD.md` for the
full design rationale and disclosed findings.
