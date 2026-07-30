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

mkdir -p "$DEPLOY_PATH/shared/database" "$DEPLOY_PATH/shared/logs" "$DEPLOY_PATH/shared/data" "$DEPLOY_PATH/backups"

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
# database/ is this repository's Python package (database.py,
# *_repository.py, etc.) -- it ships with every release like any other
# source directory. Only the runtime SQLite file inside it is shared/
# persistent, so only that file is symlinked, not the whole directory.
ln -sfn "$DEPLOY_PATH/shared/database/goldbot.db" "$RELEASE_DIR/database/goldbot.db"
ln -sfn "$DEPLOY_PATH/shared/logs" "$RELEASE_DIR/logs"
# TASK-PROD-001: data/.cache_state.json is SmartDataCache's persisted
# last-price store, written by the trading_bot.yml pipeline run (a
# separate, ephemeral GitHub Actions job) and published to
# shared/data/ by that workflow's "Publish current-price cache to VPS"
# step. Symlinking it here (instead of shipping a release-local copy)
# is what lets goldbot.service's 📈 Current Price button -- which only
# reads this file, never fetches -- see the latest price across
# releases and restarts. If the shared file does not exist yet (first
# deploy before any trading_bot.yml run has published one),
# SmartDataCache's own `os.path.exists` check on load already handles
# a missing/broken path -- an empty state, not a crash.
ln -sfn "$DEPLOY_PATH/shared/data/.cache_state.json" "$RELEASE_DIR/data/.cache_state.json"

echo "[deploy] Running pre-activation smoke test (startup verification only, no continuous execution)"
set -a
source "$DEPLOY_PATH/shared/.env"
set +a
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
else
    set -a
    source "$DEPLOY_PATH/shared/.env"
    set +a
    if ! "$DEPLOY_PATH/current/venv/bin/python" "$DEPLOY_PATH/current/scripts/health_check.py"; then
        HEALTH_OK=0
    fi
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
