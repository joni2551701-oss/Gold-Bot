# Decision Logger
Status: CANONICAL
---
# Purpose
DecisionLogger GoldBot Decision Layer ichidagi Canonical Decision Audit moduli hisoblanadi.
Uning asosiy vazifasi Decision Layer ichida yaratilgan barcha qarorlarni, ularning sabablarini va ishlatilgan ma'lumotlarni Audit uchun yozib borishdir.
DecisionLogger qaror qabul qilmaydi.
DecisionLogger Decision'ni o'zgartirmaydi.
DecisionLogger faqat Audit va Logging bilan shug'ullanadi.
---
# Objective
DecisionLogger quyidagi vazifalarni bajaradi.
• Decision Logging
• Audit Trail
• Decision History
• Decision Trace
• Performance Logging
• Diagnostic Logging
---
# Layer Position
```text
DecisionEngine
↓
DecisionLogger
↓
DecisionService
↓
Database Layer
```
---
# Responsibilities
DecisionLogger
✓ Decision yozadi
✓ Approval Status yozadi
✓ Confidence yozadi
✓ Rule natijalarini yozadi
✓ Timestamp yaratadi
✓ Audit Trail yaratadi
---
# Not Responsible
DecisionLogger
✗ Decision Making
✗ Rule Validation
✗ AI Analysis
✗ Risk Calculation
✗ Trade Execution
✗ Database Management
---
# Input
DecisionLogger qabul qiladi.
• Final Decision
• Decision Context
• Decision Confidence
• Approval Result
• Rule Report
---
# Output
DecisionLogger yaratadi.
• Decision Log
• Audit Record
• Decision Trace
• Log Metadata
---
# Workflow
```text
Receive Decision
↓
Build Audit Record
↓
Generate Metadata
↓
Write Log
↓
DecisionService
↓
Database Layer
```
---
# Golden Rules
1. Har bir Decision log qilinishi shart.
2. Log o'zgartirilmaydi.
3. Timestamp majburiy.
4. Audit Trail uzluksiz bo'lishi kerak.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
DecisionLogger/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
DecisionLogger GoldBot ichidagi barcha Trading Decision'larni Audit va History uchun saqlovchi Canonical Logging moduli hisoblanadi.
