"""Phase 61.5 TASK 4 — User Registration Integration: real /start -> Phone Share Button -> Phone Hash -> UserRecord -> Trial Check -> FREE account flow. First live wiring of trial_started_at persistence and contact-message routing."""

import asyncio
from types import SimpleNamespace

from telegram.command_router import route_command, route_contact
from telegram.user_service import UserService
from core.phone_hash import hash_phone_number


def _run(coro):
    return asyncio.run(coro)


def _contact_message(telegram_id, phone_number, contact_user_id=None):
    """
    contact_user_id defaults to telegram_id -- the real Phone Share
    Button always populates aiogram's Contact.user_id with the
    sender's own id (V2 Phase 3 ownership check). Pass a different
    value to simulate a forwarded contact card for someone else.
    """
    return SimpleNamespace(
        from_user=SimpleNamespace(id=telegram_id, username="phoneuser"),
        contact=SimpleNamespace(
            phone_number=phone_number,
            user_id=telegram_id if contact_user_id is None else contact_user_id,
        ),
        text=None,
    )


def test_register_phone_for_unknown_user_reports_not_found():
    result = UserService().register_phone("999888", "+1 555 000 1111")
    assert result.success is False
    assert "not found" in result.reason.lower()


def test_register_phone_starts_a_trial_for_a_new_user():
    UserService().register_user("501", username="a")
    result = UserService().register_phone("501", "+1 555 111 2222")

    assert result.success is True
    assert result.trial_active is True
    assert result.trial_expires_at is not None


def test_register_phone_persists_only_the_hash_never_the_raw_number():
    UserService().register_user("502", username="b")
    UserService().register_phone("502", "+1 555 333 4444")

    profile = UserService().get_profile("502").profile
    assert profile.phone_hash == hash_phone_number("+1 555 333 4444")
    assert "555" not in profile.phone_hash
    assert "3334444" not in profile.phone_hash


def test_register_phone_persists_trial_started_at():
    UserService().register_user("503", username="c")
    UserService().register_phone("503", "+1 555 555 5555")

    profile = UserService().get_profile("503").profile
    assert profile.trial_started_at is not None


def test_register_phone_a_second_time_never_resets_the_trial_window():
    UserService().register_user("504", username="d")
    UserService().register_phone("504", "+1 555 666 7777")
    first_started_at = UserService().get_profile("504").profile.trial_started_at

    UserService().register_phone("504", "+1 555 666 7777")
    second_started_at = UserService().get_profile("504").profile.trial_started_at

    assert first_started_at == second_started_at


def test_register_phone_reused_by_another_account_blocks_the_trial():
    UserService().register_user("505", username="original")
    UserService().register_phone("505", "+1 555 999 0000")

    UserService().register_user("506", username="second_account")
    result = UserService().register_phone("506", "+1 555 999 0000")

    assert result.success is False
    assert "already registered" in result.reason.lower()


def test_register_phone_reused_still_stores_the_phone_hash_for_audit():
    UserService().register_user("507", username="original")
    UserService().register_phone("507", "+1 555 888 1234")

    UserService().register_user("508", username="reuser")
    UserService().register_phone("508", "+1 555 888 1234")

    profile = UserService().get_profile("508").profile
    assert profile.phone_hash == hash_phone_number("+1 555 888 1234")


def test_route_contact_end_to_end_registers_a_free_account():
    _run(route_command("/start", telegram_id="601"))

    message = _contact_message("601", "+1 555 222 3333")
    result = _run(route_contact(message))

    assert "tasdiqlandi" in result.text.lower()
    assert "sinov" in result.text.lower()


def test_route_contact_attaches_the_persistent_reply_keyboard_on_completion():
    """V2 Phase 6.1 (Director Decision 7): a successful phone share (Wizard
    COMPLETE) gets ReplyKeyboardRemove() on this reply, followed by a
    second message (result.followup) carrying the USER-tier persistent
    Reply Keyboard with localized (UZ default) labels -- the literal
    Phone Share -> ReplyKeyboardRemove() -> Persistent Reply Keyboard
    sequence."""
    from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

    _run(route_command("/start", telegram_id="618"))
    result = _run(route_contact(_contact_message("618", "+1 555 444 0001")))

    assert isinstance(result.keyboard, ReplyKeyboardRemove)
    assert isinstance(result.followup.keyboard, ReplyKeyboardMarkup)
    buttons = [b.text for row in result.followup.keyboard.keyboard for b in row]
    assert buttons == [
        "🏠 Bosh sahifa", "👤 Profil", "📊 Signallar", "💳 Obuna", "⚙️ Sozlamalar", "❓ Yordam",
    ]


def test_route_contact_no_keyboard_when_registration_does_not_complete():
    """A rejected contact (ownership mismatch) never reaches COMPLETE -- no persistent keyboard attached, no followup."""
    _run(route_command("/start", telegram_id="619"))
    result = _run(route_contact(_contact_message("619", "+1 555 444 0002", contact_user_id="999999")))

    assert result.keyboard is None
    assert result.followup is None


