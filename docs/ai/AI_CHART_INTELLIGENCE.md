# AI Chart Intelligence (`ai/chart_intelligence/`)

Phase 66.1 (AI Chart Intelligence Foundation). Genuine new subpackage
inside the already-existing `ai/` top-level package, confirmed by
`docs/PHASE66_1_AUDIT.md`'s TASK 0 audit — the second phase in the
`66.x` AI Trading Intelligence sub-sequence, sitting immediately after
`ai/trading_analyst/` (Phase 66.0).

## Director's framing — the chart interpretation layer

Per the Director's own clarification of this phase's scope: Chart
Intelligence is not "look at one screenshot." It is the single
deterministic pipeline a future, separately-approved phase would route
every visual source through uniformly — TradingView screenshots, MT5
screenshots, Telegram images, PDF charts, and any other chart source —
rather than a TradingView-only tool. `ChartImageType` names that wide
vocabulary now, even though no Vision API call exists anywhere in this
phase (Rule 4).

## Position in the pipeline

The brief's own diagram:

```
Market → Trading Core → Trading Analyst → Chart Intelligence
   → Explanation → Content → Media
```

Chart Intelligence never decides — it reads an already-supplied chart
interpretation and narrates it, exactly the same READ ONLY posture
`ai/trading_analyst/` established for trade fields one phase earlier
(Rule 2). It never produces a BUY/SELL/NO_TRADE verdict, never opens a
trade, and never touches `decision/`, `risk/`, `execution/`,
`strategies/`, `signals/`, `context/`, or `monitoring/` (Rule 1/4).

## Why no field carries an image

Rule 4 forbids any Vision API, LLM, or image recognition model call
this phase — `ChartRuntime.analyze()` is a pure, deterministic
relay/transform over caller-supplied `ChartAnalysisInput` fields, the
same posture `ai/trading_analyst/analyst_runtime.py`'s `analyze()`
already established for trade fields. `ChartContext.image_hash` is a
content-hash *reference* only — this Foundation never stores image
bytes or a binary payload anywhere (Director Note 4). A future,
separately-approved live-wiring phase would compute that hash and the
interpreted fields upstream of this package (e.g. from a real Vision
provider's output) and pass them in as already-extracted primitives —
this phase does not perform that wiring.

## Model

- `models.py` — `ChartImageType` (TRADINGVIEW_SCREENSHOT/
  MT5_SCREENSHOT/TELEGRAM_IMAGE/PDF_CHART/OTHER, TASK 2/8's own visual
  source vocabulary), `ChartAnalysisType` (STRUCTURE/TREND/LIQUIDITY/
  ORDER_BLOCK/FVG/SUPPORT_RESISTANCE/GENERAL). `ChartAnalysisInput`
  (TASK 2's own input shape — every field caller-supplied, confidence
  0-100). `ChartAnalysis` (TASK 2's own exact output contract: symbol,
  timeframe, image_type, analysis_type, market_structure, trend,
  liquidity, order_blocks, fvg, support, resistance, confidence 0.0-1.0,
  notes, generated_at). `ChartContext` (TASK 3 — source, resolution,
  platform, created_at, image_hash; never the image itself) plus
  `has_minimum_context()`, a trivial, deterministic completeness check.

## Runtime (TASK 4/5/6/7)

`chart_runtime.py`'s `ChartRuntime` composes one real, unmodified
system — zero new business logic:

1. `analyze(data, role)` — a pure relay/transform from
   `ChartAnalysisInput` to `ChartAnalysis`; never calls a Vision API
   (Rule 4). Owner-gated.
2. `explain(chart, role, language)` — the "ChartAnalysis → Explanation"
   pipeline leg (TASK 5/6), composing the existing, unmodified
   `ExplanationBuilder.build()` (Phase 63.0/63.1) in `EDUCATION` mode —
   Chart Intelligence narrates an observation, it never produces a
   TRADE-mode verdict (Rule 2). No new Explanation engine.

`trading_analyst_adapter.py`'s `combined_explanation()` (TASK 5) is
the one file in this package permitted to import
`ai_layer.ai_engine.trading_analyst.models` — it composes an existing `TradingAnalysis`
(Phase 66.0) alongside this phase's own `ChartAnalysis` into a single
TRADE-mode `ExplanationOutput`, the pipeline's own "TradingAnalysis →
ChartAnalysis → Explanation" order. `direction`/`market_bias` are
relayed from `trading` unchanged — this function never produces its
own verdict either.

## Content Integration (TASK 6)

`content_adapter.py`'s `prepare_content()` composes the same three
real, unmodified Content → Media → Broadcast functions
`ai/trading_analyst/content_adapter.py` already uses:

1. `ContentEngine.create(ContentType.LIVE_ANALYSIS, ...)` — reused a
   second time (no new `ContentType` member).
2. `media_layer.content_manager.media_pipeline.prepare_media_from_content()` — with
   `MediaType.IMAGE` (Phase 63.0, reused as-is) rather than `TEXT`,
   since a Chart Analysis is visually sourced even though this
   Foundation never stores the image.
3. `media_layer.telegram_broadcast.broadcast_adapter.broadcast_asset_from_content_and_media()`
   + `BroadcastManager.prepare_broadcast()`.

`chart_analysis_to_content_body()` never returns an empty string — an
analysis with no populated fields falls back to a bare
`"{symbol} {timeframe} chart analysis"` line, the same non-empty-body
guarantee `TradingAnalysis.recommendation`'s always-present field gives
`ai/trading_analyst/content_adapter.py`.

This is the one file in `ai/chart_intelligence/` permitted to import
`ai.content/`, `media/`, `broadcast/`.

## Future Vision Provider Vocabulary (TASK 8)

`vision_provider_types.py`'s `ChartVisionProviderType` (NONE/
OPENAI_VISION/GEMINI_VISION/CLAUDE_VISION/LOCAL_VISION) is pure
vocabulary — no API client, no network call, no provider wiring
anywhere in this file. Additive to `ai/capabilities/capability.py`'s
already-existing `Capability.VISION`/`Capability.IMAGE` members (Phase
61.0): that enum names *what* the AI layer can be asked to do; this one
names *which vendor* a future phase might route to. No
`ai/providers/` file references this enum.

