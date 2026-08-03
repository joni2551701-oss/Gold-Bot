# GoldBot Database Architecture (Phase 50)

SQLite, one file (`database/goldbot.db` by default, `config.Config.DB_PATH`).
Shared between the two GoldBot processes (`main.py`'s scheduled
`TradingPipeline` and the long-running `telegram/polling.py`) — see
`docs/telegram_layer.md` for how those two processes relate. For the
full column-by-column schema, see `docs/database_schema.md`; this
document is the relationship/architecture map plus the Phase 50
database-improvement audit findings.

## Diagram

```
                    Signals
                   (independent --
                    no relation to
                    users; symbol,
                    strategy,
                    ai_decision,
                    risk_status,
                    created_at)
                       ^
                       |
                (linked only by
                 application code,
                 not a DB foreign key)

Users  (telegram_id UNIQUE)
 |
 |-- Subscriptions   (telegram_id UNIQUE -- one active plan per user:
 |                     FREE / PREMIUM / VIP)
 |
 |-- Feedback        (telegram_id -- NOT unique: many feedback
 |                     entries per user are expected)
 |
 |-- Admins          (telegram_id UNIQUE -- OWNER is config-only,
                       identified by TELEGRAM_OWNER_ID, never a row
                       here; ADMIN rows live in this table)
```

Every relationship above is by `telegram_id` string equality in
application code (`WHERE telegram_id = ?`), never a SQL `FOREIGN KEY`
constraint — see "Referential Integrity" below.

## Tables

### `users`
The Telegram user profile: registration, settings (`language`,
`trading_style`, `risk_percent`, `timeframe`, `strategy`,
`notifications_enabled`), and lifecycle state (`status`:
`NEW`/`ACTIVE`/`BANNED`, `last_activity`). One row per Telegram user,
enforced by `telegram_id UNIQUE NOT NULL`. Owned by
`database_layer/user_repository/user_repository.py` / `database_layer/user_repository/user_models.py`.

### `subscriptions`
One active plan (`FREE`/`PREMIUM`/`VIP`) per user, `telegram_id UNIQUE
NOT NULL`. Deliberately separate from `users.status` — subscription
plan and account lifecycle are independent concerns (a `BANNED` user
can still technically hold a `PREMIUM` plan; access control checks
both). Owned by `database_layer/user_repository/subscription_repository.py` /
`database_layer/user_repository/subscription_models.py`.

### `signals`
Every signal candidate the trading pipeline produces, approved or not
— `TradingPipeline.run()` persists all of them (Phase 39/48) so
rejected/blocked signals stay available for analytics even though they
never reach Telegram. No relation to `users` at all; this table is
written exclusively by the scheduled pipeline process, read by the
Telegram layer (`/signal`, `/history`) and `core_layer/health_monitor/performance.py`.
Owned by `database_layer/trade_repository/signal_repository.py` / `database_layer/trade_repository/signal_record.py`.

### `feedback`
Free-text feedback messages from users, `status`
(`OPEN`/`REVIEWED`/`RESOLVED`). `telegram_id` is intentionally **not**
unique — many feedback entries per user are valid and expected. Owned
by `database_layer/user_repository/feedback_repository.py` / `database_layer/user_repository/feedback_models.py`.

### `admins`
ADMIN-tier Telegram users, `telegram_id UNIQUE NOT NULL`, `role`
(currently always `"ADMIN"` — OWNER is identified purely by
`TELEGRAM_OWNER_ID` and never gets a row here). Owned by
`database_layer/user_repository/admin_repository.py` / `database_layer/user_repository/admin_models.py`.

