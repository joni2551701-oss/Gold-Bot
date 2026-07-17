# GoldBot — Decision Engine

Governed by `docs/constitution/CONSTITUTION.md` Article 1. Verified
directly against `decision/decision_engine.py`.

**AI qaror bermaydi.** The Decision Engine is the one place a trade
signal becomes APPROVED, REJECTED, or held. It reads the AI's analysis
as one input value; it never lets the AI layer call it, and the AI
layer never calls `decision/`, `risk/`, or `execution/` back.

## The real formula

**Correction to a simplified brief sketch**: the blend is not three
terms (Technical + AI + Risk). `decision/decision_engine.py`'s
`_weighted_score()` blends **four** components, per `DecisionWeights`:

```
final_confidence = weighted(
    signal_confidence,   # from SignalCandidate.confidence
    htf_score,            # from HTFBiasResult.confidence (0-100 -> 0.0-1.0)
    risk_score,            # inverted AI risk score
    ai_score,               # from AIAnalysisResult.confidence
)
```

All four are on the same 0.0–1.0 scale as every other confidence field
in this codebase before blending — `htf_score` is the one that needs
converting in, since `HTFBiasResult.confidence` is natively 0–100.

## Thresholds → outcome

```
final_confidence < min_confidence (default 0.50)      → NO_TRADE
final_confidence < approve_confidence (default 0.80)   → REJECT
final_confidence >= approve_confidence                  → APPROVE
```

`min_confidence`/`approve_confidence` live in `DecisionConfig`, never
hardcoded inline in `evaluate()` — the same "config, not a magic
number" convention the rest of this codebase follows.

## `DecisionResult`

Carries `ai_confidence` explicitly (not folded silently into
`final_confidence`) so a caller — including `docs/trading/RISK_SYSTEM.md`'s
`RiskManager` and any Telegram-facing explanation — can see the AI's
own contribution separately from the blended outcome.

## Related

- `docs/trading/TRADING_ARCHITECTURE.md` — where Decision sits in the
  trading-scoped pipeline order.
- `docs/DECISION_PRINCIPLES.md` — the original decision-principles
  document.
- `docs/constitution/CONSTITUTION.md` Article 1, the boundary this
  entire module exists to enforce.
