# 15 — Real Runtime Evidence (REAL-DATA-011, Item O)

## Mavjud dalil

- CI real-data probe mavjud: `scripts/verification/real_price_stream_probe.py`,
  `scripts/verification/real_market_data_probe.py`.
- `python main.py` trace mavjud va graceful (barcha stage'lar, batch
  path o'zgarmagan).
- Oldingi real-runtime dalillari: REAL-DATA-008 run `31253603648`
  (3/3 real current-price updates), REAL-DATA-009 run `31240675527`
  (data→risk to'liq PASS), REAL-DATA-004 real XAU/USD 200 candle.

## CI run placeholder

> **PLACEHOLDER — CI evidence:** Orchestrator REAL-DATA-011 uchun yangi
> CI run dispatch qiladi (Worker DISPATCH QILMAYDI — guardrail O).
> Run ID va natija (real XAU/USD price, PRICE_UPDATED publish count,
> data→risk PASS) shu joyga qo'shiladi:
>
> - Run ID: `__PENDING_ORCHESTRATOR_DISPATCH__`
> - Natija: `__PENDING__`

Bu passda Worker CI dispatch qilmadi; dalil o'rni qoldirildi.
