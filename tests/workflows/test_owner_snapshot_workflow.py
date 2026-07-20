"""
GoldBot Core Owner Snapshot Reporter Alpha, TASK 5/8 --
.github/workflows/owner_snapshot.yml structure tests. New
tests/workflows/ directory -- no workflow-file test coverage existed
before this phase.

Plain string/line checks against the raw YAML text, not a YAML
parser: PyYAML is not a declared project dependency
(requirements.txt only lists aiogram/requests) and this phase does
not need to add one just to test a single, hand-written workflow
file.
"""

import pathlib


def _workflow_path():
    return pathlib.Path(__file__).resolve().parents[2] / ".github" / "workflows" / "owner_snapshot.yml"


def _workflow_text():
    return _workflow_path().read_text()


def test_owner_snapshot_workflow_file_exists():
    assert _workflow_path().exists()


def test_owner_snapshot_workflow_has_15_minute_cron():
    assert 'cron: "*/15 * * * *"' in _workflow_text()


def test_owner_snapshot_workflow_supports_manual_dispatch():
    assert "workflow_dispatch:" in _workflow_text()


def test_owner_snapshot_workflow_has_a_schedule_trigger():
    assert "schedule:" in _workflow_text()


def test_owner_snapshot_workflow_has_a_job():
    assert "jobs:" in _workflow_text()
    assert "runs-on: ubuntu-latest" in _workflow_text()


def test_owner_snapshot_workflow_checks_out_production_branch():
    content = _workflow_text()
    assert "actions/checkout@v4" in content
    assert "ref: claude/code-analysis-optimization-pwfo3q" in content


def test_owner_snapshot_workflow_installs_requirements():
    assert "pip install -r requirements.txt" in _workflow_text()


def test_owner_snapshot_workflow_invokes_run_snapshot_entry_point():
    assert "python -m monitoring.run_snapshot" in _workflow_text()


def test_owner_snapshot_workflow_passes_required_secrets():
    content = _workflow_text()
    for name in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_OWNER_ID", "TWELVE_DATA_API_KEY", "GEMINI_API_KEY"):
        assert f"{name}: ${{{{ secrets.{name} }}}}" in content, name


def test_owner_snapshot_workflow_never_hardcodes_a_secret_value():
    content = _workflow_text()
    for line in content.splitlines():
        if "TELEGRAM_BOT_TOKEN:" in line or "TELEGRAM_OWNER_ID:" in line:
            assert "secrets." in line


def test_owner_snapshot_workflow_has_its_own_concurrency_group_not_shared_with_trading_pipeline():
    content = _workflow_text()
    assert "group: goldbot-owner-snapshot" in content
    assert "group: goldbot\n" not in content


def test_owner_snapshot_workflow_uses_python_311():
    assert 'python-version: "3.11"' in _workflow_text()


def test_run_snapshot_entry_point_module_exists():
    import monitoring.run_snapshot as run_snapshot_module

    assert run_snapshot_module is not None


def test_run_snapshot_entry_point_has_main_function():
    import monitoring.run_snapshot as run_snapshot_module

    assert callable(run_snapshot_module.main)


def test_trading_bot_workflow_still_present_and_unaffected():
    """Belt-and-suspenders: adding this workflow must not disturb the existing one."""
    trading_bot_path = _workflow_path().parent / "trading_bot.yml"
    assert trading_bot_path.exists()
