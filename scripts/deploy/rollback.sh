#!/usr/bin/env bash
set -euo pipefail

# scripts/deploy/rollback.sh -- Phase P1 (Production Deployment
# Pipeline Foundation), TASK 10.
#
# Switches `current` back to the previous release (or an explicitly
# given target) and restarts the service. Never rebuilds anything and
# never touches releases/ contents -- the target release's venv is
# already installed from when it was originally deployed, so this is
# just a symlink switch + restart. Called automatically by
# release_deploy.sh on a failed post-restart health check, and usable
# standalone for a manual rollback:
#
#   scripts/deploy/rollback.sh /opt/goldbot goldbot
#   scripts/deploy/rollback.sh /opt/goldbot goldbot 20260721101500  # explicit target

DEPLOY_PATH="${1:?usage: rollback.sh <deploy_path> [service_name] [target_release_id]}"
SERVICE_NAME="${2:-goldbot}"
TARGET_RELEASE="${3:-}"

MANAGER="$DEPLOY_PATH/current/scripts/deploy/release_manager.py"
if [[ ! -f "$MANAGER" ]]; then
    # `current` may already be broken/missing -- fall back to the
    # newest release's own copy of the module, which is identical
    # logic regardless of which release ships it.
    MANAGER="$(find "$DEPLOY_PATH/releases" -maxdepth 4 -path '*/scripts/deploy/release_manager.py' 2>/dev/null | sort | tail -n1)"
fi

if [[ -z "$MANAGER" ]]; then
    echo "[rollback] FAILED: could not locate release_manager.py in any release." >&2
    exit 1
fi

if [[ -z "$TARGET_RELEASE" ]]; then
    TARGET_RELEASE="$(python3 "$MANAGER" previous "$DEPLOY_PATH")"
fi

if [[ -z "$TARGET_RELEASE" ]]; then
    echo "[rollback] FAILED: no previous release available to roll back to." >&2
    exit 1
fi

echo "[rollback] Switching current -> $TARGET_RELEASE"
python3 "$MANAGER" activate "$DEPLOY_PATH" "$TARGET_RELEASE"

echo "[rollback] Restarting $SERVICE_NAME.service"
sudo systemctl restart "${SERVICE_NAME}.service"
sleep 2

if ! systemctl is-active --quiet "${SERVICE_NAME}.service"; then
    echo "[rollback] WARNING: $SERVICE_NAME.service is not active after rollback restart." >&2
    exit 1
fi

echo "[rollback] Rolled back to release $TARGET_RELEASE and service is active."
