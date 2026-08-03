"""
Phase 47 — Feedback Layer tests: create, resolve, admin listing.
"""

import asyncio


def test_send_feedback_creates_open_entry():
    from platform_layer.telegram.feedback_service import FeedbackService

    result = FeedbackService().send_feedback("300", "Great signal quality")
    assert result.success is True
    assert result.feedback.status == "OPEN"
    assert result.feedback.telegram_id == "300"


def test_send_feedback_rejects_empty_message():
    from platform_layer.telegram.feedback_service import FeedbackService

    result = FeedbackService().send_feedback("301", "   ")
    assert result.success is False
    assert "empty" in result.reason.lower()


def test_resolve_feedback_transitions_status():
    from platform_layer.telegram.feedback_service import FeedbackService

    service = FeedbackService()
    created = service.send_feedback("302", "Bug found in signal").feedback

    reviewed = service.resolve_feedback(created.id, "REVIEWED")
    assert reviewed.success is True
    assert reviewed.feedback.status == "REVIEWED"

    resolved = service.resolve_feedback(created.id, "RESOLVED")
    assert resolved.success is True
    assert resolved.feedback.status == "RESOLVED"


def test_resolve_feedback_rejects_invalid_status():
    from platform_layer.telegram.feedback_service import FeedbackService

    service = FeedbackService()
    created = service.send_feedback("303", "test").feedback

    result = service.resolve_feedback(created.id, "NOT_A_REAL_STATUS")
    assert result.success is False


def test_get_feedback_list_newest_first():
    from platform_layer.telegram.feedback_service import FeedbackService

    service = FeedbackService()
    service.send_feedback("304", "first")
    service.send_feedback("304", "second")

    result = service.get_feedback_list(limit=10)
    assert result.success is True
    assert len(result.feedback_list) == 2
    assert result.feedback_list[0].message == "second"


def test_feedback_handler_end_to_end_via_command_router():
    from platform_layer.telegram.command_router import route_command

    async def scenario():
        r = await route_command("/feedback Signal juda yaxshi", telegram_id="305")
        assert r.text.startswith("✅ Fikr-mulohaza qabul qilindi.")
        assert "ID: #" in r.text
        assert "Holat: OPEN" in r.text

    asyncio.run(scenario())


def test_admin_get_feedback_matches_service():
    from platform_layer.telegram.feedback_service import FeedbackService
    from platform_layer.telegram.admin_service import AdminService

    FeedbackService().send_feedback("306", "admin visibility check")

    result = AdminService().get_feedback()
    assert result.success is True
    assert any(item.telegram_id == "306" for item in result.feedback_list)
