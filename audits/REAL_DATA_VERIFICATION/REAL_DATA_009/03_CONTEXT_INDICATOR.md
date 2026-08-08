# 03 — Context → Indicator — REAL-DATA-009

## Transition

Context → Indicator (market_phase / feature_engine; Parallel Execution).

- **INPUT:** `context` (ContextSnapshot) — `pipeline.py:369`.
- **PROCESSING:**
  - `compute_market_phase(context)` — `pipeline.py:381`
    (`context_layer/trend/market_phase/market_phase.py`). 6-holatli
    klassifikatsiya (ACCUMULATION/MANIPULATION/DISTRIBUTION/MARKUP/
    MARKDOWN/UNKNOWN) — `context`dagi mavjud ma'lumotdan (wyckoff_events,
    amd_events, market_regime), yangi detection logikasi yo'q.
  - `compute_market_features(context, explanation, symbol, interval,
    htf_bias)` — `pipeline.py:453`
    (`core_layer/features/feature_engine.py`) — standardizatsiya
    qatlami, MarketFeatures obyektini quradi.
- **OUTPUT:** `market_phase: MarketPhaseResult` (`pipeline.py:381`),
  `features: List[MarketFeatures]` (`pipeline.py:452`).
- **NEXT CONSUMER:** market_phase → signal_history
  (`pipeline.py:526`); features → run() natija dict (`pipeline.py:642`,
  advisory, kelajakdagi consumer uchun).

## Parallel Execution Rule

market_phase va feature_engine mustaqil, "indicator-ekvivalent"
advisory hisoblagichlar — ular bir-birini bloklamaydi va signal/
decision/risk oqimiga ta'sir qilmaydi (pipeline docstring:70-79,
99-116).

## Ownership

`indicator_layer/indicator_service/` — skeleton (ownership placeholder);
haqiqiy indicator-ekvivalent hisob context_layer detektorlarida va
`core_layer/features/feature_engine.py`da bajariladi.

## Real runtime dalil

Run `31240675527`: `market_phase MARKUP`, `features
[('TRENDING','LONDON_NEW_YORK_OVERLAP','B')]` — real data bilan.

## Status: PASS
</content>
