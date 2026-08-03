# ai_layer / knowledge_ai / learning_loop

**Module**

## Purpose

No module-level docstring was present in `__init__.py` at the time this file was generated (2026-08-03) by the Engineering Standard v1.0 rollout (Director Order No. 012/013). This is a placeholder pending a real description from a future Development Phase -- content below is limited to what could be verified mechanically from the code.

## Files

- `__init__.py`
- `confidence.py` -- Learning Layer — Confidence Engine (Phase 60.7: Adaptive Intelligence
- `models.py` -- Learning Layer — Learning Data Model (Phase 60.6: Learning Loop
- `outcome_analyzer.py` -- Learning Layer — Trade Outcome Analyzer (Phase 60.6: Learning Loop
- `pattern_detector.py` -- Learning Layer — Failure/Success Pattern Detector (Phase 60.6:
- `regime_memory.py` -- Learning Layer — Market Regime Memory (Phase 60.7: Adaptive
- `trade_event_bridge.py` -- Learning Layer — Trade Event Bridge (Phase 60.7: Adaptive

## Responsibilities

See `CONTRACTS.md` and `MODULE_MAP.md` in this directory.

## Dependencies

See `CONTRACTS.md` in this directory for cross-layer dependencies (mechanically derived from actual imports).

## Public API

- `confidence.py`: class `PatternConfidence`
- `confidence.py`: function `compute_pattern_confidence()`
- `models.py`: class `LearningRecord`
- `models.py`: function `generate_learning_record_id()`
- `models.py`: function `create_learning_record()`
- `outcome_analyzer.py`: class `TradeAnalysis`
- `outcome_analyzer.py`: function `analyze_trade_result()`
- `pattern_detector.py`: class `PatternInsight`
- `pattern_detector.py`: function `group_records_for_patterns()`
- `pattern_detector.py`: function `detect_patterns()`
- `pattern_detector.py`: function `filter_high_failure_patterns()`
- `pattern_detector.py`: function `filter_high_success_patterns()`
- `pattern_detector.py`: function `format_pattern_insight()`
- `regime_memory.py`: class `RegimeObservation`
- `regime_memory.py`: class `RegimeMemory`
- `regime_memory.py`: function `record_from_context()`
- `regime_memory.py`: function `format_regime_summary()`
- `trade_event_bridge.py`: function `build_learning_record_from_trade()`
- `trade_event_bridge.py`: function `bridge_closed_trade()`

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Documentation standardization only -- content mechanically derived from existing code, not authored from scratch.*
