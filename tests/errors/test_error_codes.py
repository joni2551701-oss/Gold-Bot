"""
Phase A18 -- Error Classification tests: error codes
(core/errors/codes.py).
"""

import pytest

from core.errors import codes


def test_code_pattern_matches_every_defined_code():
    for code in codes.CODE_REGISTRY:
        assert codes.CODE_PATTERN.match(code), f"{code} does not match CODE_PATTERN"


def test_no_duplicate_codes():
    """CODE_REGISTRY is a dict, so a literal duplicate key would silently overwrite -- assert the module-level names stay distinct too."""
    all_code_values = [
        codes.CONFIG_001, codes.CONFIG_002,
        codes.DATA_001, codes.DATA_002,
        codes.API_001, codes.API_002,
        codes.DB_001, codes.DB_002,
        codes.VALIDATION_001, codes.VALIDATION_002,
        codes.PERMISSION_001,
        codes.STRATEGY_001,
        codes.DECISION_001,
        codes.EXECUTION_001,
    ]
    assert len(all_code_values) == len(set(all_code_values))


def test_every_module_level_code_is_registered():
    all_code_values = [
        codes.CONFIG_001, codes.CONFIG_002,
        codes.DATA_001, codes.DATA_002,
        codes.API_001, codes.API_002,
        codes.DB_001, codes.DB_002,
        codes.VALIDATION_001, codes.VALIDATION_002,
        codes.PERMISSION_001,
        codes.STRATEGY_001,
        codes.DECISION_001,
        codes.EXECUTION_001,
    ]
    for code in all_code_values:
        assert code in codes.CODE_REGISTRY


def test_registry_size_matches_defined_codes():
    """Guards against a code being added to the registry but not as a module-level name, or vice versa."""
    assert len(codes.CODE_REGISTRY) == 14


@pytest.mark.parametrize("prefix,expected_codes", [
    ("CONFIG", {"CONFIG_001", "CONFIG_002"}),
    ("DATA", {"DATA_001", "DATA_002"}),
    ("API", {"API_001", "API_002"}),
    ("DB", {"DB_001", "DB_002"}),
    ("VALIDATION", {"VALIDATION_001", "VALIDATION_002"}),
    ("PERMISSION", {"PERMISSION_001"}),
    ("STRATEGY", {"STRATEGY_001"}),
    ("DECISION", {"DECISION_001"}),
    ("EXECUTION", {"EXECUTION_001"}),
])
def test_each_category_has_its_expected_codes(prefix, expected_codes):
    category_codes = {c for c in codes.CODE_REGISTRY if c.startswith(prefix + "_")}
    assert category_codes == expected_codes


def test_is_valid_code_format_accepts_well_formed_codes():
    assert codes.is_valid_code_format("DATA_001") is True
    assert codes.is_valid_code_format("EXECUTION_999") is True


def test_is_valid_code_format_rejects_malformed_codes():
    assert codes.is_valid_code_format("data_001") is False  # lowercase
    assert codes.is_valid_code_format("DATA-001") is False  # wrong separator
    assert codes.is_valid_code_format("DATA_1") is False  # not zero-padded to 3
    assert codes.is_valid_code_format("DATA") is False  # no number
    assert codes.is_valid_code_format("") is False


def test_is_known_code():
    assert codes.is_known_code("DATA_001") is True
    assert codes.is_known_code("DATA_999") is False
