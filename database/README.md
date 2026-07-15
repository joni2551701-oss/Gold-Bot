# database/

## Purpose
SQLite persistence — the only place SQL is written anywhere in this
codebase.

## Flow
```
Service (telegram/*_service.py or core/pipeline.py)
      |
      v
Repository (database/*_repository.py)   -- parameterized SQL only
      |
      v
SQLite (database/goldbot.db)
```

## Responsibilities
One repository/model pair per table (`users`, `signals`,
`subscriptions`, `feedback`, `admins`, Phase 59.3's `raw_candles`/
`market_snapshots`, Phase 59.5's `sync_state`, Phase 59.6's
`audit_log`/`config_snapshots`, and — Phase 59.7 —
`runtime_features`); idempotent `CREATE TABLE IF NOT EXISTS` +
`PRAGMA table_info()`-guarded migrations + `CREATE INDEX IF NOT
EXISTS` (Phase 50), all in `models.py`. `database.py` owns connection
lifecycle (`__enter__`/`__exit__`, commit-or-rollback, always closes).

`runtime_features` (Phase 59.7: Runtime Feature Toggle Center, TASK 3)
is one row per feature name — `RuntimeFeatureRepository.set_feature()`
upserts it (same convention as `sync_state`'s
`update_sync_state()`), preserving `created_at` across every later
update while `updated_at`/`enabled`/`updated_by`/`reason` change. The
persisted backing store for
`configuration.runtime_feature_manager.RuntimeFeatureManager` —
`database/` itself knows nothing about dependency validation, audit
logging, or snapshotting; those live entirely in `configuration/`
(a new, one-directional `configuration/` → `database/` dependency, see
`configuration/README.md`).

`audit_log`/`config_snapshots` (Phase 59.6: Audit & Observability
Foundation, TASK 2/6) are both append-only — neither repository
exposes an update/delete method, matching an audit trail's own
purpose (a record that can't be quietly edited after the fact).
`audit_log_repository.py`'s `log_action()` records one owner/admin
action; nothing calls it automatically yet — no owner command is wired
to log itself in this phase. `config_snapshot_repository.py`'s
`save_snapshot()` persists a `configuration.feature_registry.build_feature_registry()`
capture for a future rollback; no apply/restore function exists yet.
See `docs/AUDIT_SYSTEM.md`/`docs/CONFIG_SNAPSHOT.md`.

`sync_state` (Phase 59.5: Historical Data Collection & Validation
Foundation, TASK 2) is one row per `(provider, symbol, timeframe)`,
tracking `data/historical_data_collector.py`'s
`sync_historical_candles()` own incremental watermark
(`last_timestamp`) so a repeated sync call resumes forward instead of
re-fetching a large window. Fully isolated, no SQL foreign key to
`raw_candles` (same no-foreign-key convention every table pair here
already follows) -- `sync_state_repository.py`'s
`update_sync_state()` upserts the row (check-then-branch UPDATE/INSERT,
same idiom as `SubscriptionRepository._update()`/`create_subscription()`).

`raw_candles`/`market_snapshots` (Phase 59.3, TASK 2: Raw Market
Storage Foundation) are the first tables added by any Phase A/AC/
Phase-59 module — every prior raw-market-data foundation
(`data/market_data_snapshot.py`) deliberately stayed in-memory-only.
Both are fully isolated new tables (no relation to `signals` or any
other existing table); see `docs/DATABASE.md`'s own entries for the
full schema. `database/raw_candle_models.py`'s `from_market_candle()`
(Phase 59 Real Market Validation Foundation, TASK 3) and
`RawCandleRepository.save_market_candles()` are the bridge from the
provider layer's own `MarketCandle` (`data/providers/`, Phase 59.1/
59.2 — e.g. `TwelveDataProvider.get_candles()`'s real output) into a
persisted `raw_candles` row — the first time those two pieces were
connected. MT5 stays unconnected (`MT5Provider` remains an inert
stub); nothing about the bridge itself is provider-specific.

## Input
Typed values from a repository method's caller (a service, or
`core/pipeline.py`'s `save_signal_record()`).

## Output
Domain records (`UserRecord`, `SubscriptionRecord`, `FeedbackRecord`,
`AdminRecord`) or plain `dict` rows (`SignalRepository`, which
returns `dict(row)` since its consumers read a flexible column
subset — see `docs/PERFORMANCE.md` for why this one repository's
`SELECT *` calls were deliberately not narrowed).

## Dependencies
`core/secrets.py` is not used here — no database credential exists
beyond a local file path (`config.Config.DB_PATH`). No dependency on
`telegram/`, `ai/`, `decision/`, `risk/`, `context/`, or `strategies/`
— a repository knows nothing about any of them.

## Future Expansion
See `docs/DATABASE.md` for the full schema/index/PostgreSQL-readiness
audit and `database/migrations/README.md` for the migration
philosophy a future dedicated migration script would follow.
