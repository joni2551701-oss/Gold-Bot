# Backtesting Layer Data Flow
Status: CANONICAL
---
# Purpose
Ushbu hujjat Backtesting Layer ichidagi ma'lumot oqimini tavsiflaydi.
Bu implementatsiya emas.
Bu Backtesting Layer uchun Canonical Data Flow hisoblanadi.
---
# Layer Data Flow
```text
Owner Command (Backtest / Replay Request)
        │
        ▼
BacktestService (Entry)
        │
        ▼
BacktestEngine
        │
        ▼
    DataFeed
        │
        ▼
  ReplayEngine
        │
        ▼
Historical Candles (Database Layer — read-only)
        │
        ▼
Context Layer          (o'zgartirilmasdan chaqiriladi)
        │
        ▼
Indicator Layer        (o'zgartirilmasdan chaqiriladi)
        │
        ▼
Strategy Layer         (o'zgartirilmasdan chaqiriladi)
        │
        ▼
Signal Layer           (o'zgartirilmasdan chaqiriladi)
        │
        ▼
AI Layer               (o'zgartirilmasdan chaqiriladi)
        │
        ▼
Decision Layer         (o'zgartirilmasdan chaqiriladi)
        │
        ▼
Risk Layer             (MAJBURIY — chetlab o'tilmaydi)
        │
        ▼
PaperTrading (11_Trade_Monitoring_Layer)
Execution (Simulated) + Trade Monitoring (Simulated)
        │
        ▼
   Statistics
        │
        ▼
 BacktestReport
        │
        ▼
BacktestService (Exit)
        │
        ▼
      Owner
```
---
# Replay Session Flow
```text
Owner Command (start / pause / resume / stop / restart / step)
        │
        ▼
BacktestService (Entry)
        │
        ▼
ReplayController
        │
        ▼
  ReplayEngine
        │
        ▼
   Candle Stream
        │
        ▼
BacktestService (Exit)
```
---
# Input Sources
• Owner Command (Backtest Request, Replay Request — Platform Layer orqali)
• Historical Candles (Database Layer'dan, faqat o'qish)
• Backtest / Replay Configuration
• Parameter Space (Optimization uchun)
---
# Output
• Backtest Report
• Performance Metrics
• Equity Curve
• Replay Status
• Optimization Result
---
# Data Flow Rules
1. Backtesting Layer faqat tarixiy ma'lumot bilan ishlaydi — Live Data ishlatilmaydi.
2. Tarixiy ma'lumot faqat o'qiladi, hech qachon yozilmaydi.
3. Context, Indicators, Strategies, Signal, AI, Decision va Risk Layer'lari o'zgartirilmasdan chaqiriladi.
4. Risk Layer majburiy bosqich hisoblanadi — chetlab o'tish taqiqlanadi.
5. Execution (Simulated) va Trade Monitoring (Simulated) PaperTrading orqali bajariladi.
6. Backtesting hech qachon real Broker yoki Execution Layer bilan bevosita ishlamaydi (Backtesting Isolation Rule).
7. Barcha kirish va chiqish faqat BacktestService orqali amalga oshiriladi.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Summary
Backtesting Layer tarixiy ma'lumotni o'qib, mavjud GoldBot Layer'larini o'zgartirmasdan chaqiradi va simulyatsiya natijasini Statistics hamda BacktestReport orqali Owner'ga yetkazadi. Real trading infratuzilmasi bu oqimda umuman ishtirok etmaydi.
