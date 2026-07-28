"""
Phase P1 (Production Deployment Pipeline Foundation), TASK 1/2/12 --
.github/workflows/production_deploy.yml structure tests.

Plain string/line checks against the raw YAML text, not a YAML
parser: PyYAML is not a declared project dependency
(requirements.txt only lists aiogram/requests) and this phase does
not add one just to test a single, hand-written workflow file.
"""

import pathlib


def _workflow_path():
    return (
        pathlib.Path(__file__).resolve().parents[2]
        / ".github" / "workflows" / "production_deploy.yml"
    )


def _workflow_text():
    return _workflow_path().read_text()


def test_workflow_file_exists():
    assert _workflow_path().exists()


def test_workflow_has_a_name():
    assert "name: GoldBot Production Deployment" in _workflow_text()


def test_workflow_triggers_on_push_to_production_branch():
    text = _workflow_text()
    assert "on:" in text
    assert "push:" in text
    # TASK-CICD-001: main is the single production branch -- the
    # automatic push trigger deploys main.
    assert "- main" in text


def test_workflow_does_not_trigger_on_stale_development_branch():
    """
    TASK-CICD-001 (CI/CD migration to main): main is now the sole
    production branch, so the trigger branch list must contain `- main`
    and must NOT still name the old development branch
    (claude/code-analysis-optimization-pwfo3q). This is the inverse of
    the original Phase P1 contract, which is intentionally superseded.
    """
    text = _workflow_text()
    # Isolate the real `on:` trigger block (a top-level key, so it
    # starts at column 0) rather than the first "branches:" substring,
    # which can also appear inside the header comment.
    on_block = text.split("\non:", 1)[1].split("\njobs:", 1)[0]
    branches_section = on_block.split("branches:", 1)[1].split("workflow_dispatch:", 1)[0]
    assert "- main" in branches_section
    assert "claude/code-analysis-optimization-pwfo3q" not in branches_section


def test_workflow_supports_manual_dispatch():
    assert "workflow_dispatch:" in _workflow_text()


def test_workflow_has_concurrency_group():
    text = _workflow_text()
    assert "concurrency:" in text
    assert "group: production-deploy" in text


def test_workflow_concurrency_does_not_cancel_in_progress_deploys():
    """A deploy that's already running to the VPS must not be cancelled mid-way."""
    assert "cancel-in-progress: false" in _workflow_text()


def test_workflow_has_validate_job():
    assert "validate:" in _workflow_text()


def test_workflow_has_deploy_job():
    assert "deploy:" in _workflow_text()


def test_workflow_deploy_job_needs_validate():
    text = _workflow_text()
    deploy_section = text.split("deploy:", 1)[1]
    assert "needs: validate" in deploy_section


def test_workflow_validate_job_checks_out_repository():
    assert "actions/checkout@v4" in _workflow_text()


def test_workflow_validate_job_sets_up_python_311():
    text = _workflow_text()
    assert "actions/setup-python@v5" in text
    assert 'python-version: "3.11"' in text


def test_workflow_validate_job_installs_dependencies():
    text = _workflow_text()
    assert "pip install -r requirements.txt" in text


def test_workflow_validate_job_lints_with_pyflakes():
    text = _workflow_text()
    assert "pyflakes" in text
    assert "python -m pyflakes" in text


def test_workflow_validate_job_runs_compileall():
    assert "python -m compileall -q ." in _workflow_text()


def test_workflow_validate_job_runs_pytest():
    assert "python -m pytest tests/" in _workflow_text()


def test_workflow_validate_job_order_lint_before_compile_before_tests():
    text = _workflow_text()
    lint_idx = text.index("Lint (pyflakes)")
    compile_idx = text.index("Compile check")
    test_idx = text.index("Run tests")
    assert lint_idx < compile_idx < test_idx


def test_workflow_uses_no_plaintext_vps_credentials():
    """
    Every VPS-facing value must come from secrets.* -- the literal
    words host/user/key must never appear as a hardcoded value (only
    as part of a ${{ secrets.VPS_* }} reference or a comment).
    """
    text = _workflow_text()
    for secret_name in ["VPS_HOST", "VPS_PORT", "VPS_USER", "VPS_SSH_KEY", "DEPLOY_PATH"]:
        assert f"secrets.{secret_name}" in text, f"{secret_name} must be referenced via secrets.*"


def test_workflow_does_not_echo_ssh_key_secret_directly():
    """The raw ssh-private-key value must only be passed to the ssh-agent action input, never echoed."""
    text = _workflow_text()
    for line in text.splitlines():
        if "echo" in line:
            assert "VPS_SSH_KEY" not in line


