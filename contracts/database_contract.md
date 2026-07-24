# Database

## Responsibility
Persistence only. **Database never makes a business decision.**
`CLAUDE.md`'s Architecture Rules state this explicitly:
"Repositories own SQL only — no business rule belongs in a
`database/*_repository.py` file." See `docs/DECISION_PRINCIPLES.md`'s
Principle 5.

## Input
`database.signal_record.SignalRecord` (`SignalRepository.save_signal_record()`)
— built by `create_signal_record(signal, decision, risk_result,
timeframe)`, itself requiring a full `(SignalCandidate, TradeDecision,
RiskResult)` triple. User/subscription/feedback/admin data via
`database/*_repository.py`'s own typed methods
(`UserRepository.get_user()`, etc.).

## Output
Rows in the real, existing tables: **`signals`, `users`,
`subscriptions`, `feedback`, `admins`** (`database/models.py`'s exact
`CREATE TABLE` statements). Repository query methods return typed
Python objects (`SignalRecord`, user model rows), never raw cursors
to a caller outside `database/`.

**A deliberate correction to the brief's own example**: the brief
names "snapshots" and "analytics" as things Database "may store."
Neither table exists today — `context.snapshot.ContextSnapshotSchema`
(Phase A16) is explicitly "never itself written to the database in
this phase," and no analytics table has been created by any phase so
far. This document states the real, current table set; a future
`context_snapshots`/`analytics` table is a named, not-yet-approved
extension (see "Future Extension" below), not a present capability.

## Allowed Dependencies
✅ Whatever typed record/model each repository persists
(`SignalRecord` from `signals/`+`decision/`+`risk/`, user/
subscription/feedback/admin models defined in `database/` itself). A
repository reads the shape it's given; it does not compute new
values from it.

## Forbidden Dependencies
❌ Business decisions — a repository does not decide whether a
signal was good, does not compute a score, and does not gate what
gets saved based on quality. Every candidate's outcome is persisted
regardless of `APPROVE`/`REJECT`/`NO_TRADE` (see
`core/pipeline.py`'s unconditional `create_signal_record()` call per
candidate) — the notification-eligibility filter (what reaches a
*user*) lives in `core/pipeline.py`, never in `database/`.
❌ `telegram/` — `database/*_repository.py` never imports `telegram/`;
a repository knows nothing about Telegram, permissions, or commands
(`docs/ARCHITECTURE.md`'s Dependency Rules).
❌ `strategies/`, `ai/`, `decision/` logic — a repository imports
their *types* (`SignalCandidate`, `TradeDecision`, `RiskResult`) to
know what shape to persist, never their evaluation logic.

## Error Contract
Repository methods let a genuine SQL/connection failure propagate
(SQLite errors are not swallowed) — persistence failure is not a
business condition to degrade gracefully from, unlike a missing
market-data field. Per `contracts/error_contract.md`, a database
failure should be surfaced as `ConfigurationError` (bad path/schema)
or a dedicated future `DataError` subtype, not left as a bare
`sqlite3.Error` reaching the pipeline caller — not yet formally
implemented as typed exceptions; `core/pipeline.py`'s own
`persist_signals=True` gate means a default/backtesting run never
touches the database at all, avoiding the failure mode entirely
unless explicitly opted in.

## Future Extension
`context_snapshots`/`analytics` tables (per the brief's own naming)
are named, not-yet-approved future additions — Phase A16's
`ContextSnapshotSchema` and a future `SignalSchema`/`RiskResult`
analytics join are the natural shapes such tables would persist, once
a phase explicitly proposes the migration (this phase, and every
phase through A16, explicitly excludes database migration).
