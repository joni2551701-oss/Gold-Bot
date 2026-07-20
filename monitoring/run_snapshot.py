"""
Monitoring Layer — Owner Snapshot Reporter entry point (GoldBot Core
Owner Snapshot Reporter Alpha, TASK 6; hardened by the v1.1
Operational Intelligence Upgrade / Audit & Hardening briefs).

Invoked by .github/workflows/owner_snapshot.yml every 15 minutes.
One-shot: verify secrets -> collect -> format -> send -> exit. No
infinite loop -- unlike telegram/polling.py (a long-running listener),
GitHub Actions expects this process to terminate on its own every run.

TASK 7 -- validates presence (never value) of TELEGRAM_BOT_TOKEN,
TELEGRAM_OWNER_ID, TWELVE_DATA_API_KEY, GEMINI_API_KEY before
collecting. TELEGRAM_BOT_TOKEN/TELEGRAM_OWNER_ID are the only two
secrets this reporter actually needs to deliver a message -- their
absence aborts the run with a specific, grep-able reason (so the
workflow's failure is easy to diagnose from Actions' own log output).
TWELVE_DATA_API_KEY/GEMINI_API_KEY are logged for visibility only:
their absence degrades monitoring/snapshot_collector.py's own fields
gracefully (never crashes), matching that module's existing
defensive-read behavior.

Owner failure notification (Audit & Hardening TASK 4): if
collect_snapshot()/format_snapshot() itself raises, the Owner still
gets a short "Snapshot Failed" message (module/error/time) instead of
the run only showing up as red in GitHub Actions -- Actions failures
are not otherwise visible to the Owner in Telegram.
"""

import asyncio
import sys
import time
from dataclasses import replace
from datetime import datetime, timezone

from core.logger import setup_logger
from core.secrets import Secrets
from monitoring.snapshot_collector import collect_snapshot, next_check_time
from telegram.owner.snapshot_formatter import format_snapshot
from telegram.owner.snapshot_sender import send_snapshot

logger = setup_logger("SnapshotReporter")

_REQUIRED_SECRET_NAMES = (
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_OWNER_ID",
    "TWELVE_DATA_API_KEY",
    "GEMINI_API_KEY",
)


def _verify_secrets() -> bool:
    """
    Logs presence/absence (never the value) of every required secret.
    Returns True only if TELEGRAM_BOT_TOKEN and TELEGRAM_OWNER_ID are
    both present -- see this module's own docstring for why the other
    two don't block sending.
    """
    secrets = Secrets()
    presence = {}
    for name in _REQUIRED_SECRET_NAMES:
        try:
            presence[name] = bool(getattr(secrets, name))
        except Exception:
            presence[name] = False
        logger.info(f"{name}: {'present' if presence[name] else 'missing'}")

    if not presence["TELEGRAM_BOT_TOKEN"]:
        logger.error("Snapshot send aborted: Missing TELEGRAM_BOT_TOKEN")
        return False
    if not presence["TELEGRAM_OWNER_ID"]:
        logger.error("Snapshot send aborted: Missing TELEGRAM_OWNER_ID")
        return False
    return True


def _format_failure_message(module: str, error: str) -> str:
    """Audit & Hardening TASK 4's own exact worked format. Never logs a secret -- `error` is str(Exception), which this codebase's own error paths never populate with a secret value."""
    when = datetime.now(timezone.utc).strftime("%H:%M UTC")
    return "\n".join([
        "\U0001F534 GoldBot Snapshot Failed",
        "Module:",
        module,
        "Error:",
        error,
        "Time:",
        when,
    ])


async def _notify_owner_of_failure(module: str, error: str) -> None:
    """Best-effort only: a failure notification that itself fails must never raise -- the run has already failed once."""
    try:
        await send_snapshot(_format_failure_message(module, error))
    except Exception as e:
        logger.error(f"Failure notification itself failed: {e}")


async def run_snapshot_report() -> bool:
    """Returns True if the snapshot was sent successfully, False otherwise. Never raises."""
    if not _verify_secrets():
        return False

    collect_started = time.perf_counter()
    try:
        snapshot = collect_snapshot()
        execution_seconds = round(time.perf_counter() - collect_started, 3)
        # runtime_execution_seconds/runtime_next_check are filled in
        # here (not in collect_snapshot() itself) because the former
        # can only honestly measure collect+format time -- it cannot
        # include the Telegram send that hasn't happened yet, and the
        # message being formatted needs a final value to display.
        snapshot = replace(
            snapshot,
            runtime_execution_seconds=execution_seconds,
            runtime_next_check=next_check_time(),
        )
        message = format_snapshot(snapshot)
    except Exception as e:
        logger.error(f"Snapshot collection/formatting failed: {e}")
        await _notify_owner_of_failure("monitoring.run_snapshot", str(e))
        return False

    result = await send_snapshot(message)
    return result.sent


def main() -> None:
    success = asyncio.run(run_snapshot_report())
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
