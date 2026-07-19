# AI Chart Intelligence (`ai/chart_intelligence/`)

Phase 66.1 (AI Chart Intelligence Foundation). Genuine new subpackage
inside the already-existing `ai/` top-level package, confirmed by
`docs/PHASE66_1_AUDIT.md`'s TASK 0 audit — the second phase in the
`66.x` AI Trading Intelligence sub-sequence, sitting immediately after
`ai/trading_analyst/` (Phase 66.0) in the pipeline.

## What this package is

The **chart interpretation layer** — the single deterministic pipeline
a future, separately-approved phase would route TradingView
screenshots, MT5 screenshots, Telegram images, and PDF charts through
uniformly (`ChartImageType`). This phase builds the contract and the
pipeline shape only; no Vision API, LLM, or image recognition model is
called anywhere in this package (Rule 4).

## What this package is not

- No signal generation, no BUY/SELL/NO_TRADE verdict of any kind
  (Rule 2 — READ ONLY).
- No Vision API call — `OpenAI Vision`/`Gemini Vision`/`Claude Vision`/
  any real image recognition model (Rule 4). `vision_provider_types.py`
  is pure future-compatible vocabulary only.
- No image storage — `ChartContext.image_hash` is a content-hash
  *reference*, never image bytes or a binary payload (Director Note 4).
- No new Chart Engine, Vision Engine, Image AI, or CV Engine top-level
  package (Rule 3) — this is a subpackage inside the existing `ai/`.
- Never imports `decision/`, `risk/`, `execution/`, `strategies/`,
  `signals/`, `context/`, `monitoring/`, `database/`, `telegram/`,
  `assistant/`, or `voice/` — zero exceptions, permanently enforced by
  `tests/ai/chart_intelligence/test_chart_intelligence_isolation.py`.
- Not wired into `core/pipeline.py` or any Telegram command this
  phase — foundation only.

## Related

- `docs/PHASE66_1_AUDIT.md`, `docs/PHASE66_1_FREEZE.md` — full
  documentation of this phase.
- `docs/ai/AI_CHART_INTELLIGENCE.md` — the full subsystem documentation.
- `ai/trading_analyst/` — the sibling package this phase's
  `trading_analyst_adapter.py` composes with (type-only reads).
- `ai/explanation/`, `ai/content/`, `media/`, `broadcast/` — the four
  existing systems this package composes.
