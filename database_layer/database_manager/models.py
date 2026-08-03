import sqlite3
from core_layer.logger.logger import setup_logger

logger = setup_logger("DatabaseModels")

def init_schema(connection: sqlite3.Connection):
    """
    Defines and creates the signals table schema, then migrates any
    pre-existing table (created before Phase 39) to include the newer
    display columns. Safe to call on every construction: CREATE TABLE
    IF NOT EXISTS is a no-op once the table exists, and the migration
    step below only adds a column that isn't already there.
    """
    query = """
    CREATE TABLE IF NOT EXISTS signals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        signal_id TEXT UNIQUE NOT NULL,
        symbol TEXT NOT NULL,
        direction TEXT NOT NULL,
        entry_zone_min REAL NOT NULL,
        entry_zone_max REAL NOT NULL,
        stop_loss REAL NOT NULL,
        take_profit_1 REAL NOT NULL,
        take_profit_2 REAL NOT NULL,
        risk_percent REAL NOT NULL,
        lot_size REAL NOT NULL,
        strategy_name TEXT NOT NULL,
        confidence_score REAL NOT NULL,
        ai_explanation TEXT,
        status TEXT DEFAULT 'OPEN',
        result TEXT DEFAULT 'OPEN',
        created_at TEXT NOT NULL,
        closed_at TEXT,
        strategy TEXT DEFAULT 'UNKNOWN',
        timeframe TEXT DEFAULT 'M15',
        rr_ratio REAL DEFAULT 0,
        ai_decision TEXT DEFAULT 'N/A',
        risk_status TEXT DEFAULT 'N/A',
        risk_amount REAL DEFAULT 0,
        signal_status TEXT DEFAULT 'NEW'
    );
    """
    try:
        connection.execute(query)
        connection.commit()
        logger.info("Database schema (signals table) initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize database schema: {e}")
        raise

    _migrate_signals_schema(connection)
    _create_signals_indexes(connection)


def _create_signals_indexes(connection: sqlite3.Connection):
    """
    Phase 50 index audit: 'status' (SignalRepository.get_open_signals()/
    get_closed_signals()) and 'created_at' (get_latest_signal()/
    get_recent_signals()'s ORDER BY) are the two columns actually
    filtered/sorted on today. signal_id already has an implicit index
    via its UNIQUE constraint, so it is not duplicated here.
    CREATE INDEX IF NOT EXISTS is idempotent -- safe on every
    construction, including against a database that already has these
    indexes from a prior run.
    """
    statements = [
        "CREATE INDEX IF NOT EXISTS idx_signals_status ON signals(status)",
        "CREATE INDEX IF NOT EXISTS idx_signals_created_at ON signals(created_at)",
    ]
    try:
        for statement in statements:
            connection.execute(statement)
        connection.commit()
    except sqlite3.Error as e:
        logger.error(f"Failed to create signals indexes: {e}")
        raise


def _migrate_signals_schema(connection: sqlite3.Connection):
    """
    Adds the Phase 39 display columns to a 'signals' table created
    before this phase. SQLite has no "ADD COLUMN IF NOT EXISTS", so
    each column's presence is checked via PRAGMA table_info first --
    on a fresh table (already created with all columns above) every
    column is already present and this is a no-op.
    """
    new_columns = [
        ("strategy", "TEXT DEFAULT 'UNKNOWN'"),
        ("timeframe", "TEXT DEFAULT 'M15'"),
        ("rr_ratio", "REAL DEFAULT 0"),
        ("ai_decision", "TEXT DEFAULT 'N/A'"),
        ("risk_status", "TEXT DEFAULT 'N/A'"),
        ("risk_amount", "REAL DEFAULT 0"),
        ("signal_status", "TEXT DEFAULT 'NEW'"),
    ]

    try:
        cursor = connection.execute("PRAGMA table_info(signals)")
        existing_columns = {row[1] for row in cursor.fetchall()}
    except sqlite3.Error as e:
        logger.error(f"Failed to inspect signals table for migration: {e}")
        raise

    migrated = False
    for column_name, column_def in new_columns:
        if column_name in existing_columns:
            continue
        try:
            connection.execute(f"ALTER TABLE signals ADD COLUMN {column_name} {column_def}")
            logger.info(f"Migrated signals table: added column '{column_name}'.")
            migrated = True
        except sqlite3.Error as e:
            logger.error(f"Failed to add column '{column_name}' to signals table: {e}")
            raise

    if migrated:
        connection.commit()


