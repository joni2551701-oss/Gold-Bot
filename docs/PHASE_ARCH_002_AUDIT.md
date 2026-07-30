# PHASE_ARCH_002 — STEP-07A Architecture Semantics & Boundary Audit

**Task:** TASK-ARCH-002 / STEP-07A — file-by-file semantic boundary
audit. Per file: what it does, what it must not do, what it depends on,
what it must not depend on. Refactor **only** a file caught doing another
layer's job; otherwise no code change.

**Result:** **No boundary violation found.** Per the task's own rule
("Agar topilmasa: kod o'zgarmaydi, faqat audit doc yoziladi") this phase
is **audit-only — no code was moved, renamed, or rewritten.** This
document is the finer, file-granularity companion to
`docs/PHASE_ARCH_001_AUDIT.md`.

**Method:**
- Cross-layer import scan (upstream→downstream) for every boundary layer.
- Reverse-import scan (would an upstream layer import a downstream one?).
- Keyword scan inside `stream/` and `data/providers/` for hidden
  analysis / business logic that imports wouldn't reveal.

---

## 1. Boundary evidence (what the scans found)

| Check | Result |
|---|---|
| `stream/` imports business layers? | **No** — only `dataclasses`. |
| `data/` + `data/providers/` import analysis layers (market/context/strategies/signals/decision/risk/ai)? | **No.** |
| `market/` imports `context`/`strategies`/`signals`? | **No** — reads a passed-in context schema via `from_context()`. |
| `strategies/` imports `decision`/`risk`/`execution`? | **No.** |
| `signals/` imports `decision`/`risk`/`execution`? | **No.** |
| `context/` imports `signals`/`decision`/`risk`/`execution`? | **No** — the one grep hit (`fundamental_scoring.py:27`) is a **docstring sentence**, not a Python import. |
| Hidden analysis in `stream/`? | **No** — every keyword hit is a boundary-declaring docstring ("computes NO signal, indicator, or decision"). |
| Hidden analysis in `data/providers/`? | **No** — `get_macro_indicator()` / `indicators` are **raw FRED fundamental data points** (rates/CPI/DXY), not technical detection. `base_provider` docstring: "A provider NEVER generates a signal / NEVER knows about a strategy / NEVER knows about a decision." |

---

## 2. Per-file Layer Contracts (Input / Output / Allowed / Forbidden / Depends on / Must not depend on)

### data/providers/
- **Input:** external API responses (Twelve Data, FRED, Binance, Bitget, MT5, Keynorq).
- **Output:** raw candles / `FundamentalSnapshot` / `FundamentalDataPoint`.
- **Allowed:** API calls, auth, ret/err mapping (`provider_errors.py`), raw fundamental fetch.
- **Forbidden:** structure math, indicators, signal, strategy, decision.
- **Depends on:** `core/` (logger/secrets), `config`.
- **Must not depend on:** market/context/strategies/signals/decision/risk/ai.

### stream/
- **Input:** provider events / price ticks.
- **Output:** `StreamEvent`, current price, `StreamState`.
- **Allowed:** real-time event flow, open/closed clock, validation (structured absence).
- **Forbidden:** detectors, indicators, signal, strategy, decision, risk, execution, rendering.
- **Depends on:** `dataclasses` only (self-contained data-flow).
- **Must not depend on:** any analysis or business layer.

### market/
- **Input:** stream + an already-built context schema.
- **Output:** `MarketStructureView` / `*State` views / `MarketData` (façade DTOs).
- **Allowed:** read-only projection / aggregation.
- **Forbidden:** HH/HL/BOS/CHoCH recompute, detectors, strategy, signal.
- **Depends on:** own view types; reads context via `from_context()`.
- **Must not depend on:** context/strategies/signals internals (reads passed-in schema by public attribute).

### context/  — **FROZEN (TASK-CORE-006)**
- **Input:** candles (`data.twelve_data_client.Candle`).
- **Output:** `ContextSnapshot`.
- **Allowed:** structure, liquidity, OB, FVG, trend/bias, session, volatility, regime.
- **Forbidden:** signal, setup, decision, risk, execution.
- **Depends on:** `data.twelve_data_client`, `core/`.
- **Must not depend on:** strategies/signals/decision/risk/execution.

