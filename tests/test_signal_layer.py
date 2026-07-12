"""
Phase 17.2.1 — Signal Layer Import & Instantiation Runtime Test.

Scope (per Director specification):
- Verify import chain (no ModuleNotFoundError / ImportError)
- Verify class instantiation (constructors execute without error)
- Verify dependency wiring (SignalEngine -> StrategyManager -> strategies)

Explicitly OUT of scope for this phase:
- generate_signals() execution (Phase 17.2.2)
- Mock ContextSnapshot (Phase 17.2.2)
- Strategy logic / signal quality (BUG-004, BUG-005, BUG-006 verification)
- TwelveData, Gemini, Telegram, MT5 — none of these are touched.
"""

import sys
import traceback


def run_test() -> bool:
    print("=" * 60)
    print("Phase 17.2.1 — Signal Layer Import & Instantiation Test")
    print("=" * 60)

    # Step 1: Import chain
    try:
        print("\n[1/3] Importing signals.signal_engine.SignalEngine ...")
        from signals.signal_engine import SignalEngine
        print("      OK: SignalEngine imported successfully.")

        print("[1/3] Importing signals.strategy_manager.StrategyManager ...")
        from strategies.strategy_manager import StrategyManager
        print("      OK: StrategyManager imported successfully.")

        print("[1/3] Importing signals.liquidity_strategy.LiquidityStrategy ...")
        from strategies.liquidity_strategy import LiquidityStrategy
        print("      OK: LiquidityStrategy imported successfully.")

        print("[1/3] Importing signals.fvg_strategy.FVGStrategy ...")
        from strategies.fvg_strategy import FVGStrategy
        print("      OK: FVGStrategy imported successfully.")

        print("[1/3] Importing signals.amd_strategy.AMDStrategy ...")
        from strategies.amd_strategy import AMDStrategy
        print("      OK: AMDStrategy imported successfully.")

    except Exception:
        print("\nFAIL: Import chain broken.")
        traceback.print_exc()
        return False

    # Step 2: Standalone instantiation of each strategy
    try:
        print("\n[2/3] Instantiating individual strategy classes ...")
        _ = LiquidityStrategy()
        print("      OK: LiquidityStrategy() instantiated.")
        _ = FVGStrategy()
        print("      OK: FVGStrategy() instantiated.")
        _ = AMDStrategy()
        print("      OK: AMDStrategy() instantiated.")
    except Exception:
        print("\nFAIL: Individual strategy instantiation failed.")
        traceback.print_exc()
        return False

    # Step 3: Full dependency chain via SignalEngine
    try:
        print("\n[3/3] Instantiating SignalEngine (full dependency wiring) ...")
        engine = SignalEngine()
        print("      OK: SignalEngine() instantiated.")

        if not isinstance(engine.strategy_manager, StrategyManager):
            print("FAIL: engine.strategy_manager is not a StrategyManager instance.")
            return False
        print("      OK: engine.strategy_manager is a valid StrategyManager instance.")

        expected_types = {LiquidityStrategy, FVGStrategy, AMDStrategy}
        actual_types = {type(s) for s in engine.strategy_manager.strategies}
        if actual_types != expected_types:
            print(f"FAIL: Strategy registration mismatch. "
                  f"Expected {expected_types}, got {actual_types}.")
            return False
        print("      OK: All 3 strategies registered correctly in StrategyManager.")

    except Exception:
        print("\nFAIL: SignalEngine dependency wiring failed.")
        traceback.print_exc()
        return False

    print("\n" + "=" * 60)
    print("RESULT: PASS — Signal Layer import chain and instantiation verified.")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
