#!/usr/bin/env bash
# scripts/notify_failure.sh -- crash/failure alert (Phase 58 monitoring
# foundation).
#
# Invoked by systemd's OnFailure= directive when a GoldBot unit
# (goldbot-polling.service / goldbot-pipeline.service) fails. Sends a
# plain-text alert to the configured TELEGRAM_OWNER_ID via the
# Telegram Bot API directly (curl) -- deliberately outside the Python
# application (telegram/ package) so a Python-level crash cannot also
# take down the alert path.
#
# Requires TELEGRAM_BOT_TOKEN and TELEGRAM_OWNER_ID in the environment
# (same values as .env.production) -- systemd supplies them via
# EnvironmentFile=. See deploy/systemd/goldbot-notify-failure@.service
# and docs/production_setup.md.
#
# Never fails the calling unit: a missing credential or a network
# error is logged to stderr and this script still exits 0, so a
# broken alert path cannot itself cause a restart loop.

set -uo pipefail

UNIT_NAME="${1:-unknown-unit}"

if [[ -z "${TELEGRAM_BOT_TOKEN:-}" || -z "${TELEGRAM_OWNER_ID:-}" ]]; then
    echo "notify_failure.sh: TELEGRAM_BOT_TOKEN or TELEGRAM_OWNER_ID not set, cannot alert." >&2
    exit 0
fi

MESSAGE="GoldBot ALERT: systemd unit '${UNIT_NAME}' failed on $(hostname) at $(date -u +'%Y-%m-%dT%H:%M:%SZ')."

curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -d chat_id="${TELEGRAM_OWNER_ID}" \
    -d text="${MESSAGE}" > /dev/null \
    || echo "notify_failure.sh: failed to reach Telegram API." >&2

exit 0
