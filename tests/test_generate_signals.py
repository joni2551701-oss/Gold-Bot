"""
Phase 17.2.2 — Runtime Generate Signals Test.

Scope (per Director specification):
- Build a minimal mock ContextSnapshot (all collections empty).
- Instantiate SignalEngine and call generate_signals(mock_context).
- Verify: no exception raised, result is a List, every element (if any)
  is a SignalCandidate. An empty list is a PASS.

Explicitly OUT of scope for this phase:
- Real market data (TwelveData), AI (Gemini), Telegram, MT5.
- Non-empty mock data / strategy logic quality (BUG-004/005/006
  verification with real setups) — that belongs to a later phase.
- main.py changes.
- GitHub Actions workflow creation.

Contract source (confirmed this session, context/context_orchestrator.py):
    ContextSnapshot(
        candles, structure, bos_events, choch_events,
        liquidity_zones, liquidity_sweeps, order_blocks,
        fair_value_gaps, amd_events
    )
All fields are required (no defaults) — every field must be supplied,
even as an empty list.
"""

import sys
import traceback


def run_test() -> bool:
    print("=" * 60)
    print("Phase 17.2.2 — Runtime generate_signals() Test")
    print("=" * 60)

    # Step 1: Build mock ContextSnapshot
    try:
        print("\n[1/3] Building mock ContextSnapshot (all fields empty) ...")
        from context.context_orchestrator import ContextSnapshot

        mock_context = ContextSnapshot(
            candles=[],
            structure=[],
            bos_events=[],
            choch_events=[],
            liquidity_zones=[],
            liquidity_sweeps=[],
            order_blocks=[],
            fair_value_gaps=[],
            amd_events=[],
        )
        print("      OK: ContextSnapshot constructed with all 9 required fields.")

    except Exception:
        print("\nFAIL: Could not construct mock ContextSnapshot.")
        traceback.print_exc()
        return False

    # Step 2: Instantiate SignalEngine
    try:
        print("\n[2/3] Instantiating SignalEngine ...")
        from signals.signal_engine import SignalEngine
        from signals.models import SignalCandidate

        engine = SignalEngine()
        print("      OK: SignalEngine() instantiated.")

    except Exception:
        print("\nFAIL: Could not instantiate SignalEngine.")
        traceback.print_exc()
        return False

    # Step 3: Call generate_signals() and validate result
    try:
        print("\n[3/3] Calling engine.generate_signals(mock_context) ...")
        result = engine.generate_signals(mock_context)
        print(f"      OK: generate_signals() returned without raising an exception.")

        if not isinstance(result, list):
            print(f"FAIL: Expected result type 'list', got '{type(result).__name__}'.")
            return False
        print(f"      OK: Result is a list (length={len(result)}).")

        if len(result) == 0:
            print("      INFO: Empty list returned — this is a PASS "
                  "(expected with an all-empty mock context).")
        else:
            for i, item in enumerate(result):
                if not isinstance(item, SignalCandidate):
                    print(f"FAIL: Element {i} is not a SignalCandidate "
                          f"(got '{type(item).__name__}').")
                    return False
            print(f"      OK: All {len(result)} element(s) are valid SignalCandidate instances.")

    except Exception:
        print("\nFAIL: generate_signals() raised an exception.")
        traceback.print_exc()
        return False

    print("\n" + "=" * 60)
    print("RESULT: PASS — generate_signals() executed successfully "
          "with a mock ContextSnapshot.")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
