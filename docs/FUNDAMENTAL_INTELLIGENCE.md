# Fundamental Intelligence Foundation (Phase 60.5)

**Not wired into the live bot.** Same "real function, not live-wired"
posture as every phase before it. Nothing in `core/pipeline.py`,
`decision/`, `risk/`, `execution/`, `strategies/`, or `signals/` is
touched or called by anything in this phase.

**The one hard rule** (per the Director's own brief): this whole
layer is a **Macro Context Engine**, not a signal generator.

```
❌ BUY
❌ SELL
❌ trade ochmaydi (never opens a trade)

✅ Macro Bias: BULLISH GOLD / BEARISH GOLD / NEUTRAL
✅ Confidence: 0-100%
✅ Reasons: a short list of which indicators drove the bias
```

The Decision Engine, not this layer, is what would ever turn any of
this into a trade -- and this phase does not wire that connection.

## Where this sits

```
FRED (data_layer/providers/fred_provider.py)         -- still an honest, inert stub
      |  collect_snapshot() (TASK 3, this phase)
      v
FundamentalSnapshot (data_layer/providers/fundamental_base.py)   -- unchanged, provider-layer bundle
      |
      v  (caller-classified per-indicator biases, not computed here -- see TASK 5)
context.fundamental_scoring.compute_fundamental_score()    -- TASK 5, this phase
      |
      v
FundamentalScoreResult (gold_bias, confidence, macro_score, reasons)
      |
      v  merge_fundamental_score() (TASK 2, this phase)
FundamentalContextSnapshot (context_layer/fundamental/fundamental_context.py) -- extended, not replaced
      |
      v  attach_fundamental_context() (TASK 6, this phase)
EnrichedContextSnapshot { context: ContextSnapshot, fundamental: FundamentalContextSnapshot }
      |
      v
ai.prompts.prompt_manager.PromptManager.get_fundamental_analysis_prompt()  -- TASK 7, this phase
      |
      v
(future v0.4+ AI Assistant Core -- not built this phase)
```

## TASK 1: Reuse audit

Read `context_layer/fundamental/fundamental_context.py` (Phase 59.3, TASK 6 --
`FundamentalContextSnapshot`/`compute_fundamental_context()`, already
a real Context-layer adapter), `data_layer/providers/fundamental_base.py`
(Phase 59.2, TASK 4 -- `FundamentalDataPoint`/`FundamentalSnapshot`/
`FundamentalDataProvider`), and `data_layer/providers/fred_provider.py`
(Phase 59.2, TASK 4 -- `FredProvider`, an honest, inert stub: every
fetch method raises `NotImplementedError`). No Gemini fundamental
engine, no news module, and no economic-calendar provider exist
anywhere in this codebase. `ai/prompts/prompt_manager.py`'s
`PromptManager` (Phase 55) was also confirmed as the correct,
already-existing extension point for TASK 7 (see below).

Two of the Director's brief's suggested new paths were found, by this
audit, to already have a better home:

- **TASK 2**'s "Yangi modul: `context/fundamental/`" -- not created.
  `context_layer/fundamental/fundamental_context.py` already is the real, tested,
  Context-layer home for a fundamental snapshot; `context/` itself has
  no subpackages today (every topic -- `bos.py`, `choch.py`, `fvg.py`,
  `liquidity.py`, `wyckoff.py`, etc. -- is a flat file), so introducing
  the first subpackage for this one phase would be a structural
  precedent shift the Module Reuse Principle counsels against. TASK 2
  extends the existing file; TASK 4/5 add flat sibling files
  (`context_layer/fundamental/economic_events.py`, `context_layer/fundamental/fundamental_scoring.py`),
  matching every other module already there.
- **TASK 7**'s "Yangi: `ai/fundamental_prompt.py`" -- not created.
  `ai/prompts/prompt_manager.py`'s `PromptManager` is already the
  general-purpose, `MarketContext`-shaped template registry a
  fundamental-analysis prompt belongs in (see that module's own
  docstring, which explicitly distinguishes it from the older,
  Gemini-specific `ai/ai_prompt.py`). TASK 7 adds one new method to
  the existing class instead.

## TASK 2: `context_layer/fundamental/fundamental_context.py` -- scoring-field extension

`FundamentalContextSnapshot` gains eight new `Optional` fields
(`dxy_bias`, `rates_bias`, `inflation_bias`, `fed_expectation`,
`risk_sentiment`, `gold_bias`, `confidence`, `macro_score`), all
defaulting to `None`. `compute_fundamental_context()` itself is
**unchanged** -- it still only sets `fed_rate`/`inflation`, so every
Phase 59.3 test keeps passing unmodified. A new function,
`merge_fundamental_score(snapshot, score)`, returns a new (frozen
dataclass, `dataclasses.replace()`) `FundamentalContextSnapshot` with
those eight fields filled in from an already-computed
`FundamentalScoreResult` (TASK 5).

## TASK 3: FRED Integration Layer -- `FredProvider.collect_snapshot()`

An extension of the existing `FredProvider` class (Module Reuse
Principle: extend, not a new collector module), not a new file. Calls
`get_interest_rate()`/`get_inflation_data()`/`get_macro_indicator(SERIES_DOLLAR_INDEX)`
and bundles whichever succeed into one
`data_layer.providers.fundamental_base.FundamentalSnapshot`, keyed by
logical name (`"interest_rate"`/`"inflation"`/`"dollar_index"`),
catching each `NotImplementedError` individually. Today every call
still raises (`FredProvider` remains a foundation-only stub -- no real
FRED HTTP integration was added; that needs an API key via
`core/secrets.py` and is its own, separately-approvable future step,
not implied by "collect the three series" alone), so
`collect_snapshot()` returns a real, all-empty `FundamentalSnapshot`,
never an exception. Once a real connection exists, this method starts
returning real values with no code change.

## TASK 4: `context_layer/fundamental/economic_events.py`

`EventImpact` (`HIGH`/`MEDIUM`/`LOW`, the standard three-tier
economic-calendar convention) + `EconomicEvent` (`name`, `date`,
`impact`, `currency`, `expected`, `actual`, plus a computed `surprise`
property = `actual - expected`, `None` unless both are known). A flat
file directly under `context/`, matching every other topic file there
(`bos.py`, `choch.py`, etc.) -- not a new subpackage (see TASK 1).
Data model only; nothing in this codebase populates one yet (no
economic-calendar provider exists).

## TASK 5: `context_layer/fundamental/fundamental_scoring.py`

`FundamentalScoreWeights` (`dxy=20.0`, `rates=15.0`, `inflation=10.0`,
`risk=15.0` -- magnitudes only) + `FundamentalScoreResult` +
`compute_fundamental_score(dxy_bias=None, rates_bias=None,
inflation_bias=None, risk_sentiment=None, fed_expectation=None,
weights=None)` + `explain_fundamental_score()` +
`format_fundamental_score()`.

**Does not classify a raw macro number into a bias.** Every input
(`dxy_bias`/`rates_bias`/`inflation_bias`/`risk_sentiment`) is already
a `"BULLISH"`/`"BEARISH"`/`"NEUTRAL"` judgment *for gold*, supplied by
the caller (a future analyst/AI layer) -- `context_layer/fundamental/fundamental_context.py`'s
own docstring already discloses that a real classification "would need
a historical baseline/threshold model this codebase has no real data
to calibrate today," and TASK 1's reuse audit found nothing has closed
that gap. This module only aggregates already-classified biases into
one score.

Formula: each component contributes `+weight` (BULLISH), `-weight`
(BEARISH), or `0` (NEUTRAL/None); `macro_score = 50 + (raw / max_raw) *
50`, naturally bounded to `[0, 100]` and centered at 50 (fully
neutral); `gold_bias` = BULLISH if `macro_score >= 60`, BEARISH if
`<= 40`, else NEUTRAL; `confidence = min(abs(macro_score - 50) * 2,
100)`. `fed_expectation` is carried through but not part of the score
(informational only).

**On the Director's own worked example**: `"DXY: -20, Rates: -15,
Inflation: +10, Risk: +15 -> Gold Score: +70"` does not arithmetically
sum to +70, so this module does not attempt to literally reproduce
those four numbers -- it reproduces the *shape* (a weighted,
disclosed, deterministic 0-100 score with a Reasons breakdown), the
same "worked example is illustrative, not literal arithmetic"
precedent this codebase already applied to `compute_r_multiple()`'s
fixed SL/BE values.

## TASK 6: Context Integration -- composition, not modification

`context.context_orchestrator.ContextSnapshot`'s own docstring states
its field set is required, "no defaults by design" -- a stable
contract every existing caller (`core/pipeline.py`,
`backtesting_layer/backtest_engine/backtest_engine.py`, every test that builds one) depends
on. Adding a fundamental field directly onto it would force all of
them to change: a real breaking change `CLAUDE.md`'s own restrictions
forbid without explicit approval, and this task's own boundary ("Bu
yerda signalga tegilmaydi... Decision hali o'zgarmaydi") does not ask
for.

Instead, `context_layer/fundamental/fundamental_context.py` gained
`EnrichedContextSnapshot` (`context: ContextSnapshot`, `fundamental:
FundamentalContextSnapshot`) + `attach_fundamental_context(context,
fundamental)` -- pure composition, zero changes to `ContextSnapshot`
itself, not constructed anywhere in `core/pipeline.py` or any live
path this phase.

## TASK 7: AI Preparation Layer -- `PromptManager.get_fundamental_analysis_prompt()`

One new method on the existing `ai.prompts.prompt_manager.PromptManager`
class (see TASK 1). Builds a combined technical + fundamental prompt
from an already-built `MarketContext` and `FundamentalContextSnapshot`,
matching the Director's own worked example shape ("Technical: H4
bearish / Fundamental: Fed hawkish, DXY strong"). Template only -- no
LLM call, no network access, same posture as every other method on
this class. States its own advisory-only boundary in its system prompt
text ("Do NOT say 'BUY' or 'SELL'... the Decision Engine, not this
prompt, turns any of this into a trade").

## TASK 8: `telegram/owner/fundamental_commands.py`

`get_macro_status(fundamental)`, `get_fundamental_score_report(score)`,
`get_fed_status(fundamental)` -- the future `/macro_status`,
`/fundamental_score`, `/fed_status` commands. Thin wrappers only, same
"compute from supplied data, don't fetch" posture as
`validation_commands.py`/`performance_commands.py`. Not registered
into `telegram/commands.py`, not called from
`telegram/command_router.py` or `telegram/handlers.py`.

## TASK 9: Database

No new table. This phase adds nothing to `database/` -- every new
type here is in-memory only, matching the same foundation-only
posture every prior phase's own analytics/context modules already
established (Phase 60.4's own TASK 6 decision is the most recent
precedent).

## Dependencies

`context_layer/fundamental/fundamental_context.py` imports `context.fundamental_scoring.FundamentalScoreResult`
and `context.context_orchestrator.ContextSnapshot` (both
`TYPE_CHECKING`-only, same-layer sibling imports, no cycle --
`context_orchestrator.py` does not import `fundamental_context.py`)
plus `data_layer.providers.fundamental_base.FundamentalDataPoint`
(`TYPE_CHECKING`-only, unchanged from Phase 59.3).
`context_layer/fundamental/fundamental_scoring.py` and `context_layer/fundamental/economic_events.py`
import nothing beyond stdlib. `data_layer/providers/fred_provider.py`
gained one new import, `data_layer.providers.fundamental_base.FundamentalSnapshot`
(already a sibling import in that package). `ai/prompts/prompt_manager.py`
gained one new `TYPE_CHECKING`-only import,
`context.fundamental_context.FundamentalContextSnapshot`.
`telegram/owner/fundamental_commands.py` imports
`context.fundamental_context.FundamentalContextSnapshot`,
`context.fundamental_scoring.FundamentalScoreResult`/`format_fundamental_score()`,
and `telegram.owner.provider_commands.ProviderCommandResult`. None of
these import `database/`, `risk/`, `decision/`, `execution/`,
`strategies/`, or `signals/`.

## Known gaps (disclosed, not hidden)

- No real FRED HTTP connection exists -- `collect_snapshot()` always
  returns an empty `FundamentalSnapshot` today. A real integration
  needs an API key and is a separate, explicitly-approvable future
  step.
- No threshold/classification model exists to turn a raw macro number
  into a `"BULLISH"`/`"BEARISH"`/`"NEUTRAL"` bias -- every bias input
  to `compute_fundamental_score()` must be supplied already-classified
  by a future analyst/AI layer. This gap was already disclosed by
  Phase 59.3's own `dollar_strength`/`risk_level` honest-`None` hooks
  and remains open.
- No economic-calendar provider exists to populate an `EconomicEvent`
  -- TASK 4's model has no real data source yet.
- Nothing in this phase is wired into `core/pipeline.py`,
  `decision_layer/decision_engine/decision_engine.py`, or any Telegram routing surface.

## Future Roadmap

Per the Director's own roadmap note, this closes the last big
foundation phase before the v0.4 AI layer:

```
Technical Intelligence
        +
Market Structure
        +
Fundamental Intelligence (this phase)
        +
Backtesting
        +
Performance Validation
```
