# Monitoring Service Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat MonitoringService modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
MonitoringService quyidagilar uchun javobgar.
✓ Public Entry Point (Execution Layer'dan Trade Monitoring Layer'ga kirish)
✓ Public Exit Point (Trade Monitoring Layer'dan Database Layer'ga chiqish)
✓ Request Validation
✓ Response Serialization
✓ Session Management
✓ API Boundary Enforcement
MonitoringService bajarmaydi.
✗ Trading Decision
✗ Risk Validation
✗ Order Execution
✗ Position Monitoring
✗ SL/TP Management
✗ Breakeven Management
✗ Trailing Stop Management
✗ Partial Close Management
✗ Recovery Management
✗ Database Management
---
# Module Boundary
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
# Input Contract
Kirish tomonida (Execution Layer'dan):
• Execution Result
• Monitoring Request
• Session Metadata

Chiqish tomonida (RecoveryManager'dan):
• Monitoring Result
---
# Output Contract
Kirish tomonida (PositionMonitor'ga):
• Validated Monitoring Request

Chiqish tomonida (Database Layer'ga):
• Monitoring Response
• Position Status
• Monitoring Report
• Service Metadata
---
# Allowed Dependencies
✓ PositionMonitor
✓ RecoveryManager
---
# Forbidden Dependencies
✗ TradeLifecycleManager (to'g'ridan-to'g'ri)
✗ SLTPMonitor (to'g'ridan-to'g'ri)
✗ BreakevenManager (to'g'ridan-to'g'ri)
✗ TrailingStop (to'g'ridan-to'g'ri)
✗ PartialClose (to'g'ridan-to'g'ri)
✗ ExecutionEngine
✗ BrokerGateway
✗ Decision Layer
✗ Risk Layer
---
# Runtime Contract
1. Trade Monitoring Layer'ga barcha kirish va chiqishlar MonitoringService orqali amalga oshirilishi shart (Boundary Gateway).
2. Har bir kirish Request Validation'dan o'tishi shart.
3. MonitoringService Business Logic bajarmaydi — faqat Entry/Exit Boundary vazifasini bajaradi.
4. Response standart formatda qaytarilishi shart.
5. RecoveryManager Layer tashqarisiga chiqmaydi — faqat MonitoringService orqali chiqadi.
6. Session holati boshqarilishi shart.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Execution Layer'dan Request qabul qilinadi.
✓ Validation bajariladi.
✓ PositionMonitor'ga uzatiladi.
✓ RecoveryManager'dan Monitoring Result qabul qilinadi.
✓ Response standartlashtiriladi.
✓ Database Layer'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
MonitoringService Contract GoldBot Trade Monitoring Layer uchun ikki tomonlama (bidirectional) Boundary Gateway sifatida ishlashini — Execution Layer'dan kirish va Database Layer'ga chiqishni — belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
