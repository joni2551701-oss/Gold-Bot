# GoldBot Folder Structure Review (Phase A1, Task 7)

Readiness assessment of the current folder/package structure against
the longer-term roadmap directions named in the Phase A1 brief: Gold,
Forex, Crypto, AI, Analytics, Education, Research, Mini App.
Recommendations only — **nothing in this document was implemented.**

## Current structure (as-is)

```
core/          orchestration, logging, secrets
data/          market data fetch/normalization
context/       SMC detection (structure, liquidity, OB, FVG, AMD)
strategies/    3 SMC methodologies -> SignalCandidate
signals/       SignalCandidate contract + aggregation
ai/            advisory evaluation (stub) + Phase 55 foundation
decision/      confidence blend -> APPROVE/REJECT/NO_TRADE
risk/          geometry/SL validation, sizing suggestion
execution/     inert MT5 scaffolding
monitoring/    performance/signal observation (unwired)
database/      SQLite persistence
telegram/      product layer (bot commands, permissions, services)
docs/          documentation
tests/         test suite (mirrors the package layout)
scripts/       ops tooling (Phase 58: health check, failure alert)
deploy/        systemd units (Phase 58)
```

## Readiness per roadmap direction

### Gold — READY (current state)

The entire existing codebase. No change needed; this review exists
because everything else is measured against how much of it Gold-
specific assumptions actually touch.

### Forex — PARTIAL

**What already generalizes cleanly**:
- `TradingPipeline.__init__(symbol, interval)` is already
  constructor-parameterized, not hardcoded — confirmed in
  `docs/FOUNDATION_GAP_ANALYSIS.md`'s Asset Manager section. Only
  `main.py`'s single call site hardcodes `"XAUUSD"`.
- `risk_layer/risk_engine/risk_manager.py`'s own docstring explicitly disclaims broker-
  specific knowledge — "No knowledge of broker specifications
  (contract size, tick value, lot step, min/max lot, stop level)" —
  confirmed by reading the file this phase. The risk-sizing math is
  already asset-agnostic by design, not gold-tuned.
- `context/`'s SMC detectors (structure, liquidity, order blocks,
  FVGs) are general price-action algorithms with no gold-specific
  constant found anywhere in this audit — they operate on
  `Candle` OHLC data regardless of what it represents.
- `data_layer/providers/twelve_data_client.py`'s symbol-formatting is documented as an
  example (`"XAUUSD"` → `"XAU/USD"`), not a hardcoded restriction —
  Twelve Data itself serves Forex pairs through the same API shape.

**What's missing**: no config surface enumerates which symbols to run
(see Foundation Gap Analysis, Asset Manager — MISSING), no per-asset-
class risk-parameter differentiation exists (a Forex pair's typical
volatility/pip-value profile differs from Gold's; `RiskConfig`'s
`risk_per_trade`/`max_daily_loss`/etc. are currently one global set of
defaults with no asset-class dimension), and every strategy's
detection thresholds were tuned and tested exclusively against
XAUUSD's real behavior — extending to Forex is a validation exercise
even where the code itself needs no structural change.

**Suggested improvement (not implemented)**: no folder restructuring
is needed to support Forex — the current single-`strategies/`,
single-`context/` structure is already symbol-agnostic in its actual
logic. The gap is orchestration (Asset Manager, per
`docs/v0.3.5_SPECIFICATION.md`) and configuration (per-symbol/per-
asset-class parameter sets), not package layout.

### Crypto — PARTIAL, same shape as Forex

Same structural readiness as Forex (symbol-agnostic pipeline/risk/
context code), with one additional open question this review flags
but does not resolve: crypto markets trade 24/7 with no session
structure, which interacts directly with two other Foundation Gap
Analysis items — `data_layer/live_data/session_filter.py`'s Monday-Friday/Tashkent-
hours gate (Session Intelligence, PARTIAL) would need to become
per-asset-class-aware rather than a single global gate, and
`.github/workflows/trading_bot.yml`'s cron window
(`*/5 3-18 * * 1-5`, weekdays only) would not fire at all on a weekend
crypto move under the current single-schedule setup. Not a folder-
structure problem — a scheduling/config problem, flagged here because
it's the kind of gap a naive "just add crypto to the symbol list"
change would miss.

### AI — READY (foundation), MISSING (implementation)

