"""
Phase 59.9, TASK 4 -- core_layer/emergency/circuit_breaker.py tests. Pure
functions -- no database, no fresh_database dependency needed (harmless
either way since it's autouse).
"""

from core_layer.emergency.circuit_breaker import (
    CircuitBreakerInput,
    CircuitDecision,
    evaluate_circuit,
)


def test_default_input_allows():
    result = evaluate_circuit(CircuitBreakerInput())
    assert result.decision == CircuitDecision.ALLOW
    assert result.reason is None


def test_three_consecutive_losses_blocks():
    result = evaluate_circuit(CircuitBreakerInput(loss_count=3))
    assert result.decision == CircuitDecision.BLOCK
    assert "3 consecutive losses" in result.reason


def test_two_consecutive_losses_does_not_block():
    result = evaluate_circuit(CircuitBreakerInput(loss_count=2))
    assert result.decision != CircuitDecision.BLOCK


def test_execution_error_blocks_regardless_of_other_signals():
    result = evaluate_circuit(CircuitBreakerInput(execution_error=True))
    assert result.decision == CircuitDecision.BLOCK
    assert "execution error" in result.reason


def test_daily_drawdown_at_limit_blocks():
    result = evaluate_circuit(CircuitBreakerInput(daily_drawdown=0.10))
    assert result.decision == CircuitDecision.BLOCK


def test_daily_drawdown_approaching_limit_warns():
    result = evaluate_circuit(CircuitBreakerInput(daily_drawdown=0.06))
    assert result.decision == CircuitDecision.WARNING


def test_degraded_api_status_warns():
    result = evaluate_circuit(CircuitBreakerInput(api_status="DEGRADED"))
    assert result.decision == CircuitDecision.WARNING
    assert "DEGRADED" in result.reason


def test_custom_thresholds_are_respected():
    result = evaluate_circuit(CircuitBreakerInput(loss_count=1), max_consecutive_losses=1)
    assert result.decision == CircuitDecision.BLOCK


def test_execution_error_outranks_loss_count_reason():
    result = evaluate_circuit(CircuitBreakerInput(loss_count=5, execution_error=True))
    assert "execution error" in result.reason


def test_circuit_breaker_input_is_frozen():
    signal = CircuitBreakerInput()
    try:
        signal.loss_count = 99
        assert False, "CircuitBreakerInput must be immutable"
    except AttributeError:
        pass
