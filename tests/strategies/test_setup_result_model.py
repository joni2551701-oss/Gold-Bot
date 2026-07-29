"""Setup layer — StrategyResult model + SignalCandidate adapter (TASK-CORE-007)."""

from types import SimpleNamespace

from strategies.result import StrategyResult, StrategyDirection, SetupStatus, compute_rr


def test_default_result_is_no_setup():
    r = StrategyResult(strategy_name="X")
    assert r.status is SetupStatus.NO_SETUP
    assert r.direction is StrategyDirection.NEUTRAL
    assert r.confidence == 0.0
    assert r.has_setup is False


def test_none_and_invalid_factories():
    n = StrategyResult.none("X", "nothing")
    assert n.status is SetupStatus.NO_SETUP and n.reasons == ["nothing"]
    i = StrategyResult.invalid("X", "bad ctx")
    assert i.status is SetupStatus.INVALID and i.reasons == ["bad ctx"]


def test_to_dict_is_json_safe():
    r = StrategyResult(strategy_name="X", direction=StrategyDirection.LONG,
                       confidence=0.7, entry_zone=(1.0, 2.0), invalidation=0.5,
                       rr=2.0, reasons=["a"], status=SetupStatus.SETUP_FOUND, metadata={"k": 1})
    d = r.to_dict()
    assert d["direction"] == "long"
    assert d["status"] == "setup_found"
    assert d["entry_zone"] == [1.0, 2.0]


def test_compute_rr():
    assert compute_rr(100, 95, 110) == 2.0   # reward 10 / risk 5
    assert compute_rr(100, 100, 110) is None  # zero risk


def test_from_signal_candidate_adapter():
    candidate = SimpleNamespace(
        signal_type=SimpleNamespace(name="BUY"), entry=100.0, stop_loss=95.0,
        take_profit=110.0, strategy_name="LIQ", confidence=0.8, reasons=["swept"],
    )
    r = StrategyResult.from_signal_candidate(candidate, strategy_name="LIQUIDITY_SETUP")
    assert r.strategy_name == "LIQUIDITY_SETUP"
    assert r.direction is StrategyDirection.LONG
    assert r.status is SetupStatus.SETUP_FOUND
    assert r.entry_zone == (100.0, 100.0)
    assert r.invalidation == 95.0
    assert r.rr == 2.0
    assert r.reasons == ["swept"]


def test_from_signal_candidate_sell_maps_to_short():
    candidate = SimpleNamespace(signal_type=SimpleNamespace(name="SELL"), entry=100.0,
                                stop_loss=105.0, take_profit=90.0, strategy_name="S",
                                confidence=0.6, reasons=[])
    r = StrategyResult.from_signal_candidate(candidate)
    assert r.direction is StrategyDirection.SHORT
