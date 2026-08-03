# Execution Service
Status: CANONICAL
---
# Purpose
ExecutionService GoldBot Execution Layer uchun Canonical Boundary Gateway hisoblanadi.
Uning asosiy vazifasi Execution Layer'ning yagona Public Entry Point va Public Exit Point bo'lishidir — Risk Layer'dan kelgan so'rovlarni ExecutionEngine'ga kiritish va ExecutionMonitor'dan qaytgan yakuniy Execution Result'ni Trade Monitoring Layer'ga chiqarish.
ExecutionService Order yubormaydi.
ExecutionService Trading Decision qabul qilmaydi.
ExecutionService faqat Entry/Exit Boundary, Validation va Serialization vazifalarini bajaradi.
---
# Objective
ExecutionService quyidagi vazifalarni bajaradi.
• Public Entry Point
• Public Exit Point
• Request Validation
• Response Serialization
• Session Management
• API Boundary Enforcement
---
# Layer Position
```text
Risk Layer
↓
ExecutionService (Entry)
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
ExecutionService (Exit)
↓
Trade Monitoring Layer
```
---
# Responsibilities
ExecutionService
✓ Risk Layer'dan Execution Request qabul qiladi (Entry)
✓ Request formatini tekshiradi
✓ ExecutionEngine'ga uzatadi
✓ ExecutionMonitor'dan Execution Result qabul qiladi
✓ Standard Response yaratadi
✓ Trade Monitoring Layer'ga uzatadi (Exit)
---
# Not Responsible
ExecutionService
✗ Trading Decision
✗ Risk Validation
✗ Order Validation
✗ Order Management
✗ Order Routing
✗ Broker Communication
✗ Execution Monitoring
---
# Input
ExecutionService qabul qiladi.
• Risk Approval (Risk Layer'dan)
• Execution Result (ExecutionMonitor'dan)
• Session Metadata
---
# Output
ExecutionService yaratadi.
• Validated Execution Request (ExecutionEngine'ga)
• Execution Response (Trade Monitoring Layer'ga)
• Standard Response
• Service Metadata
---
# Workflow
```text
Receive Request (Risk Layer)
↓
Validate Request
↓
Forward To ExecutionEngine
↓
Receive Execution Result (ExecutionMonitor)
↓
Standardize Response
↓
Return Response (Trade Monitoring Layer)
```
---
# Golden Rules
1. ExecutionService Execution Layer'ning yagona Entry Point va yagona Exit Point hisoblanadi.
2. Business Logic ExecutionService ichida bajarilmaydi.
3. Response yagona formatga o'tkaziladi.
4. Execution Layer tashqarisiga faqat ExecutionService orqali kiriladi va chiqiladi.
5. ExecutionMonitor Layer tashqarisiga chiqmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
ExecutionService/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
ExecutionService GoldBot Execution Layer uchun ikki tomonlama (bidirectional) Boundary Gateway hisoblanadi — Risk Layer'dan Execution Layer'ga kirish va Execution Layer'dan Trade Monitoring Layer'ga chiqish uchun yagona nuqta.
