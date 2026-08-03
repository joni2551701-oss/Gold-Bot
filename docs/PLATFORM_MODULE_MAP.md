# GoldBot Platform Module Map

File-by-file responsibility map for the Platform Layer, per
`docs/DOCUMENTATION_STANDARD.md`'s convention of naming real files
rather than an idealized structure. Companion to
`docs/PLATFORM_ARCHITECTURE.md` (the narrative/flow description) and
`docs/PLATFORM_DEPENDENCY_MAP.md` (what may import what). Documentation
only — no file listed here was modified to produce this map.

## `telegram/` — top level (23 files)

| File | Responsibility |
|---|---|
| `polling.py` | Live entry point (Phase 36+). Creates the inbound aiogram `Bot`, wires the `Dispatcher`, forwards `callback_query` to `callback_router.py` unbranched, sends the Owner startup notification and heartbeat. Transport only — no business logic. |
| `command_router.py` | Parses command text, resolves required permission tier (`commands.py` registries), resolves the outgoing keyboard (Reply Keyboard section, inline value-picker, or `_start_keyboard()`), calls the handler via `getattr(handlers, f"{command}_handler")`. |
| `callback_router.py` | Routes inline `callback_query` taps (`lang_*`, `risk_*`/`strategy_*`/`timeframe_*`/`notifications_*`) to the identical handler call the equivalent text command makes. No independent business logic. |
| `commands.py` | Pure data: `COMMANDS`/`ADMIN_COMMANDS`/`OWNER_COMMANDS` registries mapping command name → description. Single source of truth for both routing and permission tier. |
| `permissions.py` | `PermissionLevel` enum (OWNER/ADMIN/USER) and tier classification. `OWNER` from `TELEGRAM_OWNER_ID` env var; `ADMIN` from the `admins` table via `AdminService`. |
| `handlers.py` | One async function per user/admin command. Handler → Service only — never imports `database.*` or `core.pipeline` (stated in its own module docstring). |
| `registration_service.py` | Registration Wizard state machine (V2 Phase 3) — tracks/advances `RegistrationStep` (LANGUAGE → PHONE → COMPLETE) via `users.registration_step`/`registration_completed`. |
| `reply_keyboard_manager.py` | Owns Reply Keyboard section resolution (`keyboard_for_command()`, `record_section()`) and the reverse submenu-label → command map (`resolve_navigation_command()`). GoldBot's sole navigation mechanism (V2 Phase 6.3). |
| `keyboards.py` | Inline keyboard foundation — `language_keyboard()`, `risk_keyboard()`, `timeframe_keyboard()`, `strategy_keyboard()`, tier-aware Main Reply Keyboard builders, Main-tier `resolve_navigation_command()`. Also retains `settings_keyboard()`/`admin_panel_keyboard()` — unreachable from routing today, intentionally kept (Phase 6 Freeze Stage 1, F1). |
| `menu_commands.py` | Registers Telegram's native Menu Button command list (`Bot.set_my_commands()`, V2 Phase 4) in three tiers (USER/ADMIN/OWNER). Registration only — routes through the existing `command_router.py`, no new dispatch path. |
| `user_service.py` | Bridges commands to `database.user_repository.UserRepository` — registration, profile read/update, lifecycle state, activity tracking. No aiogram objects, no permission logic. |
| `subscription_service.py` | Bridges `/plan`, `/subscription`, `/upgrade` to `database.subscription_repository.SubscriptionRepository`. Plan read, lazy default-subscription creation, `has_signal_access()`. No payment/billing logic. |
| `signal_access_service.py` | Pure access-decision logic for `/signal` (OWNER/ADMIN bypass + plan check). Never touches the database directly, never fetches/formats a signal. |
| `signal_service.py` | Read-only bridge to `database.signal_repository.SignalRepository` for `/signal` and `/history`. No formatting. |
| `notification_service.py` | Per-user notification on/off and the notification-respecting recipient list. Talks to `database.user_repository.UserRepository` directly (a peer of `UserService`, not routed through it). |
| `feedback_service.py` | Bridges `/feedback` (user) and `/feedbacks` (admin) to `database.feedback_repository.FeedbackRepository` — submission, listing, status transitions. |
| `admin_service.py` | Admin CRUD, statistics, system health, broadcast delivery, feedback review (delegates to `FeedbackService`). Bridges to `database.admin_repository.AdminRepository` and `database.user_repository.UserRepository`. |
| `bot.py` | Thin `aiogram.Bot` wrapper used for **outbound** delivery from the trading pipeline — a distinct `Bot` instance from `polling.py`'s inbound one. |
| `notifier.py` | Sends a `FormattedSignal` via `telegram/bot.py` to the one fixed `TELEGRAM_CHAT_ID` — the pipeline's only Telegram touchpoint. Does not consult `NotificationService`/`SignalAccessService` (documented boundary, see `docs/PLATFORM_ARCHITECTURE.md` §7). |
| `signal_formatter.py` | Formats a `SignalCandidate` + `AIAnalysisResult` + `TradeDecision` (Trading Core types, imported for type hints on its dataclass fields only) into a `FormattedSignal` string for Telegram display. |
| `result_handler.py` | Reads/updates signal outcome data via `database.signal_repository.SignalRepository`. |
| `runtime_monitor.py` | Tracks the aiogram Bot/Dispatcher's own operational state (connected / last heartbeat / error count / uptime) — process health, not trading health. |
| `__init__.py` | Package marker, no logic. |

