# Backtest Engine
Status: CANONICAL
---
# Purpose
BacktestEngine GoldBot Backtesting Layer ichidagi Canonical Orchestrator moduli hisoblanadi.
Uning asosiy vazifasi tarixiy ma'lumot ustida to'liq GoldBot zanjirini — Context, Indicators, Strategies, AI, Decision, Risk va simulyatsiya qilingan Execution/Monitoring — ketma-ket ishga tushirishdir.
BacktestEngine hech qanday trading mantiqini qayta yozmaydi — u faqat mavjud Layer'larni chaqiradi.
BacktestEngine hech qachon Risk Manager'ni chetlab o'tmaydi.
---
# Objective
BacktestEngine quyidagi vazifalarni bajaradi.
• Full Chain Simulation
• Context Reuse
• Strategy Evaluation
• AI Evaluation
• Decision Evaluation
• Risk Evaluation
• Simulated Trade Lifecycle
• Result Aggregation
---
# Layer Position
```text
BacktestService
↓
BacktestEngine
↓
DataFeed
```
---
# Responsibilities
BacktestEngine
✓ Tarixiy candle oqimini DataFeed orqali oladi
✓ Mavjud Context/Signal/AI/Decision/Risk Layer'larini o'zgartirmasdan chaqiradi
✓ Har bir tasdiqlangan Decision uchun PaperTrading orqali simulyatsiya qiladi
✓ Har bir simulyatsiya natijasini Statistics'ga uzatadi
---
# Not Responsible
BacktestEngine
✗ Trading Logic Reimplementation
✗ Signal Generation (Signal Layer vazifasi)
✗ Risk Calculation (Risk Layer vazifasi)
✗ Real Trade Execution
✗ Broker Communication
✗ Report Formatting (BacktestReport vazifasi)
---
# Input
BacktestEngine qabul qiladi.
• Backtest Configuration
• Historical Candles (DataFeed orqali)
• Strategy Selection
---
# Output
BacktestEngine yaratadi.
• Simulated Trade Results
• Signal Performance Records
• Backtest Run Metadata
---
# Workflow
```text
BacktestService
↓
BacktestEngine
↓
DataFeed
```
---
# Internal Modules (Planned — implementatsiya bosqichida to'ldiriladi)
```text
BacktestEngine
├── ChainRunner
├── CandidateEvaluator
└── SimulationLoop
```
---
# Golden Rules
1. BacktestEngine hech qanday trading mantiqini qayta yozmaydi — faqat mavjud Layer'larni chaqiradi.
2. Har bir tasdiqlangan Decision majburiy ravishda Risk Manager'dan o'tadi — chetlab o'tish taqiqlanadi.
3. Simulyatsiya qilingan Execution va Trade Monitoring PaperTrading moduli orqali bajariladi.
4. BacktestEngine hech qachon real Broker'ga murojaat qilmaydi.
5. Live Data ishlatilmaydi — faqat tarixiy ma'lumot.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
BacktestEngine/
├── README.md
├── Contracts.md
├── ModuleMap.md
└── SequenceDiagram.md
```
---
# Summary
BacktestEngine tarixiy ma'lumot ustida to'liq GoldBot zanjirini simulyatsiya qiluvchi Canonical Orchestrator hisoblanadi.
