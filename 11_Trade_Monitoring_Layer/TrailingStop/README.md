# Trailing Stop
Status: CANONICAL
---
# Purpose
TrailingStop GoldBot Trade Monitoring Layer ichidagi Canonical Dynamic Stop Loss Management moduli hisoblanadi.
Uning asosiy vazifasi foydaga chiqqan Trade uchun Stop Loss qiymatini bozor narxi harakatiga mos ravishda dinamik ravishda yangilab borishdir.
TrailingStop yangi Trade ochmaydi.
TrailingStop Trading Decision qabul qilmaydi.
TrailingStop faqat Dynamic Stop Loss Management bilan shug'ullanadi.
---
# Objective
TrailingStop quyidagi vazifalarni bajaradi.
• Trailing Rule Evaluation
• Dynamic Stop Loss Update
• Price Tracking
• Trailing Trigger Detection
• Trailing State Management
• Trailing Report Generation
---
# Layer Position
```text
BreakevenManager
↓
TrailingStop
↓
PartialClose
```
---
# Responsibilities
TrailingStop
✓ Market Price kuzatadi
✓ Trailing Rule tekshiradi
✓ Stop Loss yangilaydi
✓ Trailing Event yaratadi
✓ Trailing State boshqaradi
✓ Trailing Report yaratadi
---
# Not Responsible
TrailingStop
✗ Trading Decision
✗ Risk Validation
✗ Order Execution
✗ Break Even
✗ Partial Close
✗ Recovery Management
---
# Input
TrailingStop qabul qiladi.
• Trade Context
• Position Information
• Current Market Price
• Trailing Rules
• Monitoring Context
---
# Output
TrailingStop yaratadi.
• Updated Stop Loss
• Trailing Status
• Trailing Report
• Monitoring Metadata
• Trailing Events
---
# Trailing States
NOT_ACTIVE
↓
ACTIVE
↓
UPDATING
↓
COMPLETED
---
# Workflow
```text
Receive Trade Context
↓
Check Trailing Rules
↓
Track Market Price
↓
Update Stop Loss
↓
Generate Trailing Report
↓
PartialClose
```
---
# Golden Rules
1. Stop Loss faqat foyda tomonga siljiydi.
2. Stop Loss hech qachon orqaga qaytmaydi.
3. Har bir Stop Loss yangilanishi log qilinadi.
4. Trailing faqat aktiv Trade uchun ishlaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
TrailingStop/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
TrailingStop GoldBot Trade Monitoring Layer ichidagi Dynamic Stop Loss Management uchun Canonical modul hisoblanadi.
