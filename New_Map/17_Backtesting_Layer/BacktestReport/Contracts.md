# Backtest Report Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat BacktestReport modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
BacktestReport quyidagilar uchun javobgar.
✓ Hisoblangan statistikani yagona Report obyektiga yig'adi
✓ Report'ni o'qish uchun formatlaydi
✓ Report'ni o'zgarmas (immutable) holatda saqlaydi
BacktestReport bajarmaydi.
✗ Statistics Calculation (Statistics vazifasi)
✗ Trade Simulation
✗ Signal Generation
✗ Report Delivery (BacktestService vazifasi)
---
# Module Boundary
```text
Statistics
↓
BacktestReport
↓
BacktestService (Exit)
```
---
# Input Contract
• Performance Metrics
• Strategy Report
• Backtest Run Metadata
---
# Output Contract
• Backtest Report
• Formatted Report Text
• Report Metadata
---
# Allowed Dependencies
✓ Statistics
✓ BacktestService
---
# Forbidden Dependencies
✗ Execution Layer (real order — Backtesting Isolation Rule)
✗ Broker Gateway
✗ Platform Layer (to'g'ridan-to'g'ri)
✗ Live Data (real vaqt oqimi)
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
---
# Runtime Contract
1. BacktestReport hech qanday ko'rsatkichni o'zi hisoblamaydi.
2. Report yaratilgandan keyin o'zgarmas (immutable) hisoblanadi.
3. Report faqat BacktestService orqali tashqariga chiqadi.
4. Report real Trade natijasi bilan aralashtirilmaydi — u simulyatsiya natijasi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Statistika qabul qilinadi.
✓ Report yig'iladi.
✓ Report formatlanadi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
BacktestReport Contract BacktestReport yakuniy Backtest natijasini yig'uvchi va formatlovchi Canonical modul hisoblanadi.
