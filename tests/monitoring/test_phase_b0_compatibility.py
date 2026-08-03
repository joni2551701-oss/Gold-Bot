"""
Phase B.0 Rule 2/Rule 3 compatibility tests -- monitoring never
exposes a method that could BUY/SELL/set SL/TP/Lot/Risk/Decision.
Observer-only: every public method on the new classes is
observe/collect/report, never mutate a trading concept.
"""

import ast
import pathlib

from core_layer.health_monitor.health_monitor import classify_health
from core_layer.health_monitor.performance_collector import PerformanceCollector
from core_layer.health_monitor.resource_monitor import get_resource_snapshot, record_process_start

FORBIDDEN_NAMES = (
    "buy", "sell", "set_stop_loss", "set_take_profit", "set_lot", "set_risk",
    "approve", "reject_trade", "execute", "place_order", "cancel_order",
    "override_decision", "force_signal",
)


def _monitoring_dir():
    return pathlib.Path(__file__).resolve().parents[2] / "core_layer" / "health_monitor"


def test_performance_collector_public_methods_are_observe_only():
    public_methods = {name for name in dir(PerformanceCollector) if not name.startswith("_") and callable(getattr(PerformanceCollector, name))}
    assert public_methods == {
        "record_signal", "record_decision", "record_trade", "record_reject",
        "record_error", "record_reconnect", "get_counts",
    }


def test_no_forbidden_trading_method_name_defined_anywhere_in_phase_b0_files():
    for filename in ("resource_monitor.py", "health_monitor.py", "performance_collector.py", "access.py"):
        py_file = _monitoring_dir() / filename
        tree = ast.parse(py_file.read_text(), filename=str(py_file))
        defined_names = {
            node.name for node in ast.walk(tree)
            if isinstance(node, (ast.ClassDef, ast.FunctionDef))
        }
        assert defined_names.isdisjoint(FORBIDDEN_NAMES), f"{py_file}: {defined_names & set(FORBIDDEN_NAMES)}"


def test_classify_health_is_a_pure_function_never_mutates_arguments():
    from core_layer.health_monitor.models import SystemHealth

    health = SystemHealth(status="RUNNING", uptime_seconds=1.0, data_connection="1/1 ONLINE", database_status="OK")
    before = (health.status, health.data_connection, health.database_status)
    classify_health(health)
    after = (health.status, health.data_connection, health.database_status)
    assert before == after


def test_get_resource_snapshot_never_writes_to_the_repository_it_reads():
    from unittest.mock import MagicMock

    repository = MagicMock()
    repository.get_restart_count.return_value = 1
    get_resource_snapshot(repository=repository)
    repository.record_process_start.assert_not_called()
    repository.record_error.assert_not_called()


def test_record_process_start_only_calls_record_process_start():
    from unittest.mock import MagicMock

    repository = MagicMock()
    record_process_start(repository=repository)
    repository.record_process_start.assert_called_once()
    repository.get_restart_count.assert_not_called()


def test_performance_collector_never_reads_signal_or_decision_content():
    """Every record_* method takes no arguments -- it counts an event happened, never inspects what the event was."""
    import inspect

    collector = PerformanceCollector()
    for name in ("record_signal", "record_decision", "record_trade", "record_reject", "record_error", "record_reconnect"):
        method = getattr(collector, name)
        params = inspect.signature(method).parameters
        assert len(params) == 0, f"{name} should take no arguments (pure event tally)"
