# Order Manager
Status: CANONICAL
---
# Purpose
OrderManager GoldBot Execution Layer ichidagi Canonical Order Lifecycle Management moduli hisoblanadi.
Uning asosiy vazifasi Order'ning butun hayotiy siklini (Lifecycle) boshqarishdir.
OrderManager yangi Order yaratadi, Order holatini yangilaydi, kerak bo'lsa Order'ni bekor qiladi yoki o'zgartiradi.
OrderManager Broker bilan bevosita ishlamaydi.
OrderManager Trading Decision qabul qilmaydi.
---
# Objective
OrderManager quyidagi vazifalarni bajaradi.
• Order Creation
• Order Update
• Order Modification
• Order Cancellation
• Order Lifecycle Management
• Order State Management
---
# Layer Position
```text
OrderValidator
↓
OrderManager
↓
OrderRouter
```
---
# Responsibilities
OrderManager
✓ Order yaratadi
✓ Order ID yaratadi
✓ Order Status boshqaradi
✓ Modify Request yaratadi
✓ Cancel Request yaratadi
✓ Order Lifecycle boshqaradi
---
# Not Responsible
OrderManager
✗ Trading Decision
✗ Risk Validation
✗ Broker Communication
✗ Order Routing
✗ Execution Monitoring
✗ Position Monitoring
---
# Input
OrderManager qabul qiladi.
• Validated Order
• Execution Context
• Position Package
• Order Metadata
---
# Output
OrderManager yaratadi.
• Managed Order
• Order Context
• Order Lifecycle
• Order Metadata
---
# Order States
NEW
↓
VALIDATED
↓
READY
↓
SENT
↓
FILLED
↓
PARTIAL_FILLED
↓
MODIFIED
↓
CANCELLED
↓
REJECTED
---
# Workflow
```text
Receive Validated Order
↓
Create Order
↓
Assign Order ID
↓
Manage Lifecycle
↓
Generate Managed Order
↓
OrderRouter
```
---
# Golden Rules
1. Har bir Order yagona Order ID olishi shart.
2. Order Status faqat OrderManager tomonidan boshqariladi.
3. Lifecycle ketma-ket yuritiladi.
4. Broker bilan to'g'ridan-to'g'ri aloqa qilmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
OrderManager/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
OrderManager GoldBot Execution Layer ichidagi Order Lifecycle boshqaruvchi Canonical modul hisoblanadi.