### `raw_candles` (Phase 59.3)
The first table added by any Phase A/AC/Phase-59 foundation module —
every prior one deliberately stayed in-memory-only. One row per
`(symbol, timeframe, timestamp, provider)` — that four-part tuple is
`UNIQUE`, so the same window from two different providers is two
distinct rows, never merged. `volume` stays nullable — never coerced
to `0.0` when a provider doesn't supply it. Independent of every other
table, including `signals` — no relation, no foreign key, nothing in
`core/pipeline.py` writes to it in this phase (see
`docs/MARKET_DATA_ARCHITECTURE.md`'s "As implemented today" section
for the same disclosed non-wiring already true of the provider layer
itself). Owned by `database_layer/market_repository/raw_candle_repository.py` /
`database_layer/market_repository/raw_candle_models.py`.

### `market_snapshots` (Phase 59.3)
The persisted counterpart to `data_layer.live_data.market_data_snapshot.MarketDataSnapshot`
(Phase 59 Preparation/59.1, which stays in-memory-only itself —
`database_layer/market_repository/market_snapshot_models.py`'s `from_market_data_snapshot()`
is the one bridge between the two). `market_snapshot_id UNIQUE NOT
NULL`. Same isolation as `raw_candles` — no relation to `signals`
either, and nothing in `core/pipeline.py` writes to it in this phase.
Owned by `database_layer/market_repository/market_snapshot_repository.py` /
`database_layer/market_repository/market_snapshot_models.py`.

### `sync_state` (Phase 59.5)
One row per `(provider, symbol, timeframe)` — that three-part tuple is
`UNIQUE`, so `SyncStateRepository.update_sync_state()` upserts in
place rather than appending a new row per sync. Tracks
`data_layer/historical_data/historical_data_collector.py`'s `sync_historical_candles()` own
incremental watermark (`last_timestamp`), letting a repeated sync call
resume forward instead of re-fetching a large window every time.
Independent of every other table, including `raw_candles` — no
foreign key, linked only by convention (shared `provider`/`symbol`/
`timeframe` values), nothing in `core/pipeline.py` writes to it.
Owned by `database_layer/market_repository/sync_state_repository.py` /
`database_layer/market_repository/sync_state_models.py`.

### `audit_log` (Phase 59.6)
Append-only — no update/delete method exists on
`AuditLogRepository`. One row per recorded owner/admin action
(`actor`, `action`, `target`, `result` default `'SUCCESS'`,
`details`, `created_at`). Independent of every other table, including
`admins` — `actor` holds the same kind of identifier by convention,
never enforced structurally. Nothing calls `log_action()`
automatically yet. Owned by `database_layer/audit_log/audit_log_repository.py` /
`database_layer/audit_log/audit_log_models.py`.

### `config_snapshots` (Phase 59.6)
Append-only, same posture as `audit_log`. One row per captured
`configuration.feature_registry.build_feature_registry()` state
(`snapshot_id UNIQUE NOT NULL`, `feature_state` — a JSON object string
of `{feature_name: enabled}`, `taken_at`, `taken_by`, `reason`). No
apply/restore function exists — capture and read only. Owned by
`database_layer/journal_repository/config_snapshot_repository.py` /
`database_layer/journal_repository/config_snapshot_models.py`. As of Phase 59.7, every
successful `RuntimeFeatureManager` toggle also writes one of these
rows — no longer purely a manual/future-command capture.

### `runtime_features` (Phase 59.7)
One row per feature name (`feature UNIQUE NOT NULL`, `enabled`,
`created_at`, `updated_at`, `updated_by`, `reason`).
`RuntimeFeatureRepository.set_feature()` upserts in place — `created_at`
is stamped once on the first INSERT and never touched by any later
UPDATE, so it always reflects when a feature was first toggled, not
when it was most recently changed. Independent of every other table —
no foreign key. Owned by `database_layer/journal_repository/runtime_feature_repository.py` /
`database_layer/journal_repository/runtime_feature_models.py`.

---

## Phase 50 Audit Findings

### Schema Report

**users** — Status: OK. `telegram_id UNIQUE NOT NULL` correctly
prevents duplicates; `created_at NOT NULL`; every settings/lifecycle
column has a schema `DEFAULT`, so a pre-migration row always reads
back a real value, never `NULL`. Issues: none. Indexes: `telegram_id`
(implicit, via `UNIQUE`), `status` and `created_at` (added this phase
— see Index Audit). Recommendation: none further.