`ai/`'s Phase 55 foundation (`interfaces.py`'s
`AIAnalyzerInterface`, `memory/`, `prompts/`, `profiles/`) is already
provider-agnostic and asset-agnostic by construction — nothing in its
interface contract mentions Gold, Forex, or Crypto specifically. The
folder structure is ready; the actual heuristic/model implementation
behind `AIAnalyzer.analyze()` is the gap (see Architecture Audit's #1
finding), unrelated to folder layout.

### Analytics — PARTIAL

`core_layer/health_monitor/performance.py` exists, imports `SignalRepository`, and is
fully built — but has zero external callers (Architecture Audit
finding) and there is no dedicated `analytics/` package or Telegram-
facing analytics surface. The current `monitoring/` folder is
positioned correctly for this (its name already says "analytics-
adjacent"), but nothing routes into or out of it today.

**Suggested improvement (not implemented)**: if a v0.4+ phase builds
out real cross-symbol/cross-strategy analytics (once Asset Manager and
Signal Quality Score exist), `monitoring/` is a reasonable home for it
as-is — no new top-level package is obviously needed based on what
exists today. Revisit if analytics scope grows large enough to warrant
its own package (e.g. a dedicated `analytics/` reporting layer distinct
from `monitoring/`'s current "observe a running signal" framing) —
not clearly needed yet.

### Education — MISSING

No folder, module, or content pipeline for user-facing educational
material exists anywhere in this repository. This is a **content**
product direction, not primarily a code direction — this review notes
its absence but does not speculate on what a folder for it should look
like, since that depends entirely on a product decision (in-bot
lessons via Telegram commands? A separate content repository? A
`telegram/education_service.py` following the existing service
pattern?) not yet made anywhere in this codebase's history.

### Research — MISSING

No backtesting engine, no historical-signal-replay tooling, and no
research/notebook-style module exists anywhere — confirmed by grep
this phase (only false-positive hits, e.g. comment text unrelated to
backtesting). This is a genuine, structural gap: every strategy/
decision/risk parameter in this codebase today is tuned by manual
judgment and live/paper observation, not by a backtest harness that
replays historical `Candle` data through `context/` → `strategies/` →
`signals/` → `decision/` → `risk/` and measures outcomes.

**Suggested improvement (not implemented)**: a future `research/` (or
`backtest/`) package could reuse the existing pipeline's layers
directly — `context/`, `strategies/`, `signals/`, `decision/`, `risk/`
are all pure functions/classes over `Candle` sequences with no live-
network or live-Telegram dependency baked in (confirmed throughout
this audit's dependency map: none of those five packages import
`telegram/` or make network calls directly), which means a backtest
harness could drive them with historical data with comparatively
little adaptation. This is the audit's most promising "the pieces are
already shaped for this" finding for Research, mirroring the HTF-Bias/
Data-Quality pattern found elsewhere (built-shaped-right, just not
built-yet, in this case).

### Mini App — MISSING

No Telegram WebApp/Mini App integration exists — confirmed by grep
this phase (zero hits for `webapp`/`miniapp` across the codebase).
`telegram/`'s entire product surface today is command-based
(`aiogram` `Dispatcher.message()` handlers), not WebApp-based. Adding
a Mini App would be a genuinely new `telegram/` (or sibling
`webapp/`) surface, not an extension of the existing command-router
pattern — `telegram/command_router.py`'s routing model (parse command
+ args → permission tier → handler) doesn't naturally extend to a
WebApp's typical request shape (a served HTML/JS frontend + a
different auth flow, Telegram's `initData` validation, not a chat
command). Flagged as a genuinely new subsystem for a future phase to
scope from scratch, not a folder-structure tweak.

## Overall Suggested Improvements (not implemented)

1. **No structural change is needed for Gold/Forex/Crypto/AI/
   Analytics readiness** — the existing package boundaries
   (`context/`, `strategies/`, `signals/`, `decision/`, `risk/`) are
   already asset-agnostic in their actual logic (verified this phase,
   not assumed); what those directions need is orchestration
   (Asset Manager) and configuration (per-asset-class parameters), both
   already specified at a high level in `docs/v0.3.5_SPECIFICATION.md`.
2. **Research is the one direction where a genuinely new top-level
   package is the natural next step**, and the audit found the
   existing pipeline's layer purity (no network/Telegram dependency in
   `context/`→`risk/`) makes that package's job easier than it might
   otherwise be.
3. **Education and Mini App are product-scope decisions before they
   are folder-structure decisions** — this review deliberately does
   not propose a folder shape for either, since guessing one ahead of
   an actual product spec risks the exact "big refactor later" outcome
   this whole Phase A1 audit exists to prevent.
