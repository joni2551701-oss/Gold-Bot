# Execution Service
Status: CANONICAL
---
# Purpose
ExecutionService GoldBot Execution Layer ichidagi Canonical Public Execution Interface moduli hisoblanadi.
Uning asosiy vazifasi Execution Layer uchun yagona Service Gateway bo'lish va barcha tashqi Layer'lar bilan standart Execution API orqali ishlashdir.
ExecutionService Order yubormaydi.
ExecutionService Trading Decision qabul qilmaydi.
ExecutionService faqat Execution Layer Service Gateway hisoblanadi.
---
# Objective
ExecutionService quyidagi vazifalarni bajaradi.
• Execution Request Management
• Execution API Gateway
• Request Validation
• Response Standardization
• Execution Session Management
• Execution Layer Integration
---
# Layer Position
```text
Risk Layer
↓
ExecutionService
↓
ExecutionEngine
↓
ExecutionMonitor
↓
Trade Monitoring Layer
```
---
# Responsibilities
ExecutionService
✓ Execution Request qabul qiladi
✓ Request formatini tekshiradi
✓ ExecutionEngine'ga uzatadi
✓ Execution natijasini qabul qiladi
✓ Standard Response yaratadi
✓ Trade Monitoring Layer'ga uzatadi
---
# Not Responsible
ExecutionService
✗ Trading Decision
✗ Risk Validation
✗ Order Validation
✗ Order Routing
✗ Broker Communication
✗ Position Monitoring
---
# Input
ExecutionService qabul qiladi.
• Risk Approval
• Position Package
• Execution Request
• Session Metadata
---
# Output
ExecutionService yaratadi.
• Execution Response
• Standard Response
• Execution Status
• Service Metadata
---
# Workflow
```text
Receive Request
↓
Validate Request
↓
ExecutionEngine
↓
ExecutionMonitor
↓
Receive Execution Result
↓
Standardize Response
↓
Trade Monitoring Layer
```
---
# Golden Rules
1. Execution Layer'ga barcha kirishlar ExecutionService orqali amalga oshiriladi.
2. ExecutionService Business Logic bajarmaydi.
3. Har bir Request Validation'dan o'tadi.
4. Response yagona formatda qaytariladi.
5. Circular Dependency qat'iyan taqiqlanadi.
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
ExecutionService GoldBot Execution Layer uchun yagona Public Interface va Service Gateway hisoblanadi.
