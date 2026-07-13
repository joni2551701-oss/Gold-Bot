# Database Schema (v0.2)

SQLite, single file (`Config.DB_PATH`, default `database/goldbot.db`).
Every table is created via `CREATE TABLE IF NOT EXISTS` and, where a
phase added columns to an already-shipped table, migrated via a
`PRAGMA table_info()`-guarded `ALTER TABLE ADD COLUMN` — both are
idempotent and safe to run on every repository construction. All
schema functions live in `database/models.py`.

## `users`

Owned by `database/user_repository.py`.

| Column | Type | Default | Notes |
|---|---|---|---|
| `id` | INTEGER PK | — | internal, not exposed on `UserRecord` |
| `telegram_id` | TEXT UNIQUE NOT NULL | — | |
| `username` | TEXT | — | |
| `language` | TEXT | `'UZ'` | `UZ` / `RU` / `EN` |
| `trading_style` | TEXT | `'Intraday'` | legacy field, predates `strategy` |
| `risk_percent` | REAL | `2.0` | `1` / `2` / `3` / `5` |
| `timeframe` | TEXT | `'M15'` | `M15` / `H1` / `H4` |
| `strategy` | TEXT | `'Liquidity Sweep'` | Phase 40; `Liquidity Sweep` / `FVG` / `AMD` / `Order Block` |
| `notifications_enabled` | INTEGER | `1` | Phase 40; 0/1 boolean |
| `status` | TEXT | `'NEW'` | Phase 45; `NEW` / `ACTIVE` / `BANNED` — user *lifecycle*, independent of subscription plan |
| `last_activity` | TIMESTAMP | `NULL` | Phase 45; ISO8601 string, set by `touch_activity()` |
| `created_at` | TEXT NOT NULL | — | ISO8601 |
| `updated_at` | TEXT | `NULL` | ISO8601, set on any `update_user()` call |

## `admins`

Owned by `database/admin_repository.py`.

| Column | Type | Default |
|---|---|---|
| `id` | INTEGER PK | — |
| `telegram_id` | TEXT UNIQUE NOT NULL | — |
| `role` | TEXT | `'ADMIN'` |
| `created_at` | TEXT NOT NULL | — |

OWNER is **not** stored here — it is derived purely from the
`TELEGRAM_OWNER_ID` environment variable at read time
(`telegram/permissions.py`).

## `signals`

Owned by `database/signal_repository.py`. Written exclusively by
`core/pipeline.py` (via `database/signal_record.py`); read-only from
the Telegram layer.

| Column | Type | Default | Notes |
|---|---|---|---|
| `id` | INTEGER PK | — | |
| `signal_id` | TEXT UNIQUE NOT NULL | — | UUID, assigned at persistence time |
| `symbol` | TEXT NOT NULL | — | usually empty string; the bot is single-symbol (XAUUSD) |
| `direction` | TEXT NOT NULL | — | `BUY` / `SELL` |
| `entry_zone_min` / `entry_zone_max` | REAL NOT NULL | — | both equal `signal.entry` today |
| `stop_loss` | REAL NOT NULL | — | |
| `take_profit_1` | REAL NOT NULL | — | |
| `take_profit_2` | REAL NOT NULL | — | unused, always `0.0` |
| `risk_percent` | REAL NOT NULL | — | unused, always `0.0` (distinct from `users.risk_percent`) |
| `lot_size` | REAL NOT NULL | — | `0.0` unless the pipeline is given an `account_balance` |
| `strategy_name` | TEXT NOT NULL | — | original Phase-pre-39 field |
| `confidence_score` | REAL NOT NULL | — | 0.0–1.0 fraction |
| `ai_explanation` | TEXT | — | free text from `AIAnalysisResult.explanation` |
| `status` | TEXT | `'OPEN'` | trade lifecycle: `OPEN` / `CLOSED` |
| `result` | TEXT | `'OPEN'` | manual outcome: `OPEN` / `WIN` / `LOSS` / `BE` / `CANCELLED` |
| `created_at` | TEXT NOT NULL | — | |
| `closed_at` | TEXT | `NULL` | |
| `strategy` | TEXT | `'UNKNOWN'` | Phase 39 display field (duplicates `strategy_name`'s intent) |
| `timeframe` | TEXT | `'M15'` | Phase 39; supplied by the pipeline (`self.interval`) |
| `rr_ratio` | REAL | `0` | Phase 39; computed independently of `RiskResult.risk_reward` |
| `ai_decision` | TEXT | `'N/A'` | Phase 39; raw `DecisionAction` value (`APPROVE`/`REJECT`/`NO_TRADE`) |
| `risk_status` | TEXT | `'N/A'` | Phase 39; `PASSED` / `BLOCKED` |
| `risk_amount` | REAL | `0` | Phase 39 |
| `signal_status` | TEXT | `'NEW'` | Phase 39; not currently transitioned by any code path |

**Note:** `status`/`result` (trade lifecycle) are unrelated to
`signal_status` (Phase 39 display field, always `'NEW'` today) — two
different concepts that happen to share a naming pattern; don't
conflate them.

## `subscriptions`

Owned by `database/subscription_repository.py`. Deliberately separate
from `users` — see `docs/telegram_layer.md`'s "kept separate" note.

| Column | Type | Default |
|---|---|---|
| `id` | INTEGER PK | — |
| `telegram_id` | TEXT UNIQUE NOT NULL | — |
| `plan` | TEXT | `'FREE'` — `FREE` / `PREMIUM` / `VIP` |
| `status` | TEXT | `'ACTIVE'` — subscription's own status, distinct from `users.status` |
| `started_at` | TEXT NOT NULL | — |
| `expires_at` | TEXT | `NULL` — not currently set by any code path (no billing) |
| `created_at` | TEXT NOT NULL | — |
| `updated_at` | TEXT | `NULL` |

## `feedback`

Owned by `database/feedback_repository.py`. No `UNIQUE` constraint —
multiple entries per `telegram_id` are expected.

| Column | Type | Default |
|---|---|---|
| `id` | INTEGER PK | — user-facing ticket number (e.g. `#12`) |
| `telegram_id` | TEXT NOT NULL | — |
| `message` | TEXT NOT NULL | — |
| `status` | TEXT | `'OPEN'` — `OPEN` / `REVIEWED` / `RESOLVED` |
| `created_at` | TEXT NOT NULL | — |

## Migration guarantees (verified in `tests/test_database.py`)

- Opening a pre-Phase-39 database (no `signals` display columns) —
  columns are backfilled with their defaults, existing rows untouched.
- Opening a pre-Phase-40/45 database (`users` missing
  `strategy`/`notifications_enabled`/`status`/`last_activity`) — same
  guarantee.
- Opening a pre-Phase-42 database (no `subscriptions` table at all) —
  the table is created fresh; `users`/`admins` data is untouched.
- Every migration function is idempotent: constructing the same
  repository twice never raises a duplicate-column error.