## Owner Mode (TASK 7)

`access.py`'s `is_chart_intelligence_enabled_for(role, flags)` requires
**both** `configuration.feature_flags.FeatureFlags.enable_chart_intelligence`
(default `False`) **and** `role == AIRole.OWNER`. Mirrors
`ai/trading_analyst/access.py`'s `is_trading_analyst_enabled_for()`
shape exactly — a dedicated flag, not a reuse of
`enable_trading_analyst` (Chart Intelligence is a sibling concern to
Trading Analyst, not a dependent one — `ai/chart_intelligence/` never
imports `assistant/` or `voice/`, and only `trading_analyst_adapter.py`
imports `ai_layer.ai_engine.trading_analyst`, and only type-only).

## What it is not

- No signal generation, no order placement, no Decision Engine
  override — Rule 2: Chart Intelligence reads and narrates, it never
  decides.
- No new `Capability` member, no reuse of
  `ai/access/access_control.py`'s `AccessControl` matrix.
- No new `ContentType`, `ExplanationMode`, `ExplanationBuilder`, or
  Chart/Vision Engine class — `LIVE_ANALYSIS` and `EDUCATION` mode are
  both reused as-is (Rule 3).
- No Vision API, LLM, or image recognition model call anywhere in this
  package — `OpenAI Vision`/`Gemini Vision`/`Claude Vision`/any real
  provider (Rule 4). `vision_provider_types.py` is metadata only.
- No image storage — no field anywhere in this package's models
  carries image bytes or a binary payload (Director Note 4).
- Never imports `decision/`, `risk/`, `execution/`, `strategies/`,
  `signals/`, `context/`, `monitoring/`, `database/`, `telegram/`,
  `assistant/`, or `voice/` — zero exceptions, permanently enforced by
  `tests/ai/chart_intelligence/test_chart_intelligence_isolation.py`.
- Not wired into `core/pipeline.py` or any Telegram command this
  phase — foundation only.

## Chart ID extension (Phase 66.2)

`ChartAnalysis` gained one new, additive, trailing-defaulted field —
`chart_id: str = ""` — plus `generate_chart_id()`, added under this
phase's own LOCK terms ("✅ extension" permitted) by Phase 66.2 (AI
Trade Journal Intelligence Foundation), per this phase's own Director
Note 1 from the LOCK review ("Kelajakda har ChartAnalysis ichida
chart_id bo'lishi foydali bo'ladi... Bu Journal va Replay tizimida
kerak bo'ladi"). `ChartRuntime.analyze()` now stamps every
`ChartAnalysis` it produces with a unique `chart_id`. See
`docs/PHASE66_2_AUDIT.md`'s "Chart ID extension" section and
`docs/ai/AI_TRADE_JOURNAL.md`.

## Related

- `docs/PHASE66_1_AUDIT.md`, `docs/PHASE66_1_FREEZE.md` — full
  documentation of this phase.
- `ai/chart_intelligence/README.md` — the package's own top-level
  README.
- `ai/trading_analyst/` — the sibling package this phase's
  `trading_analyst_adapter.py` composes with (type-only reads).
- `ai/explanation/`, `ai/content/`, `media/`, `broadcast/` — the four
  existing systems this package composes.
- `docs/ai/AI_TRADING_ANALYST.md` — the immediately preceding phase's
  own documentation, whose Article 3 resolution this phase's models
  follow exactly.
- `docs/ai/AI_TRADE_JOURNAL.md` — `ai/trade_journal/` (Phase 66.2),
  the next phase in the `66.x` sub-sequence, whose own
  `trading_analyst_adapter.py` reads `ChartAnalysis.chart_id` from
  this package's `models.py`, type-only.
