# GoldBot Platform Architecture

Scope note: this document describes the **Platform Layer** only —
the Telegram product surface (`telegram/`), its platform-facing
database tables (`users`, `subscriptions`, `feedback`, `admins`), and
the localization layer (`translation/`). It does not describe, and
does not authorize changes to, the Trading Core (`context/`,
`strategies/`, `signals/`, `decision/`, `risk/`, `ai/`, `core/pipeline.py`).
Written under the Senior Platform Engineer role assignment; Trading
Core stays frozen per that assignment unless a dedicated Director task
says otherwise.

This is a **description of current, already-built state**, verified
against the code and the existing canonical docs it cross-references
below — not a proposal, not a redesign. See `docs/telegram_layer.md`
and `docs/telegram/TELEGRAM_ARCHITECTURE.md` for the pre-existing
detailed references this document sits alongside; where they overlap,
those two remain the authoritative low-level source and this document
is the platform-scoped map on top of them.

## 1. Where the Platform Layer sits

GoldBot is two independent OS processes sharing one SQLite database
(`database/goldbot.db`), per `docs/ARCHITECTURE.md`'s System Overview:

1. **Trading pipeline** (`main.py` → `core/pipeline.py`) — scheduled,
   one-shot, produces signals and one outbound Telegram broadcast per
   run. **Not** part of the Platform Layer; read-only output consumer
   only (see §7 below).
2. **Telegram product layer** (`telegram/polling.py`, long-lived) —
   **this is the Platform Layer.** User registration, settings,
   subscriptions, navigation, admin/owner panel, feedback. Reads/writes
   the same database, entirely independent of pipeline timing.

The two processes never invoke each other and share no in-memory
state — only the database file connects them.

## 2. Request flow (dispatch pipeline)

```
Telegram Update
      |
telegram/polling.py            long-lived aiogram Dispatcher, transport only
      |
telegram/command_router.py     parse command -> resolve permission tier -> pick keyboard
      |
telegram/permissions.py        OWNER/ADMIN/USER classification
telegram/owner/owner_roles.py   (Owner-command-specific gating, additional layer)
      |
telegram/handlers.py           one async function per command (Handler -> Service only)
telegram/owner/<domain>_commands.py   (Owner-tier equivalent)
      |
telegram/*_service.py          business logic (lazy repo construction, never raises)
      |
database/*_repository.py      SQL only, the only place SQL is written
      |
SQLite (database/goldbot.db)
```

A parallel path exists for inline `callback_query` taps (currently
only the `/language` picker and the four Settings value-pickers —
see §5): `polling.py` forwards the callback unbranched to
`telegram/callback_router.py`, which translates `callback_data` into
the exact same handler call the equivalent text command would make.
It is not a second business-logic path, per
`docs/telegram/TELEGRAM_ARCHITECTURE.md`.

**Dispatch is name-convention-based, not a table**:
`command_router.py` resolves `getattr(handlers, f"{command}_handler")`
— a handler whose name doesn't exactly match `<command>_handler` is
silently unreachable. This has bitten the codebase once already
(Phase 61.7, caught before merge) — see
`docs/telegram/TELEGRAM_ARCHITECTURE.md`.

## 3. Permission model

Three tiers, ranked `OWNER > ADMIN > USER` (`telegram/permissions.py`):

- **OWNER** — `TELEGRAM_OWNER_ID` env var, never hardcoded. Always
  satisfies every check.
- **ADMIN** — membership in the `admins` table
  (`database/admin_repository.py`). OWNER always counts as ADMIN.
- **USER** — any resolvable Telegram user, the default.

