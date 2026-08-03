# PHASE_DECISION — Business-Decision Layer (STEP-09 / TASK-CORE-009)

The STEP-09 `decision/` additions turn ONE canonical signal
(`signal_layer.signal_builder.schema.SignalSchema`) into ONE business verdict —
**APPROVE / REJECT / HOLD / EXPIRE** — that every downstream consumer
reads. It performs no risk sizing, no order, no platform formatting,
and it does not modify the live, frozen decision engine.

## 1. Position in the flow

```
config -> providers -> stream -> market -> context -> strategies -> signals
                                                                       │
                                                                 ┌─────┴─────┐
                                                                 │ decision  │  ← STEP-09
                                                                 └─────┬─────┘
                                                                       │  DecisionOutcome
                risk (STEP-10) · database · telegram · ai · monitoring
```

Only an **APPROVE** flows on to `risk/` (STEP-10). HOLD / REJECT /
EXPIRE are still recorded (database / ai / monitoring / telegram) but
never reach risk sizing.

## 2. Input / Output

- **Input (mandatory):** a canonical signal (`SignalSchema`), read
  duck-typed.
- **Input (optional):** a frozen-engine `TradeDecision` (when the
  caller already ran `DecisionEngine.evaluate()`) — its verdict is
  REUSED as the base status; a `now` override for testing.
- **Output:** a frozen `DecisionOutcome` — `status` (DecisionStatus),
  `confidence` (relayed from the signal, never recomputed), `reasons`,
  `rules_applied`, `signal_id/symbol/direction`, `created_at`,
  `metadata` (`base_status`, `source`), plus `to_dict()/to_json()`.
- decision/ does **not** talk to providers, stream, risk, or any
  platform.

## 3. Director decision — additive parallel + reuse-first

The **live path is FROZEN and untouched**:
`decision_layer.decision_engine.decision_engine.DecisionEngine.evaluate(signal, ai_analysis,
htf_bias=None)` still consumes a `SignalCandidate` + `AIAnalysisResult`
and returns a `TradeDecision` with a `DecisionAction`
(APPROVE / REJECT / NO_TRADE) — the confidence-blend on the live
pipeline (see `decision/README.md`).

STEP-09 is a **new, parallel layer** that consumes the canonical
signal instead and **reuses** the frozen verdict rather than
recomputing it. This honours CLAUDE.md Trading Safety (the frozen
decision flow — confidence-blend + APPROVE/REJECT/NO_TRADE thresholds —
is not modified) and the Module Reuse Principle (the STEP-09
orchestrator is `decision_manager.py`, not a rewrite of the frozen
`decision_engine.py`).

### Vocabulary mapping (the reuse / fork point)

| Source | Value | → `DecisionStatus` | Why |
|---|---|---|---|
| frozen `DecisionAction` (via `trade_decision=`) | `APPROVE` | `APPROVE` | pass-through |
| | `REJECT` | `REJECT` | pass-through |
| | `NO_TRADE` | **`HOLD`** | "no trade this cycle" is a hold, not a hard reject |
| | unknown / `None` | `HOLD` | fail-safe |
| canonical `SignalSchema.decision` (default source) | `APPROVED` | `APPROVE` | |
| | `REJECTED` | `REJECT` | |
| | `PENDING` / `None` | **`HOLD`** | decision hasn't concluded yet |

`EXPIRE` is a **new** time-based status STEP-09 adds — a stale
canonical signal (age > `DEFAULT_MAX_AGE_SECONDS`). The frozen engine
has no concept of it, so nothing is reused for it.

## 4. File responsibilities

| File | Does | Does NOT |
|---|---|---|
| `decision_status.py` | `DecisionStatus` (APPROVE/REJECT/HOLD/EXPIRE) + reuse mappings `from_decision_action` / `from_signal_decision` | recompute a verdict |
| `decision_model.py` | `DecisionOutcome` frozen dataclass (+ `is_approved`, `to_dict`, `to_json`) | hold a risk figure |
| `decision_rules.py` | pure decision rules; `RuleContext`, `apply_rules` (first override wins) | size risk / stops / exposure |
| `decision_router.py` | `DecisionConsumer` route metadata (`RISK` only for APPROVE) | send / dispatch anything |
| `decision_manager.py` | orchestrate: base status → rules → `DecisionOutcome` | modify the frozen engine |
| `__init__.py` | export the STEP-09 surface; document frozen-vs-additive | change the live path |

## 5. Business rules (decision, not risk)

Evaluated in priority order by `apply_rules()`; the **first override
wins**, otherwise the base status passes through. These are DECISION
rules — "should this signal proceed, hold, or expire" — not risk rules
(no lot size, no stop distance, no exposure; that is STEP-10 risk/).

| Rule | Fires when | Result |
|---|---|---|
| `reject_invalid` | direction not BUY/SELL, or entry/stop_loss/take_profit missing | `REJECT` |
| `expire_stale` | signal age > `DEFAULT_MAX_AGE_SECONDS` (900s) | `EXPIRE` |
| `hold_low_confidence` | base is APPROVE but `confidence_score` < `DEFAULT_MIN_CONFIDENCE` (0.5) | `HOLD` |

Thresholds (`DEFAULT_MIN_CONFIDENCE`, `DEFAULT_MAX_AGE_SECONDS`) are
STEP-09 decision-layer parameters, injectable via
`DecisionManager(min_confidence=…, max_age_seconds=…)` — distinct from
the frozen `DecisionConfig`/`DecisionWeights` (which stay Trading-Safety
protected and unchanged).

## 6. Routing

`decision_router.route(outcome)` is a pure function of `outcome.status`:

- `RISK` — included **only** for `APPROVE` (the next trading step).
- `DATABASE`, `AI`, `MONITORING`, `TELEGRAM` — **always** included, for
  the record, regardless of verdict.

It dispatches nothing — a consumer reads the route list and pulls the
outcome itself; decision/ never reaches down into risk or execution.

## 7. Trading-safety / boundary guarantees

- The FROZEN live path — `decision_engine.py`, `models.py`
  (`DecisionAction`, `TradeDecision`, `DecisionConfig`,
  `DecisionWeights`) — is **untouched**; STEP-09 imports `DecisionAction`
  read-only (as a mapping key) and constructs nothing on the live path.
- decision/ imports no `risk/`, `execution/`, `telegram/`, `database/`,
  `provider`, or `stream` runtime module; it reads a canonical signal
  duck-typed and returns data.
- Every path is fail-safe: a None/partial signal yields a defined
  `DecisionOutcome` (invalid → REJECT), never a raise.
- AI stays advisory: STEP-09 neither calls the AI layer nor lets it
  approve/reject — an AI verdict only reaches STEP-09 already folded
  into the frozen engine's `TradeDecision`, which is merely reused.

## 8. Tests

`tests/decision/test_step09_decision.py` (12 tests) cover: the status
vocabulary, both reuse mappings (incl. `NO_TRADE → HOLD`), the manager
pipeline (approve pass-through, reject, pending→hold, low-confidence
hold, stale expire, invalid reject, `trade_decision` reuse,
None-never-raises, serialization round-trip), and the router
(`RISK` only for APPROVE; observers always present). The pre-existing
`tests/unit/test_decision_engine.py` suite (the frozen engine) is
unchanged and still green.

## 9. Boundary with STEP-10 (risk/)

STEP-09 ends at the verdict. It answers *"should this signal proceed?"*
An APPROVE `DecisionOutcome` is the **input** to STEP-10 risk/, which
alone answers *"if it proceeds, at what size, stop, and exposure?"* No
risk maths lives in decision/.
