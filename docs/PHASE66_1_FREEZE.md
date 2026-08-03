# Phase 66.1 Freeze — AI Chart Intelligence Foundation

Governed by `docs/constitution/CONSTITUTION.md` Article 12 (Architecture
Evolution Law). This freeze closes Phase 66.1, the second phase in the
`66.x` AI Trading Intelligence sub-sequence, sitting immediately after
`ai/trading_analyst/` (Phase 66.0). Per the Director's own clarified
framing: Chart Intelligence is the *chart interpretation layer* —
a single deterministic pipeline a future, separately-approved phase
would route every visual source (TradingView screenshots, MT5
screenshots, Telegram images, PDF charts) through uniformly, not a
single-screenshot tool. It records what was actually built, what
remains explicitly out of scope, and the Constitution/Dependency
compliance checks run at close.

## Audit Summary

TASK 0's audit (`docs/PHASE66_1_AUDIT.md`) found no existing Chart
Analysis, Image Contract, Chart Model, or Visual Context anywhere in
the audited packages (`ai/trading_analyst/`, `ai/explanation/`,
`media/`, `ai/content/`, `knowledge/`, `ai/memory/`, `ai/reasoning/`).
`ai/trading_analyst/`'s contracts are trade-level, not chart-visual —
extending them would couple two genuinely different concerns.
`media/`'s `MediaAsset` is delivery-shaped, not interpretation-shaped.
`MediaType.IMAGE` and `Capability.VISION`/`Capability.IMAGE` already
exist as vocabulary but carry no chart-specific field shape.
`ai/providers/base_provider.py`'s abstract `vision()` method is the
generic, cross-capability provider contract — calling it would
violate Rule 4 directly, and it is not itself a data contract. No
Director Decision pause was required — the genuine gap was clear and
the package-location resolution follows Phase 66.0's own established
precedent exactly.

## Built this phase

- `ai/chart_intelligence/models.py` (new) — `ChartImageType`
  (TRADINGVIEW_SCREENSHOT/MT5_SCREENSHOT/TELEGRAM_IMAGE/PDF_CHART/
  OTHER), `ChartAnalysisType` (STRUCTURE/TREND/LIQUIDITY/ORDER_BLOCK/
  FVG/SUPPORT_RESISTANCE/GENERAL), `ChartAnalysisInput` (primitive-only
  input shape, confidence 0-100), `ChartAnalysis` (TASK 2's own exact
  output contract, confidence 0.0-1.0), `ChartContext` (TASK 3 —
  source/resolution/platform/created_at/image_hash; never the image
  itself) plus `has_minimum_context()`.
- `ai/chart_intelligence/access.py` (new) —
  `is_chart_intelligence_enabled_for(role, flags)`, requiring both
  `FeatureFlags.enable_chart_intelligence` and `role == AIRole.OWNER`.
  Mirrors `ai/trading_analyst/access.py`'s shape exactly.
- `ai/chart_intelligence/chart_runtime.py` (new) — `ChartRuntime`:
  `analyze()` (a pure relay/transform, never calls a Vision API) and
  `explain()` (composes the existing, unmodified `ExplanationBuilder`
  in `EDUCATION` mode — Chart Intelligence narrates, it never produces
  a TRADE-mode verdict). Zero new business logic.
- `ai/chart_intelligence/trading_analyst_adapter.py` (new) —
  `combined_explanation()`, composing an existing `TradingAnalysis`
  (Phase 66.0) with this phase's own `ChartAnalysis` into a single
  TRADE-mode `ExplanationOutput` — the pipeline's own "TradingAnalysis
  → ChartAnalysis → Explanation" order (TASK 5). The one file in the
  package permitted to import `ai.trading_analyst.models`.
