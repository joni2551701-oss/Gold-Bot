# Backtest Engine Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat BacktestEngine modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
BacktestEngine quyidagilar uchun javobgar.
✓ Tarixiy candle oqimini DataFeed orqali oladi
✓ Mavjud Context/Signal/AI/Decision/Risk Layer'larini o'zgartirmasdan chaqiradi
✓ Har bir tasdiqlangan Decision uchun PaperTrading orqali simulyatsiya qiladi
✓ Har bir simulyatsiya natijasini Statistics'ga uzatadi
BacktestEngine bajarmaydi.
✗ Trading Logic Reimplementation
✗ Signal Generation (Signal Layer vazifasi)
✗ Risk Calculation (Risk Layer vazifasi)
✗ Real Trade Execution
✗ Broker Communication
✗ Report Formatting (BacktestReport vazifasi)
---
# Module Boundary
```text
BacktestService
↓
BacktestEngine
↓
DataFeed
```
---
# Input Contract
• Backtest Configuration
• Historical Candles (DataFeed orqali)
• Strategy Selection
---
# Output Contract
• Simulated Trade Results
• Signal Performance Records
• Backtest Run Metadata
---
# Allowed Dependencies
✓ BacktestService
✓ DataFeed
✓ Statistics
✓ PaperTrading (11_Trade_Monitoring_Layer)
---
# Forbidden Dependencies
✗ Execution Layer (real order — Backtesting Isolation Rule)
✗ Broker Gateway
✗ Platform Layer (to'g'ridan-to'g'ri)
✗ Live Data (real vaqt oqimi)
---
# Runtime Contract
1. BacktestEngine hech qanday trading mantiqini qayta yozmaydi — faqat mavjud Layer'larni chaqiradi.
2. Har bir tasdiqlangan Decision majburiy ravishda Risk Manager'dan o'tadi — chetlab o'tish taqiqlanadi.
3. Simulyatsiya qilingan Execution va Trade Monitoring PaperTrading moduli orqali bajariladi.
4. BacktestEngine hech qachon real Broker'ga murojaat qilmaydi.
5. Live Data ishlatilmaydi — faqat tarixiy ma'lumot.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Tarixiy candle oqimi olinadi.
✓ To'liq zanjir simulyatsiya qilinadi.
✓ Risk Manager chetlab o'tilmaydi.
✓ Natijalar Statistics'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
BacktestEngine Contract BacktestEngine tarixiy ma'lumot ustida to'liq GoldBot zanjirini simulyatsiya qiluvchi Canonical Orchestrator hisoblanadi.
