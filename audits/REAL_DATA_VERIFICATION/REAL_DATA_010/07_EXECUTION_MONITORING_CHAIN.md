# 07 — Execution → Monitoring Zanjiri (REAL-DATA-010)

## Savol: simulator/execution natijasi trade monitorga uzatiladimi?

**YO'Q — NOT VERIFIED / NOT WIRED** (ham live, ham foundation/backtest).

## Simulator natijasi qayerga boradi

`ExecutionSimulationResult` (`models.py:68-79`) yagona consumer'ga
boradi — analytics/reporting:

- `backtesting_layer/statistics/execution_report.py` —
  `build_execution_record()` allaqachon hisoblangan
  `ExecutionSimulationResult`ni **faqat o'qiydi** (docstring: "No new
  execution logic here; this module only reads an already-computed
  ExecutionSimulationResult"). Bu monitor EMAS, analytics record.

Grep tasdiqi: `execution_layer` ni import qiladigan non-test modullar —
`trade_monitoring_layer/paper_trading/paper_trade.py` (faqat docstring
havolalari, `:14-19`, real import emas), `platform_layer/telegram/owner/
execution_commands.py` (owner diagnostik), `backtesting_layer/statistics/
execution_report.py` (analytics). **Bironta ham simulator natijasini
monitorga uzatmaydi.**

## Handoff elementlari

| Element | Holat |
|---|---|
| Trade/order ID hand-off (simulator→monitor) | YO'Q — `SimulatedOrder.order_id/trade_id` monitorga uzatilmaydi |
| Position-state creation from fill | YO'Q — `PaperTrade` `create_paper_trade`/`open_paper_trade`dan, fill'dan emas |
| Close detection | Bor, lekin fill'dan mustaqil (candle arifmetikasi) |
| Restart recovery | YO'Q (live) |

## Verdikt

**EXECUTION → MONITORING = NOT VERIFIED / NOT WIRED.** Simulator natijasi
va monitor — ikki parallel foundation qismi, ular o'rtasida fill→monitor
handoff kodda mavjud emas. Bu bo'shliq WIRE QILINMADI (Trading-Safety
o'zgarishi, scope'dan tashqari). REAL-DATA-005 topilmasi (`5fb4c57`)
qayta tasdiqlandi.
