# Breakeven Manager Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat BreakevenManager modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
BreakevenManager quyidagilar uchun javobgar.
✓ Break Even Rule Evaluation
✓ Break Even Trigger Detection
✓ Stop Loss Relocation
✓ Break Even State Management
✓ Break Even Report Generation
✓ Monitoring Metadata Generation
BreakevenManager bajarmaydi.
✗ Trading Decision
✗ Risk Validation
✗ Order Execution
✗ Trailing Stop
✗ Partial Close
✗ Recovery Management
---
# Module Boundary
```text
SLTPMonitor
↓
BreakevenManager
↓
TrailingStop
```
---
# Input Contract
• Trade Context
• Position Information
• Current Market Price
• Break Even Rules (Risk Policy'dan)
• Monitoring Context
---
# Output Contract
• Break Even Status
• Updated Stop Loss
• Break Even Report
• Monitoring Metadata
• Break Even Events
---
# Allowed Dependencies
✓ SLTPMonitor
✓ TrailingStop
---
# Forbidden Dependencies
✗ PartialClose
✗ RecoveryManager
✗ Execution Layer
✗ Risk Layer
✗ Decision Layer
✗ Database Layer
---
# Runtime Contract
1. Break Even Trigger qoidalarga mos bo'lishi shart.
2. Break Even faqat bir marta qo'llanilishi shart.
3. Stop Loss faqat foyda tomonga ko'chirilishi shart.
4. Break Even Event yaratilishi shart.
5. Break Even Report TrailingStop moduliga uzatilishi shart.
6. BreakevenManager Position'ni yopmaydi.
7. BreakevenManager faqat Risk Policy ruxsat bergan harakatlarni bajaradi (Allow BE) va hech qachon risk'ni qayta hisoblamaydi yoki Risk Layer'ni chaqirmaydi.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Trade Context qabul qilinadi.
✓ Break Even qoidalari tekshiriladi.
✓ Trigger aniqlanadi.
✓ Stop Loss yangilanadi.
✓ Break Even Report yaratiladi.
✓ TrailingStop moduliga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
BreakevenManager Contract GoldBot Trade Monitoring Layer ichidagi Break Even qoidalarini qo'llash, Stop Loss'ni Entry yoki BE Offset darajasiga ko'chirish hamda Break Even Report'ni TrailingStop moduliga uzatishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
