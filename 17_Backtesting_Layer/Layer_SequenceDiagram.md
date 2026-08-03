# Backtesting Layer Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Backtesting Layer Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Backtesting Layer uchun Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Owner Command
↓
BacktestService (Entry)
↓
BacktestEngine
↓
DataFeed
↓
ReplayEngine
↓
Context → Indicators → Strategies → Signal → AI → Decision → Risk
↓
PaperTrading (Execution + Trade Monitoring, Simulated)
↓
Statistics
↓
BacktestReport
↓
BacktestService (Exit)
↓
Owner
```
---
# Replay Session Sequence
```text
Owner Command
↓
BacktestService (Entry)
↓
ReplayController
↓
ReplayEngine
↓
Candle Stream
↓
BacktestService (Exit)
```
---
# Runtime Rules
1. BacktestService Backtesting Layer'ning yagona Entry va Exit nuqtasi hisoblanadi.
2. BacktestEngine barcha ichki modullarni orkestratsiya qiladi.
3. Context, Indicators, Strategies, Signal, AI, Decision va Risk Layer'lari o'zgartirilmasdan chaqiriladi.
4. Risk Layer majburiy bosqich — hech qanday holatda chetlab o'tilmaydi.
5. Execution va Trade Monitoring faqat simulyatsiya sifatida, PaperTrading orqali bajariladi.
6. Backtesting Layer hech qachon real Broker, Execution Layer yoki Live Data bilan ishlamaydi (Backtesting Isolation Rule).
7. Optimization yuqoridagi zanjirning bosqichi emas — u BacktestEngine'ni ko'p marta ishga tushiradigan parallel yo'l.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# State Flow
```text
Idle
↓
Initializing
↓
Loading Historical Data
↓
Simulating
↓
Computing Statistics
↓
Reporting
↓
Completed
```
---
# Summary
Owner Command
↓
Backtesting Layer
↓
Backtest Report
