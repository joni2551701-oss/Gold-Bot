# Position Sizing
Status: CANONICAL
---
# Purpose
PositionSizing GoldBot Risk Layer ichidagi Canonical Position Size Calculation moduli hisoblanadi.
Uning asosiy vazifasi foydalanuvchi Risk Policy va Account holatiga asoslanib optimal Position Size va Lot Size hisoblashdir.
PositionSizing Trade Approval bermaydi.
PositionSizing Risk Validation bajarmaydi.
PositionSizing faqat Position Size Calculation bilan shug'ullanadi.
---
# Objective
PositionSizing quyidagi vazifalarni bajaradi.
• Position Size Calculation
• Lot Size Calculation
• Risk Amount Calculation
• Volume Validation
• Symbol Constraints Validation
• Position Package Generation
---
# Layer Position
```text
RiskEngine
↓
PositionSizing
↓
MoneyManagement
```
---
# Responsibilities
PositionSizing
✓ Position Size hisoblaydi
✓ Lot Size hisoblaydi
✓ Risk Amount hisoblaydi
✓ Symbol Limit tekshiradi
✓ Broker Volume Step tekshiradi
✓ Position Package yaratadi
---
# Not Responsible
PositionSizing
✗ Final Decision
✗ Money Management
✗ Drawdown Control
✗ Exposure Control
✗ Trade Execution
✗ Portfolio Management
---
# Input
PositionSizing qabul qiladi.
• Risk Package
• Account Balance
• Risk %
• Entry Price
• Stop Loss
• Symbol Specification
---
# Output
PositionSizing yaratadi.
• Position Size
• Lot Size
• Risk Amount
• Position Package
• Position Metadata
---
# Workflow
```text
Receive Risk Package
↓
Calculate Risk Amount
↓
Calculate Position Size
↓
Calculate Lot Size
↓
Validate Broker Limits
↓
Generate Position Package
↓
MoneyManagement
```
---
# Golden Rules
1. Stop Loss mavjud bo'lishi shart.
2. Risk % foydalanuvchi Risk Policy'dan olinadi.
3. Broker Min/Max Volume hisobga olinadi.
4. Volume Step buzilmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
PositionSizing/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
PositionSizing GoldBot Risk Layer ichidagi Position Size va Lot Size hisoblovchi Canonical modul hisoblanadi.
