"""
Phase 17.2.2 — Runtime generate_signals() tests.

Phase 52 audit finding: same issue as test_signal_layer.py -- this
file defined run_test() (no test_ prefix), so pytest silently
collected zero tests from it despite the filename. Rewritten as real
pytest tests with the same scope.

Scope (per Director specification):
- Build a minimal ContextSnapshot (all collections empty).
- Instantiate SignalEngine and call generate_signals(context).
- Verify: no exception raised, result is a List, every element (if
  any) is a SignalCandidate. An empty list is a PASS.

Contract source (context/context_orchestrator.py): ContextSnapshot's
10 fields (Phase A5: added wyckoff_events) are all required (no
defaults) -- every field must be supplied, even as an empty list.
"""

from context.context_orchestrator import ContextSnapshot
from signals.signal_engine import SignalEngine
from signals.models import SignalCandidate


def _empty_context() -> ContextSnapshot:
    return ContextSnapshot(
        candles=[],
        structure=[],
        bos_events=[],
        choch_events=[],
        liquidity_zones=[],
        liquidity_sweeps=[],
        order_blocks=[],
        fair_value_gaps=[],
        amd_events=[],
        wyckoff_events=[],
    )


def test_generate_signals_with_empty_context_returns_empty_list():
    engine = SignalEngine()
    result = engine.generate_signals(_empty_context())

    assert isinstance(result, list)
    assert result == []


def test_generate_signals_never_raises_on_empty_context():
    engine = SignalEngine()
    # No exception is itself the assertion -- calling this at all is the test.
    engine.generate_signals(_empty_context())


def test_generate_signals_result_elements_are_signal_candidates_when_present():
    """
    Guards the return-type contract even though an all-empty context
    never produces candidates: if a future strategy change ever does
    generate output from minimal input, every element must still be a
    real SignalCandidate, not a dict/tuple/None.
    """
    engine = SignalEngine()
    result = engine.generate_signals(_empty_context())

    for item in result:
        assert isinstance(item, SignalCandidate)
