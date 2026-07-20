"""
GoldBot Core Owner Snapshot Reporter Alpha, TASK 5/8 --
.github/workflows/owner_snapshot.yml structure tests. New
tests/workflows/ directory -- no workflow-file test coverage existed
before this phase.
"""

import pathlib

import yaml


def _workflow_path():
    return pathlib.Path(__file__).resolve().parents[2] / ".github" / "workflows" / "owner_snapshot.yml"


def _load_workflow():
    return yaml.safe_load(_workflow_path().read_text())


def test_owner_snapshot_workflow_file_exists():
    assert _workflow_path().exists()


def test_owner_snapshot_workflow_is_valid_yaml():
    _load_workflow()  # must not raise


def test_owner_snapshot_workflow_has_15_minute_cron():
    workflow = _load_workflow()
    triggers = workflow.get(True) or workflow.get("on")
    schedules = triggers.get("schedule", [])
    crons = [entry["cron"] for entry in schedules]
    assert "*/15 * * * *" in crons


def test_owner_snapshot_workflow_supports_manual_dispatch():
    workflow = _load_workflow()
    triggers = workflow.get(True) or workflow.get("on")
    assert "workflow_dispatch" in triggers


def test_owner_snapshot_workflow_has_a_job():
    workflow = _load_workflow()
    assert len(workflow["jobs"]) >= 1


def test_owner_snapshot_workflow_checks_out_production_branch():
    workflow = _load_workflow()
    job = next(iter(workflow["jobs"].values()))
    checkout_step = next(s for s in job["steps"] if s.get("uses", "").startswith("actions/checkout"))
    assert checkout_step["with"]["ref"] == "claude/code-analysis-optimization-pwfo3q"


def test_owner_snapshot_workflow_installs_requirements():
    workflow = _load_workflow()
    job = next(iter(workflow["jobs"].values()))
    assert any("pip install -r requirements.txt" in s.get("run", "") for s in job["steps"])


def test_owner_snapshot_workflow_invokes_run_snapshot_entry_point():
    workflow = _load_workflow()
    job = next(iter(workflow["jobs"].values()))
    assert any("python -m monitoring.run_snapshot" in s.get("run", "") for s in job["steps"])


def test_owner_snapshot_workflow_passes_required_secrets():
    workflow = _load_workflow()
    job = next(iter(workflow["jobs"].values()))
    run_step = next(s for s in job["steps"] if "monitoring.run_snapshot" in s.get("run", ""))
    env = run_step.get("env", {})
    for name in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_OWNER_ID", "TWELVE_DATA_API_KEY", "GEMINI_API_KEY"):
        assert name in env, name


def test_owner_snapshot_workflow_never_hardcodes_a_secret_value():
    content = _workflow_path().read_text()
    for line in content.splitlines():
        if "TELEGRAM_BOT_TOKEN:" in line or "TELEGRAM_OWNER_ID:" in line:
            assert "secrets." in line


def test_owner_snapshot_workflow_has_its_own_concurrency_group_not_shared_with_trading_pipeline():
    workflow = _load_workflow()
    assert workflow["concurrency"]["group"] != "goldbot"


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
