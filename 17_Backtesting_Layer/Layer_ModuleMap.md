# Backtesting Layer Module Map
Status: CANONICAL
---
# Layer Architecture
```text
Backtesting Layer
        │
        ├── BacktestService
        │
        ├── BacktestEngine
        │
        ├── DataFeed
        │
        ├── ReplayEngine
        │
        ├── ReplayController
        │
        ├── Statistics
        │
        ├── BacktestReport
        │
        └── Optimization
```
---
# Processing Pipeline
```text
Owner Command (Platform Layer)
        │
        ▼
BacktestService (Entry)
        │
        ├───────────────────────┐
        ▼                       ▼
BacktestEngine          ReplayController
        │                       │
        ▼                       ▼
    DataFeed  ◄────────── ReplayEngine
        │
        ▼
Mavjud Layer'lar (o'zgartirilmasdan chaqiriladi)
Context → Indicators → Strategies → AI → Decision → Risk
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
`Optimization` yuqoridagi zanjirning bir bosqichi emas — u BacktestService orqali kiradigan va BacktestEngine'ni ko'p marta ishga tushiradigan parallel yo'l hisoblanadi.
---
# Module Responsibilities
| Module | Responsibility |
|---|---|
| BacktestService | Layer Boundary Gateway (Entry va Exit), Request Validation |
| BacktestEngine | Full Chain Simulation Orchestration |
| DataFeed | Data Source Abstraction (Live / Replay seam) |
| ReplayEngine | Historical Candle Loading, Clock, Traversal |
| ReplayController | Replay Session Lifecycle Management |
| Statistics | Performance Metrics, Strategy Grouping, Equity Curve |
| BacktestReport | Report Assembly va Formatting |
| Optimization | Parameter Sweep, Multi Run Comparison (Blueprint) |
---
# Dependency Structure
Har bir modulning Allowed/Forbidden Dependencies ro'yxati o'z `Contracts.md`/`ModuleMap.md` hujjatida belgilangan. Umumiy qoida:
* Barcha modullar uchun Execution Layer (real order), Broker Gateway, Platform Layer (to'g'ridan-to'g'ri) va Live Data **Forbidden** hisoblanadi (Backtesting Isolation Rule).
* Backtesting Layer'ga barcha kirish va chiqish faqat BacktestService orqali amalga oshiriladi.
* Context, Indicators, Strategies, AI, Decision va Risk Layer'lari BacktestEngine tomonidan **o'zgartirilmasdan** chaqiriladi.
* Simulyatsiya qilingan Execution/Monitoring uchun `11_Trade_Monitoring_Layer/PaperTrading` qayta ishlatiladi — yangi simulyatsiya moduli yaratilmaydi.
---
# Summary
Backtesting Layer 8 modulning Canonical xaritasi ushbu hujjatda belgilangan. Layer real trading infratuzilmasidan to'liq ajratilgan bo'lib, mavjud Layer'larni qayta yozmasdan simulyatsiya qiladi.
