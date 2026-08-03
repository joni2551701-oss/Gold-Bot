# Backtest Service Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat BacktestService modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
BacktestService quyidagilar uchun javobgar.
✓ Tashqi Backtest va Replay so'rovlarini qabul qiladi
✓ So'rovlarni tekshiradi (Symbol, Timeframe, Date Range, Strategy)
✓ BacktestEngine yoki ReplayController'ga uzatadi
✓ Yakuniy Backtest Report'ni tashqariga qaytaradi
BacktestService bajarmaydi.
✗ Simulation Execution (BacktestEngine vazifasi)
✗ Candle Traversal (ReplayEngine vazifasi)
✗ Statistics Calculation
✗ Real Trade Execution
✗ Signal Generation
✗ Risk Calculation
---
# Module Boundary
```text
Owner Command (Platform Layer)
↓
BacktestService
↓
BacktestEngine / ReplayController
```
---
# Input Contract
• Backtest Request
• Replay Request
• Backtest Configuration
---
# Output Contract
• Backtest Report
• Replay Status
• Backtest Status
• Validation Error
---
# Allowed Dependencies
✓ BacktestEngine
✓ ReplayController
✓ BacktestReport
✓ Optimization
---
# Forbidden Dependencies
✗ Execution Layer (real order — Backtesting Isolation Rule)
✗ Broker Gateway
✗ Platform Layer (to'g'ridan-to'g'ri)
✗ Live Data (real vaqt oqimi)
✗ Signal Layer (to'g'ridan-to'g'ri)
✗ AI Layer (to'g'ridan-to'g'ri)
✗ Decision Layer (to'g'ridan-to'g'ri)
✗ Risk Layer (to'g'ridan-to'g'ri)
---
# Runtime Contract
1. Backtesting Layer'ga barcha kirish va chiqish faqat BacktestService orqali amalga oshiriladi.
2. Har bir Backtest Request tekshirilishi shart.
3. BacktestService simulyatsiya mantiqini o'zi bajarmaydi.
4. BacktestService hech qachon real Broker yoki Execution Layer bilan ishlamaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Backtest Request qabul qilinadi.
✓ Request tekshiriladi.
✓ BacktestEngine ishga tushiriladi.
✓ Backtest Report qaytariladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
BacktestService Contract BacktestService Backtesting Layer'ning yagona Entry va Exit Gateway'i hisoblanadi.
