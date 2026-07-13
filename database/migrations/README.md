# GoldBot Database Migrations — Foundation

This directory is the landing spot for future versioned migration
scripts. **No migration script exists yet as of Phase 50** — this file
defines the philosophy and rules a future script must follow. Today's
schema evolution still happens the way it always has: idempotent
`CREATE TABLE IF NOT EXISTS` plus `PRAGMA table_info()`-guarded
`ALTER TABLE ADD COLUMN` calls in `database/models.py`, run on every
repository construction. That pattern is not being replaced by this
phase — this README only prepares a foundation for when a change
becomes too large for that pattern to keep handling safely (e.g. a
column type change, a data backfill, or the eventual SQLite →
PostgreSQL move).

## Migration Philosophy

1. **Additive first.** A migration should add (a table, a column, an
   index) wherever possible, not rewrite or destroy. GoldBot's schema
   history so far (Phase 39, 40, 42, 45, 46, 50) has never needed a
   destructive migration, and that track record is a goal to keep, not
   an accident.
2. **Idempotent, always.** Every migration must be safe to run twice
   (or fifty times) against the same database with no error and no
   double-effect. `database/models.py`'s existing
   `PRAGMA table_info()` guard and `CREATE TABLE IF NOT EXISTS`/
   `CREATE INDEX IF NOT EXISTS` patterns are the reference
   implementation — any future migration script should follow the
   same guard-before-write shape, not assume a fresh database.
3. **No data loss without an explicit, separate, reviewed step.** A
   migration that adds a column or index is safe to bundle into
   normal deploys. A migration that would drop, rename, or retype a
   column — or touch existing rows — is not something a future
   migration script should do silently on every app start; it needs
   its own reviewed, deliberate run, separate from the automatic
   startup path.
4. **Backward compatible during the transition window.** Application
   code should keep working against both the pre-migration and
   post-migration schema for at least one deploy cycle wherever
   feasible (this is exactly how the Phase 39/40/45/46 column
   additions were done: new columns have defaults, so old rows read
   back with a sensible value instead of `NULL`/an error).
5. **One migration, one concern.** A single migration script should
   do one schema change (one table, or one closely related group of
   columns), not bundle unrelated changes — mirroring how
   `_migrate_signals_schema()` and `_migrate_users_schema()` are
   already split by table today.

## Version Naming

When migration scripts are introduced, each file in this directory
should be named:

```
NNN_short_description.sql   (or .py, matching whatever the eventual
                              migration runner expects)
```

- `NNN` — a zero-padded, strictly increasing integer (`001`, `002`,
  `003`, ...), assigned once and never reused or reordered.
- `short_description` — snake_case, e.g. `001_add_signals_symbol_index`,
  `002_add_users_last_login_column`.

This mirrors the existing Phase-numbered convention used throughout
this codebase's own development history (Phase 39, 42, 45, 46, 50 —
each phase's schema change is independently identifiable), applied to
migration files specifically.

## Execution Order

Migrations run in strictly ascending `NNN` order, once each, tracked
by a future `schema_migrations` (or similarly named) table recording
which `NNN` values have already been applied to a given database file
— so a migration never re-runs against a database that already has
it, and a fresh database runs every migration from `001` forward in
order. No such tracking table exists yet; this is a statement of
intent for whichever future phase introduces the first real migration
script, not a claim that Phase 50 built it.

## Rollback Rules

- A migration that only adds (table/column/index) does not need a
  rollback script — the safe "undo" is simply not using the new
  addition, and `DROP COLUMN`/`DROP INDEX` is available manually if
  ever truly necessary, but is not automated.
- A migration that changes existing data or column types must ship
  with a paired rollback step reviewed at the same time as the forward
  migration, not written after the fact under pressure.
- No migration in this project may be force-applied past a failure.
  If a migration step raises, the whole migration stops (matching
  `database/models.py`'s existing pattern: every `ALTER TABLE`/
  `CREATE INDEX` call is wrapped in `try/except sqlite3.Error` that
  logs and re-raises, never silently continues past a failed
  statement).

## Relationship to `database/models.py`

`database/models.py` remains the source of truth for the current
schema shape (`CREATE TABLE IF NOT EXISTS` + guarded `ALTER TABLE`/
`CREATE INDEX` calls, run automatically on every repository
construction). This directory does not replace that file or its
pattern. It exists so that a future, larger schema change — one that
doesn't fit the "add a column with a default" shape — has an agreed
place and process to live in, instead of being bolted onto
`models.py` under time pressure.