### strategies/
- **Input:** `ContextSnapshot`.
- **Output:** `SignalCandidate` (live) / `StrategyResult` (setup layer).
- **Allowed:** setup evaluation by **reading** context; reuse frozen `analyze()`.
- **Forbidden:** structure math, context detector duplication, entering the signal engine.
- **Depends on:** `context/`, `signals.models` (SignalCandidate type — live contract).
- **Must not depend on:** decision/risk/execution.

### signals/
- **Input:** strategy output (`SignalCandidate`).
- **Output:** user-facing signal structure / quality grade.
- **Allowed:** assembly, formatting, grade-of-existing-context (`signal_quality`).
- **Forbidden:** setup detection, structure analysis, decision/risk logic.
- **Depends on:** `strategies`, `context` **types/enums only**, `core/`.
- **Must not depend on:** decision/risk/execution.

---

## 3. File-by-file verdict

**Legend:** OK = correct role · Keep as-is = correct, explicitly documented boundary · (no "Needs refactor" rows — none found).

| File | Verdict | Note |
|---|---|---|
| `data/providers/base_provider.py` | Keep as-is | ABC states "never signal/strategy/decision". |
| `data/providers/{twelve_data,binance,bitget,mt5,keynorq}_provider.py` | OK | API adapters only. |
| `data/providers/{fred_provider,fundamental_base}.py` | OK | raw macro data, not TA. |
| `data/providers/{provider_manager,registry,provider_errors}.py` | OK | orchestration/errors, no analysis. |
| `stream/*.py` (all 8) | Keep as-is | data-flow only; docstrings enforce boundary. |
| `market/market_structure.py` | Keep as-is | `from_context()` projection, never recomputes. |
| `market/{liquidity,regime,session,trend,volatility}_state.py` | OK | façade DTOs. |
| `market/{candle,current_price,ticker,orderbook,market_data,market_manager}.py` | OK | façade views/aggregation. |
| `context/*.py` (all) | OK — FROZEN | SSoT for structure math. |
| `strategies/strategy_manager.py` | OK | reads context, aggregates `SignalCandidate`. |
| `strategies/{amd,liquidity,fvg}_strategy.py` | OK | live `analyze()`; reused, not duplicated. |
| `strategies/{base,result,registry,manager}.py` + setup strategies | OK | read context, emit `StrategyResult`. |
| `signals/signal_engine.py` | OK | context→manager→candidates, no recompute. |
| `signals/signal_quality.py` | Keep as-is | grades a candidate vs already-computed context; docstring documents "no new structure detection". |
| `signals/{explainability,adapter,schema,models,signal_quality}.py` | OK | formatting/assembly. |

---

## 4. Refactor log

**None.** No file was found doing another layer's job. Refactor
preconditions (file doing wrong job / carrying another layer's
responsibility / duplicate reducible by a move) were **not met** for any
file, so per the task's refactor rule no code was touched. Public/live
contracts (`analyze()→SignalCandidate`, `SignalEngine`,
`ContextSnapshot`, `MarketStructureView.from_context()`) remain intact.

---

## 5. Audit report (short conclusion)

- **Architecture clean?** Yes — every in-scope file does its own job.
- **Unclear layers?** None. The only debatable file, `signal_quality.py`,
  is a documented `signals/`-layer grade over already-computed context
  (reuse, not analysis) → logged in `PHASE_ARCH_001_AUDIT.md §5-A`, not a
  violation.
- **Frozen layers?** `context/` (TASK-CORE-006). `strategies/` live
  `analyze()` path and `signals/` are live contracts (change only with
  explicit Director approval).
- **Refactor needed?** No — anywhere. Boundaries hold at the file level.

**Tests / CI:** no code changed; full suite remains green and CI is
confirmed on the pushed commit (see the Worker report's Commit Protocol
section).

**Acceptance criteria:** every file's role documented ✅ · no wrong
responsibility found (so none refactored) ✅ · no duplicate logic ✅ · no
layer crossing ✅ · live pipeline intact ✅ · tests pass ✅ · CI green ✅.