- `ai/chart_intelligence/content_adapter.py` (new) — `prepare_content()`,
  composing the same three real, unmodified Content → Media → Broadcast
  functions `ai/trading_analyst/content_adapter.py` already uses
  (`ContentType.LIVE_ANALYSIS` reused a second time, `MediaType.IMAGE`
  reused as-is — no new `ContentType`/`MediaType`). Never returns an
  empty content body (falls back to a bare "{symbol} {timeframe} chart
  analysis" line for a fully-empty analysis).
- `ai/chart_intelligence/vision_provider_types.py` (new) —
  `ChartVisionProviderType` (NONE/OPENAI_VISION/GEMINI_VISION/
  CLAUDE_VISION/LOCAL_VISION), pure future-compatible vocabulary, no
  API client, no provider wiring (TASK 8).
- `configuration/feature_flags.py` — extended with
  `enable_chart_intelligence: bool = False` (a dedicated flag, not a
  reuse of `enable_trading_analyst` — Chart Intelligence is a sibling
  concern, not a dependent one).
- `ai/chart_intelligence/README.md` (new) — package-level documentation.
- `tests/ai/chart_intelligence/` (new directory, 6 files) —
  `test_chart_intelligence_models.py`,
  `test_chart_intelligence_access.py`,
  `test_chart_intelligence_runtime.py`,
  `test_chart_intelligence_trading_integration.py`,
  `test_chart_intelligence_content_adapter.py`,
  `test_chart_intelligence_vision_provider_types.py`,
  `test_chart_intelligence_isolation.py` — 100 tests, exceeding the
  brief's own 80-test minimum.
- `tests/configuration/test_feature_flags.py` — extended (renamed the
  exhaustive field-name test to `..._eight_foundation_flags`, added
  `"enable_chart_intelligence"`).
- Documentation: `docs/PHASE66_1_AUDIT.md`, `docs/PHASE66_1_FREEZE.md`
  (new); `docs/ai/AI_CHART_INTELLIGENCE.md` (new);
  `docs/ai/AI_ARCHITECTURE.md`, `docs/ai/AI_TRADING_ANALYST.md`,
  `docs/ai/AI_INTELLIGENCE_PIPELINE.md`, `docs/roadmap/AI_EVOLUTION.md`,
  `docs/roadmap/VERSIONS.md` (extended).

## Not Built this phase

- No new top-level package (Rule 3) — `ai/chart_intelligence/` lives
  inside the already-existing `ai/` top-level package, confirmed by
  TASK 0's Article 11 audit, following Phase 66.0's own established
  precedent exactly.
- No new Chart Engine, Vision Engine, Image AI, or CV Engine of any
  kind — no `chart_engine2/`, `vision_engine/`, `image_ai/`,
  `cv_engine/`, or any file resembling them (Rule 3's explicit
  forbidden examples).
- No Vision API, LLM, or image recognition model call anywhere in this
  package — `OpenAI Vision`/`Gemini Vision`/`Claude Vision`/any real
  provider (Rule 4). `vision_provider_types.py` is metadata only, not
  wired into `ai/providers/` or `ai/router/`.
- No image storage — `ChartContext.image_hash` is a content-hash
  reference only; no field anywhere in `ai/chart_intelligence/models.py`
  carries image bytes or a binary payload (Director Note 4).
- No signal generation, no order placement, no Decision Engine
  override — `ChartRuntime` never calls `RiskManager.evaluate()`,
  never calls `DecisionEngine`, never writes to `decision/`/`risk/`/
  `execution/` (Rule 2).
- No rewrite or duplicate of `ExplanationBuilder`, `ContentEngine`,
  `media_layer.content_manager.media_pipeline`, or `media_layer.telegram_broadcast.broadcast_adapter` — all
  called via their existing public API, byte-for-byte unmodified.
- No new `Capability` member, no reuse of
  `ai/access/access_control.py`'s `AccessControl` matrix.
- No new `ContentType`, `MediaType`, or `ExplanationMode` — all three
  vocabularies reused exactly as they already existed.
- No Telegram command, dashboard, or `core/pipeline.py` wiring this
  phase — foundation only, same "not yet live-wired" posture every
  Owner-facing foundation in this codebase has followed since Phase
  59.x.
- No trading pipeline changes — zero diff in `core/`, `decision/`,
  `risk/`, `execution/`, `strategies/`, `signals/`, `context/`,
  `monitoring/` this phase (Rule 1).

## Constitution Compliance (checks run at close)

- **Article 3 (Import Rules), zero-exception rule** — AST sweep for
  `decision`/`risk`/`execution`/`strategies`/`signals`/`context`/
  `monitoring`/`telegram`/`database` imports across
  `ai/chart_intelligence/**/*.py`: zero matches
  (`tests/ai/chart_intelligence/test_chart_intelligence_isolation.py`).
- **Belt-and-suspenders field-type check** — every dataclass field on
  `ChartAnalysisInput`/`ChartAnalysis`/`ChartContext` inspected via
  `dataclasses.fields()` and checked against an allowlist of
  primitive/enum type fragments — none is typed as a Trading Core
  object reference, and no field name carries image bytes/binary data
  (`test_chart_analysis_input_has_no_trading_core_object_field_type`,
  `test_chart_intelligence_package_has_no_image_byte_fields`).
- **Trading pipeline zero-modification** — `git diff --stat` against
  `core/`, `decision/`, `risk/`, `execution/`, `strategies/`,
  `signals/`, `context/`, `monitoring/`: no changes in any of those
  directories this phase.
- **Article 9 (Version Compatibility)** — every pre-existing
  `ExplanationBuilder`/`ContentEngine`/`media_layer.content_manager.media_pipeline`/
  `media_layer.telegram_broadcast.broadcast_adapter`/`FeatureFlags`/`TradingAnalysis`
  public method/field signature is unchanged; `FeatureFlags` gains one
  new field (`enable_chart_intelligence`), zero changed ones.
- **Article 11 (Foundation Reuse Law)** — TASK 0's audit confirmed
  `ExplanationBuilder`, `ContentEngine`, `media_layer.content_manager.media_pipeline`,
  `media_layer.telegram_broadcast.broadcast_adapter`, and `TradingAnalysis` all already
  existed and were extended-by-call or read type-only, never
  duplicated; the one genuine gap (a Chart Intelligence contract and
  runtime) was added as a new subpackage only after confirming no
  existing module could be extended without breaking its contract.
  See `docs/PHASE66_1_AUDIT.md`.

## Dependency Compliance

`ai/chart_intelligence/models.py` and `access.py` import nothing
beyond `ai.access.permissions.AIRole`, `configuration.feature_flags`,
and the standard library. `chart_runtime.py` imports `ai.explanation.*`
only — never `ai.content/`, `media/`, `broadcast/`, or
`ai.trading_analyst`. `trading_analyst_adapter.py` is the one file in
the package permitted to import `ai.trading_analyst.models` —
confirmed confined to exactly this file by
`test_trading_analyst_import_confined_to_trading_analyst_adapter()`
and `test_only_trading_analyst_adapter_imports_ai_trading_analyst()`.
`content_adapter.py` is the one file permitted to import `ai.content/`,
`media/`, `broadcast/` — confirmed confined by
`test_content_media_broadcast_imports_confined_to_content_adapter()`
and `test_only_content_adapter_imports_ai_content()`. No file in the
package imports `assistant/`, `voice/`, `knowledge/`, `ai.memory`,
`ai.reasoning`, or `core.`. Nothing in `ai/trading_analyst/`,
`ai/explanation/`, `ai/content/`, `media/`, or `broadcast/` imports
`ai.chart_intelligence` back.

## New / Extended / Reused (Constitution Article 12, mandatory table)

| Item | New | Extended | Reused |
|------|-----|----------|--------|
| Packages | `ai/chart_intelligence/` (1, inside existing `ai/`) | — | `ai/` (top-level, unchanged itself) |
| Modules | `models.py`, `access.py`, `chart_runtime.py`, `trading_analyst_adapter.py`, `content_adapter.py`, `vision_provider_types.py`, `README.md` (7) | `configuration/feature_flags.py` (1) | `ai/explanation/explanation_builder.py`, `explanation_input.py`, `explanation_output.py`, `ai/trading_analyst/models.py`, `ai/content/content_adapter.py`, `media_layer/content_manager/media_pipeline.py`, `media_layer/telegram_broadcast/broadcast_adapter.py`, `media_layer/telegram_broadcast/broadcast_manager.py` (called/read, not modified) |
| Classes | `ChartRuntime` (1) | — | `ExplanationBuilder`, `ContentEngine`, `MediaManager`, `BroadcastManager`, `TradingAnalysis` (called/read, not modified) |
| Models | `ChartImageType`, `ChartAnalysisType`, `ChartAnalysisInput`, `ChartAnalysis`, `ChartContext`, `ChartVisionProviderType` (6) | `FeatureFlags` (+1 field) | `ExplanationInput`, `ExplanationOutput`, `ContentResult`, `MediaAsset`, `BroadcastAsset` |
| Functions | `is_chart_intelligence_enabled_for()`, `analyze()`, `explain()`, `combined_explanation()`, `prepare_content()`, `chart_analysis_to_content_body()`, `has_minimum_context()` (7) | — | `ExplanationBuilder.build()`, `ContentEngine.create()`, `prepare_media_from_content()`, `broadcast_asset_from_content_and_media()`, `BroadcastManager.prepare_broadcast()` |
| Secrets | — | — | none needed (no new external call surface) |
| Tests | 7 new files, 100 new tests | `test_feature_flags.py` (1 test renamed + widened) | — |
| Docs | `docs/PHASE66_1_AUDIT.md`, `docs/PHASE66_1_FREEZE.md`, `docs/ai/AI_CHART_INTELLIGENCE.md`, `ai/chart_intelligence/README.md` (4) | `docs/ai/AI_ARCHITECTURE.md`, `docs/ai/AI_TRADING_ANALYST.md`, `docs/ai/AI_INTELLIGENCE_PIPELINE.md`, `docs/roadmap/AI_EVOLUTION.md`, `docs/roadmap/VERSIONS.md` (5) | — |

Totals: **1 new subpackage inside the existing `ai/` top-level
package** (no new top-level Vision/Chart Engine), **1 pre-existing
file extended in place** (`configuration/feature_flags.py`, +1 field),
**1 new Runtime class**, **0 changes to any pre-existing LOCKed
class's public API**.

## Trading Pipeline Diff

**Zero.** `git diff --stat -- core/ decision/ risk/ execution/
strategies/ signals/ context/ monitoring/` returns no output.

## Next phase recommendation

Per the Director's own roadmap: `66.2` (Trade Journal Intelligence)
through `66.8` (Research Intelligence) continue the `66.x` sub-sequence.
Not decided here — requires its own dedicated Worker Brief per this
session's Director Policy.

## Related documents

- `docs/PHASE66_1_AUDIT.md` — TASK 0's Foundation Reuse Audit.
- `docs/ai/AI_CHART_INTELLIGENCE.md` — the full, current documentation
  of `ai/chart_intelligence/`'s model/runtime/adapter surfaces.
- `docs/PHASE66_0_FREEZE.md` — the prior phase's own freeze, whose
  `ai/trading_analyst/` this phase's `trading_analyst_adapter.py`
  composes with.
- `docs/policies/DIRECTOR_POLICY.md` — the Intelligence Dependency
  Principle referenced by this freeze's Dependency Compliance section.
- `docs/constitution/CONSTITUTION.md` Article 3 — the zero-exception
  rule this phase's entire architecture was designed to satisfy.
