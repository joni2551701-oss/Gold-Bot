"""Phase 61.4 TASK 5 — AI Identity Checker: pure phone-reuse check over caller-supplied telegram_ids, no database/telegram import."""

from ai.access.identity_checker import is_phone_reused_by_another_account


def test_empty_sequence_is_not_reuse():
    assert is_phone_reused_by_another_account("111", []) is False


def test_only_the_current_account_sharing_the_phone_is_not_reuse():
    assert is_phone_reused_by_another_account("111", ["111"]) is False


def test_a_different_account_sharing_the_phone_is_reuse():
    assert is_phone_reused_by_another_account("111", ["222"]) is True


def test_current_account_plus_another_account_is_still_reuse():
    assert is_phone_reused_by_another_account("111", ["111", "222"]) is True
