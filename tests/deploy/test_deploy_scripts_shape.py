"""
Phase P1 (Production Deployment Pipeline Foundation), TASK 3/4/5/9/10/12
-- shape/safety tests for scripts/deploy/release_deploy.sh and
scripts/deploy/rollback.sh.

These are real bash scripts meant to run on the VPS via SSH -- this
sandbox has no VPS, systemd, or real /opt/goldbot layout to execute
them end-to-end against, so these tests verify syntax validity
(`bash -n`) and the textual presence/absence of the safety properties
the brief's RULEs require (never overwrite shared resources, never
rebuild on rollback, never touch `current` on a failed smoke test),
matching this repository's existing convention for testing shell
artifacts it cannot fully execute in CI (see
scripts/notify_failure.sh, which has no direct test file either but
is exercised only via its systemd OnFailure= wiring).
"""

import pathlib
import subprocess


def _script_path(name):
    return pathlib.Path(__file__).resolve().parents[2] / "scripts" / "deploy" / name


def _script_text(name):
    return _script_path(name).read_text()


def _bash_syntax_ok(name):
    result = subprocess.run(
        ["bash", "-n", str(_script_path(name))],
        capture_output=True, text=True,
    )
    return result.returncode == 0, result.stderr


# ---------------------------------------------------------------------------
# release_deploy.sh
# ---------------------------------------------------------------------------

def test_release_deploy_script_exists():
    assert _script_path("release_deploy.sh").exists()


def test_release_deploy_script_is_executable():
    assert _script_path("release_deploy.sh").stat().st_mode & 0o111


def test_release_deploy_script_syntax_is_valid():
    ok, stderr = _bash_syntax_ok("release_deploy.sh")
    assert ok, stderr


def test_release_deploy_script_uses_strict_mode():
    text = _script_text("release_deploy.sh")
    assert "set -euo pipefail" in text


def test_release_deploy_script_requires_deploy_path_and_release_id():
    text = _script_text("release_deploy.sh")
    assert ':?usage:' in text


def test_release_deploy_script_defaults_service_name_to_goldbot():
    text = _script_text("release_deploy.sh")
    assert 'SERVICE_NAME="${3:-goldbot}"' in text


def test_release_deploy_script_fails_when_release_dir_missing():
    text = _script_text("release_deploy.sh")
    assert '! -d "$RELEASE_DIR"' in text
    assert "exit 1" in text


def test_release_deploy_script_fails_when_shared_env_missing():
    text = _script_text("release_deploy.sh")
    assert 'shared/.env' in text
    assert '! -f "$DEPLOY_PATH/shared/.env"' in text


def test_release_deploy_script_never_overwrites_env_symlink_target():
    """
    ln -sfn only ever recreates the symlink itself, never writes
    through it into shared/.env's contents -- RULE 4 (never
    overwrite .env).
    """
    text = _script_text("release_deploy.sh")
    assert 'ln -sfn "$DEPLOY_PATH/shared/.env"' in text


def test_release_deploy_script_symlinks_database_from_shared():
    text = _script_text("release_deploy.sh")
    assert 'ln -sfn "$DEPLOY_PATH/shared/database"' in text


def test_release_deploy_script_symlinks_logs_from_shared():
    text = _script_text("release_deploy.sh")
    assert 'ln -sfn "$DEPLOY_PATH/shared/logs"' in text


def test_release_deploy_script_creates_venv_per_release():
    text = _script_text("release_deploy.sh")
    assert 'python3.11 -m venv "$RELEASE_DIR/venv"' in text


def test_release_deploy_script_installs_requirements():
    text = _script_text("release_deploy.sh")
    assert "pip" in text
    assert "requirements.txt" in text


def test_release_deploy_script_runs_smoke_test_before_activation():
    text = _script_text("release_deploy.sh")
    smoke_idx = text.index("health_check.py")
    activate_idx = text.index("activate")
    assert smoke_idx < activate_idx


def test_release_deploy_script_aborts_without_switching_current_on_failed_smoke_test():
    text = _script_text("release_deploy.sh")
    section = text.split("Running pre-activation smoke test", 1)[1].split("PREVIOUS_RELEASE", 1)[0]
    assert "exit 1" in section
    assert "activate" not in section


