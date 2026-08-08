# 02 — Core → Context — REAL-DATA-009

## Transition

Core (market_data + htf_bias) → Context (Market Context).

- **INPUT:** `candles: List[Candle]` (`pipeline.py:325` `get_candles`) va
  `htf_bias: HTFBiasResult` (`pipeline.py:358`).
- **PROCESSING:** `build_context_snapshot(candles, htf_bias)` —
  `pipeline.py:369`. Bu `context_layer/context_engine/context_orchestrator/context_orchestrator.py`'ning
  `build_context_snapshot()` funksiyasiga o'tadi; `ContextEngine`
  barcha context detektorlarini (market_structure, liquidity,
  order_block, fvg, wyckoff, amd, session, market_regime)
  orkestratsiya qiladi.
- **OUTPUT:** `context` (ContextSnapshot) — `pipeline.py:369`.
- **NEXT CONSUMER:** market_phase stage `compute_market_phase(context)`
  (`pipeline.py:381`) va signal stage `generate_signals(context)`
  (`pipeline.py:405`).

## Ownership

- **ContextService / ContextEngine** — Market Context'ning egasi;
  `context_layer/context_engine/context_orchestrator/context_orchestrator.py`. Pipeline faqat
  `build_context_snapshot()` fasadini chaqiradi, ichki detektorlarga
  to'g'ridan-to'g'ri kirmaydi (Layer boundary saqlangan).

## Real runtime dalil

REAL-DATA-004 run `31240675527`: `stage=context (ran)` → `market_phase
MARKUP (TRENDING BULLISH)` real 200 candle bilan. Context real data
bilan qurildi.

## Status: PASS
</content>
