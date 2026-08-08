# 21 — Execution → Monitoring (REAL-DATA-005)

## Savol: execution/simulator natijasi trade monitorga uzatiladimi?

**Live production runtime'da — YO'Q (NOT VERIFIED / NOT WIRED).**
Foundation/backtesting'da ham fill→monitor handoff'i **mavjud emas** —
ExecutionSimulator natijasi va monitor ikki parallel foundation qismi,
ular o'zaro ulanmagan.

## Real kod trace

### Simulator natijasi qayerga boradi?

`ExecutionSimulationResult` (`simulator/models.py:68-79`) faqat bitta
consumer'ga boradi — analytics/reporting:

- `backtesting_layer/statistics/execution_report.py:build_execution_record()`
  (`:56+`) — "No new execution logic here; this module only reads an
  already-computed ExecutionSimulationResult" (`:11-12`). Bu monitor
  EMAS, hisobot (analytics record).

Grep tasdiqi: butun `backtesting_layer/` ichida `ExecutionSimulator`
yoki `.simulate(` ni monitorga uzatuvchi chaqiruv YO'Q.

### Monitor nimadan haydaladi?

`trade_monitoring_layer/paper_trading/paper_trade_monitor.py:42`
`check_paper_trade_against_candles(trade, candles)` — kirishi `PaperTrade`
+ candle list; u **`ExecutionSimulationResult`ni yoki fill_price'ni
umuman qabul qilmaydi**. Monitor to'g'ridan-to'g'ri `PaperTrade.entry`
ustida ishlaydi (`:83`), simulator fill'i orqali emas.

Yagona real consumer — `backtesting_layer/backtest_engine/backtest_engine.py:225`:
`paper_trade = check_paper_trade_against_candles(paper_trade, forward_candles).trade`
— bu backtest engine, live pipeline emas, va u simulator fill'ini emas,
paper_trade'ni to'g'ridan-to'g'ri uzatadi.

## Handoff elementlari (talab qilingan)

| Element | Holat | Izoh |
|---|---|---|
| Trade/order ID hand-off (simulator→monitor) | YO'Q | `SimulatedOrder.order_id`/`trade_id` monitorga uzatilmaydi |
| Position-state creation from fill | YO'Q | PaperTrade `create_paper_trade`/`open_paper_trade`dan, fill'dan emas |
| Close detection | Bor, lekin mustaqil | `check_paper_trade_against_candles` TP/SL/EXPIRED — candle arifmetikasi, simulator'siz |
| Restart recovery | YO'Q (live runtime) | Monitor stateless per-call (`paper_trade_monitor.py:60-70`); persistence live'da wired emas |

## Verdikt

**Execution → Monitoring = NOT VERIFIED / NOT WIRED.** Live production
runtime'da bu zanjir umuman mavjud emas (pipeline'da execution/monitoring
stage yo'q). Foundation/backtesting'da monitor mavjud, lekin u
ExecutionSimulator fill'idan haydalmaydi — fill→monitor handoff'i
kodda yo'q. Order bo'yicha bu holat WIRE QILINMADI (Trading-Safety
o'zgarishi, scope'dan tashqari).
</content>
