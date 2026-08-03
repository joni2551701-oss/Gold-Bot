# ai/trading_analyst/

Phase 66.0 (AI Trading Analyst Foundation). Genuine new subpackage
inside the already-existing `ai/` top-level package (not a new
top-level package — see `docs/PHASE66_0_AUDIT.md`'s "Package
location" section for why this satisfies Rule 3).

## What this package is

- `models.py` — `TradingRiskLevel` (LOW/MEDIUM/HIGH),
  `TradingAnalysisInput` (primitive-only contract — see below),
  `TradingAnalysis` (symbol/direction/confidence/market_bias/
  risk_level/rr/summary/strengths/weaknesses/recommendation/
  educational_note).
- `access.py` — `is_trading_analyst_enabled_for(role, flags)`:
  Owner-only gate, mirrors `ai_layer/ai_service/assistant/access.py`'s shape exactly.
- `analyst_runtime.py` — `TradingAnalystRuntime.analyze()`: composes
  the existing `IntelligenceRuntime.run()` (Knowledge/Memory/
  Reasoning/Conversation grounding) and `ExplanationBuilder.build()`
  (TRADE-mode explanation) into one `TradingAnalysis`. No new
  Explanation engine, no new Intelligence Runtime.
- `content_adapter.py` — `prepare_content()`: composes
  `ContentEngine.create()` → `prepare_media_from_content()` →
  `broadcast_asset_from_content_and_media()` +
  `BroadcastManager.prepare_broadcast()`, the exact same sequence
  `IntelligenceRuntime.run()` already uses for its own CONTENT/MEDIA/
  BROADCAST stages. The one file in this package permitted to import
  `ai.content/`, `media/`, `broadcast/`.

## Why `TradingAnalysisInput` is primitive-only

Constitution Article 3 forbids `ai/` (every file, no exceptions) from
importing `decision/`, `risk/`, `execution/`. `TradingAnalysisInput`
follows the exact resolution `ai/explanation/explanation_input.py`
already established: every field is a primitive value a future,
separately-approved live-wiring phase would have `core/pipeline.py`
extract from its own `TradeDecision`/`RiskResult` — never those
objects themselves. This module is never wired into `core/pipeline.py`
this phase — foundation only. See `docs/PHASE66_0_AUDIT.md`'s "central
architectural resolution" for the full reasoning.

## What this package is not

No signal generation, no order placement, no Decision Engine
override — `TradingAnalystRuntime` only narrates already-supplied
values (Rule 2: AI Explains/Analyzes/Teaches/Reviews, never Decides).
`TradingAnalysis.recommendation` is a "WHY {direction}" narrative
string built from `TradingAnalysisInput.direction` (already decided
upstream), never a new BUY/SELL/NO_TRADE verdict. Never imports
`decision/`, `risk/`, `execution/`, `strategies/`, `signals/`,
`context/`, `monitoring/`, `database/`, or `telegram/` — zero
exceptions, permanently enforced by
`tests/ai/trading_analyst/test_trading_analyst_isolation.py`. No new
`ContentType`, no new `ExplanationBuilder`, no new
`IntelligenceRuntime` — all three existing classes are called via
their already-public methods only.

## Related

- `docs/PHASE66_0_AUDIT.md`, `docs/PHASE66_0_FREEZE.md` — full
  documentation of this phase.
- `docs/ai/AI_TRADING_ANALYST.md` — the user-facing architecture doc.
- `ai/explanation/`, `ai_layer/ai_engine/intelligence_runtime.py` — the two existing
  systems `analyst_runtime.py` composes.
- `ai/content/`, `media/`, `broadcast/` — the three existing systems
  `content_adapter.py` composes.
