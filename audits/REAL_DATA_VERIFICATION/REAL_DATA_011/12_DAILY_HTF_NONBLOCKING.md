# 12 — Daily / HTF Parse Bug (REAL-DATA-011, Item K)

## Holat: KNOWN NON-BLOCKING (yashirilmagan)

REAL-DATA-004/006 da aniqlangan Daily candle parse bug'i **faqat HTF
bias'ga** ta'sir qiladi. HTF bias — **context-only / non-binding**:
DecisionEngine'ga to'rtta vaznli kirishdan biri sifatida beriladi
(`pipeline.py:487` — `decision_engine.evaluate(candidate, ai_result,
htf_bias)`), signalni bloklamaydi yoki majburlamaydi.

Dalil: pipeline Daily bias'siz ham **real signal ishlab chiqardi**
(REAL-DATA-004/006 runtime). Ya'ni bug data→risk spine'ni buzmaydi.

## Qaror (guardrail bo'yicha)

- **Bu passda TUZATILMAYDI.** RC1 oldidan candle-parser o'zgarishi
  non-blocking muammoga nomutanosib xavf.
- **Tavsiya:** keyingi ko'rib chiqilgan passda minimal-fix nomzodi
  sifatida (Daily svecha parseri), regressiya testi bilan.
- Yashirilmaydi — final hisobotda aniq qayd etiladi.

## Xulosa

Daily/HTF = **KNOWN NON-BLOCKING**, hujjatlashtirildi, tuzatilmadi.
