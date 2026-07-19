# Phase 66.1 Audit — AI Chart Intelligence Foundation (TASK 0)

Governed by `docs/constitution/CONSTITUTION.md` Article 11 (Foundation
Reuse Law). This is the mandatory TASK 0 audit for Phase 66.1 — before
any new module is created, the packages the brief names must be
checked for an existing Chart Analysis, Image Contract, Chart Model,
or Visual Context.

## Director's framing

The Director's own brief clarifies the intent behind Phase 66.1: Chart
Intelligence is not "look at one screenshot" — it is the **chart
interpretation layer** of GoldBot's architecture, the single
deterministic pipeline a future phase would route TradingView
screenshots, MT5 screenshots, Telegram images, PDF charts, and any
other visual source through uniformly. This audit and the resulting
package are built with that framing: the models below carry an
`image_type` vocabulary wide enough for all of these sources, not a
TradingView-only shape.

## Packages audited

### `ai/trading_analyst/` (Phase 66.0)

`TradingAnalysisInput`/`TradingAnalysis` (`models.py`) are trade-level
contracts — `market_bias`, `entry`/`stop_loss`/`take_profit`,
`risk_level`, `strengths`/`weaknesses` — with no chart-visual fields
(`market_structure`, `trend`, `liquidity`, `order_blocks`, `fvg`,
`support`/`resistance`, `image_type`). No Chart Analysis or Image
Contract here. `TradingAnalystRuntime.analyze()` composes
`IntelligenceRuntime`/`ExplanationBuilder` only — no image/vision
awareness anywhere in the package (confirmed via
`tests/ai/trading_analyst/test_trading_analyst_isolation.py`, which
already asserts zero `media`/`ai.content` imports outside
`content_adapter.py`). **Reused, not duplicated**: Phase 66.1's own
"Trading Analyst Integration" (TASK 5) reads `TradingAnalysis` type-only
from this package's existing, unmodified `models.py`.

### `ai/explanation/`

`ExplanationInput`/`ExplanationOutput`/`ExplanationBuilder` are
primitive-only and modality-agnostic — `ExplanationMode` has exactly
three values (`TRADE`/`NO_TRADE`/`EDUCATION`), none chart-specific,
and no field carries an image reference. This is the correct, already-
audited composition point Phase 66.1's own `chart_runtime.py` and
`trading_analyst_adapter.py` will reuse (matching the precedent
`ai/trading_analyst/analyst_runtime.py` already established) — **not**
a place to add a fourth "CHART" `ExplanationMode`, since `EDUCATION`
mode's existing `concept`/`example`/`lesson` fields already fit a
narrated chart observation without any contract change.

### `media/`

`MediaType` (`media_types.py`) already has an `IMAGE` member (Phase
63.0) — reused as-is for Chart Intelligence's own Content/Media
integration (TASK 6), no new `MediaType`. `MediaAsset`/
`media_pipeline.prepare_media_from_content()` (Phase 63.7) are
content-shaped, not image-shaped — they carry `content_id`/
`media_type`/`title`/`description`, never image bytes or a hash. No
Chart-specific model exists here.

### `ai/content/` (`content/` per the brief's own naming, confirmed to
mean `ai/content/` — see `docs/PHASE63_0_FOUNDATION_AUDIT.md`'s
already-recorded correction that there is no separate top-level
`content/` package)

