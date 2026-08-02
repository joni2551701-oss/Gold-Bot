# Trade Lifecycle Manager Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat TradeLifecycleManager modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
TradeLifecycleManager quyidagilar uchun javobgar.
✓ Trade State Management
✓ Lifecycle Management
✓ State Transition Validation
✓ Trade Event Processing
✓ Lifecycle Report Generation
✓ Lifecycle Metadata Generation
TradeLifecycleManager bajarmaydi.
✗ Trading Decision
✗ Risk Validation
✗ Order Execution
✗ Stop Loss Management
✗ Trailing Stop
✗ Partial Close
---
# Module Boundary
```text
PositionMonitor
↓
TradeLifecycleManager
↓
SLTPMonitor
```
---
# Input Contract
• Position Report
• Position Status
• Position Events
• Monitoring Context
---
# Output Contract
• Trade State
• Trade Context
• Lifecycle Report
• Lifecycle Metadata
• Trade Events
---
# Allowed Dependencies
✓ PositionMonitor
✓ SLTPMonitor
---
# Forbidden Dependencies
✗ BreakevenManager
✗ TrailingStop
✗ PartialClose
✗ RecoveryManager
✗ Execution Layer
---
# Runtime Contract
1. Har bir Trade State tekshirilishi shart.
2. Noto'g'ri State Transition rad etilishi shart.
3. Har bir Transition log qilinishi shart.
4. CLOSED holati yakuniy holat hisoblanadi.
5. Lifecycle Report SLTPMonitor'ga uzatilishi shart.
6. Trade State faqat TradeLifecycleManager tomonidan o'zgartiriladi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Position Report qabul qilinadi.
✓ Trade State tekshiriladi.
✓ State Transition bajariladi.
✓ Lifecycle Report yaratiladi.
✓ Trade Context yaratiladi.
✓ SLTPMonitor'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
TradeLifecycleManager Contract GoldBot Trade Monitoring Layer ichidagi Trade Lifecycle va State Machine'ni boshqarish, barcha State Transition'larni nazorat qilish hamda Lifecycle Report'ni SLTPMonitor moduliga uzatishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
