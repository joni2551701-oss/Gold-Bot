# Commands Reference (v0.2)

Registered in `platform_layer/telegram/commands.py` (`COMMANDS` / `OWNER_COMMANDS` /
`ADMIN_COMMANDS` — the single source of truth `command_router.py`
resolves both routing and permission tier from). Implemented in
`platform_layer/telegram/handlers.py`.

## User commands (open to everyone)

| Command | Behavior |
|---|---|
| `/start` | Registers the user (`status=NEW`) or, if already registered, confirms and touches activity (`status` → `ACTIVE` unless `BANNED`). Also ensures a default `FREE` subscription exists. |
| `/help` | Static list of all user-facing commands. |
| `/profile` | Full profile: language, trading style, strategy, risk, timeframe, plan, notifications, lifecycle status, created date. |
| `/settings` | Menu pointing to `/language`, `/risk`, `/strategy`, `/timeframe`, `/notifications`. |
| `/language [UZ\|RU\|EN]` | No argument shows the options; with an argument, updates. |
| `/risk [1\|2\|3\|5]` | Same pattern — percent only, no other values accepted. |
| `/timeframe [M15\|H1\|H4]` | Same pattern. |
| `/strategy [Liquidity Sweep\|FVG\|AMD\|Order Block]` | Same pattern; case-insensitive, accepts the full multi-word name. |
| `/notifications [on\|off]` | No argument shows current status; with `on`/`off`, toggles `notifications_enabled`. |
| `/signal` | **Plan-gated.** `FREE` → denied with an upgrade message. `PREMIUM`/`VIP`/OWNER/ADMIN → the latest persisted signal, fully formatted. |
| `/history` | **Not gated.** Last 5 signals, newest first — open to every plan. |
| `/plan` | Current subscription plan + static feature list + upgrade hint. |
| `/subscription` | Plan, subscription status, expiry (`N/A` — no billing exists). |
| `/upgrade` | Records the request; static "coming soon" reply. No payment, no plan change. |
| `/feedback [message]` | No argument prompts for a message. With a message, submits it (`status=OPEN`) and confirms with a ticket ID. |
| `/status` | Static bot-alive confirmation. |
| `/about` | Static bot description. |

## Admin commands (ADMIN or OWNER)

| Command | Behavior |
|---|---|
| `/admin` | Panel menu — OWNER sees the full panel (Users/Statistics/System/Broadcast/Admin Management); ADMIN sees a reduced one (no Broadcast/Admin Management section, though the underlying commands are still individually ADMIN-accessible). |
| `/stats` | Total users, total signals, approved/rejected counts, average confidence. |
| `/users` | Total / Active / New / Banned (lifecycle status) / created-today counts. |
| `/userinfo <telegram_id>` | Full profile for the target user, including plan, subscription status, lifecycle status, last activity. |
| `/vipinfo <telegram_id>` | Foundation only — always replies "VIP system not enabled." |
| `/system` | Health summary: database reachability + presence of `TELEGRAM_BOT_TOKEN`/`TWELVE_DATA_API_KEY`/`GEMINI_API_KEY`. No live external network calls; `API` is always `N/A`. |
| `/broadcast <message>` | Sends to every user with `notifications_enabled=1`. Reports `Sent: N / Failed: N`; a single recipient's failure never stops the batch. |
| `/feedbacks` | Lists all feedback entries, newest first, with status. |

## Owner-only commands (OWNER)

| Command | Behavior |
|---|---|
| `/addadmin <telegram_id>` | Grants ADMIN tier. Duplicate → `"Already admin."` |
| `/removeadmin <telegram_id>` | Revokes ADMIN tier. |

## Permission resolution

A command's minimum tier is derived from registry membership, not a
separate hardcoded list:

- In `ADMIN_COMMANDS` → requires ADMIN or above.
- In `OWNER_COMMANDS` only (not also in `ADMIN_COMMANDS`) → requires
  OWNER.
- Otherwise (only in `COMMANDS`) → USER (open to everyone).

`OWNER` always satisfies every check (rank 2 ≥ any required rank).
Denial always replies exactly `"Permission denied."`.

## Command interaction model

All settings/plan/admin commands take their value as a **command
argument** (`/risk 5`, `/addadmin 123456`), not via inline-keyboard
`callback_query` taps. Keyboards shown alongside some replies
(`platform_layer/telegram/keyboards.py`) are display hints only — no
`callback_query` handler is registered in `platform_layer/telegram/polling.py`.
