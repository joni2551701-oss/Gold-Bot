# Position Monitor Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat PositionMonitor modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
PositionMonitor quyidagilar uchun javobgar.
✓ Open Position Monitoring
✓ Position Synchronization
✓ Position State Detection
✓ Position Event Generation
✓ Position Report Generation
✓ Monitoring Metadata Generation
PositionMonitor bajarmaydi.
✗ Trading Decision
✗ Risk Validation
✗ Order Execution
✗ Stop Loss Management
✗ Trailing Stop
✗ Partial Close
---
# Module Boundary
```text
MonitoringService
↓
PositionMonitor
↓
TradeLifecycleManager
```
---
# Input Contract
• Execution Result
• Broker Position
• Position Metadata
• Monitoring Context
---
# Output Contract
• Position Status
• Position Context
• Position Events
• Position Report
• Monitoring Metadata
---
# Allowed Dependencies
✓ MonitoringService
✓ TradeLifecycleManager
---
# Forbidden Dependencies
✗ SLTPMonitor
✗ BreakevenManager
✗ TrailingStop
✗ PartialClose
✗ RecoveryManager
---
# Runtime Contract
1. Broker Position doimo asosiy manba hisoblanadi.
2. Har bir Position sinxronlashtirilishi shart.
3. Position Status o'zgarsa Event yaratilishi shart.
4. Position Report standart formatda yaratilishi shart.
5. PositionMonitor Position'ni boshqarish qarorini qabul qilmaydi.
6. Position Report TradeLifecycleManager'ga uzatilishi shart.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Position qabul qilinadi.
✓ Broker bilan sinxronlanadi.
✓ Position holati kuzatiladi.
✓ Position Event yaratiladi.
✓ Position Report yaratiladi.
✓ TradeLifecycleManager'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
PositionMonitor Contract GoldBot Trade Monitoring Layer ichidagi barcha ochiq Position'larni kuzatish, Broker bilan sinxronlashtirish, Position Event va Position Report yaratish hamda TradeLifecycleManager moduliga uzatishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
