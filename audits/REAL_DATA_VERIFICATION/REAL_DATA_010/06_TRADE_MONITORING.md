# 06 — Trade Monitoring (REAL-DATA-010)

## Savol: Execution result → Trade ID/Position → Monitoring mavjudmi?

**Live runtime'da — YO'Q.** Foundation/backtesting'da monitor mavjud,
ammo u ExecutionSimulator fill'idan haydalmaydi.

## Monitor nimadan haydaladi

`trade_monitoring_layer/paper_trading/paper_trade_monitor.py:42-45` —
`check_paper_trade_against_candles(trade: PaperTrade, candles: List[Candle])`.
Monitor to'g'ridan-to'g'ri `PaperTrade.entry` ustida ishlaydi (`:83`),
`ExecutionSimulationResult`ni yoki `fill_price`ni **umuman qabul
qilmaydi**.

## Talab qilingan elementlar

| Element | Holat | Dalil (file:line) |
|---|---|---|
| Fill detection | YO'Q (handoff yo'q) | monitor `SimulatedFill` qabul qilmaydi (`paper_trade_monitor.py:42-45`) |
| Position tracking | Foundation | `PaperTrade` state machine (`paper_trade.py`), lekin live loop yo'q |
| SL-TP monitoring | Bor, mustaqil | `paper_trade_monitor.py:88-103` — candle arifmetikasi, simulator'siz |
| Close detection | Bor, mustaqil | `close_paper_trade(trade, "TP"/"SL"/"EXPIRED")` (`:101-106`) |
| Restart recovery | YO'Q (live) | monitor stateless per-call (`:60-70`); `recovery_manager/__init__.py` bo'sh skeleton |
| State persistence | Live'da wired emas | `:69` raw_candle_repository'ga havola, lekin monitor o'zi accumulate qilmaydi |

## Yagona real consumer

`backtesting_layer/backtest_engine/backtest_engine.py:225` —
`check_paper_trade_against_candles(paper_trade, forward_candles).trade`.
Bu **backtest engine**, live pipeline emas; va u simulator fill'ini
emas, `paper_trade`ni to'g'ridan-to'g'ri uzatadi.

## Verdikt

**Execution result → Trade ID/Position → Monitoring = NOT VERIFIED /
NOT WIRED.** Execution live-wired bo'lmagani uchun execution natijasi
monitorga topshirilmaydi; monitorning o'zi faqat backtest'da candle
arifmetikasi sifatida ishlaydi.
