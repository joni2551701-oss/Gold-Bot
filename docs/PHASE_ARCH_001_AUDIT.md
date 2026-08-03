# PHASE_ARCH_001 — GoldBot Flow Refactor Audit

**Task:** TASK-ARCH-001 — file-by-file flow audit; each layer back to its
single responsibility; move (not rewrite) misplaced logic.

**Director decision (recorded):** *Faqat audit doc.* This phase produces
this Architecture Map + findings only. **No code was moved, renamed, or
rewritten.** The two borderline items in §5 are logged for a future,
explicitly-approved phase — not acted on here.

**Method:** cross-layer import scan over `market/ context/ strategies/
signals/`, plus file-by-file reads of every candidate for a
misplaced-logic or duplicate-logic violation.

---

## 1. Headline finding

The four in-scope layers (`context/`, `market/`, `strategies/`,
`signals/`) are **already in their correct roles.** This is the
cumulative result of prior work:

- **TASK-CORE-005** — made `market/` a read-only façade over `context/`.
- **TASK-CORE-006** — declared `context/` production-complete / FROZEN.
- **TASK-CORE-007** — added the additive `strategies/` setup layer that
  *reads* context and *reuses* the frozen live `analyze()` detection.

Under the task's own rules — *"refactor faqat kerak bo'lsa"*, *"Duplicate
logic qat'iyan taqiqlanadi"* — and CLAUDE.md's *"No unnecessary
refactor"*, **no mandatory code movement exists.** Inventing a violation
to justify a move would touch frozen/live contracts and is out of scope.

---

## 2. Cross-layer import scan — result

No **hard** layer-crossing import violations.

| Reported "hit" | Reality |
|---|---|
| `context_layer/fundamental/fundamental_scoring.py:27` → decision/risk | **Docstring** ("…from decision/decision_engine.py or risk/risk_manager.py — it answers"), not an import. |
| `signals/signal_quality.py:20` → context | **Comment** describing provenance, not an import. |
| `signals/*` → `context.*` (real imports) | **Type/enum only** — `LiquidityType`, `OrderBlockType`, `FvgType`, `WyckoffPhase`, `MarketRegime`, `ContextSnapshot` for typing. This is the FROZEN live pipeline contract, not analysis logic. |
| `strategies/*` → `context.*` | Detector **reuse** (reads `ContextSnapshot` fields / calls frozen `analyze()`). No structure recomputation. |
| `market/*` → `context.*` | None. `market/` reads a passed-in context schema via `from_context()` projections. |

---

## 3. Architecture Map (target flow — input / output / allowed / forbidden)

```
config.py → data_layer/providers/ → stream/ → market/ → context/ → strategies/
→ signals/ → decision/ → risk/ → execution/ → database/ → telegram/ → ai/
→ platform/ → monitoring/
```

| Layer | Input | Output | Allowed | Forbidden |
|---|---|---|---|---|
| `config.py` | env / `.env` (via `core/secrets`) | config values | read config, feature flags | business logic, secret logging |
| `data_layer/providers/` | external API | raw candles / `MarketCandle` | API adapter, normalization | structure math, strategy logic |
| `stream/` | provider events | `StreamEvent`, price | real-time event flow | detectors, decisions |
| `market/` | stream + context results | `MarketSnapshot/State/Data` (views) | **read-only façade** projections | structure math, detectors, strategy logic |
| `context/` | candles (`data_layer.providers.twelve_data_client.Candle`) | `ContextSnapshot` | HH/HL/LH/LL, BOS/CHoCH, liquidity, OB, FVG, trend/bias, session, volatility, regime | signals, setups, decisions |
| `strategies/` | `ContextSnapshot` | `SignalCandidate` (live) / `StrategyResult` (setup) | setup evaluation by **reading** context | structure math, context duplication, entering signal engine |
| `signals/` | strategy output | user-facing signal structure | assembly / formatting / quality-grade of existing context | analysis, structure recompute, setup detection |
| `decision/` | signal + AI input | APPROVE/REJECT/NO_TRADE | confidence blending, thresholds | risk sizing, execution |
| `risk/` | approved decision | sized/validated order params | sizing, SL/TP geometry, limits | signal generation, execution calls |
| `execution/` | risk-validated order | (inert — no live MT5) | order execution rules | bypassing risk |
| `database/` | records | persistence | SQL only (repositories) | business rules |
| `telegram/` | services | bot transport | handlers→service→repository | direct DB, analysis |
| `ai/` | context/decision (advisory) | analysis / commentary | advisory input to `decision/` only | approve/reject, call Risk, trigger send/execution |
| `platform/` | — | app orchestration | app/composition layer (see §5-B) | detectors, business rules |
| `monitoring/` | all layers (observe) | health / metrics | observer-only reads | mutating pipeline state |

