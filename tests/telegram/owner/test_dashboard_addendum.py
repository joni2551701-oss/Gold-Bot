"""Phase 61.5 Addendum (per Director review) — get_owner_summary()/get_doctor_report() direct unit tests. Not registered into command_router.py by these tests -- see tests/telegram/test_ai_command_permission_matrix.py for the live-wired path."""

from telegram.owner.dashboard import get_doctor_report, get_owner_summary


def test_owner_summary_never_raises_and_reports_expected_fields():
    result = get_owner_summary()

    assert result.success is True
    assert "System:" in result.message
    assert "AI:" in result.message
    assert "Provider:" in result.message
    assert "Users:" in result.message
    assert "Premium:" in result.message
    assert "Signals Today:" in result.message
    assert "Win Rate:" in result.message
    assert "Cost Today:" in result.message
    assert "Emergency:" in result.message


def test_owner_summary_cost_today_is_never_fabricated_when_no_audit_data():
    result = get_owner_summary()
    assert "$0.00" in result.message


def test_doctor_report_checks_every_expected_subsystem():
    result = get_doctor_report()

    assert result.success is True
    for label in ("Database", "AI", "Market Data", "Telegram", "Scheduler", "Providers", "Learning", "Cache", "Audit"):
        assert label in result.message


def test_doctor_report_scheduler_is_honestly_n_a_not_fabricated():
    result = get_doctor_report()
    assert "N/A" in result.message


def test_doctor_report_reports_overall_status():
    result = get_doctor_report()
    assert "Status:" in result.message
    assert "Healthy" in result.message or "Degraded" in result.message
