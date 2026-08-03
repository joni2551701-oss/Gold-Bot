# Monitoring Service
Status: CANONICAL
---
# Purpose
MonitoringService GoldBot Trade Monitoring Layer uchun Canonical Boundary Gateway hisoblanadi.
Uning asosiy vazifasi Trade Monitoring Layer'ning yagona Public Entry Point va Public Exit Point bo'lishidir — Execution Layer'dan kelgan so'rovlarni PositionMonitor'ga kiritish va RecoveryManager'dan qaytgan yakuniy Monitoring Result'ni Database Layer'ga chiqarish.
MonitoringService Position Monitoring bajarmaydi.
MonitoringService Trade Management bajarmaydi.
MonitoringService faqat Entry/Exit Boundary, Validation va Serialization vazifalarini bajaradi.
---
# Objective
MonitoringService quyidagi vazifalarni bajaradi.
• Public Entry Point
• Public Exit Point
• Request Validation
• Response Serialization
• Session Management
• API Boundary Enforcement
---
# Layer Position
```text
Execution Layer
↓
MonitoringService (Entry)
↓
PositionMonitor
↓
TradeLifecycleManager
↓
SLTPMonitor
↓
BreakevenManager
↓
TrailingStop
↓
PartialClose
↓
RecoveryManager
↓
MonitoringService (Exit)
↓
Database Layer
```
---
# Responsibilities
MonitoringService
✓ Execution Layer'dan Monitoring Request qabul qiladi (Entry)
✓ Request formatini tekshiradi
✓ PositionMonitor'ga uzatadi
✓ RecoveryManager'dan Monitoring Result qabul qiladi
✓ Standard Response yaratadi
✓ Database Layer'ga uzatadi (Exit)
---
# Not Responsible
MonitoringService
✗ Trading Decision
✗ Risk Validation
✗ Order Execution
✗ Position Monitoring
✗ SL/TP Management
✗ Breakeven Management
✗ Trailing Stop Management
✗ Partial Close Management
✗ Recovery Management
---
# Input
MonitoringService qabul qiladi.
• Execution Result (Execution Layer'dan)
• Monitoring Result (RecoveryManager'dan)
• Session Metadata
---
# Output
MonitoringService yaratadi.
• Validated Monitoring Request (PositionMonitor'ga)
• Monitoring Response (Database Layer'ga)
• Position Status
• Service Metadata
---
# Workflow
```text
Receive Request (Execution Layer)
↓
Validate Request
↓
Forward To PositionMonitor
↓
Receive Monitoring Result (RecoveryManager)
↓
Standardize Response
↓
Return Response (Database Layer)
```
---
# Golden Rules
1. MonitoringService Trade Monitoring Layer'ning yagona Entry Point va yagona Exit Point hisoblanadi.
2. Business Logic MonitoringService ichida bajarilmaydi.
3. Response yagona formatga o'tkaziladi.
4. Trade Monitoring Layer tashqarisiga faqat MonitoringService orqali kiriladi va chiqiladi.
5. RecoveryManager Layer tashqarisiga chiqmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
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
MonitoringService GoldBot Trade Monitoring Layer uchun ikki tomonlama (bidirectional) Boundary Gateway hisoblanadi — Execution Layer'dan Trade Monitoring Layer'ga kirish va Trade Monitoring Layer'dan Database Layer'ga chiqish uchun yagona nuqta.