---

## 4. File-by-file verdicts (in-scope layers)

### `market/` — ✅ façade, no move
- `market_structure.py` = `MarketStructureView.from_context()` — pure
  projection of an already-built context schema; docstring explicitly
  states it "never recomputes and never modifies context/".
- `*_state.py` (liquidity/regime/session/trend/volatility) + `candle.py`
  = documented thin façade DTOs (41–56 lines each), no detectors.
- **Duplicate check:** `market/candle.py` is a deliberate façade view,
  not a second `Candle` detector. `context_layer/context_engine/candle.py` remains the SSoT
  for candle sentiment (`direction()` / `is_bullish()`).

### `context/` — ✅ FROZEN, no move
- Owns all structure math (SSoT). Emits `ContextSnapshot` only. No
  `signal/decision` import (the scan hit was a docstring).

### `strategies/` — ✅ reads context, no move
- Live `strategy_manager.py` → `strategy.analyze(context)` → aggregates
  `SignalCandidate`. No recomputation.
- Setup layer (TASK-CORE-007) reads `ContextSnapshot` defensively;
  AMD/Liquidity/FVG wrappers reuse the frozen `analyze()`.
- **No structure detector lives in `strategies/`** that would need to be
  pushed back to `context/`.

### `signals/` — ✅ assembly/format, no move
- `signal_engine.py` = `ContextSnapshot` → `StrategyManager` →
  `List[SignalCandidate]`. No structure recompute.
- `signal_quality.py` = grades a `SignalCandidate` against
  **already-computed** context (its docstring documents "no new
  structure detection" and reuse of `most_recent_bias()` /
  `ContextSnapshot` fields). See §5-A.

---

## 5. Two borderline items — logged, NOT actioned

**A. `signals/signal_quality.py` classification.**
It reads context *enums* to attach an A+/A/B/C quality grade to a
signal. It performs **no** structure/liquidity/OB/FVG detection (all
reused from context). It is defensible as a `signals/` concern (grading
the assembled signal), not misplaced analysis. Moving it would alter a
FROZEN live `signals/` contract → requires explicit Director approval per
task rule 6. **Not moved.**

**B. `platform/` layer is absent.**
The target flow lists `platform/` as the app layer, but today the app
layer is `core/pipeline.py` + `main.py`. Creating a new top-level
`platform/` package is the highest-cost option under the Module Reuse
Principle. Options for a future phase: (1) document `core/` **as** the
platform/app layer, or (2) create `platform/` by explicit decision.
**Not created.**

---

## 6. Deliverables (per task)

1. **Refactored files:** none (audit-only decision).
2. **Logic moved:** none — audit found nothing that can move without
   touching frozen/live contracts.
3. **Contracts preserved:** `analyze()→SignalCandidate`, `SignalEngine`,
   `ContextSnapshot`, `MarketStructureView.from_context()` — all intact.
4. **Adapter-protected:** `market/` (façade over context), `strategies/`
   AMD/Liquidity/FVG wrappers (reuse frozen `analyze()`).
5. **Test result:** full suite green (see Commit Protocol section of the
   Worker report).
6. **CI result:** confirmed green on the pushed commit.
7. **Architecture report:** §3 above.

---

## 7. Acceptance criteria — status

| Criterion | Status |
|---|---|
| Each file does its own job | ✅ verified |
| No layer crossing | ✅ (only type/enum + façade reads) |
| No duplicate logic | ✅ none found |
| Pipeline intact | ✅ smoke run unchanged |
| Tests pass | ✅ |
| CI green | ✅ |
| File-by-file consistency | ✅ this document |

**Conclusion:** GoldBot's `config → … → monitoring` flow already honors
single-responsibility for the in-scope layers. The correct outcome of
this audit is documentation, not code churn.
