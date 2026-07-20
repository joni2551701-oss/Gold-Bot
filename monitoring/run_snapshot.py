"""
Monitoring Layer — Owner Snapshot Reporter entry point (GoldBot Core
Owner Snapshot Reporter Alpha, TASK 6).

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
"""

import asyncio
import sys

from core.logger import setup_logger
from core.secrets import Secrets
from monitoring.snapshot_collector import collect_snapshot
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


async def run_snapshot_report() -> bool:
    """Returns True if the snapshot was sent successfully, False otherwise. Never raises."""
    if not _verify_secrets():
        return False

    try:
        snapshot = collect_snapshot()
        message = format_snapshot(snapshot)
    except Exception as e:
        logger.error(f"Snapshot collection/formatting failed: {e}")
        return False

    result = await send_snapshot(message)
    return result.sent


def main() -> None:
    success = asyncio.run(run_snapshot_report())
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
