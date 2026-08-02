# Trade Monitoring Layer Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat Trade Monitoring Layer uchun rasmiy Architecture Contract hisoblanadi.
---
# Layer Responsibility
Trade Monitoring Layer quyidagilar uchun javobgar.
✓ Position Monitoring
✓ Trade Lifecycle Management
✓ Stop Loss Monitoring
✓ Take Profit Monitoring
✓ Break Even Management
✓ Trailing Stop Management
✓ Partial Close Management
✓ Recovery Management
✓ Monitoring Report Generation
---
# Layer Does NOT
✗ Signal Generation
✗ AI Analysis
✗ Trading Decision
✗ Risk Calculation
✗ Order Execution
✗ Portfolio Management
---
# Input Contract
Trade Monitoring Layer qabul qiladi.
• Execution Result
• Position Information
• Broker Position
• Current Market Price
• Monitoring Rules
• Recovery Configuration
---
# Output Contract
Trade Monitoring Layer yaratadi.
• Position Status
• Trade Status
• Monitoring Report
• Recovery Report
• Monitoring Events
• Monitoring Metadata
---
# Layer Pipeline
```text
MonitoringService
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
Database Layer
```
---
# Layer Rules
1. Monitoring faqat OPEN Position uchun boshlanadi.
2. PositionMonitor Broker holatini sinxronlashtirishi shart.
3. TradeLifecycleManager Trade State'ni boshqarishi shart.
4. SLTPMonitor Trigger'larni tekshirishi shart.
5. BreakevenManager Break Even qoidalarini qo'llashi shart.
6. TrailingStop Stop Loss'ni faqat foyda tomonga siljitishi shart.
7. PartialClose Position hajmini qoidalarga muvofiq kamaytirishi shart.
8. RecoveryManager Restart holatida Trade'larni tiklashi shart.
9. Monitoring natijalari Database Layer'ga uzatilishi shart.
10. MonitoringService barcha tashqi aloqalar uchun yagona Gateway hisoblanadi.
11. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Position qabul qilinadi.
✓ Monitoring boshlanadi.
✓ Trade Lifecycle boshqariladi.
✓ SL/TP kuzatiladi.
✓ Break Even ishlaydi.
✓ Trailing Stop ishlaydi.
✓ Partial Close bajariladi.
✓ Recovery bajariladi.
✓ Monitoring Report yaratiladi.
✓ Database Layer'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
Trade Monitoring Layer Contract GoldBot arxitekturasidagi Canonical Trade Lifecycle Management qatlami sifatida ishlashini, ochiq Position'larni real vaqt rejimida kuzatishni, Trade'ning butun hayot siklini boshqarishni hamda Monitoring natijalarini Database Layer'ga uzatishni belgilovchi rasmiy Architecture Contract hisoblanadi.
