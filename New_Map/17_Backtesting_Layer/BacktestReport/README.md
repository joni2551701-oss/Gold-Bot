# Backtest Report
Status: CANONICAL
---
# Purpose
BacktestReport GoldBot Backtesting Layer ichidagi Canonical Report moduli hisoblanadi.
Uning asosiy vazifasi hisoblangan statistikani yagona o'zgarmas (immutable) Backtest Report obyektiga yig'ish va uni o'qish uchun formatlashdir.
BacktestReport hech qanday ko'rsatkichni o'zi hisoblamaydi.
---
# Objective
BacktestReport quyidagi vazifalarni bajaradi.
• Report Assembly
• Report Formatting
• Immutable Result Object
• Report Metadata
---
# Layer Position
```text
Statistics
↓
BacktestReport
↓
BacktestService (Exit)
```
---
# Responsibilities
BacktestReport
✓ Hisoblangan statistikani yagona Report obyektiga yig'adi
✓ Report'ni o'qish uchun formatlaydi
✓ Report'ni o'zgarmas (immutable) holatda saqlaydi
---
# Not Responsible
BacktestReport
✗ Statistics Calculation (Statistics vazifasi)
✗ Trade Simulation
✗ Signal Generation
✗ Report Delivery (BacktestService vazifasi)
---
# Input
BacktestReport qabul qiladi.
• Performance Metrics
• Strategy Report
• Backtest Run Metadata
---
# Output
BacktestReport yaratadi.
• Backtest Report
• Formatted Report Text
• Report Metadata
---
# Workflow
```text
Statistics
↓
BacktestReport
↓
BacktestService (Exit)
```
---
# Internal Modules (Planned — implementatsiya bosqichida to'ldiriladi)
```text
BacktestReport
├── ReportBuilder
├── ReportFormatter
└── ReportModel
```
---
# Golden Rules
1. BacktestReport hech qanday ko'rsatkichni o'zi hisoblamaydi.
2. Report yaratilgandan keyin o'zgarmas (immutable) hisoblanadi.
3. Report faqat BacktestService orqali tashqariga chiqadi.
4. Report real Trade natijasi bilan aralashtirilmaydi — u simulyatsiya natijasi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
BacktestReport/
├── README.md
├── Contracts.md
├── ModuleMap.md
└── SequenceDiagram.md
```
---
# Summary
BacktestReport yakuniy Backtest natijasini yig'uvchi va formatlovchi Canonical modul hisoblanadi.