**subscriptions** — Status: OK. `telegram_id UNIQUE NOT NULL`;
`started_at`/`created_at NOT NULL`; `plan`/`status` both default.
Issues: none. Indexes: `telegram_id` (implicit, via `UNIQUE`) only —
see Index Audit for why `plan`/`status` indexes were considered and
not added. Recommendation: none further.

**signals** — Status: OK. `signal_id UNIQUE NOT NULL`; all core
trade-geometry columns `NOT NULL`; Phase 39 display columns all
default. Issues: `symbol` is schema-`NOT NULL` but every insert
hardcodes `""` (`signal_repository.py:39`, unrelated to this phase's
allowed scope — flagged, not changed since it's a data-population
concern in `save_signal_record()`'s caller, not a schema defect).
Indexes: `signal_id` (implicit, via `UNIQUE`), `status` and
`created_at` (added this phase). Recommendation: populate a real
`symbol` value if/when multi-symbol support is ever added (v0.4+, not
this phase).

**feedback** — Status: OK. `telegram_id`/`message`/`created_at
NOT NULL`; `status` defaults; intentionally no `UNIQUE` on
`telegram_id` (multiple entries per user by design). Issues: none.
Indexes: `status` and `created_at` (added this phase); `telegram_id`
deliberately not indexed — see Index Audit. Recommendation: none
further.

**admins** — Status: OK. `telegram_id UNIQUE NOT NULL`; `created_at
NOT NULL`; `role` defaults. Issues: none. Indexes: `telegram_id`
(implicit, via `UNIQUE`) only — `role` considered and not added, see
Index Audit. Recommendation: none further.

### Index Audit

Added this phase (`database_layer/database_manager/models.py`, `CREATE INDEX IF NOT EXISTS`,
idempotent):

| Table | Column | Backing query |
|---|---|---|
| `users` | `status` | `get_active_users()`, `count_by_status()` |
| `users` | `created_at` | `count_users_created_today()` (see caveat below) |
| `signals` | `status` | `get_open_signals()`, `get_closed_signals()` |
| `signals` | `created_at` | `get_latest_signal()`/`get_recent_signals()` `ORDER BY` |
| `feedback` | `status` | `count_open_feedback()` |
| `feedback` | `created_at` | `get_all_feedback()` `ORDER BY` |

Caveat: `count_users_created_today()`'s predicate is
`WHERE date(created_at) = date('now')` — wrapping the column in
`date()` means SQLite's planner will not actually use a plain index on
`created_at` for this specific query (function results aren't
sargable against a normal B-tree index). The index is still added
because it is genuinely useful for any future direct `created_at`
range query, and adding it costs nothing today; the existing query
itself was left untouched since rewriting it changes an actively
correct predicate for a query-planner nuance, not a scope this phase
covers ("Query Optimization" only, no query logic changes).

**Deliberately not added** (recommended by the task brief's generic
per-table list, but not backed by any query that actually filters on
them — adding would be pure speculative index bloat with zero
measurable benefit today):

- `users.telegram_id`, `subscriptions.telegram_id`,
  `admins.telegram_id` — already covered by each table's `UNIQUE`
  constraint, which SQLite backs with an implicit index. A second,
  explicit index on the same column would be a duplicate.
- `subscriptions.plan`, `subscriptions.status` — no repository method
  filters `WHERE plan = ?` or `WHERE status = ?`; plan/status checks
  happen in Python at the service layer after fetching by
  `telegram_id`, not via SQL predicate.
- `signals.symbol` — no query filters on it, and the column is always
  an empty string today (see Schema Report above).
- `signals.ai_decision`, `signals.risk_status` — no repository method
  filters on either column.
- `feedback.telegram_id` — no repository method filters
  `WHERE telegram_id = ?` on this table today (`get_feedback()` filters
  by `id`; there is no "feedback by user" lookup method).
- `admins.role` — no repository method filters on it (`get_all_admins()`
  has no `WHERE`; every lookup is by `telegram_id`).

### Referential Integrity

No SQL `FOREIGN KEY` constraints exist anywhere in this schema —
`subscriptions`/`feedback`/`admins` relate to `users` by `telegram_id`
string equality enforced entirely in application code, never at the
database level. This is a **pre-existing, repo-wide design choice**
(not something this phase changed), and this phase's Critical Rules
explicitly forbid adding one ("Majburan Foreign Key qo'shma"), so
none was added.

What this means concretely: `SubscriptionService`/`FeedbackService`/
`AdminService.add_admin()` do not check that a `users` row exists
before writing a `subscriptions`/`feedback`/`admins` row for a given
`telegram_id` (confirmed by reading those services — none imports or
calls `UserRepository`/`UserService` as a precondition). In every
real Telegram flow a user's first interaction is `/start`
(`UserService.register_user()`), so an orphan is unlikely in practice,
but it is not structurally prevented — a `telegram_id` could in
principle get a `subscriptions`/`feedback`/`admins` row with no
matching `users` row. This is a **report-only finding**: fixing it
would mean either adding a `FOREIGN KEY` (forbidden this phase) or
adding a precondition check in the service layer (outside this
phase's `database/`-only scope). No duplicate `telegram_id` rows or
`NULL`-where-`NOT NULL` values are possible today — those are already
prevented by each table's own `UNIQUE`/`NOT NULL` constraints,
verified directly from the schema in `database_layer/database_manager/models.py`.

### Timestamp Consistency

Every `created_at`/`started_at`/`updated_at`/`closed_at` value written
anywhere in `database/*_repository.py` is produced by
`datetime.now(timezone.utc).isoformat()` — consistently UTC,
consistently ISO 8601, across all five repositories, with no
exceptions found. `last_activity` (`users`) is the same pattern.
`expires_at` (`subscriptions`) is written from a caller-supplied
`datetime` via `.isoformat()` (or left `NULL` if none is supplied),
same format. No inconsistent timestamp format was found anywhere in
this scope.

### Repository Layer Audit (Task 4)

Both findings below are pre-existing, low-risk, and are **reported
only** per this phase's explicit "Majburan ko'chirma" (do not
force-move) rule:

- `UserRepository.update_last_activity()`
  (`database_layer/user_repository/user_repository.py`) embeds a small lifecycle business
  rule directly in the repository: it promotes a `NEW` user to
  `ACTIVE` as a side effect of recording activity, rather than that
  decision being made in `telegram/user_service.py`. Low risk as-is
  (well-documented, single call site, test-covered), but is business
  logic living below the service layer.
- `SignalRepository.update_signal_result()`
  (`database_layer/trade_repository/signal_repository.py`) validates its `result` argument
  against a hardcoded `ALLOWED_RESULTS` set and raises `ValueError` on
  an invalid value — a validation rule, not pure SQL. Low risk as-is
  (defensive, prevents bad data from ever reaching the table), same
  "reported, not moved" treatment.

No other repository method contains business logic, Telegram
formatting, or handler-level logic — every other method is a direct,
parameterized CRUD operation.

---

## PostgreSQL Readiness

| Item | Status | Notes |
|---|---|---|
| `INTEGER PRIMARY KEY AUTOINCREMENT` | Needs change | SQLite-specific rowid alias + autoincrement keyword; Postgres equivalent is `GENERATED ALWAYS AS IDENTITY` / `SERIAL`. |
| `PRAGMA table_info(...)` | Needs change | SQLite-only introspection; Postgres equivalent is querying `information_schema.columns`. |
| `date('now')` | Needs change | SQLite date function (`database_layer/user_repository/user_repository.py:131`); Postgres equivalent is `CURRENT_DATE`. |
| `?` parameter placeholders | Needs change | SQLite's `sqlite3` driver style; `psycopg2`/most Postgres drivers use `%s`. Used everywhere in this codebase — a mechanical but repo-wide change. |
| `sqlite3.IntegrityError` | Needs change | Driver-specific exception class caught in `user_repository.py`, `subscription_repository.py`, `admin_repository.py`, `signal_repository.py` for duplicate-key handling; Postgres drivers raise a different exception type. |
| `sqlite3.connect()` / `row_factory = sqlite3.Row` | Needs change | `database_layer/database_manager/database.py`'s `Database` class is written directly against the stdlib `sqlite3` module; a Postgres port needs an equivalent connection/row-mapping layer. |
| `notifications_enabled INTEGER DEFAULT 1` (bool-as-int) | Ready | Works identically in Postgres as an `INTEGER` column storing 0/1; not idiomatic (Postgres has a native `BOOLEAN`), but functionally portable with zero code change. |
| Timestamps stored as `TEXT` (ISO 8601) | Ready | ISO 8601 strings sort/compare correctly lexicographically in both engines; functionally portable, though a native `TIMESTAMPTZ` column would be more idiomatic on Postgres. |
| `CREATE TABLE IF NOT EXISTS` / `CREATE INDEX IF NOT EXISTS` | Ready | Both are valid Postgres syntax as well. |
| Parameterized `f"UPDATE ... SET {col} = ?"` dynamic SET-clause building (`user_repository.py`, `subscription_repository.py`) | Ready | Portable once the placeholder syntax above is addressed — the column-name interpolation itself is allowlist-guarded, not user input, and isn't SQLite-specific. |
| SQLite-only functions (`printf()`, `json_extract()`, etc.) | Not Applicable | None found anywhere in this codebase. |

No PostgreSQL conversion, ORM, or driver change was made this phase —
this table is an audit only, per the Critical Rules.

### Performance Report

**Good** (O(1)/O(log n) today, or after this phase's index additions,
even at large row counts):
- Every `telegram_id`-keyed lookup (`get_user`, `get_subscription`,
  `get_admin`, `is_admin`, `user_exists`, `subscription_exists`,
  `update_user`, `update_status`, etc.) — O(log n) via each table's
  `UNIQUE` index, unaffected by table growth.
- `get_signal(signal_id)` — O(log n) via the `UNIQUE` index on
  `signal_id`.
- `get_open_signals()`/`get_closed_signals()` — O(log n) partial scan
  after this phase's new `idx_signals_status`, versus O(n) before.
- `get_latest_signal()`/`get_recent_signals()` — improved from an
  O(n log n) full-table sort to an index-assisted scan after this
  phase's new `idx_signals_created_at`.
- `get_active_users()`/`count_by_status()` — improved the same way via
  the new `idx_users_status`.
- `count_open_feedback()` and `get_all_feedback()`'s `ORDER BY` —
  improved via the new `idx_feedback_status`/`idx_feedback_created_at`.

**Needs Optimization** (not changed this phase — no query logic was
touched per the Critical Rules, flagged for awareness only):
- `count_users_created_today()` — the `date(created_at) = date('now')`
  predicate cannot use a plain index (see Index Audit caveat above);
  remains an O(n) full scan regardless of this phase's new index.

**Future Risk** (fine today, worth watching as data grows):
- `get_all_users()` (`O(n)`, used by `AdminService.broadcast()`) and
  `get_all_subscriptions()`/`get_all_admins()`/`get_all_feedback()`
  (unbounded `get_all_feedback` has a `limit` param, the others do
  not) — full-table materialization into Python objects. Fine at
  hundreds-to-low-thousands of rows; at 10,000+ users, `get_all_users()`
  in particular (driving every broadcast) would benefit from batching/
  pagination in a future phase. Not changed here since it would touch
  `AdminService`/`Notifier` call sites outside `database/`'s scope.
- `count_users()`, `SELECT COUNT(*)` style aggregates generally — O(n)
  in SQLite (no maintained row-count cache); acceptable well past
  100,000 rows for a single aggregate, but worth knowing if these
  start being called in a hot path rather than an on-demand `/stats`
  command.
