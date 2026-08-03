# Partial Close
Status: CANONICAL
---
# Purpose
PartialClose GoldBot Trade Monitoring Layer ichidagi Canonical Partial Position Management moduli hisoblanadi.
Uning asosiy vazifasi Trade ochilish vaqtida Risk Layer tomonidan yaratilgan Risk Policy (Partial Close Rules) doirasida ochiq Position'ning ma'lum qismini yopish va qolgan qismini monitoring qilishdir.
PartialClose yangi Trade ochmaydi.
PartialClose Trading Decision qabul qilmaydi.
PartialClose faqat Partial Position Close boshqaruvi bilan shug'ullanadi.
---
# Objective
PartialClose quyidagi vazifalarni bajaradi.
• Partial Close Rule Evaluation
• Position Size Reduction
• Partial Close Execution Request
• Partial Close Validation
• Partial Close Report Generation
• Partial Close State Management
---
# Layer Position
```text
TrailingStop
↓
PartialClose
↓
RecoveryManager
```
---
# Responsibilities
PartialClose
✓ Partial Close Trigger tekshiradi
✓ Close Volume hisoblaydi
✓ Position Size yangilaydi
✓ Partial Close Event yaratadi
✓ Partial Close Status boshqaradi
✓ Partial Close Report yaratadi
---
# Not Responsible
PartialClose
✗ Trading Decision
✗ Risk Validation
✗ Order Execution
✗ Break Even
✗ Trailing Stop
✗ Recovery
---
# Input
PartialClose qabul qiladi.
• Trade Context
• Position Information
• Current Position Size
• Partial Close Rules
• Monitoring Context
---
# Output
PartialClose yaratadi.
• Updated Position
• Remaining Position
• Partial Close Status
• Partial Close Report
• Monitoring Metadata
---
# Partial Close States
NOT_READY
↓
READY
↓
EXECUTING
↓
COMPLETED
---
# Workflow
```text
Receive Trade Context
↓
Check Partial Close Rules
↓
Calculate Close Volume
↓
Update Position
↓
Generate Partial Close Report
↓
RecoveryManager
```
---
# Golden Rules
1. Partial Close faqat Strategy qoidalariga mos bo'lsa bajariladi.
2. Position Volume hech qachon manfiy bo'lmaydi.
3. Har bir Partial Close log qilinishi shart.
4. Remaining Position monitoringda qoladi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
PartialClose/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
PartialClose GoldBot Trade Monitoring Layer ichidagi Position'ni qisman yopishni boshqaruvchi Canonical Monitoring moduli hisoblanadi.
