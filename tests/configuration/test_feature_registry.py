"""
Phase 59.6, TASK 4 -- configuration/feature_registry.py tests.
"""

from goldbot.core_layer.configuration.feature_registry import FeatureDescriptor, build_feature_registry


def test_build_feature_registry_returns_a_list_of_descriptors():
    registry = build_feature_registry()

    assert len(registry) > 0
    assert all(isinstance(entry, FeatureDescriptor) for entry in registry)


def test_registry_names_are_unique():
    registry = build_feature_registry()
    names = [entry.name for entry in registry]
    assert len(names) == len(set(names))


def test_real_flags_are_marked_implemented():
    registry = build_feature_registry()
    by_name = {entry.name: entry for entry in registry}

    assert by_name["ENABLE_MT5"].implemented is True
    assert by_name["ENABLE_TWELVEDATA"].implemented is True
    assert by_name["VALIDATION_MODE"].implemented is True
    assert by_name["enable_ai"].implemented is True


def test_real_flags_reflect_actual_config_values():
    from config import Config

    registry = build_feature_registry()
    by_name = {entry.name: entry for entry in registry}

    assert by_name["ENABLE_MT5"].enabled == Config.ENABLE_MT5
    assert by_name["ENABLE_TWELVEDATA"].enabled == Config.ENABLE_TWELVEDATA
    assert by_name["VALIDATION_MODE"].enabled == Config.VALIDATION_MODE


def test_declared_only_features_are_not_implemented_and_disabled():
    registry = build_feature_registry()
    by_name = {entry.name: entry for entry in registry}

    for name in ("ENABLE_NEWS", "ENABLE_PAPER", "ENABLE_BACKTEST",
                 "ENABLE_ANALYTICS", "ENABLE_OWNER", "ENABLE_DATASET_SYNC",
                 "ENABLE_MARKET_PHASE", "ENABLE_BITGET", "ENABLE_BINANCE", "ENABLE_FRED"):
        entry = by_name[name]
        assert entry.implemented is False
        assert entry.enabled is False
        assert entry.source == "declared"


def test_trading_pipeline_gates_are_not_present_in_the_registry():
    """
    Phase 60.9 (Runtime Registry Separation): ENABLE_SIGNALS/ENABLE_AI
    (uppercase)/ENABLE_EXECUTION/ENABLE_DATABASE/ENABLE_RISK/
    ENABLE_DECISION are all Trading-pipeline concerns (see
    docs/FEATURE_REGISTRY_SEPARATION.md's audit table) and must not
    appear in this registry at all -- not even declared-only.
    core/guards/pipeline_guard.py's PipelineGuard now reads exclusively
    from EmergencyManager for every pipeline-stage decision.
    """
    registry = build_feature_registry()
    names = {entry.name for entry in registry}

    for trading_name in ("ENABLE_SIGNALS", "ENABLE_AI", "ENABLE_EXECUTION",
                          "ENABLE_DATABASE", "ENABLE_RISK", "ENABLE_DECISION"):
        assert trading_name not in names


def test_build_feature_registry_never_raises():
    build_feature_registry()  # must not raise


def test_feature_descriptor_is_frozen():
    registry = build_feature_registry()
    entry = registry[0]
    try:
        entry.enabled = True
        assert False, "FeatureDescriptor must be immutable"
    except AttributeError:
        pass
