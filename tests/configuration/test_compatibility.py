"""
Phase A13 -- Configuration Layer tests: existing config.py
compatibility.

config.py is not rewritten by this phase -- these tests guard that
every attribute the rest of the codebase already depends on
(database/database.py's Config.DB_PATH, main.py's
Config.TIMEFRAME_HISTORY, etc.) is still present and behaves exactly
as before configuration/ was added.
"""

import os
from datetime import timezone

from config import Config


def test_existing_config_attributes_are_unchanged():
    assert Config.TIMEZONE == timezone.utc
    assert isinstance(Config.APP_ENV, str)
    assert isinstance(Config.DEBUG, bool)
    assert os.path.isdir(Config.BASE_DIR)
    # DB_PATH itself is swapped to a per-test tmp file by tests/conftest.py's
    # autouse isolation fixture -- assert the attribute is still a real
    # path string, not that it equals the production default.
    assert Config.DB_PATH.endswith(".db")


def test_existing_timeframe_history_is_unchanged():
    """main.py's Config.TIMEFRAME_HISTORY["M15"] lookup (outputsize) must keep working."""
    assert Config.TIMEFRAME_HISTORY["M15"] == 200
    assert Config.TIMEFRAME_HISTORY["M5"] == 200
    assert Config.TIMEFRAME_HISTORY["H1"] == 200
    assert Config.TIMEFRAME_HISTORY["H4"] == 100
    assert Config.TIMEFRAME_HISTORY["Daily"] == 100


def test_configuration_layer_does_not_mutate_config_module():
    """Importing configuration/ must not have side effects on config.Config's class attributes."""
    import configuration.settings
    import configuration.environment
    import configuration.feature_flags

    assert configuration.settings.ApplicationSettings is not None
    assert configuration.environment.Environment is not None
    assert configuration.feature_flags.FeatureFlags is not None
    assert Config.TIMEZONE == timezone.utc
    assert Config.TIMEFRAME_HISTORY["M15"] == 200
