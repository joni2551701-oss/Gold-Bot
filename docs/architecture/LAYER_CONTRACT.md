# GoldBot — Layer Contract

One page. For every layer, exactly four lines: **what it takes, what it
gives, what it may do, what it must never do.** If a change would break
any "Forbidden" line, it is wrong by construction — stop and re-read this
file before writing it.

This is the plain-language contract. The mechanically-enforced rules
live in `docs/constitution/CONSTITUTION.md` (Article 2, Dependency Law),
`docs/architecture/MODULE_DEPENDENCIES.md`, and
`docs/architecture/IMPORT_RULES.md` — where this document and those
disagree on a detail, those are authoritative. `docs/architecture/SYSTEM_LAYERS.md`
groups the same modules by responsibility cluster.

## The pipeline chain

```
config.py → data_layer/providers/ → stream/ → market/ → context/
   → strategies/ → signals/ → decision/ → risk/ → execution/
ai/ feeds decision/ as ADVISORY input only. telegram/ is the delivery
edge. database/ is storage. monitoring/ only observes.
```

---

## Trading pipeline layers

### Layer: `config.py` + `core/`
- **Input:** `.env` / environment, feature flags.
- **Output:** `Config` / `Settings`, `SETTINGS`, pipeline orchestration (`core/pipeline.py`), emergency/system state.
- **Allowed:** read secrets (the ONE place `.env` is read), hold configuration, orchestrate the pipeline.
- **Forbidden:** market analysis, signal, decision, risk, execution logic. Never log a secret value.

### Layer: `data_layer/providers/` (FROZEN)
- **Input:** provider credentials (via `config.get_settings()`), symbol/timeframe requests.
- **Output:** raw normalized candles / prices (`MarketCandle`), provider status; `ProviderManager` chain.
- **Allowed:** call the real provider API, classify provider errors, pick an active provider.
- **Forbidden:** market structure, signal, decision, risk, execution. No structure math. Contract is frozen — Critical bug / Security / real-API impl / Director-approved change only.

### Layer: `stream/`
- **Input:** provider data (`data_layer/providers/`), incoming ticks/candles.
- **Output:** `StreamEvent`s, live `CurrentPrice`, stream mode (active/weekend/paused); distributes to subscribers.
- **Allowed:** hold the real-time flow, update current price, route events, decide weekend/wait mode.
- **Forbidden:** compute market structure, emit a signal, make a decision, compute risk. No secret read/log.

### Layer: `market/`
- **Input:** `stream/` current price + `context.snapshot.ContextSnapshotSchema` (context's PUBLIC contract only).
- **Output:** one `MarketSnapshot` / `MarketState` / `MarketData` read-only aggregated view.
- **Allowed:** aggregate + project the already-computed view into one facade for downstream consumers.
- **Forbidden:** recompute HH/HL/BOS/CHoCH/liquidity/OB/FVG, write a strategy, emit a signal. No duplicate structure math; never touch context internals.

### Layer: `context/`
- **Input:** normalized candles (from `data/` / `market/`), optional HTF bias.
- **Output:** `ContextSnapshot` (internal) + `ContextSnapshotSchema` (public): structure, liquidity, OB, FVG, trend/bias, regime, session, volatility.
- **Allowed:** compute the full market analysis (swing/HH/HL/LH/LL, BOS, CHoCH, liquidity, OB, FVG, regime, session, volatility).
- **Forbidden:** open a trade, emit a signal, run execution, compute risk, write to the database. Analysis only.

### Layer: `strategies/`
- **Input:** `context/` output (analysis), configuration.
- **Output:** strategy selection / strategy candidates.
- **Allowed:** apply strategy rules on top of the context analysis.
- **Forbidden:** compute market structure, touch a raw provider, make the final trade decision.

### Layer: `signals/`
- **Input:** `strategies/` output.
- **Output:** `SignalCandidate` / `SignalSchema` (a proposed signal + quality score).
- **Allowed:** turn a strategy result into a structured signal, score it.
- **Forbidden:** re-analyze the market, make the APPROVE/REJECT decision, compute risk.

### Layer: `decision/` (`decision/decision_engine.py`)
- **Input:** a `signals/` signal, plus one ADVISORY `AIAnalysisResult` value from `ai/`.
- **Output:** `APPROVE` / `REJECT` / `NO_TRADE` (confidence-blended).
- **Allowed:** decide whether a signal becomes a trade; blend confidence.
- **Forbidden:** re-analyze the market, size the trade, send an order, call into `ai/`/`telegram/`/`execution/`. `DecisionEngine` thresholds change only with explicit approval.

### Layer: `risk/` (`risk/risk_manager.py`)
- **Input:** an APPROVED decision + account state.
- **Output:** lot size, stop-loss, take-profit, exposure verdict (`RiskManager.evaluate()`).
- **Allowed:** position sizing, SL/TP geometry, drawdown/daily-loss/exposure limits, duplicate-trade guard.
- **Forbidden:** be bypassed (EVERY trade passes through here), re-decide the signal, send the order. Geometry/sizing formulas change only with explicit approval.

### Layer: `execution/` (intentionally inert)
- **Input:** a risk-approved order intent.
- **Output:** (none live — no MT5 order call exists yet).
- **Allowed:** hold the execution contract/simulation only.
- **Forbidden:** place a real order until wiring is a Director-approved change; re-decide or re-size.

---

## Edge & support layers

### Layer: `ai/` (advisory only)
- **Input:** context / market view, prompts.
- **Output:** `AIAnalysisResult` — an ADVISORY value consumed by `decision/` only.
- **Allowed:** analyze, explain, advise; produce a typed result.
- **Forbidden:** approve/reject a trade, call the Risk Manager, trigger a Telegram send or execution. Advisory input to `decision/` — nothing more.

### Layer: `telegram/` (delivery edge)
- **Input:** `decision/`/`risk/` trading output + `ai/` explanation.
- **Output:** messages to the user; owner commands.
- **Allowed:** deliver. Handler → Service → Repository only.
- **Forbidden:** direct database access from handlers; business logic in handlers; any trading/analysis computation.

### Layer: `database/` (storage)
- **Input:** service calls.
- **Output:** persisted records (`*_repository.py`).
- **Allowed:** SQL only.
- **Forbidden:** business rules in a repository; being called directly by a Telegram handler.

### Layer: `monitoring/` (observer)
- **Input:** events/metrics from every layer.
- **Output:** health / snapshots / counters.
- **Allowed:** read and report.
- **Forbidden:** change pipeline behavior, emit a signal, make a decision. Observe only.

---

## The one rule behind all of the above

Each layer talks only to the layer immediately below it and never reaches
two layers down (Constitution Article 2). A new capability lands in the
layer whose **Allowed** line already covers it; if none does, it is a new
layer decision, not a quiet import. Reuse is the default; duplicate
structure/decision/risk logic across layers is forbidden.
