# AI Trading Analyst (`ai/trading_analyst/`)

Phase 66.0 (AI Trading Analyst Foundation). Genuine new subpackage
inside the already-existing `ai/` top-level package, confirmed by
`docs/PHASE66_0_AUDIT.md`'s TASK 0 audit. This is the first phase in
the `66.x` AI Trading Intelligence sub-sequence: GoldBot's AI layer
begins narrating the Trading Core's own already-made decisions like a
professional analyst, rather than only holding general-purpose
conversational Foundation.

## Position in the pipeline

The brief's own diagram:

```
Market → Trading Core → Signal → Decision → Risk → Execution →
Trade Monitor → AI Trading Analyst → Explanation → Content → Media → Broadcast
```

AI Trading Analyst never decides — it explains, analyzes, teaches, and
reviews an **already-made** Trading Core result (Rule 2). It never
overrides the Decision Engine, never opens an order, never touches
`decision/`, `risk/`, `execution/`, `strategies/`, `signals/`,
`context/`, or `monitoring/` (Rule 1/4).

## Why `TradingAnalysisInput` is primitive-only

Constitution Article 3 is absolute: `ai/` (every file, no exceptions)
must never import `decision/`, `risk/`, or `execution/`. This appears
to conflict with the brief's own diagram — it does not, once resolved
the same way `ai/explanation/explanation_input.py`'s own
`ExplanationInput` already resolved it: `TradingAnalysisInput`'s every
field is a primitive (`str`/`float`/`Sequence[str]`) or an enum
defined in this same package — never a `decision_layer.decision_engine.models.TradeDecision`,
`risk_layer.risk_engine.risk_manager.RiskResult`, or `signal_layer.signal_builder.models.SignalCandidate`
object reference. A future, separately-approved live-wiring phase
would have `core/pipeline.py` (the only place already permitted to
see every trading layer's own output) extract these plain values from
its own `TradeDecision`/`RiskResult` after the Trade Monitor stage —
this phase does not wire that call, foundation only. See
`docs/PHASE66_0_AUDIT.md`'s "central architectural resolution" for the
full reasoning.

## Model

- `models.py` — `TradingRiskLevel` (LOW/MEDIUM/HIGH), caller-supplied,
  never computed by this package. `TradingAnalysisInput`: `symbol`,
  `direction` (the Decision Engine's own already-decided action,
  narrated only), `market_bias`, `confidence` (0-100),
  `signal_score`/`htf_score`/`risk_score`/`ai_score` (relayed
  `TradeDecision` component breakdown), `risk_level`, `risk_reward`,
  `entry`/`stop_loss`/`take_profit`, `technical_reason`/`risk_reason`/
  `invalidation`, Market Analysis fields (`session`/`htf_trend`/
  `liquidity_note`/`structure_note`/`volume_note`/`volatility_note`,
  TASK 4), `strengths`/`weaknesses`, `language`. `TradingAnalysis`
  (TASK 2's own exact field list): `symbol`, `direction`, `confidence`
  (0.0-1.0), `market_bias`, `risk_level`, `rr`, `summary`, `strengths`,
  `weaknesses`, `recommendation`, `educational_note`, `generated_at`.

## Runtime (TASK 3/4/5/6/7)

`analyst_runtime.py`'s `TradingAnalystRuntime.analyze()` composes two
real, unmodified systems — zero new business logic:

1. `IntelligenceRuntime.run(topic=symbol)` (Phase 64.0, unmodified) —
   Knowledge/Memory/Reasoning/Conversation grounding, exactly TASK 3's
   own pipeline order. Informational only; never blocks or alters this
   method's own output.
2. `ExplanationBuilder.build()` (Phase 63.0/63.1, unmodified) — a
   `TRADE`-mode `ExplanationInput` assembled from
   `TradingAnalysisInput`'s own fields. No new Explanation engine
   (TASK 7).

`TradingAnalysis.recommendation` (TASK 5, "WHY BUY / WHY SELL / WHY
WAIT / WHY SKIP") is a narrative string built from
`TradingAnalysisInput.direction` — already decided upstream, never a
new BUY/SELL/NO_TRADE verdict (Director Note 1).
`TradingAnalysis.educational_note` (TASK 6) is relayed directly from
`ExplanationOutput.educational_note` — no new teaching logic.

Owner-gated: `analyze()` re-checks
`ai.trading_analyst.access.is_trading_analyst_enabled_for()` itself,
returning `None` for a denied caller before either composed system is
ever touched.

## Content Integration (TASK 8)

`content_adapter.py`'s `prepare_content()` composes three real,
unmodified functions/methods — the exact same Content → Media →
Broadcast sequence `IntelligenceRuntime.run()` already uses for its
own CONTENT/MEDIA/BROADCAST stages:

1. `ContentEngine.create(ContentType.LIVE_ANALYSIS, ...)` (Phase 61.5,
   unmodified) — `ContentType.LIVE_ANALYSIS` (Phase 63.8) is reused
   as-is, no new `ContentType` member.
2. `media.media_pipeline.prepare_media_from_content()` (Phase 63.7,
   unmodified).
3. `broadcast.broadcast_adapter.broadcast_asset_from_content_and_media()`
   + `BroadcastManager.prepare_broadcast()` (Phase 63.8, unmodified).

This is the one file in `ai/trading_analyst/` permitted to import
`ai.content/`, `media/`, `broadcast/` — `models.py`, `access.py`, and
`analyst_runtime.py` never do.

## Owner Mode (TASK 9)

`access.py`'s `is_trading_analyst_enabled_for(role, flags)` requires
**both** `configuration.feature_flags.FeatureFlags.enable_trading_analyst`
(default `False`) **and** `role == AIRole.OWNER`. Mirrors
`assistant/access.py`'s `is_personal_ai_enabled_for()` shape exactly —
a dedicated flag, not a reuse of `enable_personal_ai` (Trading Analyst
is a sibling concern to Personal AI Assistant, not a dependent one;
`ai/trading_analyst/` never imports `assistant/` or `voice/`).

## What it is not

- No signal generation, no order placement, no Decision Engine
  override — Rule 2: AI Explains/Analyzes/Teaches/Reviews, never
  Decides.
- No new `Capability` member, no reuse of
  `ai/access/access_control.py`'s `AccessControl` matrix (would grant
  `ADMIN` too).
- No new `ContentType`, `ExplanationBuilder`, or `IntelligenceRuntime`
  — all three existing classes are called via their already-public
  methods only.
- Never imports `decision/`, `risk/`, `execution/`, `strategies/`,
  `signals/`, `context/`, `monitoring/`, `database/`, `telegram/`,
  `assistant/`, or `voice/` — zero exceptions, permanently enforced by
  `tests/ai/trading_analyst/test_trading_analyst_isolation.py`.
- Not wired into `core/pipeline.py` or any Telegram command this
  phase — foundation only, same "not yet live-wired" posture every
  Owner-facing foundation in this codebase has followed since Phase
  59.x.

## Related

- `docs/PHASE66_0_AUDIT.md`, `docs/PHASE66_0_FREEZE.md` — full
  documentation of this phase.
- `ai/trading_analyst/README.md` — the package's own top-level README.
- `ai/explanation/`, `ai/intelligence_runtime.py` — the two existing
  systems `analyst_runtime.py` composes.
- `ai/content/`, `media/`, `broadcast/` — the three existing systems
  `content_adapter.py` composes.
- `docs/ai/AI_CHART_INTELLIGENCE.md` — `ai/chart_intelligence/` (Phase
  66.1), the next phase in the `66.x` sub-sequence; its own
  `trading_analyst_adapter.py` reads `TradingAnalysis` from this
  package's `models.py`, type-only.
- `docs/ai/AI_TRADE_JOURNAL.md` — `ai/trade_journal/` (Phase 66.2),
  whose own `trading_analyst_adapter.py` also reads `TradingAnalysis`
  from this package's `models.py`, type-only.
- `docs/constitution/CONSTITUTION.md` Article 3 — the zero-exception
  rule this package's own dependency direction is checked against.
