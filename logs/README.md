# GoldBot Logs — Foundation

This directory is the landing spot for future log **files**. As of
Phase 51, `core_layer/logger/logger.py`'s `setup_logger()` writes to **stdout
only** (`logging.StreamHandler(sys.stdout)`) — there is no file
handler anywhere in the codebase yet, and this phase does not add one.
This README documents the planned category split for whenever
file-based logging is introduced; it is a naming/foundation contract,
not a working feature yet.

Today, stdout is genuinely enough: `main.py` runs as a scheduled
GitHub Actions job (`trading_bot.yml`) whose console output is already
captured and retained by Actions itself, and `platform_layer/telegram/polling.py`
runs as a long-lived process wherever its host process manager (systemd,
a container runtime, etc.) already captures stdout. File-based logging
becomes valuable once GoldBot moves to persistent VPS hosting where
that automatic capture no longer applies — this foundation exists so
that move doesn't require inventing the category split from scratch.

## Planned Categories

| File | Would contain | Sourced from (logger names) |
|---|---|---|
| `app.log` | Everything not covered by a more specific category below — general application lifecycle, startup/shutdown, pipeline orchestration. | `GoldBot`, `TradingPipeline`, `ContextEngine`, `AMD`, `BOSEngine`, `ChochEngine`, `MarketStructureEngine` |
| `error.log` | Every `ERROR`/`EXCEPTION`-level record, mirrored here regardless of which logger produced it — a single place to check "what broke" without knowing which module to look in first. | All loggers, filtered by level |
| `telegram.log` | The Telegram product layer: polling, command routing, permissions, handlers, and every `telegram.*` service. | `TelegramPolling`, `CommandRouter`, `Handlers`, `Permissions`, `TelegramBot`, `Notifier`, `UserService`, `AdminService`, `SubscriptionService`, `NotificationService`, `FeedbackService`, `SignalService`, `SignalAccessService`, `ResultHandler` |
| `database.log` | Connection lifecycle, schema/migration/index events, and critical query failures only — never per-query spam (see `docs/LOGGING.md`'s Database Logging Policy). | `DatabaseManager`, `DatabaseModels`, `UserRepository`, `SignalRepository`, `SubscriptionRepository`, `FeedbackRepository`, `AdminRepository` |
| `trade.log` | The trading-decision chain specifically: market data, signal generation, AI evaluation, decision, and risk outcomes for each pipeline cycle. | `MarketDataNormalizer`, `TwelveDataClient`, `SmartDataCache`, `SessionFilter`, `AIAnalyzer`, `PerformanceTracker` (decision/risk currently log through `TradingPipeline`, which stays in `app.log` since it's the orchestrator, not a trade-specific log emitter itself) |

## What This Phase Did NOT Do

- No log rotation (size-based, time-based, or otherwise).
- No file `Handler` added to `core_layer/logger/logger.py` — `setup_logger()` is
  unchanged and still stdout-only.
- No per-logger routing to the files above — the table is a target
  mapping for a future phase to implement, not a claim that it's wired
  up today.
- No third-party logging library (`logging.handlers.RotatingFileHandler`
  is stdlib and would be the natural fit later, but wasn't added here
  either — this phase is foundation only, per its own explicit scope).

## Why Not Now

Adding real file handlers changes `core_layer/logger/logger.py`'s behavior for
every single logger in the codebase simultaneously (over 30 modules
call `setup_logger()`) — that's exactly the kind of repo-wide behavior
change this phase's Critical Rules explicitly want to avoid ("mavjud
loggerlarni bekorga almashtirma", "log formatini keraksiz
o'zgartirma"). This directory and its category map exist so that when
file-based logging *is* introduced (a future, dedicated phase), the
naming and routing decisions are already made and reviewed, rather
than improvised under deployment pressure.
