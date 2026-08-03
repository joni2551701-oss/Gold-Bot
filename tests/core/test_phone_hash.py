"""Phase 61.4 TASK 4 — core_layer/secrets/phone_hash.py: deterministic, salted phone number hashing. The raw phone number is never returned."""

from core_layer.secrets.phone_hash import hash_phone_number


def test_same_phone_always_hashes_the_same():
    first = hash_phone_number("+998901234567", salt="test-salt")
    second = hash_phone_number("+998901234567", salt="test-salt")
    assert first == second


def test_different_phones_hash_differently():
    a = hash_phone_number("+998901234567", salt="test-salt")
    b = hash_phone_number("+998907654321", salt="test-salt")
    assert a != b


def test_formatting_differences_normalize_to_the_same_hash():
    a = hash_phone_number("+998 90 123-45-67", salt="test-salt")
    b = hash_phone_number("998901234567", salt="test-salt")
    assert a == b


def test_different_salt_produces_a_different_hash():
    a = hash_phone_number("+998901234567", salt="salt-one")
    b = hash_phone_number("+998901234567", salt="salt-two")
    assert a != b


def test_output_never_contains_the_raw_phone_number():
    digest = hash_phone_number("+998901234567", salt="test-salt")
    assert "998901234567" not in digest
    assert "+998901234567" not in digest


def test_empty_phone_does_not_raise():
    result = hash_phone_number("", salt="test-salt")
    assert isinstance(result, str)
    assert len(result) == 64


def test_no_explicit_salt_still_produces_a_deterministic_hash():
    """Falls back to Secrets().PHONE_HASH_SALT or the built-in default pepper -- never raises, never varies across calls with no configured env var."""
    first = hash_phone_number("+998901234567")
    second = hash_phone_number("+998901234567")
    assert first == second