def test_route_contact_for_unregistered_user_is_localized():
    # Phase 1.6 -- contact_handler no longer echoes UserService's raw
    # English reason string; DB default language is UZ.
    message = _contact_message("609", "+1 555 444 5555")
    result = _run(route_contact(message))

    assert result.text == "Foydalanuvchi topilmadi -- avval /start yuboring."


def test_route_contact_for_a_reused_phone_number_is_localized():
    _run(route_command("/start", telegram_id="610"))
    _run(route_contact(_contact_message("610", "+1 555 777 8888")))

    _run(route_command("/start", telegram_id="611"))
    result = _run(route_contact(_contact_message("611", "+1 555 777 8888")))

    assert result.text == "Bu telefon raqami boshqa hisobda allaqachon ro'yxatdan o'tgan."


def test_start_reply_carries_the_phone_share_keyboard():
    """New user: Wizard step is LANGUAGE, so /start's keyboard is the language picker."""
    result = _run(route_command("/start", telegram_id="602"))
    assert result.keyboard is not None


def test_route_contact_rejects_a_contact_for_a_different_person():
    """V2 Phase 3: a forwarded contact card for someone else must never register that phone."""
    _run(route_command("/start", telegram_id="612"))

    message = _contact_message("612", "+1 555 111 0000", contact_user_id="999999")
    result = _run(route_contact(message))

    assert result.text == "Iltimos, tugma orqali o'zingizning telefon raqamingizni yuboring."
    assert UserService().get_profile("612").profile.phone_hash is None


def test_route_contact_rejects_a_contact_with_no_user_id():
    """A contact card with no linked Telegram account (user_id=None) is also rejected, not silently accepted."""
    _run(route_command("/start", telegram_id="613"))

    message = _contact_message("613", "+1 555 222 0001", contact_user_id=None)
    message.contact.user_id = None  # override the default-to-telegram_id behavior explicitly
    result = _run(route_contact(message))

    assert result.text == "Iltimos, tugma orqali o'zingizning telefon raqamingizni yuboring."


def test_route_contact_accepts_the_senders_own_contact():
    """Sanity check: the ownership guard must not break the legitimate Phone Share Button flow."""
    _run(route_command("/start", telegram_id="614"))

    message = _contact_message("614", "+1 555 333 0002")
    result = _run(route_contact(message))

    assert "tasdiqlandi" in result.text.lower()
    assert UserService().get_profile("614").profile.phone_hash is not None


def test_start_keyboard_is_the_phone_share_keyboard_once_at_the_phone_step():
    """V2 Phase 3: after the Language step is done, /start's keyboard becomes Phone Share."""
    from telegram.registration_service import RegistrationService

    _run(route_command("/start", telegram_id="615"))
    RegistrationService().advance_past_language("615")

    result = _run(route_command("/start", telegram_id="615"))

    assert result.keyboard is not None
    assert result.keyboard.keyboard[0][0].request_contact is True


def test_start_keyboard_is_the_persistent_reply_keyboard_once_registration_is_complete():
    """V2 Phase 5.1: COMPLETE replaces "no keyboard" with the USER-tier persistent Reply Keyboard, localized (UZ default) labels."""
    from aiogram.types import ReplyKeyboardMarkup
    from telegram.registration_service import RegistrationService

    _run(route_command("/start", telegram_id="616"))
    RegistrationService().complete("616")

    result = _run(route_command("/start", telegram_id="616"))

    assert isinstance(result.keyboard, ReplyKeyboardMarkup)
    buttons = [b.text for row in result.keyboard.keyboard for b in row]
    assert buttons == [
        "🏠 Bosh sahifa", "👤 Profil", "📊 Signallar", "💳 Obuna", "⚙️ Sozlamalar", "❓ Yordam",
    ]


# ---------------------------------------------------------------------------
# V2 Phase 6.1.1 (Director-reported bug, root-caused) -- database/models.py's
# _backfill_registration_state() (V2 Phase 3) permanently set
# registration_step='PHONE' for any pre-existing row with no phone_hash,
# which includes operator accounts (OWNER/ADMIN) created before the
# mandatory Phone Share Wizard existed. Without the fix, such an account's
# /start reply keeps re-attaching phone_share_keyboard() forever -- these
# tests pin the exact stuck-at-PHONE scenario and confirm OWNER/ADMIN now
# always get the tier-aware persistent Reply Keyboard regardless of
# registration_step, while a regular USER stuck the same way is unaffected
# (still correctly re-offered Phone Share -- Phase 3's mandatory-completion
# policy for ordinary signups is untouched).
# ---------------------------------------------------------------------------


def test_start_keyboard_is_persistent_for_owner_stuck_at_phone_step(monkeypatch):
    from aiogram.types import ReplyKeyboardMarkup
    from database.user_repository import UserRepository
    from telegram.permissions import PermissionLevel

    _run(route_command("/start", telegram_id="624"))
    UserRepository().set_registration_step("624", "PHONE")  # simulates the Phase 3 backfill

    monkeypatch.setattr(
        "telegram.command_router.get_permission_level", lambda telegram_id: PermissionLevel.OWNER,
    )

    result = _run(route_command("/start", telegram_id="624"))

    assert isinstance(result.keyboard, ReplyKeyboardMarkup)
    buttons = [b.text for row in result.keyboard.keyboard for b in row]
    assert "🛠 Admin" in buttons
    assert "👑 Owner" in buttons


