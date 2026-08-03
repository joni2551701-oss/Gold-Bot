# Backtesting Layer Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat Backtesting Layer uchun rasmiy Architecture Contract hisoblanadi.
---
# Layer Responsibility
Backtesting Layer quyidagilar uchun javobgar.
✓ Historical Replay
✓ Full Chain Simulation
✓ Strategy Testing
✓ AI Testing
✓ Risk Testing
✓ Parameter Optimization
✓ Performance Statistics
✓ Backtest Reporting
---
# Layer Does NOT
✗ Live Trading
✗ Broker Communication
✗ Real Trade Execution
✗ Signal Logic (Signal Layer vazifasi)
✗ AI Logic (AI Layer vazifasi)
✗ Decision Logic (Decision Layer vazifasi)
✗ Risk Logic (Risk Layer vazifasi)
✗ Historical Data Fetching (01_Data_Layer vazifasi)
---
# Input Contract
Backtesting Layer qabul qiladi.
• Backtest Request (Owner Command, Platform Layer orqali)
• Replay Request (Owner Command, Platform Layer orqali)
• Backtest Configuration (Symbol, Timeframe, Date Range, Strategy)
• Historical Candles (Database Layer'dan, faqat o'qish)
• Parameter Space (Optimization uchun)
---
# Output Contract
Backtesting Layer yaratadi.
• Backtest Report
• Performance Metrics
• Equity Curve
• Replay Status
• Optimization Result
---
# Layer Pipeline
```text
Owner Command
↓
BacktestService (Entry)
↓
BacktestEngine
↓
DataFeed → ReplayEngine → Historical Candles
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
# Layer Rules
1. Backtesting Layer real trading infratuzilmasidan to'liq ajratilgan bo'lishi shart (Backtesting Isolation Rule).
2. Backtesting Layer hech qachon real Broker, Platform yoki Trade Execution bilan bevosita ishlamaydi.
3. Backtesting Layer hech qanday trading mantiqini qayta yozmaydi — faqat mavjud Layer'larni o'zgartirmasdan chaqiradi.
4. Har bir tasdiqlangan Decision majburiy ravishda Risk Manager'dan o'tadi — chetlab o'tish qat'iyan taqiqlanadi.
5. Execution (Simulated) va Trade Monitoring (Simulated) `11_Trade_Monitoring_Layer/PaperTrading` orqali bajariladi — yangi simulyatsiya moduli yaratilmaydi.
6. Tarixiy ma'lumot faqat o'qiladi — hech qachon yozilmaydi.
7. Live Data ishlatilmaydi.
8. Backtesting Layer'ga barcha kirish va chiqish faqat BacktestService orqali amalga oshiriladi.
9. Backtesting natijasi real Trade natijasi bilan hech qachon aralashtirilmaydi.
10. Optimization natijasi avtomatik ravishda real savdoga qo'llanmaydi.
11. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Backtest Request BacktestService orqali qabul qilinadi.
✓ Tarixiy candle oqimi DataFeed/ReplayEngine orqali olinadi.
✓ Mavjud Layer'lar o'zgartirilmasdan chaqiriladi.
✓ Risk Manager chetlab o'tilmaydi.
✓ Simulyatsiya PaperTrading orqali bajariladi.
✓ Statistics hisoblanadi va BacktestReport yaratiladi.
✓ Hech qanday real Broker chaqiruvi bo'lmaydi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Backtesting Layer Contract GoldBot arxitekturasidagi Canonical Simulation qatlamining rasmiy shartnomasi hisoblanadi. U tarixiy ma'lumot ustida Strategy, AI va Risk xatti-harakatini tekshirishni, real trading infratuzilmasidan to'liq ajratilgan bo'lishni va Risk Manager'ni hech qachon chetlab o'tmaslikni belgilaydi.
