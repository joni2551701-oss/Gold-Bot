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
`subscriptions`, `feedback`, `admins`); idempotent
`CREATE TABLE IF NOT EXISTS` + `PRAGMA table_info()`-guarded
migrations + `CREATE INDEX IF NOT EXISTS` (Phase 50), all in
`models.py`. `database.py` owns connection lifecycle
(`__enter__`/`__exit__`, commit-or-rollback, always closes).

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