A command's tier is derived from which registry it's declared in
(`telegram/commands.py`'s `COMMANDS`/`ADMIN_COMMANDS`/`OWNER_COMMANDS`)
— one source of truth, no second hardcoded list anywhere. Denial
always replies exactly `"Permission denied."`.

Owner-only commands under `telegram/owner/` are gated a second time by
`telegram/owner/owner_roles.py` before their handler runs — see
`docs/owner/OWNER_PANEL.md`.

## 4. User lifecycle vs. subscription — two independent axes

Never conflated in code or in any reply:

- **Lifecycle status** (`users.status`): `NEW` → `ACTIVE` → `BANNED`.
  A `BANNED` user is never silently reactivated by further activity —
  checked in three independent places (`handlers.start_handler()`,
  `command_router._start_keyboard()`, `handlers._registration_step()`'s
  fallthrough), per `docs/PHASE6_FREEZE.md` Stage 2.
- **Subscription plan** (`subscriptions.plan`): `FREE` / `PREMIUM` /
  `VIP`. Drives `/signal` access only, via
  `telegram/subscription_service.py` + `telegram/signal_access_service.py`.

### Subscription platform, current shape

- `FREE` is the default plan, lazily created on first `/start`.
- `/signal` — gated: `FREE` denied with an upgrade message;
  `PREMIUM`/`VIP`/OWNER/ADMIN get the latest persisted signal.
- `/history` — **not** gated (last 5 signals, any plan) — deliberate:
  proof the bot works, without giving away the thing worth upgrading
  for.
- `/plan`, `/subscription` — read-only display of current plan/status/
  expiry (`expires_at` always shows `N/A` — no billing system exists).
- `/upgrade` — records the request, static "coming soon" reply. No
  payment integration, no plan change, today.
- No dedicated `telegram/owner/subscription_commands.py` exists yet —
  subscription management lives in `telegram/subscription_service.py`,
  called from whichever owner command file needs it. `docs/owner/OWNER_PANEL.md`
  names this as an honest gap, not an oversight (v0.5 Business Layer on
  the roadmap is where a dedicated file may be justified).
- A one-directional bridge exists **out of** the Platform Layer:
  `ai/access/subscription_policy.py` maps `subscriptions.plan` strings
  to an `AIRole` enum for the (unwired) AI access-control foundation.
  This is `ai/` reading a value the Platform Layer already defines —
  `telegram/` does not import anything from `ai/access/` in return. See
  `docs/PLATFORM_DEPENDENCY_MAP.md` §5.

## 5. Navigation system

**Director-approved rule (V2 Phase 6.3, binding): the Reply Keyboard
is GoldBot's sole navigation mechanism.** Inline keyboards are used
only where a real *choice* is being made (Language selection, a
Settings value picker) — never to move between screens. This retired
an earlier inline "Navigation Controller" (`telegram/navigation.py`,
now deleted) outright.

Owned by `telegram/reply_keyboard_manager.py` (which section keyboard
attaches to which command's reply, and the reverse label→command map)
plus `telegram/keyboards.py` (the tier-aware Main keyboard and the
inline value-pickers).

**Six live sections**, each ending in a trailing "◀️ Ortga" (Back) row
that resolves unconditionally to `/start` → Main (Director decision:
no separate Home button):

| Section | Reached from |
|---|---|
| Main | `/start`, and the default for any unlisted command |
| Settings | `/settings`, `/language`, `/risk`, `/strategy`, `/timeframe`, `/notifications` |
| Admin | `/admin`, `/users`, `/stats`, `/system`, `/broadcast`, `/removeadmin` |
| Owner | `/owner`, `/runtime`, `/health`, `/performance`, `/errors`, `/pipeline`, `/report` |
| Profile | `/profile`, `/subscription` |
| Signals | `/signal`, `/history`, `/upgrade` |

Section tracking (`_LAST_SECTION`) is process-local, in-memory, never
persisted — a stray tap after a restart falls back to a full-map
search rather than failing. Inline value-pickers (Risk/Strategy/
Timeframe/Notifications) redraw in place and never change the tracked
section.

### Registration Wizard drives the keyboard for new users

```
new user --/start--> LANGUAGE --(lang tap)--> PHONE --(share contact)--> COMPLETE
             |                      |                      |
     language_keyboard()   phone_share_keyboard()   Main Reply Keyboard
```

An existing OWNER/ADMIN account, or a `COMPLETE` user, always resolves
straight to the Main keyboard. A `BANNED` account always gets
`ReplyKeyboardRemove()` — checked before any wizard-step logic. Full
trace: `docs/PHASE6_FREEZE.md` Stage 2–3.

### Persistent Menu (Telegram's native Menu Button)

`telegram/menu_commands.py` (V2 Phase 4) registers three fixed tiers
via `Bot.set_my_commands()` — USER (Home/Profile/Signals/Subscription/
Settings/Help), ADMIN (+Admin), OWNER (+Owner). This is registration
only; every menu entry routes through the same
`command_router.route_command()` a hand-typed command would use — no
second dispatch path.

### Reply Menu layout is frozen

Per `docs/PHASE6_FREEZE.md` Stage 5 (binding Director decision,
intended for GoldBot Constitution v2.0): the current Main Reply
Keyboard layout does not change to accommodate a future module. A
future module occupies a **reserved slot** and ships as a "Coming
Soon" placeholder until wired — see §8.

## 6. Localization / UX

`translation/ui_catalog.py` — a static UZ/RU/EN string catalog (111
keys as of Phase 6 Freeze), looked up via `t(key, language, **kwargs)`
(caller's language → EN → any entry, never raises). Distinct from
`translation.translation_manager.TranslationManager`, which is a
deliberate no-op for dynamic/AI-generated content (no machine-translation
call anywhere in this package).

- **Localized today**: all 17 `COMMANDS`-registry (USER-tier) handlers,
  all USER-tier keyboards, `/language`'s own replies.
- **Stays English by design**: every OWNER/ADMIN-tier command
  (internal operator tooling, Director decision); `signal_formatter.py`/
  `signal_access_service.py` (deferred to V2.1); `command_router.py`'s
  generic error constants (deferred to V2.2).
- **Default language**: `users.language` defaults to `'UZ'` — a fresh
  user gets Uzbek, not English, by product decision (tests assert
  against this default).

## 7. Known architectural boundary: pipeline broadcast bypasses the Platform Layer

The scheduled pipeline (`main.py` → `core/pipeline.py` →
`telegram/notifier.py` → `telegram/bot.py`) delivers to one fixed
`TELEGRAM_CHAT_ID` per run. It does **not** iterate per-user and does
**not** consult `NotificationService` or `SignalAccessService` — this
is a deliberate, documented scope boundary
(`telegram/notification_service.py`'s own module docstring), not a
gap to close as Platform work. Per-user notification preference and
plan-based access control apply only to the Telegram-layer commands
(`/broadcast`, `/signal`, etc.), never to the pipeline's own outbound
message. `telegram/bot.py`'s `Bot` instance for outbound delivery is a
separate instance from `telegram/polling.py`'s inbound listener — no
shared state between the two processes' Telegram clients.

## 8. Dashboard

`telegram/owner/dashboard.py` (Phase 59.8, extended 61.5 Addendum) is
the closest thing to a unified dashboard today — it does not invent
new health/status/provider logic, it composes already-built pieces:

- `get_dashboard()` — concatenated text sections: system status
  (`status_commands.get_system_status()`), feature-flag ON/OFF count
  (`control_commands.get_feature_states()`), provider availability
  (`provider_commands.list_providers()`).
- `get_owner_summary()` (`/owner`) — a compact key-value panel: system
  health, AI online/provider, total users, Premium count (PREMIUM+VIP),
  signals today, win rate, cost today (currently always `$0.00` — no
  live AI-audit source wired yet), Emergency state.
- `get_doctor_report()` (`/doctor`) — nine independent subsystem
  reachability checks (Database/AI/Market Data/Telegram/Scheduler
  [N/A — external]/Providers/Learning/Cache/Audit); one failing check
  never hides the rest.

Every section degrades independently on failure — never a fabricated
number, never an unhandled exception reaching the user. There is no
`/dashboard` command wired to `get_dashboard()` yet in
`telegram/command_router.py`/`telegram/commands.py` — confirm before
assuming it's reachable; `/owner` and `/doctor` are the two functions
of this file that are live-wired today per the file's own docstring.

## 9. Reserved future modules (not live, not this phase's scope)

Per `docs/PHASE6_FREEZE.md` Stage 6 — recorded here as current state,
not a plan to implement:

| Module | Status |
|---|---|
| Chart | Not started |
| AI Assistant | Foundation exists (`assistant/`, `ai/conversation/`, `voice/`) — no Telegram entry point |
| AI Analyst | Foundation exists (`ai/trading_analyst/`) — no Telegram entry point |
| Economic Calendar | Not started (fundamental data exists in `context_layer/fundamental/economic_events.py`, no Telegram surface) |
| News Center | Not started |
| Academy | Foundation exists (`ai/learning/`) — no Telegram entry point |
| Analytics | Partially live (`/performance`, `/report` under Owner) |
| Portfolio | Foundation exists (`ai/portfolio/`) — no Telegram entry point |
| Trade Journal | Foundation exists (`ai/trade_journal/`) — no Telegram entry point |
| Trade Replay | Foundation exists (`backtesting/replay_*`, `telegram/owner/replay_commands.py`) — Owner-only, partially reachable |
| Market Scanner | Not started |
| Notifications Center | Partially live (`/notifications` on/off; no per-category center) |
| Community / Marketplace | Not started |

No "Coming Soon" placeholder button exists for any of these yet —
adding one is a Reply Menu change, explicitly deferred to a future,
separately-scoped phase.

## Related documents

- `docs/telegram_layer.md`, `docs/telegram/TELEGRAM_ARCHITECTURE.md` —
  pre-existing detailed dispatch/service reference (authoritative for
  low-level detail).
- `docs/commands_reference.md` — every command, tier, and behavior.
- `docs/owner/OWNER_PANEL.md` — the Owner command surface in full.
- `docs/PHASE6_FREEZE.md` — the current-state freeze record this
  document's Navigation/Reply Menu sections are built from.
- `docs/PLATFORM_MODULE_MAP.md` — file-by-file responsibility map.
- `docs/PLATFORM_DEPENDENCY_MAP.md` — what the Platform Layer may and
  may not import.
