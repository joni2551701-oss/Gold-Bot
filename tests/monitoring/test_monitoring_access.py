"""Phase B.0 Rule 5 -- core_layer/health_monitor/access.py tests."""

from core_layer.configuration.feature_flags import FeatureFlags
from core_layer.health_monitor.access import is_owner_monitoring_enabled

ENABLED = FeatureFlags(enable_owner_monitoring=True)
DISABLED = FeatureFlags(enable_owner_monitoring=False)


def test_is_owner_monitoring_enabled_true_when_flag_set():
    assert is_owner_monitoring_enabled(ENABLED) is True


def test_is_owner_monitoring_enabled_false_when_flag_unset():
    assert is_owner_monitoring_enabled(DISABLED) is False


def test_is_owner_monitoring_enabled_defaults_to_false():
    assert is_owner_monitoring_enabled() is False


def test_is_owner_monitoring_enabled_never_raises():
    assert is_owner_monitoring_enabled(FeatureFlags()) is False