`ContentType` (`content_types.py`) has nine members; none is
chart-specific. `LIVE_ANALYSIS` (Phase 63.8, already reused by Phase
66.0's own `TradingAnalysis` content integration) is generic enough to
carry a Chart Analysis's content body too — reused again here (TASK 6),
no new `ContentType` member, per the Module Reuse Principle.

### `knowledge/`

Six static categories (`smc.py`, `wyckoff.py`, `psychology.py`,
`risk.py`, `examples.py`, `faq.py`) — text-based lesson content, no
image/chart contract. Not composed by this phase (Chart Intelligence's
pipeline position, per the brief's own diagram, sits after Trading
Analyst and before Explanation — Knowledge is reached, if at all, only
indirectly through `IntelligenceRuntime`, which this phase does not
call, matching Rule 4's "no LLM/Vision API" scope).

### `ai/memory/`

`MemoryEntry`/`MemoryScope` (`models.py`) are text/primitive value
storage — no image or chart-specific scope exists (`MemoryScope`'s six
categories are TRADE_HISTORY/USER_PREFERENCE/CONVERSATION/LEARNING/
FUNDAMENTAL/SYSTEM_STATE, none chart-shaped). Not composed by this
phase, for the same reason as `knowledge/` above.

### `ai/reasoning/`

`ReasoningResult`/`ReasoningStep` (`models.py`) are deterministic
Knowledge/Memory-linking records — no chart or image field. Not
composed by this phase.

### `ai/providers/base_provider.py` — related but distinct

`BaseAIProvider` already declares an abstract `vision(prompt,
image_ref)` method and `Capability.VISION`/`Capability.IMAGE` already
exist in `ai/capabilities/capability.py` (Phase 61.0's original fixed
vocabulary). This is the **generic, cross-capability AI provider
contract** — every placeholder provider inherits it, unused, exactly
like `chat()`/`image()`/`voice()`. It is not a Chart Analysis, Image
Contract, or Visual Context: it carries no `market_structure`/`trend`/
`order_blocks` shape, and calling it would violate Rule 4 (no Vision
API this phase) directly. TASK 8's "Future Compatibility" vocabulary is
additive to this existing `VISION`/`IMAGE` capability naming, not a
duplicate of it — `ai/chart_intelligence/vision_provider_types.py`
names *which vendor* a future phase might route to, a narrower question
`Capability.VISION` itself does not answer (the same relationship
`ai/providers/provider_capabilities.py` already has to `Capability`
generally).

## Answers to the audit's four questions

1. **Chart Analysis mavjudmi?** No. No dataclass anywhere in the repo
   carries `market_structure`/`trend`/`liquidity`/`order_blocks`/`fvg`/
   `support`/`resistance` together.
2. **Image Contract mavjudmi?** No structured one. `MediaType.IMAGE`
   is a vocabulary member, not a contract with fields; `BaseAIProvider.vision()`
   is a generic method signature, not a data contract.
3. **Chart Model mavjudmi?** No.
4. **Visual Context mavjudmi?** No. Nothing in the repo carries
   `source`/`resolution`/`platform`/`image_hash` together as a single
   metadata contract.

## Conclusion — genuine gap, TASK 1's package decision

Per Constitution Article 11 step 2 ("can an existing module be
extended without breaking its contract"): `ai/trading_analyst/`'s
contract is trade-level, not chart-visual — extending it would couple
two genuinely different concerns (a Decision Engine's trade breakdown
vs. a chart's own structural reading) into one dataclass, the same
"too narrow/too general-purpose to extend" reasoning Phase 66.0's own
audit used to justify a new subpackage rather than extending
`ai/explanation/`. `media/`'s `MediaAsset` is a delivery-shaped
contract (`content_id`/`status`/`title`), not an interpretation-shaped
one, and extending it with `market_structure`/`trend`/etc. would
misuse a package whose whole job (Phase 63.7) is asset preparation for
delivery, not chart reading.

**Decision: `ai/chart_intelligence/` — a new subpackage inside the
already-existing `ai/` top-level package** (Rule 3 forbids a new
top-level Chart *Engine*; a subpackage inside `ai/`, following the
exact precedent `ai/trading_analyst/` set one phase ago, is not that).

## Related documents

- `docs/PHASE66_0_AUDIT.md` — the immediately preceding phase's own
  audit, whose "package location" reasoning this audit mirrors.
- `docs/ai/AI_CHART_INTELLIGENCE.md` — this phase's own full
  documentation (TASK 10).
- `docs/constitution/CONSTITUTION.md` Article 3 — the zero-exception
  `ai/` → `decision/`/`risk/`/`execution/`/`strategies/`/`signals/`/
  `context/`/`monitoring/` import rule this phase's models are checked
  against, same as Phase 66.0.
