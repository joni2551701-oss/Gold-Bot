"""V2 Phase 3 -- telegram/registration_service.py's Wizard state machine."""

from database_layer.user_repository.user_repository import UserRepository
from telegram.registration_service import RegistrationService, RegistrationStep


def test_current_step_for_a_brand_new_user_is_language():
    UserRepository().create_user("701", username="alice")
    assert RegistrationService().current_step("701") == RegistrationStep.LANGUAGE


def test_current_step_for_an_unknown_user_is_none():
    assert RegistrationService().current_step("does-not-exist") is None


def test_current_step_for_a_banned_user_is_none():
    repo = UserRepository()
    repo.create_user("702", username="bob")
    repo.update_user("702", status="BANNED")
    assert RegistrationService().current_step("702") is None


def test_current_step_for_a_completed_user_is_none():
    repo = UserRepository()
    repo.create_user("703", username="carol")
    repo.complete_registration("703")
    assert RegistrationService().current_step("703") is None


def test_current_step_reflects_the_phone_step_after_advancing():
    repo = UserRepository()
    repo.create_user("704", username="dave")
    RegistrationService().advance_past_language("704")
    assert RegistrationService().current_step("704") == RegistrationStep.PHONE


def test_advance_past_language_moves_language_to_phone():
    repo = UserRepository()
    repo.create_user("705", username="erin")

    advanced = RegistrationService().advance_past_language("705")

    assert advanced is True
    assert repo.get_user("705").registration_step == RegistrationStep.PHONE


def test_advance_past_language_is_a_noop_for_a_user_already_past_language():
    """An already-registered user changing language later via /language must never reopen the Wizard."""
    repo = UserRepository()
    repo.create_user("706", username="frank")
    repo.complete_registration("706")

    advanced = RegistrationService().advance_past_language("706")

    assert advanced is False
    assert repo.get_user("706").registration_step == RegistrationStep.COMPLETE


def test_advance_past_language_is_a_noop_for_an_unknown_user():
    assert RegistrationService().advance_past_language("does-not-exist") is False


def test_complete_sets_step_and_flag_together():
    repo = UserRepository()
    repo.create_user("707", username="grace")

    completed = RegistrationService().complete("707")

    user = repo.get_user("707")
    assert completed is True
    assert user.registration_step == RegistrationStep.COMPLETE
    assert user.registration_completed is True


def test_complete_is_idempotent():
    repo = UserRepository()
    repo.create_user("708", username="heidi")
    RegistrationService().complete("708")

    second_call = RegistrationService().complete("708")

    assert second_call is True
    assert repo.get_user("708").registration_step == RegistrationStep.COMPLETE