def test_start_keyboard_is_persistent_for_admin_stuck_at_phone_step(monkeypatch):
    from aiogram.types import ReplyKeyboardMarkup
    from database.user_repository import UserRepository
    from telegram.permissions import PermissionLevel

    _run(route_command("/start", telegram_id="625"))
    UserRepository().set_registration_step("625", "PHONE")

    monkeypatch.setattr(
        "telegram.command_router.get_permission_level", lambda telegram_id: PermissionLevel.ADMIN,
    )

    result = _run(route_command("/start", telegram_id="625"))

    assert isinstance(result.keyboard, ReplyKeyboardMarkup)
    buttons = [b.text for row in result.keyboard.keyboard for b in row]
    assert "🛠 Admin" in buttons
    assert "👑 Owner" not in buttons


def test_start_keyboard_still_offers_phone_share_for_a_regular_user_stuck_at_phone_step():
    """Regression guard: the OWNER/ADMIN bypass must not leak to ordinary USER-tier accounts -- Phase 3's mandatory Phone Share policy for them is untouched."""
    from database.user_repository import UserRepository

    _run(route_command("/start", telegram_id="626"))
    UserRepository().set_registration_step("626", "PHONE")

    result = _run(route_command("/start", telegram_id="626"))

    assert result.keyboard is not None
    assert result.keyboard.keyboard[0][0].request_contact is True


def test_start_keyboard_is_reply_keyboard_remove_for_a_banned_user():
    """V2 Phase 5 Decision 3: a BANNED /start gets ReplyKeyboardRemove(), not None."""
    from aiogram.types import ReplyKeyboardRemove
    from telegram.user_service import UserService as _US

    _run(route_command("/start", telegram_id="617"))
    _US().ban_user("617")

    result = _run(route_command("/start", telegram_id="617"))

    assert isinstance(result.keyboard, ReplyKeyboardRemove)
    assert result.text == "Sizning hisobingiz bloklangan."


# ---------------------------------------------------------------------------
# V2 Phase 5 Decision 4 -- the persistent Reply Keyboard is tier-aware,
# same superset policy as Phase 4's Persistent Menu (menu_commands.py).
# ---------------------------------------------------------------------------


def test_start_keyboard_is_the_admin_reply_keyboard_for_a_completed_admin(monkeypatch):
    from database.admin_repository import AdminRepository
    from telegram.registration_service import RegistrationService

    monkeypatch.delenv("TELEGRAM_OWNER_ID", raising=False)
    _run(route_command("/start", telegram_id="620"))
    RegistrationService().complete("620")
    AdminRepository().add_admin("620")

    result = _run(route_command("/start", telegram_id="620"))

    buttons = [b.text for row in result.keyboard.keyboard for b in row]
    assert buttons == [
        "🏠 Bosh sahifa", "👤 Profil", "📊 Signallar", "💳 Obuna", "⚙️ Sozlamalar", "❓ Yordam", "🛠 Admin",
    ]


def test_start_keyboard_is_the_owner_reply_keyboard_for_a_completed_owner(monkeypatch):
    from telegram.registration_service import RegistrationService

    monkeypatch.setenv("TELEGRAM_OWNER_ID", "621")
    _run(route_command("/start", telegram_id="621"))
    RegistrationService().complete("621")

    result = _run(route_command("/start", telegram_id="621"))

    buttons = [b.text for row in result.keyboard.keyboard for b in row]
    assert buttons == [
        "🏠 Bosh sahifa", "👤 Profil", "📊 Signallar", "💳 Obuna", "⚙️ Sozlamalar", "❓ Yordam", "🛠 Admin", "👑 Owner",
    ]


def test_start_keyboard_reply_labels_follow_the_users_language():
    """V2 Phase 5.1: labels localize to whatever language the user has selected, not just the UZ default."""
    from telegram.user_service import UserService

    _run(route_command("/start", telegram_id="622"))
    UserService().change_language("622", "EN")
    from telegram.registration_service import RegistrationService
    RegistrationService().complete("622")

    result = _run(route_command("/start", telegram_id="622"))

    buttons = [b.text for row in result.keyboard.keyboard for b in row]
    assert buttons == ["🏠 Home", "👤 Profile", "📊 Signals", "💳 Subscription", "⚙️ Settings", "❓ Help"]


def test_navigation_label_from_the_reply_keyboard_routes_to_the_same_handler_as_its_command():
    """V2 Phase 5.1: tapping a localized Reply Keyboard button behaves identically to typing its "/command"."""
    _run(route_command("/start", telegram_id="623"))
    by_label = _run(route_command("👤 Profil", telegram_id="623"))
    by_command = _run(route_command("/profile", telegram_id="623"))

    assert by_label.text == by_command.text
