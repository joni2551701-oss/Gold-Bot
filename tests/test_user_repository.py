"""
Phase 61.4 TASK 4 -- database/user_repository.py's phone_hash column
tests. Real SQLite (tests/conftest.py's autouse fresh_database
fixture), no mocks. The raw phone number is never written by this
repository -- only an already-computed hash.
"""

from core.phone_hash import hash_phone_number
from database.user_repository import UserRepository


def test_new_user_has_no_phone_hash_by_default():
    repo = UserRepository()
    user = repo.create_user("111", username="alice")
    assert user.phone_hash is None


def test_set_phone_hash_persists_the_hash():
    repo = UserRepository()
    repo.create_user("111", username="alice")
    digest = hash_phone_number("+998901234567", salt="test-salt")

    updated = repo.set_phone_hash("111", digest)

    assert updated is True
    assert repo.get_user("111").phone_hash == digest


def test_get_users_by_phone_hash_finds_the_matching_user():
    repo = UserRepository()
    repo.create_user("111", username="alice")
    digest = hash_phone_number("+998901234567", salt="test-salt")
    repo.set_phone_hash("111", digest)

    matches = repo.get_users_by_phone_hash(digest)

    assert [u.telegram_id for u in matches] == ["111"]


def test_get_users_by_phone_hash_detects_the_same_phone_across_two_accounts():
    """The exact abuse pattern TASK 5's trial_manager.py needs to catch: one phone_hash, two telegram_ids."""
    repo = UserRepository()
    repo.create_user("111", username="alice")
    repo.create_user("222", username="alice_second_account")
    digest = hash_phone_number("+998901234567", salt="test-salt")
    repo.set_phone_hash("111", digest)
    repo.set_phone_hash("222", digest)

    matches = repo.get_users_by_phone_hash(digest)

    assert {u.telegram_id for u in matches} == {"111", "222"}


def test_get_users_by_phone_hash_with_no_match_returns_empty_list():
    repo = UserRepository()
    assert repo.get_users_by_phone_hash("no-such-hash") == []


def test_update_user_still_rejects_unknown_fields():
    """phone_hash addition to the allowed set must not have loosened this guard for anything else."""
    repo = UserRepository()
    repo.create_user("111", username="alice")
    assert repo.update_user("111", not_a_real_column="x") is False
