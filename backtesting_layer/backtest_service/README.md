# Backtest Service
Status: CANONICAL
---
# Purpose
BacktestService GoldBot Backtesting Layer'ning yagona Canonical Boundary Gateway moduli hisoblanadi.
Barcha tashqi Backtest va Replay so'rovlari faqat BacktestService orqali kiradi va natijalar faqat BacktestService orqali chiqadi.
BacktestService simulyatsiya mantiqini o'zi bajarmaydi — u faqat orkestratsiya va Boundary vazifasini bajaradi.
---
# Objective
BacktestService quyidagi vazifalarni bajaradi.
• Backtest Request Validation
• Replay Request Validation
• Layer Entry Gateway
• Layer Exit Gateway
• Backtest Lifecycle Coordination
• Result Delivery
---
# Layer Position
```text
Owner Command (Platform Layer)
↓
BacktestService
↓
BacktestEngine / ReplayController
```
---
# Responsibilities
BacktestService
✓ Tashqi Backtest va Replay so'rovlarini qabul qiladi
✓ So'rovlarni tekshiradi (Symbol, Timeframe, Date Range, Strategy)
✓ BacktestEngine yoki ReplayController'ga uzatadi
✓ Yakuniy Backtest Report'ni tashqariga qaytaradi
---
# Not Responsible
BacktestService
✗ Simulation Execution (BacktestEngine vazifasi)
✗ Candle Traversal (ReplayEngine vazifasi)
✗ Statistics Calculation
✗ Real Trade Execution
✗ Signal Generation
✗ Risk Calculation
---
# Input
BacktestService qabul qiladi.
• Backtest Request
• Replay Request
• Backtest Configuration
---
# Output
BacktestService yaratadi.
• Backtest Report
• Replay Status
• Backtest Status
• Validation Error
---
# Workflow
```text
Owner Command (Platform Layer)
↓
BacktestService
↓
BacktestEngine / ReplayController
```
---
# Internal Modules (Planned — implementatsiya bosqichida to'ldiriladi)
```text
BacktestService
├── RequestValidator
├── BacktestCoordinator
└── ResultDispatcher
```
---
# Golden Rules
1. Backtesting Layer'ga barcha kirish va chiqish faqat BacktestService orqali amalga oshiriladi.
2. Har bir Backtest Request tekshirilishi shart.
3. BacktestService simulyatsiya mantiqini o'zi bajarmaydi.
4. BacktestService hech qachon real Broker yoki Execution Layer bilan ishlamaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
BacktestService/
├── README.md
├── Contracts.md
├── ModuleMap.md
└── SequenceDiagram.md
```
---
# Summary
BacktestService Backtesting Layer'ning yagona Entry va Exit Gateway'i hisoblanadi.
