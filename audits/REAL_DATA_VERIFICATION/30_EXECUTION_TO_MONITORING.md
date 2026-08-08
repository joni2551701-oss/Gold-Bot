# 30 — Execution → Trade Monitoring (TASK-08)

## Transition
Execution → Trade Monitoring (PositionMonitor / TradeLifecycleManager /
RecoveryManager / BreakevenManager / TrailingStop / PartialClose; Trade
Monitoring risk'ni qayta hisoblamasligi yoki Risk Manager'ni chetlab
o'tmasligi kerak).

## Input
Real ochilgan pozitsiya (real broker order natijasi).

## Processing (file:line)
- Real pozitsiya mavjud emas (29-hujjat: execution inert). Shu sababli
  monitoring uchun real kirish yo'q.
- `trade_monitoring_layer` `core_layer/pipeline/pipeline.py`ga import
  QILINMAGAN (import bloki `:1-29` — trade_monitoring_layer yo'q). Ya'ni
  live pipeline'da Trade Monitoring bosqichi ishlamaydi.
- Modullar mavjud, lekin live yo'lda emas:
  `trade_monitoring_layer/position_monitor/`,
  `trade_monitoring_layer/trade_lifecycle_manager/`,
  `trade_monitoring_layer/recovery_manager/`,
  `trade_monitoring_layer/breakeven_manager/`,
  `trade_monitoring_layer/trailing_stop/`,
  `trade_monitoring_layer/partial_close/`.
- `paper_trading` (`trade_monitoring_layer/paper_trading/`) mavjud, lekin
  `pipeline.run()`ga ulanmagan.

## Output
Yo'q (real pozitsiya monitoring'i mavjud emas).

## Ownership-rule check
- Trade Monitoring risk'ni qayta hisoblamaydi / Risk Manager'ni chetlab
  o'tmaydi — chunki u live pipeline yo'lida umuman ishtirok etmaydi
  (import yo'q). Chetlab o'tish imkoniyati runtime'da mavjud emas.

## Status
**NOT VERIFIED (dizayn bo'yicha)** — real pozitsiyaning Trade Monitoring'i
execution inert bo'lgani uchun real dalil bera olmaydi. Bu dizayn holati,
nosozlik emas.

## Unblock qilish uchun
Avval Execution yoqilishi kerak (29-hujjat, Director approval), keyin
real pozitsiya monitoring'i tekshirilishi mumkin.
</content>
