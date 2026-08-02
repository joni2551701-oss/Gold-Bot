# Breakeven Manager
Status: CANONICAL
---
# Purpose
BreakevenManager GoldBot Trade Monitoring Layer ichidagi Canonical Break Even Management moduli hisoblanadi.
Uning asosiy vazifasi Trade belgilangan foyda darajasiga yetganda Stop Loss'ni Entry Price (Break Even) yoki belgilangan BE Offset qiymatiga ko'chirishdir.
BreakevenManager yangi Trade ochmaydi.
BreakevenManager Trading Decision qabul qilmaydi.
BreakevenManager faqat Break Even qoidalarini boshqaradi.
---
# Objective
BreakevenManager quyidagi vazifalarni bajaradi.
• Break Even Trigger Detection
• Stop Loss Relocation
• Break Even Validation
• Break Even Event Generation
• Break Even Report Generation
• Break Even State Management
---
# Layer Position
```text
SLTPMonitor
↓
BreakevenManager
↓
TrailingStop
```
---
# Responsibilities
BreakevenManager
✓ Break Even Trigger tekshiradi
✓ Stop Loss'ni Entry Price'ga ko'chiradi
✓ BE Offset qo'llaydi
✓ Break Even Event yaratadi
✓ Break Even Status boshqaradi
✓ Break Even Report yaratadi
---
# Not Responsible
BreakevenManager
✗ Trading Decision
✗ Risk Validation
✗ Order Execution
✗ Trailing Stop
✗ Partial Close
✗ Recovery Management
---
# Input
BreakevenManager qabul qiladi.
• Trade Context
• Position Information
• Current Market Price
• Break Even Rules
• Monitoring Context
---
# Output
BreakevenManager yaratadi.
• Break Even Status
• Updated Stop Loss
• Break Even Report
• Monitoring Metadata
• Break Even Events
---
# Break Even States
NOT_READY
↓
READY
↓
ACTIVATED
↓
COMPLETED
---
# Workflow
```text
Receive Trade Context
↓
Check Break Even Rules
↓
Validate Trigger
↓
Move Stop Loss
↓
Generate Break Even Report
↓
TrailingStop
```
---
# Golden Rules
1. Break Even faqat bir marta qo'llaniladi.
2. Trigger Strategy qoidalariga mos bo'lishi shart.
3. Stop Loss faqat foyda tomonga ko'chiriladi.
4. Break Even Event log qilinishi shart.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
BreakevenManager/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
BreakevenManager GoldBot Trade Monitoring Layer ichidagi Break Even qoidalarini boshqaruvchi Canonical Monitoring moduli hisoblanadi.
