# Backtesting Layer
Status: CANONICAL
---
# Purpose
Backtesting Layer GoldBot arxitekturasidagi Canonical Simulation qatlami hisoblanadi.
Uning asosiy vazifasi tarixiy ma'lumot ustida to'liq GoldBot zanjirini — Context, Indicators, Strategies, AI, Decision, Risk va simulyatsiya qilingan Execution/Trade Monitoring — ishga tushirib, Strategy, AI va Risk xatti-harakatini tekshirishdir.
Backtesting Layer hech qachon Live Trading qilmaydi.
Backtesting Layer hech qachon Broker bilan ulanmaydi.
Backtesting Layer hech qachon Risk Manager'ni chetlab o'tmaydi.
Backtesting Layer hech qachon Decision Layer'ni almashtirmaydi.
---
# Objective
Backtesting Layer quyidagi vazifalarni bajaradi.
• Strategy Testing
• AI Testing
• Risk Testing
• Historical Replay
• Parameter Optimization
• Performance Statistics
• Backtest Reporting
---
# Layer Position
```text
Historical Data (Database Layer, read-only)
↓
Backtesting Layer
↓
Owner / Platform Layer (Report)
```
---
# Internal Modules
```text
Backtesting Layer
├── BacktestService
├── BacktestEngine
├── DataFeed
├── ReplayEngine
├── ReplayController
├── Statistics
├── BacktestReport
└── Optimization
```
---
# Module Overview
## BacktestService
Backtesting Layer'ning yagona Boundary Gateway'i — Entry va Exit.
---
## BacktestEngine
Tarixiy ma'lumot ustida to'liq GoldBot zanjirini ishga tushiruvchi Canonical Orchestrator. Hech qanday trading mantiqini qayta yozmaydi.
---
## DataFeed
"Candle qayerdan keladi" savolini qolgan mantiqdan ajratuvchi yagona seam. Iste'molchi Live yoki Replay rejimini ajrata olmaydi.
---
## ReplayEngine
Tarixiy candle'larni yuklaydi va bosqichma-bosqich uzatadi (Clock + Feed).
---
## ReplayController
Replay sessiyalarini session_id bo'yicha boshqaradi (start/pause/resume/stop/restart/step).
---
## Statistics
Simulyatsiya natijalaridan Win Rate, Profit Factor, Drawdown va Equity Curve hisoblaydi.
---
## BacktestReport
Hisoblangan statistikani yagona o'zgarmas Report obyektiga yig'adi va formatlaydi.
---
## Optimization
Turli parametrlar bilan ko'p marta Backtest ishga tushirib natijalarni taqqoslaydi (Blueprint bosqichi).
---
# Canonical Pipeline
```text
Historical Data
↓
Context
↓
Indicators
↓
Strategies
↓
AI
↓
Decision
↓
Risk
↓
Execution (Simulated)
↓
Trade Monitoring (Simulated)
↓
Statistics
↓
Report
```
Ushbu zanjirdagi Context, Indicators, Strategies, AI, Decision va Risk bosqichlari **mavjud Layer'lar tomonidan o'zgartirilmasdan** bajariladi — Backtesting Layer ularni faqat chaqiradi, qayta yozmaydi.
`Execution (Simulated)` va `Trade Monitoring (Simulated)` bosqichlari `11_Trade_Monitoring_Layer/PaperTrading` moduli orqali bajariladi — Backtesting Layer o'zining alohida simulyatsiya moduli yaratmaydi (Module Reuse Principle).
---
# Responsibilities
Backtesting Layer
✓ Historical Replay
✓ Full Chain Simulation
✓ Strategy / AI / Risk Testing
✓ Parameter Optimization
✓ Performance Statistics
✓ Backtest Reporting
---
# Not Responsible
Backtesting Layer
✗ Live Trading
✗ Broker Communication
✗ Real Trade Execution
✗ Signal Logic (Signal Layer vazifasi)
✗ Risk Logic (Risk Layer vazifasi)
✗ Decision Logic (Decision Layer vazifasi)
✗ Historical Data Fetching (01_Data_Layer vazifasi)
---
# Golden Rules
1. Backtesting Layer real trading infratuzilmasidan to'liq ajratilgan (Backtesting Isolation Rule).
2. Backtesting hech qachon real Broker, Platform yoki Trade Execution bilan bevosita ishlamaydi.
3. Backtesting hech qanday trading mantiqini qayta yozmaydi — faqat mavjud Layer'larni chaqiradi.
4. Har bir tasdiqlangan Decision majburiy ravishda Risk Manager'dan o'tadi — chetlab o'tish taqiqlanadi.
5. Simulyatsiya qilingan Execution va Trade Monitoring PaperTrading moduli orqali bajariladi.
6. Tarixiy ma'lumot faqat o'qiladi — hech qachon yozilmaydi.
7. Backtesting natijasi real Trade natijasi bilan aralashtirilmaydi.
8. Backtesting Layer'ga barcha kirish va chiqish faqat BacktestService orqali amalga oshiriladi.
9. Optimization natijasi avtomatik ravishda real savdoga qo'llanmaydi.
10. Circular Dependency qat'iyan taqiqlanadi.
---
# Repository Structure
```text
17_Backtesting_Layer/
├── README.md
├── Layer_ModuleMap.md
├── Layer_DataFlow.md
├── Layer_SequenceDiagram.md
├── Layer_Contracts.md
│
├── BacktestService/
├── BacktestEngine/
├── DataFeed/
├── ReplayEngine/
├── ReplayController/
├── Statistics/
├── BacktestReport/
└── Optimization/
```
Har bir modul o'z README.md, Contracts.md, ModuleMap.md va SequenceDiagram.md fayllariga ega.
---
# Summary
Backtesting Layer GoldBot arxitekturasidagi Canonical Simulation qatlami bo'lib, tarixiy ma'lumot ustida Strategy, AI va Risk xatti-harakatini real savdoga ta'sir qilmasdan tekshirish imkonini beradi. U real trading infratuzilmasidan to'liq ajratilgan va hech qachon Risk Manager'ni chetlab o'tmaydi.
