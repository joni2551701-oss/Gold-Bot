# Execution Layer
Status: CANONICAL
---
# Purpose
Execution Layer GoldBot arxitekturasidagi Canonical Trade Execution qatlami hisoblanadi.
Uning asosiy vazifasi Risk Layer tomonidan APPROVED qilingan Trade'larni Broker yoki Exchange orqali bozorga yuborish, Order Lifecycle'ni boshqarish va Execution natijalarini qaytarishdir.
Execution Layer Risk hisoblamaydi.
Execution Layer Trading Decision qabul qilmaydi.
Execution Layer faqat Trade Execution bilan shug'ullanadi.
---
# Objective
Execution Layer quyidagi vazifalarni bajaradi.
• Order Validation
• Order Management
• Order Routing
• Broker Communication
• Execution Monitoring
• Execution Reporting
---
# Layer Position
```text
Decision Layer
↓
Risk Layer
↓
Execution Layer
↓
Trade Monitoring Layer
```
---
# Internal Modules
```text
Execution Layer
├── ExecutionEngine
├── OrderManager
├── OrderRouter
├── OrderValidator
├── ExecutionMonitor
├── BrokerGateway
└── ExecutionService
```
---
# Responsibilities
Execution Layer
✓ Order yaratadi
✓ Order tekshiradi
✓ Order Broker'ga yuboradi
✓ Execution Status oladi
✓ Partial Fill kuzatadi
✓ Order Reject holatini qayta ishlaydi
✓ Execution Report yaratadi
---
# Not Responsible
Execution Layer
✗ Signal Generation
✗ AI Analysis
✗ Trading Decision
✗ Risk Calculation
✗ Portfolio Management
✗ Position Management
---
# Input
Execution Layer qabul qiladi.
• Risk Approval
• Position Size
• Lot Size
• Entry Price
• Stop Loss
• Take Profit
• Order Metadata
---
# Output
Execution Layer yaratadi.
• Execution Result
• Order Status
• Execution Report
• Execution Metadata
---
# Execution States
```text
PENDING
↓
SENT
↓
ACCEPTED
↓
PARTIAL_FILL
↓
FILLED
↓
CANCELLED
↓
REJECTED
↓
FAILED
```
---
# Workflow
```text
Receive Risk Approval
↓
ExecutionService
↓
ExecutionEngine
↓
OrderValidator
↓
OrderManager
↓
OrderRouter
↓
BrokerGateway
↓
ExecutionMonitor
↓
Trade Monitoring Layer
```
---
# Golden Rules
1. Faqat APPROVED Risk qabul qilinadi.
2. Har bir Order Validation'dan o'tishi shart.
3. Broker javobi tekshirilishi shart.
4. Har bir Execution log qilinishi shart.
5. Execution Layer Trading Decision'ni o'zgartirmaydi.
6. Broker bilan barcha aloqa BrokerGateway orqali amalga oshiriladi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
10_Execution_Layer/
├── README.md
├── ExecutionEngine/
├── OrderManager/
├── OrderRouter/
├── OrderValidator/
├── ExecutionMonitor/
├── BrokerGateway/
├── ExecutionService/
├── Layer_DataFlow.md
├── Layer_SequenceDiagram.md
├── Layer_ModuleMap.md
└── Layer_Contracts.md
```
---
# Summary
Execution Layer GoldBot arxitekturasidagi Canonical Trade Execution Layer hisoblanadi.
Decision Layer savdoga ruxsat beradi.
Risk Layer kapitalni himoya qiladi.
Execution Layer esa tasdiqlangan Order'ni Broker yoki Exchange orqali bozorga yuboradi va uning butun Execution Lifecycle'ni boshqaradi.
