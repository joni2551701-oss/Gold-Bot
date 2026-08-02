# Recovery Manager Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat RecoveryManager modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
RecoveryManager quyidagilar uchun javobgar.
✓ Restart Recovery
✓ Open Position Recovery
✓ Trade State Restoration
✓ Monitoring Session Recovery
✓ Recovery Validation
✓ Recovery Report Generation
RecoveryManager bajarmaydi.
✗ Trading Decision
✗ Risk Validation
✗ Order Execution
✗ Stop Loss Management
✗ Trailing Stop
✗ Partial Close
---
# Module Boundary
```text
PartialClose
↓
RecoveryManager
↓
Database Layer
```
---
# Input Contract
• Trade Context
• Broker Open Positions
• Monitoring Metadata
• Recovery Configuration
---
# Output Contract
• Recovered Position
• Recovery Status
• Recovery Report
• Recovery Metadata
• Recovery Events
---
# Allowed Dependencies
✓ PartialClose
✓ Database Layer
---
# Forbidden Dependencies
✗ PositionMonitor
✗ TradeLifecycleManager
✗ Execution Layer
✗ Risk Layer
✗ Decision Layer
---
# Runtime Contract
1. Restart aniqlanishi shart.
2. Broker Open Positions to'liq yuklanishi shart.
3. Har bir Position uchun Recovery bajarilishi shart.
4. Recovery Validation muvaffaqiyatli yakunlanishi shart.
5. Recovery Report Database Layer'ga uzatilishi shart.
6. Recovery tugamaguncha Monitoring davom ettirilmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Restart aniqlanadi.
✓ Open Position'lar yuklanadi.
✓ Trade State tiklanadi.
✓ Recovery Validation bajariladi.
✓ Recovery Report yaratiladi.
✓ Database Layer'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
RecoveryManager Contract GoldBot Trade Monitoring Layer ichidagi Restart Recovery, Open Position Recovery va Trade State Restoration jarayonlarini boshqarish, Recovery Report'ni Database Layer'ga uzatish hamda Monitoring uzluksizligini ta'minlashni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