def init_user_schema(connection: sqlite3.Connection):
    """
    Defines and creates the users table schema (Telegram user profile
    foundation), then migrates any pre-existing table (created before
    Phase 40/45) to include the newer settings/lifecycle columns. No
    relation to the signals table -- separate, independently-initialized
    table.
    """
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT UNIQUE NOT NULL,
        username TEXT,
        language TEXT DEFAULT 'UZ',
        trading_style TEXT DEFAULT 'Intraday',
        risk_percent REAL DEFAULT 2.0,
        timeframe TEXT DEFAULT 'M15',
        created_at TEXT NOT NULL,
        updated_at TEXT,
        strategy TEXT DEFAULT 'Liquidity Sweep',
        notifications_enabled INTEGER DEFAULT 1,
        status TEXT DEFAULT 'NEW',
        last_activity TIMESTAMP,
        phone_hash TEXT,
        trial_started_at TEXT,
        registration_step TEXT DEFAULT 'LANGUAGE',
        registration_completed INTEGER DEFAULT 0
    );
    """
    try:
        connection.execute(query)
        connection.commit()
        logger.info("Database schema (users table) initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize users schema: {e}")
        raise

    _migrate_users_schema(connection)
    _create_users_indexes(connection)


def _create_users_indexes(connection: sqlite3.Connection):
    """
    Phase 50 index audit: 'status' is filtered by get_active_users()/
    count_by_status(); 'created_at' is filtered by
    count_users_created_today() (via date(created_at) = date('now') --
    note this specific function-wrapped predicate will not itself be
    accelerated by a plain B-tree index, but the column is kept
    indexed for any future direct created_at range query). telegram_id
    already has an implicit index via its UNIQUE constraint, so it is
    not duplicated here. CREATE INDEX IF NOT EXISTS is idempotent.
    """
    statements = [
        "CREATE INDEX IF NOT EXISTS idx_users_status ON users(status)",
        "CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at)",
    ]
    try:
        for statement in statements:
            connection.execute(statement)
        connection.commit()
    except sqlite3.Error as e:
        logger.error(f"Failed to create users indexes: {e}")
        raise


def _migrate_users_schema(connection: sqlite3.Connection):
    """
    Adds the Phase 40 settings columns, Phase 45 lifecycle columns
    (status, last_activity), Phase 61.4 TASK 4's phone_hash column,
    Phase 61.5 TASK 4's trial_started_at column, and V2 Phase 3's
    registration_step/registration_completed columns to a 'users'
    table created before those phases. SQLite has no "ADD COLUMN IF
    NOT EXISTS", so each column's presence is checked via PRAGMA
    table_info first -- on a fresh table (already created with all
    columns above) every column is already present and this is a
    no-op. Idempotent: safe to call every time a UserRepository is
    constructed, including a second run against an already-migrated
    table (no duplicate-column error).
    """
    new_columns = [
        ("strategy", "TEXT DEFAULT 'Liquidity Sweep'"),
        ("notifications_enabled", "INTEGER DEFAULT 1"),
        ("status", "TEXT DEFAULT 'NEW'"),
        ("last_activity", "TIMESTAMP"),
        ("phone_hash", "TEXT"),
        ("trial_started_at", "TEXT"),
        ("registration_step", "TEXT DEFAULT 'LANGUAGE'"),
        ("registration_completed", "INTEGER DEFAULT 0"),
    ]

    try:
        cursor = connection.execute("PRAGMA table_info(users)")
        existing_columns = {row[1] for row in cursor.fetchall()}
    except sqlite3.Error as e:
        logger.error(f"Failed to inspect users table for migration: {e}")
        raise

    migrated = False
    registration_columns_are_new = "registration_step" not in existing_columns
    for column_name, column_def in new_columns:
        if column_name in existing_columns:
            continue
        try:
            connection.execute(f"ALTER TABLE users ADD COLUMN {column_name} {column_def}")
            logger.info(f"Migrated users table: added column '{column_name}'.")
            migrated = True
        except sqlite3.Error as e:
            logger.error(f"Failed to add column '{column_name}' to users table: {e}")
            raise

    if registration_columns_are_new:
        _backfill_registration_state(connection)

    if migrated:
        connection.commit()


def _backfill_registration_state(connection: sqlite3.Connection):
    """
    V2 Phase 3: one-time backfill for rows that predate the
    registration_step/registration_completed columns -- these users
    already went through the (then-optional) Phone Share flow under
    the pre-Phase-3 product, so they must not be sent back through
    the Language step. A row with phone_hash already set is treated
    as having completed registration under the old model; a row
    without one still needs the now-mandatory Phone Share step, but
    not the Language step (Language was never gated for them either).
    Brand new rows created after this migration get the column
    defaults applied by init_user_schema()'s own CREATE TABLE
    (registration_step='LANGUAGE', registration_completed=0) instead,
    since they never reach this function.
    """
    try:
        connection.execute(
            "UPDATE users SET registration_step = 'COMPLETE', registration_completed = 1 "
            "WHERE phone_hash IS NOT NULL"
        )
        connection.execute(
            "UPDATE users SET registration_step = 'PHONE' WHERE phone_hash IS NULL"
        )
        logger.info("Backfilled registration_step/registration_completed for pre-existing users.")
    except sqlite3.Error as e:
        logger.error(f"Failed to backfill registration state: {e}")
        raise


def init_subscription_schema(connection: sqlite3.Connection):
    """
    Defines and creates the subscriptions table schema (Phase 42
    Subscription Foundation). Independent of the users/signals/admins
    tables -- linked to users via telegram_id, not a SQL foreign key
    (none of the other tables here use one either). Brand new table,
    so unlike init_schema()/init_user_schema() there is no pre-Phase-42
    column set to migrate from: CREATE TABLE IF NOT EXISTS alone is
    safe for both a fresh database and an existing one that simply
    doesn't have this table yet.
    """
    query = """
    CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT UNIQUE NOT NULL,
        plan TEXT DEFAULT 'FREE',
        status TEXT DEFAULT 'ACTIVE',
        started_at TEXT NOT NULL,
        expires_at TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT
    );
    """
    try:
        connection.execute(query)
        connection.commit()
        logger.info("Database schema (subscriptions table) initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize subscriptions schema: {e}")
        raise


def init_feedback_schema(connection: sqlite3.Connection):
    """
    Defines and creates the feedback table schema (Phase 46 Feedback
    System Foundation). Independent of the other tables. Brand new
    table -- no migration needed (same reasoning as
    init_subscription_schema(), Phase 42): CREATE TABLE IF NOT EXISTS
    alone is safe for both a fresh database and an existing one that
    simply doesn't have this table yet. telegram_id/created_at use
    TEXT (not INTEGER/TIMESTAMP) to match every other table's
    convention in this schema (str(telegram_id), ISO-format
    timestamps) -- SQLite's dynamic typing makes this a pure
    consistency choice, not a functional one.
    """
    query = """
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT NOT NULL,
        message TEXT NOT NULL,
        status TEXT DEFAULT 'OPEN',
        created_at TEXT NOT NULL
    );
    """
    try:
        connection.execute(query)
        connection.commit()
        logger.info("Database schema (feedback table) initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize feedback schema: {e}")
        raise

    _create_feedback_indexes(connection)


def _create_feedback_indexes(connection: sqlite3.Connection):
    """
    Phase 50 index audit: 'status' is filtered by count_open_feedback();
    'created_at' is sorted on by get_all_feedback()'s ORDER BY.
    telegram_id has no current WHERE-clause usage anywhere in
    FeedbackRepository, so it is intentionally not indexed here (no
    query would benefit today -- see docs/DATABASE.md).
    CREATE INDEX IF NOT EXISTS is idempotent.
    """
    statements = [
        "CREATE INDEX IF NOT EXISTS idx_feedback_status ON feedback(status)",
        "CREATE INDEX IF NOT EXISTS idx_feedback_created_at ON feedback(created_at)",
    ]
    try:
        for statement in statements:
            connection.execute(statement)
        connection.commit()
    except sqlite3.Error as e:
        logger.error(f"Failed to create feedback indexes: {e}")
        raise


def init_admin_schema(connection: sqlite3.Connection):
    """
    Defines and creates the admins table schema (Owner/Admin permission
    foundation). Independent of the signals/users tables.
    """
    query = """
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT UNIQUE NOT NULL,
        role TEXT DEFAULT 'ADMIN',
        created_at TEXT NOT NULL
    );
    """
    try:
        connection.execute(query)
        connection.commit()
        logger.info("Database schema (admins table) initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize admins schema: {e}")
        raise


def init_raw_candle_schema(connection: sqlite3.Connection):
    """
    Defines and creates the raw_candles table schema (Phase 59.3, TASK
    2: Raw Market Storage Foundation -- the first real database
    migration added by any Phase A/AC/Phase-59 foundation module; see
    database_layer/market_repository/raw_candle_models.py's own module docstring). Independent
    of every other table -- no ALTER, no shared column, no foreign
    key (same no-SQL-foreign-key convention every other table in this
    schema already follows).

    UNIQUE(symbol, timeframe, timestamp, provider): the same candle
    window from two different providers is two distinct rows, never
    merged or overwritten -- a duplicate insert from the SAME provider
    for the SAME window is what this constraint actually prevents (see
    database_layer/market_repository/raw_candle_repository.py's own IntegrityError handling).
    """
    query = """
    CREATE TABLE IF NOT EXISTS raw_candles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        timeframe TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        open REAL NOT NULL,
        high REAL NOT NULL,
        low REAL NOT NULL,
        close REAL NOT NULL,
        volume REAL,
        provider TEXT NOT NULL,
        created_at TEXT NOT NULL,
        UNIQUE(symbol, timeframe, timestamp, provider)
    );
    """
    try:
        connection.execute(query)
        connection.commit()
        logger.info("Database schema (raw_candles table) initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize raw_candles schema: {e}")
        raise

    _create_raw_candle_indexes(connection)


def _create_raw_candle_indexes(connection: sqlite3.Connection):
    """
    (symbol, timeframe) is the primary lookup pattern (a backtest
    reconstructing one symbol/timeframe's history); timestamp is
    filtered/sorted on for a date-range query. The UNIQUE constraint
    above already gives (symbol, timeframe, timestamp, provider) an
    implicit index, so it is not duplicated here. CREATE INDEX IF NOT
    EXISTS is idempotent, same pattern as every other table's own
    index-creation function in this file.
    """
    statements = [
        "CREATE INDEX IF NOT EXISTS idx_raw_candles_symbol_timeframe ON raw_candles(symbol, timeframe)",
        "CREATE INDEX IF NOT EXISTS idx_raw_candles_timestamp ON raw_candles(timestamp)",
    ]
    try:
        for statement in statements:
            connection.execute(statement)
        connection.commit()
    except sqlite3.Error as e:
        logger.error(f"Failed to create raw_candles indexes: {e}")
        raise


def init_market_snapshot_schema(connection: sqlite3.Connection):
    """
    Defines and creates the market_snapshots table schema (Phase 59.3,
    TASK 2). Independent of every other table, including raw_candles
    (no SQL foreign key -- linked only by shared symbol/timeframe/
    provider values, same convention as every other table pair in this
    schema). The persisted counterpart to data_layer.live_data.market_data_snapshot.MarketDataSnapshot
    (Phase 59 Preparation/59.1, in-memory only) -- see
    database_layer/market_repository/market_snapshot_models.py's own module docstring.
    """
    query = """
    CREATE TABLE IF NOT EXISTS market_snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        market_snapshot_id TEXT UNIQUE NOT NULL,
        symbol TEXT NOT NULL,
        timeframe TEXT NOT NULL,
        provider TEXT,
        candle_count INTEGER NOT NULL,
        first_timestamp TEXT,
        last_timestamp TEXT,
        candles_reference TEXT NOT NULL,
        data_quality TEXT,
        created_at TEXT NOT NULL
    );
    """
    try:
        connection.execute(query)
        connection.commit()
        logger.info("Database schema (market_snapshots table) initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize market_snapshots schema: {e}")
        raise

    _create_market_snapshot_indexes(connection)


def _create_market_snapshot_indexes(connection: sqlite3.Connection):
    """(symbol, timeframe) is the lookup pattern; created_at is sorted on for a recent-snapshots query. market_snapshot_id already has an implicit index via its UNIQUE constraint."""
    statements = [
        "CREATE INDEX IF NOT EXISTS idx_market_snapshots_symbol_timeframe ON market_snapshots(symbol, timeframe)",
        "CREATE INDEX IF NOT EXISTS idx_market_snapshots_created_at ON market_snapshots(created_at)",
    ]
    try:
        for statement in statements:
            connection.execute(statement)
        connection.commit()
    except sqlite3.Error as e:
        logger.error(f"Failed to create market_snapshots indexes: {e}")
        raise


def init_sync_state_schema(connection: sqlite3.Connection):
    """
    Defines and creates the sync_state table schema (Phase 59.5:
    Historical Data Collection & Validation Foundation, TASK 2).
    Independent of every other table, including raw_candles -- one row
    per (provider, symbol, timeframe), tracking the incremental
    collector's own watermark. See database_layer/market_repository/sync_state_models.py's own
    module docstring.

    UNIQUE(provider, symbol, timeframe): exactly one current sync state
    per key -- SyncStateRepository.update_sync_state() upserts this row
    rather than appending a new one per sync.
    """
    query = """
    CREATE TABLE IF NOT EXISTS sync_state (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        provider TEXT NOT NULL,
        symbol TEXT NOT NULL,
        timeframe TEXT NOT NULL,
        last_timestamp TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        UNIQUE(provider, symbol, timeframe)
    );
    """
    try:
        connection.execute(query)
        connection.commit()
        logger.info("Database schema (sync_state table) initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize sync_state schema: {e}")
        raise


def init_audit_log_schema(connection: sqlite3.Connection):
    """
    Defines and creates the audit_log table schema (Phase 59.6: Audit
    & Observability Foundation, TASK 2). Independent of every other
    table -- no foreign key, no relation to `admins`/`users` beyond
    `actor` holding the same kind of identifier by convention, never
    enforced structurally. Append-only by design: this repository
    exposes no update/delete method, matching an audit log's own
    purpose (a record that can't be quietly edited after the fact).
    """
    query = """
    CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        actor TEXT NOT NULL,
        action TEXT NOT NULL,
        target TEXT,
        result TEXT NOT NULL DEFAULT 'SUCCESS',
        details TEXT,
        created_at TEXT NOT NULL
    );
    """
    try:
        connection.execute(query)
        connection.commit()
        logger.info("Database schema (audit_log table) initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize audit_log schema: {e}")
        raise

    _create_audit_log_indexes(connection)


def _create_audit_log_indexes(connection: sqlite3.Connection):
    """actor is the lookup pattern (a future "what did owner X do" query); created_at is sorted on for a recent-entries query. CREATE INDEX IF NOT EXISTS is idempotent."""
    statements = [
        "CREATE INDEX IF NOT EXISTS idx_audit_log_actor ON audit_log(actor)",
        "CREATE INDEX IF NOT EXISTS idx_audit_log_created_at ON audit_log(created_at)",
    ]
    try:
        for statement in statements:
            connection.execute(statement)
        connection.commit()
    except sqlite3.Error as e:
        logger.error(f"Failed to create audit_log indexes: {e}")
        raise


def init_config_snapshot_schema(connection: sqlite3.Connection):
    """
    Defines and creates the config_snapshots table schema (Phase 59.6:
    Audit & Observability Foundation, TASK 6). Independent of every
    other table -- no foreign key. Append-only, same posture as
    audit_log: this repository exposes no update/delete, a snapshot is
    a fixed point-in-time record.
    """
    query = """
    CREATE TABLE IF NOT EXISTS config_snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        snapshot_id TEXT UNIQUE NOT NULL,
        feature_state TEXT NOT NULL,
        taken_at TEXT NOT NULL,
        taken_by TEXT,
        reason TEXT
    );
    """
    try:
        connection.execute(query)
        connection.commit()
        logger.info("Database schema (config_snapshots table) initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize config_snapshots schema: {e}")
        raise

    _create_config_snapshot_indexes(connection)


def _create_config_snapshot_indexes(connection: sqlite3.Connection):
    """taken_at is sorted on for a "most recent snapshot" query. snapshot_id already has an implicit index via its UNIQUE constraint."""
    try:
        connection.execute("CREATE INDEX IF NOT EXISTS idx_config_snapshots_taken_at ON config_snapshots(taken_at)")
        connection.commit()
    except sqlite3.Error as e:
        logger.error(f"Failed to create config_snapshots indexes: {e}")
        raise


def init_runtime_feature_schema(connection: sqlite3.Connection):
    """
    Defines and creates the runtime_features table schema (Phase 59.7:
    Runtime Feature Toggle Center, TASK 3). Independent of every other
    table, including config_snapshots -- no foreign key. One row per
    feature name (`feature UNIQUE NOT NULL`) --
    RuntimeFeatureRepository.set_feature() upserts this row rather than
    appending a new one per toggle, same convention as
    database_layer/market_repository/sync_state_repository.py's update_sync_state().
    """
    query = """
    CREATE TABLE IF NOT EXISTS runtime_features (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        feature TEXT UNIQUE NOT NULL,
        enabled INTEGER NOT NULL,
        created_at TEXT,
        updated_at TEXT NOT NULL,
        updated_by TEXT,
        reason TEXT
    );
    """
    try:
        connection.execute(query)
        connection.commit()
        logger.info("Database schema (runtime_features table) initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize runtime_features schema: {e}")
        raise


def init_emergency_state_schema(connection: sqlite3.Connection):
    """
    Defines and creates the emergency_states table schema (Phase 59.9:
    Emergency Safety Layer Foundation, TASK 2). Independent of every
    other table -- no foreign key. Append-only: every transition is a
    new row (no UNIQUE constraint on `state`), unlike runtime_features'
    one-row-per-name upsert -- history must never be lost, per this
    task's own brief. "Current state" is derived by the repository as
    the most recent row (ORDER BY id DESC LIMIT 1), not a separate
    column.
    """
    query = """
    CREATE TABLE IF NOT EXISTS emergency_states (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        state TEXT NOT NULL,
        reason TEXT,
        source TEXT NOT NULL DEFAULT 'system',
        changed_by TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    """
    try:
        connection.execute(query)
        connection.commit()
        logger.info("Database schema (emergency_states table) initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize emergency_states schema: {e}")
        raise


def init_learning_schema(connection: sqlite3.Connection):
    """
    Defines and creates the learning_records table schema (Phase 60.6:
    Learning Loop Foundation, TASK 5; extended Phase 60.7: Adaptive
    Intelligence Layer Foundation, TASK 3). Independent of every other
    table -- no foreign key, `trade_id`/`signal_id` hold the same kind
    of identifier as `trade_monitoring_layer.paper_trading.paper_trade.PaperTrade`/`SignalSchema`
    by convention, never enforced structurally (same posture
    `audit_log`'s own `actor` column already established). Append-only
    by design, same "history must never be lost" rule
    `emergency_states`'s own docstring states: this repository exposes
    no update/delete method.
    """
    query = """
    CREATE TABLE IF NOT EXISTS learning_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        record_id TEXT UNIQUE NOT NULL,
        trade_id TEXT NOT NULL,
        signal_id TEXT NOT NULL,
        strategy_name TEXT,
        market_phase TEXT,
        session TEXT,
        timeframe TEXT,
        result TEXT,
        r_multiple REAL,
        failure_type TEXT,
        success_pattern TEXT,
        htf_bias TEXT,
        volatility_state TEXT,
        fundamental_bias TEXT,
        confidence_score REAL,
        engine_version TEXT,
        sample_size INTEGER,
        created_at TEXT NOT NULL
    );
    """
    try:
        connection.execute(query)
        connection.commit()
        logger.info("Database schema (learning_records table) initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize learning_records schema: {e}")
        raise

    _create_learning_records_indexes(connection)
    _migrate_learning_records_schema(connection)


def _migrate_learning_records_schema(connection: sqlite3.Connection):
    """
    Adds the Phase 60.7 columns (`htf_bias`/`volatility_state`/
    `fundamental_bias`/`confidence_score`/`engine_version`/
    `sample_size`) to a `learning_records` table created before this
    phase. SQLite has no "ADD COLUMN IF NOT EXISTS", so each column's
    presence is checked via PRAGMA table_info first -- on a fresh
    table (already created with all columns above) every column is
    already present and this is a no-op. Every new column is
    `NULL`-default -- purely additive, no existing row's meaning
    changes.
    """
    new_columns = [
        ("htf_bias", "TEXT"),
        ("volatility_state", "TEXT"),
        ("fundamental_bias", "TEXT"),
        ("confidence_score", "REAL"),
        ("engine_version", "TEXT"),
        ("sample_size", "INTEGER"),
    ]

    try:
        cursor = connection.execute("PRAGMA table_info(learning_records)")
        existing_columns = {row[1] for row in cursor.fetchall()}
    except sqlite3.Error as e:
        logger.error(f"Failed to inspect learning_records table for migration: {e}")
        raise

    migrated = False
    for column_name, column_def in new_columns:
        if column_name in existing_columns:
            continue
        try:
            connection.execute(f"ALTER TABLE learning_records ADD COLUMN {column_name} {column_def}")
            logger.info(f"Migrated learning_records table: added column '{column_name}'.")
            migrated = True
        except sqlite3.Error as e:
            logger.error(f"Failed to add column '{column_name}' to learning_records table: {e}")
            raise

    if migrated:
        connection.commit()


def _create_learning_records_indexes(connection: sqlite3.Connection):
    """strategy_name/session are the group-by dimensions learning.pattern_detector.detect_patterns() uses; trade_id is the lookup pattern for a single trade's record."""
    statements = [
        "CREATE INDEX IF NOT EXISTS idx_learning_records_strategy_name ON learning_records(strategy_name)",
        "CREATE INDEX IF NOT EXISTS idx_learning_records_session ON learning_records(session)",
        "CREATE INDEX IF NOT EXISTS idx_learning_records_trade_id ON learning_records(trade_id)",
    ]
    try:
        for statement in statements:
            connection.execute(statement)
        connection.commit()
    except sqlite3.Error as e:
        logger.error(f"Failed to create learning_records indexes: {e}")


def init_monitoring_schema(connection: sqlite3.Connection):
    """
    Defines and creates the monitoring_error_events,
    monitoring_decision_pipeline, and monitoring_process_starts table
    schemas (GoldBot Core Owner Monitoring Alpha, TASK 9; the third
    table and the `stage_durations_ms` column added by Phase B.0 --
    see `docs/PHASE_B0_AUDIT.md`). All independent of every other
    table -- no foreign key. All append-only, same "history must never
    be lost" posture as `init_emergency_state_schema()`. SystemHealth/
    MarketHealth/SignalHealth are computed live, never persisted --
    see `docs/PHASE_CORE_MONITORING_AUDIT.md`'s TASK 9 conclusion for
    why. `monitoring_process_starts` is the one fact Phase B.0 adds
    that cannot be computed live -- a restart count only exists across
    process lifetimes.
    """
    query = """
    CREATE TABLE IF NOT EXISTS monitoring_error_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        module TEXT NOT NULL,
        error_type TEXT NOT NULL,
        message TEXT NOT NULL,
        severity TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS monitoring_decision_pipeline (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        timeframe TEXT NOT NULL,
        criteria_met TEXT NOT NULL,
        criteria_total INTEGER NOT NULL,
        decision TEXT NOT NULL,
        reason TEXT,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS monitoring_process_starts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL
    );
    """
    try:
        connection.executescript(query)
        connection.commit()
        logger.info(
            "Database schema (monitoring_error_events, monitoring_decision_pipeline, "
            "monitoring_process_starts tables) initialized successfully."
        )
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize monitoring schema: {e}")
        raise

    _migrate_monitoring_decision_pipeline_stage_durations(connection)


def _migrate_monitoring_decision_pipeline_stage_durations(connection: sqlite3.Connection):
    """
    Phase B.0 TASK 5: guarded `ALTER TABLE ADD COLUMN` for
    `stage_durations_ms` on a table that may already exist from the
    prior phase without this column -- mirrors `database_layer/database_manager/models.py`'s
    own established migration pattern (see `_migrate_signals_table()`
    and its sibling migrations). A no-op when the column is already
    present.
    """
    try:
        cursor = connection.execute("PRAGMA table_info(monitoring_decision_pipeline)")
        existing_columns = {row[1] for row in cursor.fetchall()}
    except sqlite3.Error as e:
        logger.error(f"Failed to inspect monitoring_decision_pipeline table for migration: {e}")
        raise

    if "stage_durations_ms" in existing_columns:
        return

    try:
        connection.execute(
            "ALTER TABLE monitoring_decision_pipeline ADD COLUMN stage_durations_ms TEXT DEFAULT ''"
        )
        connection.commit()
        logger.info("Migrated monitoring_decision_pipeline table: added column 'stage_durations_ms'.")
    except sqlite3.Error as e:
        logger.error(f"Failed to add column 'stage_durations_ms' to monitoring_decision_pipeline table: {e}")
        raise


def init_risk_schema(connection: sqlite3.Connection):
    """
    Defines and creates the risk_decisions and risk_account_state
    table schemas (Phase V1.0.1: Risk Management Hardening Patch,
    TASK 8/10 -- see docs/PHASE_V1_0_1_RISK_AUDIT.md's TASK 4/10
    sections for why neither table could reuse an existing one). Both
    independent of every other table -- no foreign key.

    risk_decisions: append-only (same "history must never be lost"
    posture as init_emergency_state_schema()) -- one row per
    RiskManager.evaluate() call, whatever the outcome.

    risk_account_state: one row per symbol, upserted (same
    one-row-per-name convention as init_runtime_feature_schema()) --
    holds the drawdown baseline (starting_equity/current_equity) and
    the daily-loss baseline (daily_start_balance/daily_date) together,
    since both are small, related, per-symbol account-state facts
    read/written by risk.account_state_tracker.AccountStateTracker.
    """
    query = """
    CREATE TABLE IF NOT EXISTS risk_decisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        strategy_name TEXT,
        direction TEXT,
        risk_percent REAL,
        risk_reward REAL,
        drawdown_percent REAL,
        decision TEXT NOT NULL,
        reason TEXT NOT NULL,
        reject_category TEXT,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS risk_account_state (
        symbol TEXT PRIMARY KEY,
        starting_equity REAL,
        current_equity REAL,
        drawdown_status TEXT NOT NULL DEFAULT 'NORMAL',
        daily_start_balance REAL,
        daily_date TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    """
    try:
        connection.executescript(query)
        connection.commit()
        logger.info("Database schema (risk_decisions, risk_account_state tables) initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize risk schema: {e}")
        raise