## `telegram/owner/` — Owner command surface (24 files)

Grouped by section per `docs/owner/OWNER_PANEL.md`'s mapping (real
files, not an idealized structure — several sections share a file or
have no dedicated file yet, noted as honest gaps in that document):

| Section | File(s) | Notes |
|---|---|---|
| System | `system_commands.py`, `status_commands.py`, `control_commands.py` | Health, status, runtime feature toggles |
| AI | `ai_commands.py`, `runtime_commands.py`, `runtime_notifications.py` | `runtime_commands.py` is the only Platform-side file with a real `ai/runtime/` dependency (`AIService`, `RuntimeManager`, `self_check`) |
| Provider | `provider_commands.py` | Registered market-data provider availability |
| Users | `owner_roles.py` | Role/permission gating for every command in this package (not a user-CRUD file itself) |
| Trading (visibility only) | `execution_commands.py` | Read-only surface; `execution/` itself stays inert |
| Decision (visibility/replay) | `replay_commands.py`, `backtest_commands.py` | Signal/decision replay, backtest triggers |
| Broadcast | `broadcast_commands.py`, `runtime_notifications.py` | Live delivery loop for queued alerts is an open gap per `docs/PHASE61_7_FREEZE.md` |
| Analytics | `performance_commands.py`, `report_commands.py`, `dataset_commands.py`, `feature_commands.py`, `fundamental_commands.py`, `learning_commands.py` | |
| Emergency | `emergency_commands.py` | Backed by `core_layer/emergency/` + `database/emergency_repository.py` |
| Security | `security.py` | Owner-tier security surface |
| Cross-cutting | `dashboard.py`, `validation_commands.py`, `monitoring_commands.py` | Summary/validation surfaces spanning several sections — see `docs/PLATFORM_ARCHITECTURE.md` §8 for `dashboard.py` |
| — | `__init__.py` | Package marker |

**No dedicated file exists today** for: Subscription (lives in
`telegram/subscription_service.py`, called from whichever owner file
needs it), Risk (surfaced read-only through `status_commands.py`/
`dashboard.py`, never a control surface), Backup (`config_snapshot_*`
under `database/`, read via the relevant owner file). Recorded as
honest current state, not an omission — see `docs/owner/OWNER_PANEL.md`.

## `database/` — platform-facing tables and repositories

Only the four tables the Platform Layer itself owns; the remaining
~15 `database/*_repository.py` files (signals, raw_candles, audit_log,
emergency_states, learning_records, risk_decisions, etc.) belong to
Trading Core / foundation layers, out of Platform Engineer scope.

| Table | Models / Repository | Owning service |
|---|---|---|
| `users` | `user_models.py` / `user_repository.py` | `telegram/user_service.py`, `telegram/notification_service.py` |
| `subscriptions` | `subscription_models.py` / `subscription_repository.py` | `telegram/subscription_service.py` |
| `feedback` | `feedback_models.py` / `feedback_repository.py` | `telegram/feedback_service.py`, `telegram/admin_service.py` |
| `admins` | `admin_models.py` / `admin_repository.py` | `telegram/admin_service.py`, `telegram/permissions.py` |

Schema definitions (`init_user_schema()`, `init_subscription_schema()`,
`init_feedback_schema()`, `init_admin_schema()`) live in
`database/models.py`, alongside every other table's schema function —
this file is shared infrastructure, not Platform-owned, even though
these four functions are Platform-relevant.

Key `users` columns beyond identity: `language` (default `'UZ'`),
`trading_style`, `risk_percent`, `timeframe`, `strategy`,
`notifications_enabled`, `status` (`NEW`/`ACTIVE`/`BANNED`),
`last_activity`, `phone_hash`, `trial_started_at`,
`registration_step`/`registration_completed` (V2 Phase 3). `subscriptions`:
`plan` (`FREE`/`PREMIUM`/`VIP`), `status`, `started_at`/`expires_at`
(no billing wired, `expires_at` unused today).

## `translation/` (6 files)

| File | Responsibility |
|---|---|
| `ui_catalog.py` | Static UZ/RU/EN string catalog (111 keys), `t(key, language, **kwargs)` lookup — hand-written UI strings only. |
| `translation_manager.py` | Deliberate no-op for dynamic/AI-generated content — no machine-translation API call anywhere in this package. |
| `language_registry.py` | Supported-language registry backing the catalog/manager. |
| `models.py` | `Language` enum and related translation data types. |
| `README.md` | Module documentation. |
| `__init__.py` | Package marker. |

## Adjacent, out-of-scope boundary (noted, not owned)

`ai/access/subscription_policy.py` reads the Platform Layer's plan
concept (`plan_to_ai_role()` maps `subscriptions.plan` strings to
`AIRole`) for the AI foundation's own (unwired) access-control layer.
This file lives under `ai/`, not `telegram/` or `database/`, and is
out of Platform Engineer scope — listed here only so its existence
isn't mistaken for an undocumented Platform module. See
`docs/PLATFORM_DEPENDENCY_MAP.md` §5.

## Related documents

- `docs/PLATFORM_ARCHITECTURE.md` — flow, permission model, navigation,
  subscription behavior, dashboard.
- `docs/PLATFORM_DEPENDENCY_MAP.md` — allowed/forbidden imports.
- `docs/owner/OWNER_PANEL.md`, `docs/telegram_layer.md`,
  `docs/telegram/TELEGRAM_ARCHITECTURE.md`, `docs/commands_reference.md`
  — pre-existing detailed references this map is built from.
