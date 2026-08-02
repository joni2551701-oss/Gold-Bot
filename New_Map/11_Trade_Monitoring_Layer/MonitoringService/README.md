# Monitoring Service
Status: CANONICAL
---
# Purpose
MonitoringService GoldBot Trade Monitoring Layer ichidagi Canonical Public Monitoring Interface moduli hisoblanadi.
Uning asosiy vazifasi Trade Monitoring Layer uchun yagona Service Gateway bo'lish va barcha tashqi Layer'lar bilan standart Monitoring API orqali ishlashdir.
MonitoringService Position Monitoring bajarmaydi.
MonitoringService Trade Management bajarmaydi.
MonitoringService faqat Monitoring Layer Service Gateway hisoblanadi.
---
# Objective
MonitoringService quyidagi vazifalarni bajaradi.
• Monitoring Request Management
• Monitoring API Gateway
• Request Validation
• Response Standardization
• Monitoring Session Management
• Monitoring Layer Integration
---
# Layer Position
```text
Execution Layer
↓
MonitoringService
↓
PositionMonitor
↓
RecoveryManager
↓
Database Layer
```
---
# Responsibilities
MonitoringService
✓ Monitoring Request qabul qiladi
✓ Request formatini tekshiradi
✓ PositionMonitor'ga uzatadi
✓ Monitoring natijasini qabul qiladi
✓ Standard Response yaratadi
✓ Database Layer'ga uzatadi
---
# Not Responsible
MonitoringService
✗ Trading Decision
✗ Risk Validation
✗ Order Execution
✗ Position Monitoring
✗ Trailing Stop
✗ Partial Close
---
# Input
MonitoringService qabul qiladi.
• Execution Result
• Monitoring Request
• Session Metadata
---
# Output
MonitoringService yaratadi.
• Monitoring Response
• Position Status
• Monitoring Report
• Service Metadata
---
# Workflow
```text
Receive Request
↓
Validate Request
↓
PositionMonitor
↓
Trade Monitoring Pipeline
↓
Receive Monitoring Result
↓
Standardize Response
↓
Database Layer
```
---
# Golden Rules
1. Trade Monitoring Layer'ga barcha kirishlar MonitoringService orqali amalga oshiriladi.
2. MonitoringService Business Logic bajarmaydi.
3. Har bir Request Validation'dan o'tadi.
4. Response yagona formatda qaytariladi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
MonitoringService/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
MonitoringService GoldBot Trade Monitoring Layer uchun yagona Public Interface va Service Gateway hisoblanadi.
