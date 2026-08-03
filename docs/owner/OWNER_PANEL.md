# GoldBot — Owner Panel Architecture

Governed by `docs/constitution/CONSTITUTION.md` Article 2 and 4. The
Owner Panel is not a single module — it is the set of Owner-only
command groups under `platform_layer/telegram/owner/`, each following the same
Handler → Service → Repository flow as every other Telegram command
(Constitution Article 4), gated by `platform_layer/telegram/owner/owner_roles.py`.

## Owner Telegram Control Center — current shape

`platform_layer/telegram/owner/` today (19 files), grouped into the sections the
Director's brief asks for. This maps real files to sections — it does
not invent a unified dashboard module that doesn't exist yet
(v0.6 on `docs/roadmap/VERSIONS.md` is where that consolidation is
planned):

| Section | Real file(s) |
|---|---|
| **System** | `system_commands.py`, `status_commands.py`, `control_commands.py` |
| **AI** | `ai_commands.py`, `runtime_commands.py` (`/runtime_status`, `/runtime_check` — Phase 61.7), `runtime_notifications.py` |
| **Provider** | `provider_commands.py` |
| **Users** | `owner_roles.py` (role/permission gating for every command in this package) |
| **Subscription** | *(subscription management lives in `platform_layer/telegram/subscription_service.py`, called from the relevant owner command file rather than a dedicated `platform_layer/telegram/owner/subscription_commands.py` today — v0.5 Business Layer on the roadmap is where this may grow a dedicated file per Article 7's reuse-first process)* |
| **Trading** | `execution_commands.py` |
| **Risk** | *(no dedicated `platform_layer/telegram/owner/risk_commands.py` exists today; risk visibility is surfaced through `status_commands.py`/`dashboard.py` reading `risk_layer/risk_engine/risk_manager.py` output — read-only, never a control surface, per Constitution Article 1/`CLAUDE.md` Trading Safety)* |
| **Decision** | `replay_commands.py` (signal/decision replay), `backtest_commands.py` |
| **Broadcast** | `runtime_notifications.py` (queues alerts; live delivery loop is the still-open v0.7 gap noted in `docs/PHASE61_7_FREEZE.md`) |
| **Analytics** | `performance_commands.py`, `report_commands.py`, `dataset_commands.py`, `feature_commands.py`, `fundamental_commands.py`, `learning_commands.py` |
| **Backup** | `config_snapshot_repository.py`/`config_snapshot_models.py` (under `database/`) are read via the relevant owner command file — no dedicated `platform_layer/telegram/owner/backup_commands.py` exists today |
| **Emergency** | `emergency_commands.py`, backed by `core_layer/emergency/` and `database_layer/trade_repository/emergency_repository.py` |

`dashboard.py` and `validation_commands.py` provide cross-cutting
summary and validation surfaces over several of the sections above
rather than owning one section exclusively.

## Flow (same as every other Telegram command)

```
Owner (Telegram) → command_router.py → permissions.py (owner_roles.py check)
    → platform_layer/telegram/owner/<domain>_commands.py handler
    → telegram/*_service.py or ai/runtime/ai_service.py
    → database/*_repository.py
```

No `platform_layer/telegram/owner/*.py` file queries the database directly — the
same Handler → Service → Repository discipline applies here as
everywhere else (Constitution Article 4).

## Honest gaps (not silently omitted)

Several sections above ("Subscription," "Risk," "Backup") do not yet
have a dedicated file — they are covered by adjacent, real modules
today. Per Constitution Article 7, creating a new
`platform_layer/telegram/owner/*.py` file for any of these is only justified once a
concrete task needs logic that doesn't fit its current host file; this
document records the current state honestly rather than pre-creating
placeholder modules.

## Related documents

- `docs/telegram/TELEGRAM_ARCHITECTURE.md` — the full dispatch
  mechanism this panel's commands run through.
- `docs/roadmap/VERSIONS.md` — v0.5 (Business Layer) and v0.6 (Owner
  Control Center) where several of the gaps above are planned to
  close.
- `docs/PHASE61_7_FREEZE.md` — the Runtime/Broadcast section's current
  state in detail.
