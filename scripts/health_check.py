#!/usr/bin/env python3
"""
scripts/health_check.py -- production health check (Phase 58; two
import checks added by Phase P1, Production Deployment Pipeline
Foundation, TASK 8/9).

Standalone, ops-facing script. Not part of the trading pipeline or
Telegram layer -- not imported by core/pipeline.py, main.py,
telegram/polling.py, or any application module. Meant to be run from
systemd/cron on a VPS (see deploy/systemd/goldbot-healthcheck.timer
and docs/production_setup.md) to verify the deployment is alive:
config loads, the database is reachable, the required secrets are
present, and the two entry-point modules (`main`/`telegram.polling`)
import cleanly. Never prints a secret's value, only whether it is
present. Never executes either entry point -- only imports the
module, so this stays a static "does it start" check, never a real
pipeline cycle or a real polling session.

Phase P1 reuses this exact script for two distinct purposes rather
than adding a separate one (Module Reuse Principle): as the
pre-activation smoke test (TASK 9, run against a new release before
`current` is switched to it) and as the post-restart health check
(TASK 8, run against the live `current` release after
`goldbot.service` restarts) -- see scripts/deploy/release_deploy.sh.

Exit code 0 -- all checks passed.
Exit code 1 -- one or more checks failed (detail on stderr).
"""

import importlib
import os
import sys

# Running as `python scripts/health_check.py` puts only scripts/ on
# sys.path, not the repository root -- add it explicitly so `config`,
# `core`, and `database` (all repo-root packages) are importable
# regardless of the caller's cwd (systemd sets WorkingDirectory, but a
# manual `python scripts/health_check.py` from elsewhere would not).
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def check_config():
    try:
        from config import Config
        _ = Config.DB_PATH
        return True, "config: OK"
    except Exception as e:
        return False, f"config: FAILED ({e})"


def check_secrets():
    from core_layer.secrets import Secrets

    required = ["TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID", "TWELVE_DATA_API_KEY"]
    secrets = Secrets()
    missing = []
    for name in required:
        try:
            getattr(secrets, name)
        except Exception:
            missing.append(name)
    if missing:
        return False, f"secrets: MISSING {', '.join(missing)}"
    return True, "secrets: OK"


def check_database():
    from database_layer.database_manager.database import Database

    try:
        with Database() as conn:
            conn.execute("SELECT 1").fetchone()
        return True, "database: OK"
    except Exception as e:
        return False, f"database: FAILED ({e})"


def check_main_imports():
    try:
        importlib.import_module("core_layer.pipeline")
        return True, "main: OK"
    except Exception as e:
        return False, f"main: FAILED ({e})"


def check_telegram_imports():
    try:
        importlib.import_module("telegram.polling")
        return True, "telegram: OK"
    except Exception as e:
        return False, f"telegram: FAILED ({e})"


def main() -> int:
    checks = [
        check_config(),
        check_secrets(),
        check_database(),
        check_main_imports(),
        check_telegram_imports(),
    ]
    healthy = all(ok for ok, _ in checks)
    for ok, message in checks:
        print(message, file=sys.stdout if ok else sys.stderr)
    return 0 if healthy else 1


if __name__ == "__main__":
    sys.exit(main())
