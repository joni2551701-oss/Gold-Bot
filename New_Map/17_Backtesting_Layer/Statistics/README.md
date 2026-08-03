# Statistics
Status: CANONICAL
---
# Purpose
Statistics GoldBot Backtesting Layer ichidagi Canonical Statistics moduli hisoblanadi.
Uning asosiy vazifasi simulyatsiya natijalaridan samaradorlik ko'rsatkichlarini hisoblashdir.
Statistics savdo qarorini baholamaydi — u faqat natijalarni o'lchaydi.
---
# Objective
Statistics quyidagi vazifalarni bajaradi.
• Signal Performance Calculation
• Strategy Grouping
• Win Rate / Profit Factor
• Drawdown Calculation
• Equity Curve
• Benchmark Comparison
---
# Layer Position
```text
BacktestEngine
↓
Statistics
↓
BacktestReport
```
---
# Responsibilities
Statistics
✓ Har bir simulyatsiya natijasi uchun samaradorlikni hisoblaydi
✓ Natijalarni Strategy bo'yicha guruhlaydi
✓ Win Rate, Profit Factor, Drawdown va Equity Curve hisoblaydi
✓ Hisoblangan ko'rsatkichlarni BacktestReport'ga uzatadi
---
# Not Responsible
Statistics
✗ Trade Simulation (BacktestEngine vazifasi)
✗ Report Formatting (BacktestReport vazifasi)
✗ Signal Generation
✗ Trading Decision
✗ Risk Calculation
---
# Input
Statistics qabul qiladi.
• Simulated Trade Results
• Signal Performance Records
---
# Output
Statistics yaratadi.
• Performance Metrics
• Strategy Report
• Equity Curve
• Statistics Metadata
---
# Workflow
```text
BacktestEngine
↓
Statistics
↓
BacktestReport
```
---
# Internal Modules (Planned — implementatsiya bosqichida to'ldiriladi)
```text
Statistics
├── PerformanceMetrics
├── StrategyReport
├── EquityCurve
└── Benchmark
```
---
# Golden Rules
1. Statistics faqat allaqachon yakunlangan simulyatsiya natijalari ustida ishlaydi.
2. Hech qanday ko'rsatkich to'qib chiqarilmaydi — ma'lumot yetishmasa None qaytariladi.
3. Statistics savdo qarorini baholamaydi.
4. Statistics real Trade natijalarini o'zgartirmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
Statistics/
├── README.md
├── Contracts.md
├── ModuleMap.md
└── SequenceDiagram.md
```
---
# Summary
Statistics simulyatsiya natijalaridan samaradorlik ko'rsatkichlarini hisoblovchi Canonical modul hisoblanadi.
