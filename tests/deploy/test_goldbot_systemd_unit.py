"""
Phase P1 (Production Deployment Pipeline Foundation), TASK 6/12 --
deploy/systemd/goldbot.service structure tests.

Plain text checks against the unit file, matching this repository's
existing convention for workflow-file tests (no systemd/dbus
available in this sandbox to actually load the unit).
"""

import pathlib


def _unit_path():
    return (
        pathlib.Path(__file__).resolve().parents[2]
        / "deploy" / "systemd" / "goldbot.service"
    )


def _unit_text():
    return _unit_path().read_text()


def test_unit_file_exists():
    assert _unit_path().exists()


def test_unit_has_unit_section():
    assert "[Unit]" in _unit_text()


def test_unit_has_service_section():
    assert "[Service]" in _unit_text()


def test_unit_has_install_section():
    assert "[Install]" in _unit_text()


def test_unit_type_is_simple():
    """Long-running process (telegram.polling), not oneshot."""
    text = _unit_text()
    assert "Type=simple" in text


def test_unit_restarts_always():
    assert "Restart=always" in _unit_text()


def test_unit_has_restart_delay():
    assert "RestartSec=5" in _unit_text()


def test_unit_runs_as_non_root_user():
    text = _unit_text()
    assert "User=" in text
    for line in text.splitlines():
        if line.strip().startswith("User="):
            user = line.strip().split("=", 1)[1].strip()
            assert user != "root"
            assert user != ""


def test_unit_runs_as_senior_per_brief():
    assert "User=senior" in _unit_text()


def test_unit_working_directory_is_current_symlink_path():
    assert "WorkingDirectory=/opt/goldbot/current" in _unit_text()


def test_unit_exec_start_uses_current_symlink_venv():
    text = _unit_text()
    assert "ExecStart=/opt/goldbot/current/venv/bin/python" in text


def test_unit_exec_start_runs_telegram_polling():
    assert "-m telegram.polling" in _unit_text()


def test_unit_exec_start_never_runs_trading_pipeline():
    """
    The trading pipeline stays on GitHub Actions (trading_bot.yml) --
    this unit must never launch main.py, to avoid a double-cycle
    overlap against the same database (the exact hazard
    docs/production_setup.md's goldbot-pipeline.timer already warns
    about for the older direct-install layout).
    """
    text = _unit_text()
    for line in text.splitlines():
        if line.strip().startswith("ExecStart="):
            assert "main.py" not in line


def test_unit_environment_file_points_at_shared_env():
    assert "EnvironmentFile=/opt/goldbot/shared/.env" in _unit_text()


def test_unit_environment_file_is_not_inside_a_release_directory():
    """.env must be a shared, per-deploy-path resource, never release-specific (RULE 4)."""
    text = _unit_text()
    for line in text.splitlines():
        if line.strip().startswith("EnvironmentFile="):
            assert "/releases/" not in line


def test_unit_has_on_failure_alert_hook():
    assert "OnFailure=goldbot-notify-failure@%n.service" in _unit_text()


def test_unit_logs_to_journal():
    text = _unit_text()
    assert "StandardOutput=journal" in text
    assert "StandardError=journal" in text


def test_unit_has_syslog_identifier():
    assert "SyslogIdentifier=goldbot" in _unit_text()


def test_unit_waits_for_network():
    text = _unit_text()
    assert "After=network-online.target" in text
    assert "Wants=network-online.target" in text


def test_unit_installed_for_multi_user_target():
    assert "WantedBy=multi-user.target" in _unit_text()


def test_unit_never_hardcodes_a_release_timestamp():
    """
    The whole point of the `current` symlink indirection: this file
    itself must never reference a specific releases/<id> path -- only
    release_deploy.sh's atomic symlink switch changes what `current`
    resolves to.
    """
    text = _unit_text()
    assert "/releases/" not in text