def test_release_deploy_script_captures_previous_release_before_activating():
    text = _script_text("release_deploy.sh")
    previous_idx = text.index('"$MANAGER" previous')
    activate_idx = text.index('"$MANAGER" activate')
    assert previous_idx < activate_idx


def test_release_deploy_script_restarts_service_via_systemctl():
    text = _script_text("release_deploy.sh")
    assert 'sudo systemctl restart "${SERVICE_NAME}.service"' in text


def test_release_deploy_script_checks_service_is_active_after_restart():
    text = _script_text("release_deploy.sh")
    assert "systemctl is-active" in text


def test_release_deploy_script_rolls_back_automatically_on_post_restart_failure():
    text = _script_text("release_deploy.sh")
    assert "rollback.sh" in text
    assert "PREVIOUS_RELEASE" in text


def test_release_deploy_script_exits_non_zero_after_auto_rollback():
    """A deploy that had to auto-rollback must still be visibly a failed workflow run."""
    text = _script_text("release_deploy.sh")
    rollback_section = text.split('echo "[deploy] FAILED: post-restart health check', 1)[1]
    assert "exit 1" in rollback_section


def test_release_deploy_script_delegates_release_selection_to_release_manager():
    text = _script_text("release_deploy.sh")
    assert "release_manager.py" in text


def test_release_deploy_script_never_deletes_a_release_directory():
    text = _script_text("release_deploy.sh")
    assert "rm -rf" not in text
    assert "rm -f" not in text


def test_release_deploy_script_never_contains_a_plaintext_looking_secret():
    text = _script_text("release_deploy.sh")
    lowered = text.lower()
    for marker in ["bot_token=1", "api_key=sk-", "password="]:
        assert marker not in lowered


# ---------------------------------------------------------------------------
# rollback.sh
# ---------------------------------------------------------------------------

def test_rollback_script_exists():
    assert _script_path("rollback.sh").exists()


def test_rollback_script_is_executable():
    assert _script_path("rollback.sh").stat().st_mode & 0o111


def test_rollback_script_syntax_is_valid():
    ok, stderr = _bash_syntax_ok("rollback.sh")
    assert ok, stderr


def test_rollback_script_uses_strict_mode():
    text = _script_text("rollback.sh")
    assert "set -euo pipefail" in text


def test_rollback_script_accepts_an_explicit_target_release():
    text = _script_text("rollback.sh")
    assert "TARGET_RELEASE" in text


def test_rollback_script_defaults_to_previous_release_when_no_target_given():
    text = _script_text("rollback.sh")
    assert '"$MANAGER" previous "$DEPLOY_PATH"' in text


def test_rollback_script_fails_loudly_when_no_target_available():
    text = _script_text("rollback.sh")
    assert 'no previous release available' in text
    assert "exit 1" in text


def test_rollback_script_never_rebuilds_a_release():
    """RULE 5: rollback must only switch `current`, no rebuild -- no venv creation, no dependency install."""
    text = _script_text("rollback.sh")
    assert "pip install" not in text
    assert "-m venv" not in text


def test_rollback_script_never_deletes_release_directories():
    text = _script_text("rollback.sh")
    assert "rm -rf" not in text
    assert "rm -f" not in text


def test_rollback_script_activates_via_release_manager():
    text = _script_text("rollback.sh")
    assert '"$MANAGER" activate "$DEPLOY_PATH" "$TARGET_RELEASE"' in text


def test_rollback_script_restarts_service_via_systemctl():
    text = _script_text("rollback.sh")
    assert 'sudo systemctl restart "${SERVICE_NAME}.service"' in text


def test_rollback_script_verifies_service_active_after_restart():
    text = _script_text("rollback.sh")
    assert "systemctl is-active" in text


def test_rollback_script_falls_back_to_locating_release_manager_when_current_broken():
    text = _script_text("rollback.sh")
    assert "find" in text
    assert "release_manager.py" in text


def test_rollback_script_defaults_service_name_to_goldbot():
    text = _script_text("rollback.sh")
    assert 'SERVICE_NAME="${2:-goldbot}"' in text
