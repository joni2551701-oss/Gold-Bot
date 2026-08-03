"""GoldBot Core Owner Monitoring Alpha, TASK 4 -- core_layer/health_monitor/signal_monitor.py's new get_signal_health() tests. The pre-existing SignalMonitor/MonitorConfig/MonitorResult placeholder is untouched (Article 9) and not re-tested here."""

from unittest.mock import MagicMock

from core_layer.health_monitor.models import SignalHealth
from core_layer.health_monitor.signal_monitor import get_signal_health


def _repository(rows):
    repository = MagicMock()
    repository.get_signals_today.return_value = rows
    return repository


def test_get_signal_health_returns_signal_health():
    health = get_signal_health(signal_repository=_repository([]))
    assert isinstance(health, SignalHealth)


def test_get_signal_health_empty_table_all_zero():
    health = get_signal_health(signal_repository=_repository([]))
    assert health.total_signals == 0
    assert health.buy_count == 0
    assert health.sell_count == 0
    assert health.none_count == 0
    assert health.average_confidence == 0.0


def test_get_signal_health_counts_buy():
    rows = [{"direction": "BUY", "confidence_score": 0.8}]
    health = get_signal_health(signal_repository=_repository(rows))
    assert health.buy_count == 1
    assert health.sell_count == 0
    assert health.none_count == 0


def test_get_signal_health_counts_sell():
    rows = [{"direction": "SELL", "confidence_score": 0.6}]
    health = get_signal_health(signal_repository=_repository(rows))
    assert health.sell_count == 1
    assert health.buy_count == 0


def test_get_signal_health_counts_none_for_other_directions():
    rows = [{"direction": "", "confidence_score": 0.0}, {"direction": "REJECT", "confidence_score": 0.0}]
    health = get_signal_health(signal_repository=_repository(rows))
    assert health.none_count == 2
    assert health.buy_count == 0
    assert health.sell_count == 0


def test_get_signal_health_total_matches_row_count():
    rows = [
        {"direction": "BUY", "confidence_score": 0.7},
        {"direction": "SELL", "confidence_score": 0.5},
        {"direction": "", "confidence_score": 0.0},
    ]
    health = get_signal_health(signal_repository=_repository(rows))
    assert health.total_signals == 3
    assert health.buy_count + health.sell_count + health.none_count == 3


def test_get_signal_health_average_confidence():
    rows = [{"direction": "BUY", "confidence_score": 0.8}, {"direction": "SELL", "confidence_score": 0.4}]
    health = get_signal_health(signal_repository=_repository(rows))
    assert abs(health.average_confidence - 0.6) < 1e-9


def test_get_signal_health_ignores_non_numeric_confidence():
    rows = [{"direction": "BUY", "confidence_score": None}, {"direction": "SELL", "confidence_score": 0.5}]
    health = get_signal_health(signal_repository=_repository(rows))
    assert health.average_confidence == 0.5


def test_get_signal_health_never_raises_on_database_failure():
    repository = MagicMock()
    repository.get_signals_today.side_effect = Exception("boom")
    health = get_signal_health(signal_repository=repository)
    assert health.total_signals == 0
    assert health.average_confidence == 0.0


def test_get_signal_health_never_writes_to_repository():
    """Read-only: get_signal_health() never calls any mutating repository method."""
    repository = _repository([])
    get_signal_health(signal_repository=repository)
    repository.create_signal.assert_not_called()
    repository.update_signal_status.assert_not_called()
    repository.update_signal_result.assert_not_called()


def test_get_signal_health_default_construction_never_raises():
    """No repository override -- constructs a real SignalRepository() internally, never raises."""
    health = get_signal_health()
    assert isinstance(health, SignalHealth)


def test_get_signal_health_never_computes_a_verdict():
    from dataclasses import fields
    field_names = {f.name for f in fields(SignalHealth)}
    forbidden = {"signal", "decision", "verdict"}
    assert field_names.isdisjoint(forbidden)


def test_get_signal_health_missing_confidence_key_never_raises():
    rows = [{"direction": "BUY"}]
    health = get_signal_health(signal_repository=_repository(rows))
    assert health.total_signals == 1
    assert health.average_confidence == 0.0
