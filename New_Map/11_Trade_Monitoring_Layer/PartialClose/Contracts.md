# Partial Close Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat PartialClose modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
PartialClose quyidagilar uchun javobgar.
✓ Partial Close Rule Evaluation
✓ Close Volume Calculation
✓ Position Size Update
✓ Partial Close State Management
✓ Partial Close Report Generation
✓ Monitoring Metadata Generation
PartialClose bajarmaydi.
✗ Trading Decision
✗ Risk Validation
✗ Order Execution
✗ Break Even
✗ Trailing Stop
✗ Recovery Management
---
# Module Boundary
```text
TrailingStop
↓
PartialClose
↓
RecoveryManager
```
---
# Input Contract
• Trade Context
• Position Information
• Current Position Size
• Partial Close Rules (Risk Policy'dan)
• Monitoring Context
---
# Output Contract
• Updated Position
• Remaining Position
• Partial Close Status
• Partial Close Report
• Monitoring Metadata
---
# Allowed Dependencies
✓ TrailingStop
✓ RecoveryManager
---
# Forbidden Dependencies
✗ PositionMonitor
✗ TradeLifecycleManager
✗ Execution Layer
✗ Risk Layer
✗ Decision Layer
✗ Database Layer
✗ MonitoringService
✗ SLTPMonitor
✗ BreakevenManager
---
# Runtime Contract
1. Partial Close Rules tekshirilishi shart.
2. Close Volume Position hajmidan oshmasligi shart.
3. Remaining Position to'g'ri hisoblanishi shart.
4. Partial Close faqat bir marta bajarilishi kerak bo'lgan bosqichda bajariladi.
5. Partial Close Report RecoveryManager moduliga uzatilishi shart.
6. PartialClose Position'ni to'liq yopmaydi.
7. PartialClose faqat Risk Policy ruxsat bergan harakatlarni bajaradi (Allow Partial Close, Max Partial %) va hech qachon risk'ni qayta hisoblamaydi yoki Risk Layer'ni chaqirmaydi.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Trade Context qabul qilinadi.
✓ Partial Close qoidalari tekshiriladi.
✓ Close Volume hisoblanadi.
✓ Position hajmi yangilanadi.
✓ Partial Close Report yaratiladi.
✓ RecoveryManager moduliga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
PartialClose Contract GoldBot Trade Monitoring Layer ichidagi Position'ni qisman yopish, qolgan Position hajmini yangilash hamda Partial Close Report'ni RecoveryManager moduliga uzatishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
