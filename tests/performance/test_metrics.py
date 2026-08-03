"""
Phase A19 -- Performance Metrics tests: model, serialization,
validation (core_layer/performance/metrics.py).
"""

import dataclasses
import json

import pytest

from core_layer.performance.metrics import (
    PerformanceMetric,
    ValidationResult,
    generate_metric_id,
    validate_metric,
    ALLOWED_STATUSES,
)


def test_metric_creation_matches_director_example():
    """PerformanceMetric(name=..., module=..., duration_ms=...) -- the brief's own three-argument example."""
    metric = PerformanceMetric(name="strategy_execution", module="StrategyEngine", duration_ms=50)

    assert metric.name == "strategy_execution"
    assert metric.module == "StrategyEngine"
    assert metric.duration_ms == 50
    assert metric.status == "success"
    assert metric.metadata == {}
    assert metric.error_code is None
    assert metric.metric_id  # auto-generated, non-empty
    assert metric.timestamp is not None  # auto-generated


def test_metric_creation_with_full_fields():
    metric = PerformanceMetric(
        name="context_analysis",
        module="ContextEngine",
        duration_ms=124,
        status="success",
        metadata={"candles": 200},
    )

    assert metric.duration_ms == 124
    assert metric.status == "success"
    assert metric.metadata == {"candles": 200}


def test_generate_metric_id_produces_unique_real_ids():
    ids = {generate_metric_id() for _ in range(100)}
    assert len(ids) == 100
    for metric_id in ids:
        assert isinstance(metric_id, str)
        assert len(metric_id) == 36  # standard UUID4 string length


def test_metric_is_immutable():
    metric = PerformanceMetric(name="x", module="M", duration_ms=1)
    with pytest.raises(dataclasses.FrozenInstanceError):
        metric.duration_ms = 999


def test_future_compatibility_field_shape_is_stable():
    field_names = {f.name for f in dataclasses.fields(PerformanceMetric)}
    assert field_names == {
        "metric_id", "name", "module", "duration_ms", "timestamp",
        "status", "metadata", "error_code",
    }


# --- Serialization ---

def test_to_dict_matches_brief_example_shape():
    metric = PerformanceMetric(name="context_analysis", module="ContextEngine", duration_ms=124, status="success")
    data = metric.to_dict()

    assert data["name"] == "context_analysis"
    assert data["module"] == "ContextEngine"
    assert data["duration_ms"] == 124
    assert data["status"] == "success"
    assert isinstance(data["timestamp"], str)


def test_to_dict_is_json_safe():
    metric = PerformanceMetric(name="x", module="M", duration_ms=1, metadata={"k": "v"})
    data = metric.to_dict()
    json.dumps(data)  # raises TypeError if anything isn't JSON-native


def test_to_json_produces_valid_json():
    metric = PerformanceMetric(name="x", module="M", duration_ms=1)
    parsed = json.loads(metric.to_json())
    assert parsed["metric_id"] == metric.metric_id
    assert parsed["name"] == "x"


# --- Validation ---

def test_valid_metric_passes_validation():
    metric = PerformanceMetric(name="x", module="M", duration_ms=1)
    result = validate_metric(metric)
    assert isinstance(result, ValidationResult)
    assert result.valid is True
    assert result.errors == []


def test_missing_name_is_rejected():
    metric = PerformanceMetric(name="", module="M", duration_ms=1)
    result = validate_metric(metric)
    assert result.valid is False
    assert "name is required" in result.errors


def test_missing_module_is_rejected():
    metric = PerformanceMetric(name="x", module="", duration_ms=1)
    result = validate_metric(metric)
    assert result.valid is False
    assert "module is required" in result.errors


def test_negative_duration_is_rejected():
    metric = PerformanceMetric(name="x", module="M", duration_ms=-1)
    result = validate_metric(metric)
    assert result.valid is False
    assert any("duration_ms" in e for e in result.errors)


def test_zero_duration_is_valid():
    metric = PerformanceMetric(name="x", module="M", duration_ms=0)
    assert validate_metric(metric).valid is True


def test_invalid_status_is_rejected():
    metric = PerformanceMetric(name="x", module="M", duration_ms=1, status="bogus")
    result = validate_metric(metric)
    assert result.valid is False
    assert any("status must be one of" in e for e in result.errors)


def test_both_allowed_statuses_are_valid():
    for status in ALLOWED_STATUSES:
        metric = PerformanceMetric(name="x", module="M", duration_ms=1, status=status)
        assert validate_metric(metric).valid is True


def test_error_code_field_matches_brief_error_integration_example():
    metric = PerformanceMetric(
        name="strategy_execution", module="StrategyEngine", duration_ms=150,
        status="failed", error_code="STRATEGY_001",
    )
    data = metric.to_dict()
    assert data["status"] == "failed"
    assert data["error_code"] == "STRATEGY_001"
