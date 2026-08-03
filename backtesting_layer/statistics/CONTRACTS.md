# Statistics Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat Statistics modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
Statistics quyidagilar uchun javobgar.
✓ Har bir simulyatsiya natijasi uchun samaradorlikni hisoblaydi
✓ Natijalarni Strategy bo'yicha guruhlaydi
✓ Win Rate, Profit Factor, Drawdown va Equity Curve hisoblaydi
✓ Hisoblangan ko'rsatkichlarni BacktestReport'ga uzatadi
Statistics bajarmaydi.
✗ Trade Simulation (BacktestEngine vazifasi)
✗ Report Formatting (BacktestReport vazifasi)
✗ Signal Generation
✗ Trading Decision
✗ Risk Calculation
---
# Module Boundary
```text
BacktestEngine
↓
Statistics
↓
BacktestReport
```
---
# Input Contract
• Simulated Trade Results
• Signal Performance Records
---
# Output Contract
• Performance Metrics
• Strategy Report
• Equity Curve
• Statistics Metadata
---
# Allowed Dependencies
✓ BacktestEngine
✓ BacktestReport
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
1. Statistics faqat allaqachon yakunlangan simulyatsiya natijalari ustida ishlaydi.
2. Hech qanday ko'rsatkich to'qib chiqarilmaydi — ma'lumot yetishmasa None qaytariladi.
3. Statistics savdo qarorini baholamaydi.
4. Statistics real Trade natijalarini o'zgartirmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Simulyatsiya natijalari qabul qilinadi.
✓ Ko'rsatkichlar hisoblanadi.
✓ Strategy bo'yicha guruhlanadi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Statistics Contract Statistics simulyatsiya natijalaridan samaradorlik ko'rsatkichlarini hisoblovchi Canonical modul hisoblanadi.