def test_workflow_installs_ssh_agent_action():
    assert "webfactory/ssh-agent" in _workflow_text()


def test_workflow_adds_vps_to_known_hosts():
    assert "ssh-keyscan" in _workflow_text()
    assert "known_hosts" in _workflow_text()


def test_workflow_computes_a_release_id():
    text = _workflow_text()
    assert "Compute release id" in text
    assert "date -u +%Y%m%d%H%M%S" in text


def test_workflow_release_id_step_has_an_id_for_output_reference():
    text = _workflow_text()
    step_section = text.split("Compute release id", 1)[1].split("Install SSH key", 1)[0]
    assert "id: release" in step_section


def test_workflow_uploads_release_via_rsync():
    assert "rsync -az" in _workflow_text()


def test_workflow_rsync_excludes_env_file():
    text = _workflow_text()
    rsync_section = text.split("rsync -az", 1)[1].split("Activate release", 1)[0]
    assert "--exclude='.env'" in rsync_section


def test_workflow_rsync_excludes_database_file():
    """
    Only the runtime SQLite file is excluded -- the database/ Python
    package (database.py, *_repository.py, etc.) must still ship with
    every release. See docs/deployment/PRODUCTION_DEPLOYMENT.md's
    "package vs. runtime data" section.
    """
    text = _workflow_text()
    rsync_section = text.split("rsync -az", 1)[1].split("Activate release", 1)[0]
    assert "--exclude='database/*.db'" in rsync_section


def test_workflow_rsync_does_not_exclude_the_whole_database_package():
    """
    Regression guard for the real bug caught on the first VPS deploy:
    excluding the bare 'database' directory silently drops the Python
    package, breaking `from database.database import Database`
    everywhere. Only the scoped database/*.db pattern is allowed.
    """
    text = _workflow_text()
    rsync_section = text.split("rsync -az", 1)[1].split("Activate release", 1)[0]
    assert "--exclude='database'" not in rsync_section
    for line in rsync_section.splitlines():
        stripped = line.strip().rstrip("\\").strip()
        if stripped.startswith("--exclude="):
            assert stripped != "--exclude='database'"


def test_workflow_rsync_exclude_pattern_matches_only_db_files_not_package_source():
    """
    Verifies the *effect* of the exclude pattern against this
    repository's real database/ package: real source files must never
    match it, while a runtime .db file must.
    """
    import fnmatch
    import pathlib

    text = _workflow_text()
    rsync_section = text.split("rsync -az", 1)[1].split("Activate release", 1)[0]
    exclude_line = [
        line for line in rsync_section.splitlines() if "--exclude='database" in line
    ][0]
    pattern = exclude_line.split("--exclude='")[1].split("'")[0]

    database_dir = pathlib.Path(__file__).resolve().parents[2] / "database"
    source_files = [p for p in database_dir.rglob("*.py")]
    assert source_files, "expected real .py files under database/ to test against"
    for path in source_files:
        rel = path.relative_to(database_dir.parent).as_posix()
        assert not fnmatch.fnmatch(rel, pattern), (
            f"{rel} must not be excluded by rsync pattern {pattern!r}"
        )

    assert fnmatch.fnmatch("database/goldbot.db", pattern)


def test_workflow_rsync_excludes_logs():
    text = _workflow_text()
    rsync_section = text.split("rsync -az", 1)[1].split("Activate release", 1)[0]
    assert "--exclude='logs'" in rsync_section


def test_workflow_rsync_excludes_venv():
    text = _workflow_text()
    rsync_section = text.split("rsync -az", 1)[1].split("Activate release", 1)[0]
    assert "--exclude='venv'" in rsync_section


def test_workflow_rsync_excludes_git_directory():
    text = _workflow_text()
    rsync_section = text.split("rsync -az", 1)[1].split("Activate release", 1)[0]
    assert "--exclude='.git'" in rsync_section


def test_workflow_activates_release_via_ssh_calling_release_deploy_script():
    text = _workflow_text()
    assert "Activate release" in text
    assert "release_deploy.sh" in text


def test_workflow_deploy_step_passes_release_id_to_deploy_script():
    text = _workflow_text()
    activate_section = text.split("Activate release", 1)[1]
    assert "steps.release.outputs.id" in activate_section


def test_workflow_deploy_step_passes_service_name_goldbot():
    text = _workflow_text()
    activate_section = text.split("Activate release", 1)[1]
    assert "goldbot" in activate_section
