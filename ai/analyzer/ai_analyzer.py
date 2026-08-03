"""
Phase 55 AI folder restructure — new professional-layout entry point.

The canonical implementation stays at ai/ai_analyzer.py, unmoved. Five
production modules already depend on that exact import path
(core/pipeline.py, decision_layer/decision_engine/decision_engine.py, decision_layer/decision_engine/models.py,
platform_layer/telegram/signal_formatter.py, plus tests/conftest.py) -- physically
relocating it would be the "katta migration" this phase's spec
explicitly says to avoid when the move is risky. This file is the
compatibility layer in the *other* direction: the new, professional
ai/analyzer/ path re-exports the untouched original, so
`from ai.analyzer.ai_analyzer import AIAnalyzer` works going forward
without a single existing import site being touched.
"""

from ai.ai_analyzer import AIAnalyzer, AIAnalysisResult

__all__ = ["AIAnalyzer", "AIAnalysisResult"]
