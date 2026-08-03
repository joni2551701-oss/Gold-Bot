# Trailing Stop Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat TrailingStop modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
TrailingStop quyidagilar uchun javobgar.
✓ Trailing Rule Evaluation
✓ Dynamic Stop Loss Update
✓ Price Tracking
✓ Trailing State Management
✓ Trailing Report Generation
✓ Monitoring Metadata Generation
TrailingStop bajarmaydi.
✗ Trading Decision
✗ Risk Validation
✗ Order Execution
✗ Break Even
✗ Partial Close
✗ Recovery Management
---
# Module Boundary
```text
BreakevenManager
↓
TrailingStop
↓
PartialClose
```
---
# Input Contract
• Trade Context
• Position Information
• Current Market Price
• Trailing Rules (Risk Policy'dan)
• Monitoring Context
---
# Output Contract
• Updated Stop Loss
• Trailing Status
• Trailing Report
• Monitoring Metadata
• Trailing Events
---
# Allowed Dependencies
✓ BreakevenManager
✓ PartialClose
---
# Forbidden Dependencies
✗ RecoveryManager
✗ MonitoringService
✗ PositionMonitor
✗ TradeLifecycleManager
✗ SLTPMonitor
✗ Execution Layer
✗ Risk Layer
✗ Decision Layer
✗ Database Layer
---
# Runtime Contract
1. Trailing faqat aktiv Position uchun ishlashi shart.
2. Stop Loss faqat foyda tomonga siljitilishi shart.
3. Stop Loss hech qachon orqaga qaytmasligi shart.
4. Har bir yangilanish log qilinishi shart.
5. Trailing Report PartialClose moduliga uzatilishi shart.
6. TrailingStop Position'ni yopmaydi.
7. TrailingStop faqat Risk Policy ruxsat bergan harakatlarni bajaradi (Allow Trailing) va hech qachon risk'ni qayta hisoblamaydi yoki Risk Layer'ni chaqirmaydi.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Trade Context qabul qilinadi.
✓ Trailing qoidalari tekshiriladi.
✓ Market Price kuzatiladi.
✓ Stop Loss yangilanadi.
✓ Trailing Report yaratiladi.
✓ PartialClose moduliga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
TrailingStop Contract GoldBot Trade Monitoring Layer ichidagi Dynamic Stop Loss boshqaruvini amalga oshirish, Stop Loss'ni foyda tomonga dinamik ravishda yangilash va Trailing Report'ni PartialClose moduliga uzatishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
