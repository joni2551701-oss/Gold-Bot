#!/usr/bin/env bash
set -euo pipefail

# scripts/deploy/release_deploy.sh -- Phase P1 (Production Deployment
# Pipeline Foundation).
#
# Runs on the VPS (invoked over SSH by
# .github/workflows/production_deploy.yml) after the new release's
# files have already been rsynced into
# $DEPLOY_PATH/releases/$RELEASE_ID/. Activates the release only if
# venv install + the pre-activation smoke test both succeed; on any
# failure it leaves `current` and the running service untouched (a
# broken release never goes live). If the *post*-restart health check
# fails, it automatically rolls back to the previous release via
# rollback.sh and exits non-zero so the workflow run is visibly
# marked failed even though the live service recovered.
#
# All release-selection logic (which release is current/previous,
# atomically switching `current`) lives in release_manager.py, not
# here -- this script only does what genuinely needs a shell: venv
# creation, symlinking shared resources, and systemctl.

DEPLOY_PATH="${1:?usage: release_deploy.sh <deploy_path> <release_id> [service_name]}"
RELEASE_ID="${2:?usage: release_deploy.sh <deploy_path> <release_id> [service_name]}"
SERVICE_NAME="${3:-goldbot}"

RELEASE_DIR="$DEPLOY_PATH/releases/$RELEASE_ID"
MANAGER="$RELEASE_DIR/scripts/deploy/release_manager.py"

echo "[deploy] Activating release $RELEASE_ID at $RELEASE_DIR"

if [[ ! -d "$RELEASE_DIR" ]]; then
    echo "[deploy] FAILED: release directory not found: $RELEASE_DIR" >&2
    exit 1
fi

mkdir -p "$DEPLOY_PATH/shared/database" "$DEPLOY_PATH/shared/logs" "$DEPLOY_PATH/backups"

if [[ ! -f "$DEPLOY_PATH/shared/.env" ]]; then
    echo "[deploy] FAILED: $DEPLOY_PATH/shared/.env does not exist." >&2
    echo "[deploy] Create it once, manually, with real secret values before the first deploy." >&2
    echo "[deploy] See docs/deployment/PRODUCTION_DEPLOYMENT.md." >&2
    exit 1
fi

echo "[deploy] Creating virtualenv"
python3.11 -m venv "$RELEASE_DIR/venv"
"$RELEASE_DIR/venv/bin/pip" install --quiet --upgrade pip
"$RELEASE_DIR/venv/bin/pip" install --quiet -r "$RELEASE_DIR/requirements.txt"

echo "[deploy] Linking shared resources (never overwritten, always reused)"
ln -sfn "$DEPLOY_PATH/shared/.env" "$RELEASE_DIR/.env"
ln -sfn "$DEPLOY_PATH/shared/database" "$RELEASE_DIR/database"
ln -sfn "$DEPLOY_PATH/shared/logs" "$RELEASE_DIR/logs"

echo "[deploy] Running pre-activation smoke test (startup verification only, no continuous execution)"
if ! "$RELEASE_DIR/venv/bin/python" "$RELEASE_DIR/scripts/health_check.py"; then
    echo "[deploy] FAILED: smoke test failed for release $RELEASE_ID." >&2
    echo "[deploy] current release left untouched, $SERVICE_NAME.service not restarted." >&2
    exit 1
fi

PREVIOUS_RELEASE="$(python3 "$MANAGER" previous "$DEPLOY_PATH" || true)"

echo "[deploy] Smoke test passed -- switching current -> $RELEASE_ID"
python3 "$MANAGER" activate "$DEPLOY_PATH" "$RELEASE_ID"

echo "[deploy] Restarting $SERVICE_NAME.service"
sudo systemctl restart "${SERVICE_NAME}.service"
sleep 2

HEALTH_OK=1
if ! systemctl is-active --quiet "${SERVICE_NAME}.service"; then
    HEALTH_OK=0
elif ! "$DEPLOY_PATH/current/venv/bin/python" "$DEPLOY_PATH/current/scripts/health_check.py"; then
    HEALTH_OK=0
fi

if [[ "$HEALTH_OK" -eq 0 ]]; then
    echo "[deploy] FAILED: post-restart health check failed for release $RELEASE_ID." >&2
    if [[ -n "$PREVIOUS_RELEASE" ]]; then
        echo "[deploy] Rolling back to previous release $PREVIOUS_RELEASE" >&2
        "$RELEASE_DIR/scripts/deploy/rollback.sh" "$DEPLOY_PATH" "$SERVICE_NAME" "$PREVIOUS_RELEASE" || true
    else
        echo "[deploy] No previous release available to roll back to -- manual intervention required." >&2
    fi
    exit 1
fi

echo "[deploy] Release $RELEASE_ID is live and healthy."
