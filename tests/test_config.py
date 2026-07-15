"""
Phase 59 Real Market Validation Foundation, TASK 1 --
config.Config.VALIDATION_MODE tests. No dedicated test file existed
for config.py before this phase.
"""

import importlib

from config import Config


def test_validation_mode_defaults_to_false():
    assert Config.VALIDATION_MODE is False


def test_validation_mode_reads_from_environment(monkeypatch):
    monkeypatch.setenv("VALIDATION_MODE", "True")
    import config

    importlib.reload(config)
    try:
        assert config.Config.VALIDATION_MODE is True
    finally:
        importlib.reload(config)  # restore the default for every later test


def test_validation_mode_is_a_real_bool_not_a_string():
    assert isinstance(Config.VALIDATION_MODE, bool)
