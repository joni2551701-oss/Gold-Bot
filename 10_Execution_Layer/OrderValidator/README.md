# Order Validator
Status: CANONICAL
---
# Purpose
OrderValidator GoldBot Execution Layer ichidagi Canonical Order Validation moduli hisoblanadi.
Uning asosiy vazifasi Order Broker yoki Exchange'ga yuborilishidan oldin barcha parametrlarni tekshirish va Order'ning Execution uchun tayyor ekanligini tasdiqlashdir.
OrderValidator Order yaratmaydi.
OrderValidator Trading Decision qabul qilmaydi.
OrderValidator faqat Order Validation bilan shug'ullanadi.
---
# Objective
OrderValidator quyidagi vazifalarni bajaradi.
• Order Validation
• Price Validation
• Volume Validation
• SL/TP Validation
• Symbol Validation
• Validation Report Generation
---
# Layer Position
```text
ExecutionEngine
↓
OrderValidator
↓
OrderManager
```
---
# Responsibilities
OrderValidator
✓ Order formatini tekshiradi
✓ Symbol parametrlarini tekshiradi
✓ Entry Price tekshiradi
✓ Stop Loss tekshiradi
✓ Take Profit tekshiradi
✓ Lot Size tekshiradi
✓ Validation Report yaratadi
---
# Not Responsible
OrderValidator
✗ Trading Decision
✗ Risk Validation
✗ Order Creation
✗ Broker Communication
✗ Order Routing
✗ Position Monitoring
---
# Input
OrderValidator qabul qiladi.
• Order Request
• Position Package
• Symbol Specification
• Execution Context
---
# Output
OrderValidator yaratadi.
• Validated Order
• Validation Report
• Validation Status
• Validation Metadata
---
# Validation States
VALID
↓
WARNING
↓
INVALID
↓
REJECTED
---
# Workflow
```text
Receive Order
↓
Validate Order Structure
↓
Validate Price
↓
Validate Volume
↓
Validate SL/TP
↓
Generate Validation Report
↓
OrderManager
```
---
# Golden Rules
1. Har bir Order Validation'dan o'tishi shart.
2. Invalid Order Broker'ga yuborilmaydi.
3. Validation natijasi o'zgartirilmaydi.
4. Validation standart formatda yaratiladi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
OrderValidator/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
OrderValidator GoldBot Execution Layer ichidagi barcha Order parametrlarini tekshiruvchi Canonical Validation moduli hisoblanadi.
