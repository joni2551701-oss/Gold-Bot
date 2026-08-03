# Telegram Product Layer — Architecture (v0.2)

## Shape

```
Telegram Update
      |
      v
platform_layer/telegram/polling.py        (aiogram Dispatcher; long-running process, separate from main.py)
      |
      v
platform_layer/telegram/command_router.py (parses command + args, resolves permission tier, attaches a hint keyboard)
      |
      v
platform_layer/telegram/handlers.py       (one async function per command; Handler -> Service only, never -> Database/Core)
      |
      v
Services                   (see table below)
      |
      v
Repositories                (SQL lives here, and only here)
      |
      v
SQLite (database/goldbot.db by default; see database_schema.md)
```

`main.py` (the scheduled `TradingPipeline` run) and `platform_layer/telegram/polling.py`
(the long-running command listener) are two separate processes. They
share the same SQLite database file but are never invoked from one
another.

## Services

| Service | File | Responsibility |
|---|---|---|
| `UserService` | `platform_layer/telegram/user_service.py` | Registration, profile read/update, lifecycle state (`NEW`/`ACTIVE`/`BANNED`), activity tracking |
| `SubscriptionService` | `platform_layer/telegram/subscription_service.py` | Plan read (`FREE`/`PREMIUM`/`VIP`), lazy default-subscription creation, `has_signal_access()` |
| `SignalAccessService` | `platform_layer/telegram/signal_access_service.py` | Access decision only (OWNER/ADMIN bypass + plan check) — never touches the database directly |
| `SignalService` | `platform_layer/telegram/signal_service.py` | Read-only signal retrieval (`/signal`, `/history`) |
| `NotificationService` | `platform_layer/telegram/notification_service.py` | Per-user notification on/off, recipient list for notification-respecting sends |
| `FeedbackService` | `platform_layer/telegram/feedback_service.py` | Feedback submission, listing, status transitions |
| `AdminService` | `platform_layer/telegram/admin_service.py` | Admin CRUD, statistics, system health, broadcast delivery, feedback review (delegates to `FeedbackService`) |

Every service follows the same contract: lazy repository construction
(a bare `Service()` never touches disk until a method is called),
every public method wrapped in `try/except` so a database or network
failure degrades to a `success=False` result — never an exception that
reaches a handler or the Dispatcher.

## Permission model

Three tiers, ranked `OWNER > ADMIN > USER`:

- **OWNER** — identified by `TELEGRAM_OWNER_ID` (env var only, never
  hardcoded). Always satisfies every permission check.
- **ADMIN** — membership stored in the `admins` table
  (`database_layer/user_repository/admin_repository.py`). OWNER always counts as ADMIN too.
- **USER** — any resolvable Telegram user ID; the default tier.

A command's required tier is derived from which registry it's
declared in (`platform_layer/telegram/commands.py`'s `COMMANDS` / `OWNER_COMMANDS` /
`ADMIN_COMMANDS`) — there is exactly one place a command name is
listed as belonging to a tier; `command_router.py` never hardcodes a
second list. A command present in both `OWNER_COMMANDS` and
`ADMIN_COMMANDS` (e.g. `/admin`, `/broadcast`) resolves to
"ADMIN-or-above", and the handler itself may still render different
content for OWNER vs ADMIN (e.g. `/admin`'s panel).

A denied command always replies exactly `"Permission denied."` — never
an exception, never a partial response.

## Command reference

See `docs/commands_reference.md` for the full command-by-command
table (tier, arguments, and behavior).

## User lifecycle vs. subscription — kept separate

These are two independent axes, never conflated in code or in any
Telegram reply:

- **Lifecycle status** (`users.status`): `NEW` → `ACTIVE` → `BANNED`.
  Tracked by `UserService.touch_activity()`, called from every
  activity-relevant handler (`/start`'s duplicate-registration branch,
  `/profile`, `/settings`, `/signal`, `/history`, `/plan`,
  `/subscription`, `/feedback`). A `BANNED` user is never silently
  reactivated by further activity.
- **Subscription plan** (`subscriptions.plan`): `FREE` / `PREMIUM` /
  `VIP`. Drives `/signal` access only.

`/userinfo` (admin) and `/profile` (self) show both axes as clearly
separate fields (`Status:` vs. `Plan:` / `Subscription Status:`).

## Signal access control

`/signal` is gated: `FREE` → denied with an upgrade message;
`PREMIUM`/`VIP` → the real latest signal; OWNER/ADMIN → always
allowed regardless of plan. `/history` is intentionally **not**
gated — a FREE user can browse past signals (proof the bot works) but
not the live one (the thing worth upgrading for).

## Known architectural boundary

The scheduled pipeline (`main.py` → `core/pipeline.py` →
`platform_layer/telegram/notifier.py`) delivers to one fixed `TELEGRAM_CHAT_ID`
(a channel/group) per run — it does not iterate per-user and does not
consult `NotificationService` or `SignalAccessService`. Per-user
notification preference and access control apply only to the
Telegram-layer commands (`/broadcast`, `/signal`, etc.), not to the
pipeline's own outbound message. This is a deliberate scope boundary
(the pipeline is off-limits to Telegram-layer phases), documented in
`platform_layer/telegram/notification_service.py`'s module docstring.
