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
import sys


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


def test_release_deploy_script_symlinks_database_file_from_shared():
    """
    Only the runtime SQLite file is symlinked from shared/ -- the
    database/ directory itself is the Python package and ships fresh
    with every release (rsync'd, not shared). See
    docs/deployment/PRODUCTION_DEPLOYMENT.md's "package vs. runtime
    data" section for why this distinction matters.
    """
    text = _script_text("release_deploy.sh")
    assert 'ln -sfn "$DEPLOY_PATH/shared/database/goldbot.db" "$RELEASE_DIR/database/goldbot.db"' in text


def test_release_deploy_script_does_not_symlink_the_whole_database_directory():
    """
    Regression guard for the real bug caught on the first VPS deploy:
    symlinking the whole database/ directory over the release's own
    (rsync'd) Python package directory would shadow it, breaking
    `from database.database import Database`.
    """
    text = _script_text("release_deploy.sh")
    assert 'ln -sfn "$DEPLOY_PATH/shared/database" "$RELEASE_DIR/database"' not in text


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


def test_release_deploy_script_loads_shared_env_before_smoke_test():
    """
    Regression guard for the real bug caught on the second VPS deploy
    attempt: core/secrets.py reads only os.getenv() ("No .env file
    usage for production security"), and a bare python subprocess
    invocation never sees shared/.env's contents unless something
    exports them into the shell environment first. goldbot.service's
    EnvironmentFile= handles this for the live service, but the
    pre-activation smoke test runs as a direct subprocess call, not
    through systemd.
    """
    text = _script_text("release_deploy.sh")
    section = text.split("Running pre-activation smoke test", 1)[1].split(
        'if ! "$RELEASE_DIR/venv/bin/python"', 1
    )[0]
    assert "set -a" in section
    assert 'source "$DEPLOY_PATH/shared/.env"' in section
    assert "set +a" in section


def test_release_deploy_script_loads_shared_env_before_post_restart_health_check():
    """Same gap, same fix, for the post-restart health check (also a bare subprocess call, not via systemd)."""
    text = _script_text("release_deploy.sh")
    section = text.split("HEALTH_OK=1", 1)[1].split(
        'if ! "$DEPLOY_PATH/current/venv/bin/python"', 1
    )[0]
    assert "set -a" in section
    assert 'source "$DEPLOY_PATH/shared/.env"' in section
    assert "set +a" in section


def test_release_deploy_script_env_sourcing_makes_secrets_visible_to_python(tmp_path):
    """
    Verifies the *effect* of the fix, not just its textual presence:
    runs the exact set -a / source / set +a snippet from
    release_deploy.sh against a real fake .env file and confirms a
    Python subprocess actually sees the variable.
    """
    import subprocess as sp

    shared_dir = tmp_path / "goldbot" / "shared"
    shared_dir.mkdir(parents=True)
    (shared_dir / ".env").write_text("TELEGRAM_BOT_TOKEN=fake-token-value\n")

    script = (
        "set -a\n"
        f'source "{shared_dir}/.env"\n'
        "set +a\n"
        "python3 -c \"import os, sys; "
        "sys.exit(0 if os.environ.get('TELEGRAM_BOT_TOKEN') == 'fake-token-value' else 1)\"\n"
    )
    result = sp.run(["bash", "-c", script], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


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
# Simulated deploy: rsync-exclude + shared-resource-symlink flow, run for
# real against this repository's actual database/ package (no VPS/systemd
# needed -- reproduces the exact bug caught on the first real VPS deploy:
# excluding the bare 'database' directory silently dropped the Python
# package, breaking every `from database...` import).
# ---------------------------------------------------------------------------

def _repo_root():
    return pathlib.Path(__file__).resolve().parents[2]


def _rsync_exclude_patterns():
    """All --exclude='...' patterns from production_deploy.yml's rsync step, in order."""
    workflow_text = (_repo_root() / ".github" / "workflows" / "production_deploy.yml").read_text()
    rsync_section = workflow_text.split("rsync -az", 1)[1].split("Activate release", 1)[0]
    patterns = []
    for line in rsync_section.splitlines():
        stripped = line.strip().rstrip("\\").strip()
        if stripped.startswith("--exclude="):
            patterns.append(stripped.split("--exclude='")[1].rsplit("'", 1)[0])
    assert patterns, "expected at least one --exclude pattern in production_deploy.yml"
    return patterns


def test_simulated_deploy_ships_the_database_package_and_preserves_shared_db(tmp_path):
    """
    Simulates the real deploy flow (rsync excludes -> shared-resource
    symlink) using this repository's *entire* real tree, without
    needing a VPS: (1) copy the repo into a fake release directory,
    skipping exactly what production_deploy.yml's rsync excludes; (2)
    symlink the shared runtime .db file in exactly as
    release_deploy.sh does; (3) confirm `database.database` -- which
    itself imports core_layer.logger.logger and config, so a database/-only copy
    would give a false signal -- still imports cleanly, and the shared
    file's contents are reached through the symlink, not overwritten.

    This reproduces the exact bug caught on the first real VPS deploy:
    excluding the bare 'database' directory silently dropped the
    Python package, breaking every `from database...` import.
    """
    import fnmatch
    import shutil
    import subprocess as sp

    patterns = _rsync_exclude_patterns()
    repo_root = _repo_root()

    deploy_path = tmp_path / "goldbot"
    shared_database_dir = deploy_path / "shared" / "database"
    shared_database_dir.mkdir(parents=True)
    shared_db = shared_database_dir / "goldbot.db"
    shared_db.write_bytes(b"SQLITE_SHARED_CONTENT")

    release_dir = deploy_path / "releases" / "20260101000000"

    def _excluded(name, rel_posix):
        for p in patterns:
            # rsync matches a pattern with no '/' against the basename at
            # any depth; a pattern containing '/' is matched against the
            # path relative to the transfer root.
            target = rel_posix if "/" in p else name
            if fnmatch.fnmatch(target, p):
                return True
        return False

    def _ignore(dirpath, names):
        rel_dir = pathlib.Path(dirpath).relative_to(repo_root).as_posix()
        skip = []
        for name in names:
            rel = name if rel_dir == "." else f"{rel_dir}/{name}"
            if _excluded(name, rel):
                skip.append(name)
        return skip

    shutil.copytree(repo_root, release_dir, ignore=_ignore, symlinks=False)

    assert (release_dir / "database" / "database.py").exists(), (
        "database/database.py must ship with the release -- the exclude "
        "pattern must not drop the Python package"
    )
    assert not (release_dir / "database" / "goldbot.db").exists(), (
        "the runtime .db file must be excluded by rsync, not copied"
    )

    # Reproduce release_deploy.sh's symlink step exactly.
    (release_dir / "database" / "goldbot.db").symlink_to(shared_db)

    result = sp.run(
        [sys.executable, "-c", "from database.database import Database; print('OK')"],
        cwd=str(release_dir),
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "OK" in result.stdout

    # The runtime file is reached through the symlink, not copied --
    # writing to the "shared" file is visible through the release path.
    assert (release_dir / "database" / "goldbot.db").read_bytes() == b"SQLITE_SHARED_CONTENT"
    shared_db.write_bytes(b"UPDATED_BY_A_LATER_RELEASE")
    assert (release_dir / "database" / "goldbot.db").read_bytes() == b"UPDATED_BY_A_LATER_RELEASE"


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
