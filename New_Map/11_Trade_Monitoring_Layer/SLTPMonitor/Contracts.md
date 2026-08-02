# SLTP Monitor Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat SLTPMonitor modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
SLTPMonitor quyidagilar uchun javobgar.
✓ Stop Loss Monitoring
✓ Take Profit Monitoring
✓ Trigger Detection
✓ Price Validation
✓ Monitoring Report Generation
✓ Monitoring Metadata Generation
SLTPMonitor bajarmaydi.
✗ Trading Decision
✗ Risk Validation
✗ Order Execution
✗ Trailing Stop
✗ Partial Close
✗ Recovery Management
---
# Module Boundary
```text
TradeLifecycleManager
↓
SLTPMonitor
↓
BreakevenManager
```
---
# Input Contract
• Trade State
• Position Information
• Current Market Price
• Broker Position
• Monitoring Context
---
# Output Contract
• SLTP Status
• Trigger Events
• Monitoring Report
• Monitoring Metadata
• Trade Context
---
# Allowed Dependencies
✓ TradeLifecycleManager
✓ BreakevenManager
---
# Forbidden Dependencies
✗ TrailingStop
✗ PartialClose
✗ RecoveryManager
✗ Execution Layer
✗ Decision Layer
---
# Runtime Contract
1. Stop Loss har bir Price Update'da tekshirilishi shart.
2. Take Profit har bir Price Update'da tekshirilishi shart.
3. Trigger aniqlanganda Event yaratilishi shart.
4. Trigger faqat bir marta qayta ishlanishi shart.
5. Monitoring Report BreakevenManager'ga uzatilishi shart.
6. SLTPMonitor Position'ni o'zgartirmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Trade Context qabul qilinadi.
✓ Price Monitoring bajariladi.
✓ SL va TP tekshiriladi.
✓ Trigger Event yaratiladi.
✓ Monitoring Report yaratiladi.
✓ BreakevenManager'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
SLTPMonitor Contract GoldBot Trade Monitoring Layer ichidagi Stop Loss va Take Profit triggerlarini kuzatish, Trigger Event yaratish hamda Monitoring Report'ni BreakevenManager moduliga uzatishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
