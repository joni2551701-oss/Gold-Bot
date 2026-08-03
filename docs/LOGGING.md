# GoldBot Logging Standard (Phase 51)

Single logging foundation for the whole project: one shared factory
(`core_layer/logger/logger.py`'s `setup_logger()`), one format, one set of level
rules, applied consistently across every module. This document is the
reference; `core_layer/logger/logger.py` itself was **not changed** this phase —
it already implements the shape described below correctly.

## Configuration

```python
# core_layer/logger/logger.py
def setup_logger(name: str = "GoldBot"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger
```

- Every module gets its logger the same way:
  `logger = setup_logger("SomeName")`, once, at module import time.
- Output goes to **stdout only** today (see `logs/README.md` for the
  planned file-category foundation — not wired up yet).
- Level floor is `INFO` — `DEBUG` calls exist in the level policy
  below for future use but are not emitted by the current
  configuration; nothing in the codebase currently calls
  `logger.debug()`.
- `if not logger.handlers:` guards against duplicate handlers if
  `setup_logger()` is ever called twice for the same name (Python's
  `logging.getLogger(name)` returns the same singleton instance across
  calls) — already correct, unchanged.

## Log Levels

| Level | Meaning | Example from this codebase |
|---|---|---|
| `DEBUG` | Developer-only detail; verbose, off by default. | Reserved for future use — see Best Practices. |
| `INFO` | Normal workflow — something expected happened. | `logger.info("GoldBot starting...")`, `logger.info(f"[{symbol}\|{interval}] Fetched {len(candles)} candles.")` |
| `WARNING` | Recoverable issue — something failed, but the caller has a safe fallback and continues. | `logger.warning(f"is_admin check failed for user_id={user_id}: {e}")` |
| `ERROR` | An operation failed and could not recover, but the process itself keeps running. | `logger.error(f"Failed to initialize database schema: {e}")` (followed by `raise`) |
| `EXCEPTION` | Same as ERROR, but called from inside an `except` block so the log record also carries the full stack trace — use when a human will need the traceback to diagnose a fatal failure. | `logger.exception(f"GoldBot run failed: {e}")` in `main.py`, right before re-raising. |

`logger.exception()` is not a distinct level — it logs at `ERROR`
level but automatically attaches `sys.exc_info()`. Use it exactly
where a caught exception is about to be re-raised or otherwise treated
as fatal for that unit of work; use plain `logger.error()`/
`logger.warning()` for everything else, since a full traceback for
every routine recoverable failure is noise, not diagnostics.

## Logger Hierarchy

One `setup_logger("Name")` call per module, `Name` matching the
module's primary class/responsibility (`PascalCase`, no punctuation).
Full inventory as of this phase (33 loggers, zero duplicates, zero
generic/unclear names):

```
main.py                              GoldBot
core/pipeline.py                     TradingPipeline

data/twelve_data_client.py           TwelveDataClient
data/market_data.py                  MarketDataNormalizer
data/data_cache.py                   SmartDataCache
data/session_filter.py               SessionFilter

context/context_orchestrator.py      ContextEngine
context/market_structure.py          MarketStructureEngine
context/bos.py                       BOSEngine
context/choch.py                     ChochEngine
context/amd.py                       AMD

ai/ai_analyzer.py                    AIAnalyzer

decision/                            (no logger -- see Task 1 notes below)
risk/                                (no logger -- see Task 1 notes below)
signals/                             (no logger -- see Task 1 notes below)
strategies/                          (no logger -- see Task 1 notes below)
execution/                           (no logger -- inert scaffolding)

monitoring/performance.py            PerformanceTracker

database/database.py                 DatabaseManager
database/models.py                   DatabaseModels
database/user_repository.py          UserRepository
database/subscription_repository.py  SubscriptionRepository
database/signal_repository.py        SignalRepository
database/feedback_repository.py      FeedbackRepository
database/admin_repository.py         AdminRepository

telegram/polling.py                  TelegramPolling
telegram/command_router.py           CommandRouter
telegram/handlers.py                 Handlers
telegram/permissions.py              Permissions
telegram/bot.py                      TelegramBot
telegram/notifier.py                 Notifier
telegram/user_service.py             UserService
telegram/admin_service.py            AdminService
telegram/subscription_service.py     SubscriptionService
telegram/notification_service.py     NotificationService
telegram/feedback_service.py         FeedbackService
telegram/signal_service.py           SignalService
telegram/signal_access_service.py    SignalAccessService
telegram/result_handler.py           ResultHandler
```

Modules with no logger and no `try`/`except`/`raise` at all (pure
dataclasses, pure functions, or static text) intentionally have none:
`signals/models.py`, `decision/models.py`, `risk/risk_manager.py`,
`strategies/*.py`, `signals/signal_engine.py`, `telegram/keyboards.py`,
`telegram/commands.py`, `telegram/signal_formatter.py`,
`context/candle.py`, `context/context_config.py`, `context/fvg.py`,
`context/liquidity.py`, `context/order_block.py`, all `database/*_models.py`,
`ai/ai_prompt.py`, `ai/confidence_model.py`, `ai/trade_journal.py`,
`execution/*.py`, `monitoring/signal_monitor.py`. Adding a logger to a
file with nothing to log would be surface for its own sake — not done.

## Examples

**Startup / shutdown (`main.py`):**
```python
logger.info("GoldBot starting...")
logger.info("Configuration loaded.")
...
logger.info("Trading Pipeline initialized.")
...
logger.info("Starting pipeline...")
result = self.pipeline.run()
logger.info("Pipeline finished.")
...
logger.info("GoldBot finished.")   # in a finally: block -- always runs
```

**Recoverable failure inside a best-effort call (`telegram/handlers.py`):**
```python
try:
    UserService().touch_activity(telegram_id)
except Exception as e:
    logger.warning(f"profile_handler: touch_activity failed for telegram_id={telegram_id}: {e}")
    # execution continues -- touch_activity is best-effort
```

**Fatal failure, re-raised (`main.py`):**
```python
try:
    result = self.pipeline.run()
    ...
except Exception as e:
    logger.exception(f"GoldBot run failed: {e}")
    raise
```

**Professional error message shape (Task 6):** state what failed, then
why, in the message itself — not a bare `"Error"`.
```python
logger.error(f"Failed to initialize database schema: {e}")
logger.warning(f"is_admin check failed for user_id={user_id}: {e}")
logger.info("Broadcast finished: 12 sent, 1 failed.")
```

## Best Practices

1. **One logger per module, created once at import time.** Never call
   `setup_logger()` inside a function/method body — it's cheap
   (returns the same `logging.getLogger()` singleton), but a
   module-level `logger = setup_logger("X")` keeps every file's
   pattern identical and greppable.
2. **Match the level to the rubric above, not to how it feels in the
   moment.** A caught exception that the caller safely falls back from
   is `WARNING`, not `ERROR` — reserve `ERROR`/`EXCEPTION` for
   failures that actually stop the current operation.
3. **Use `logger.exception()` only inside an `except` block, and only
   when the failure is being treated as fatal** (re-raised, or the
   caller has no fallback). Calling it for a routine recoverable
   `except` just adds an irrelevant stack trace to the log stream.
4. **Never log secrets, tokens, or full user message content.**
   Confirmed clean this phase: no API key, bot token, or Telegram
   message/feedback body is ever interpolated into a log line anywhere
   in the codebase. Log the fact that something happened (a chat_id, a
   telegram_id, a byte count, a sent/failed count) — never the payload
   itself.
5. **Database logging is connection/migration/critical-failure only —
   never per-query.** No repository logs a `SELECT`/`INSERT`/`UPDATE`
   statement or its parameters; only schema init, column migrations,
   index creation, and `sqlite3.IntegrityError`/`sqlite3.Error`
   failures are logged. Keep it that way — per-query logging at
   production call volume becomes noise that hides the failures that
   actually matter.
6. **Don't log the same failure twice at the same severity in the same
   call path.** If a lower layer already logs a failure with useful
   detail (e.g. `MarketDataNormalizer.get_candles()` logging a missing
   API key at `ERROR`), a caller that receives the resulting empty/
   default value generally doesn't need to log it again — check
   whether the information is already visible before adding a second
   log line for the same event.
7. **A recoverable error gets `logger.warning()`; a fatal one gets
   `logger.exception()` immediately before its `raise`.** This is the
   single rule Task 13 of this phase enforced across every module
   touched — apply it to any new exception handling added after this
   phase too.
