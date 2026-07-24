# Data Collection Rules

What Phase 59 Real Market Validation records, where it is stored, and
what it is explicitly not allowed to be. Companion to
`docs/VALIDATION_GUIDE.md` (how a validation cycle is run) and
`docs/PHASE59_VALIDATION.md` (the metric contract this data feeds).

## Principle

Every record collected during validation exists to answer one
question later: *"did the existing foundation behave as designed under
real market conditions?"* Nothing collected here is used to change
signal logic, decision thresholds, or risk sizing during the
validation period itself — see `CLAUDE.md`'s "Trading Safety" section.
Collection is observation, not intervention.

## What is collected

| Data | Type | Where it lives | Table / module |
|---|---|---|---|
| Raw candles | `database.raw_candle_models.RawCandle` | SQLite, `raw_candles` table | `database/raw_candle_repository.py` |
| Market snapshots | `database.market_snapshot_models.MarketSnapshotRecord` | SQLite, `market_snapshots` table | `database/market_snapshot_repository.py` |
| Signal records (durable) | `database.signal_record.SignalRecord` | SQLite, `signals` table | `database/signal_repository.py` |
| Signal schema (in-memory, per cycle) | `signals.schema.SignalSchema` (includes `market_phase` as of this phase) | `core/pipeline.py`'s `run()` result dict — not persisted as its own row | `signals/schema.py` |
| Paper trades | `lifecycle.paper_trade.PaperTrade` | In-memory only — no `paper_trades` table exists | `lifecycle/paper_trade.py` |
| Signal performance | `analytics.signal_performance.SignalPerformance` | In-memory only | `analytics/signal_performance.py` |
| Failure analysis entries | `ai.journal.failure_analysis.FailureAnalysisEntry` | In-memory only | `ai/journal/failure_analysis.py` |

Only `raw_candles`, `market_snapshots`, and `signals` are durable
(SQLite). Everything else is a plain Python object a caller builds,
uses, and (today) discards at process exit — persisting them further
is explicitly out of scope for this phase (see
`docs/PHASE59_VALIDATION.md`'s "Known gaps").

## What is never collected

- **No account balance, equity curve, or PnL.**
  `SignalPerformance.profit_loss` stays a permanent, honest `None` —
  no lot-value/account-currency computation exists in this codebase,
  and building one is out of scope for a "risk logic does not change"
  phase.
- **No broker credentials, order IDs, or execution confirmations.**
  `execution/` is inert; nothing in the validation data path ever
  calls it.
- **No user personal data beyond what `database/users` already
  stores** (unrelated to validation; untouched by this phase).

## Storage rules

- New tables are additive only. `raw_candles`/`market_snapshots`
  (Phase 59.3) use `CREATE TABLE IF NOT EXISTS` with their own
  `UNIQUE` constraints and never alter or read `signals`/`users`/
  `subscriptions`/`feedback`/`admins`.
  `RawCandle`/`MarketSnapshotRecord` are frozen dataclasses — a saved
  row is never mutated in place, only inserted (duplicates are
  skipped, not overwritten, per `(symbol, timeframe, timestamp,
  provider)`'s `UNIQUE` constraint).
- Provider identity is always recorded. Every `RawCandle` carries its
  `provider` field (`"twelvedata"` today; `MT5Provider` stays an inert
  stub, never a data source) so a future backtest never confuses which
  provider a candle came from.
- In-memory records (`PaperTrade`, `SignalPerformance`,
  `FailureAnalysisEntry`) are built fresh per call from
  already-computed inputs — none of them read the database or a
  network source directly; see each module's own docstring for its
  "compute from supplied data, don't fetch" posture.

## Failure analysis entries specifically

`ai.journal.failure_analysis.FailureAnalysisEntry`'s `reason`/`context`
fields are free text, written by whoever runs the validation cycle
(today: a human; nothing in this codebase auto-generates them). Two
rules for what belongs there, since these entries are the seed of a
future AI training dataset (this phase's own stated goal):

1. **Describe what happened, not what should have happened.**
   `"H4 bullish but M15 failed"` is a factual context note; "AI should
   have caught this" is not — that judgment belongs to the future
   phase that actually trains on this dataset, not to data collection.
2. **Never fabricate a reason.** If the cause of a loss genuinely isn't
   known yet, `reason` should say so plainly (e.g. `"unclear -- needs
   review"`) rather than guessing — an honest gap in the dataset is
   more useful later than a confidently wrong label.

## Retention

No retention/deletion policy exists yet for any table this phase
touches — validation data accumulates for as long as the operator
chooses to run the collection steps in `docs/VALIDATION_GUIDE.md`.
Defining a retention policy is future work, out of scope here.
