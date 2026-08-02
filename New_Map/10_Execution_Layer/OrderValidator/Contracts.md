# Order Validator Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat OrderValidator modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
OrderValidator quyidagilar uchun javobgar.
✓ Order Structure Validation
✓ Price Validation
✓ Volume Validation
✓ SL/TP Validation
✓ Symbol Validation
✓ Validation Report Generation
OrderValidator bajarmaydi.
✗ Trading Decision
✗ Risk Validation
✗ Order Creation
✗ Broker Communication
✗ Order Routing
✗ Position Monitoring
---
# Module Boundary
```text
ExecutionEngine
↓
OrderValidator
↓
OrderManager
```
---
# Input Contract
• Order Request
• Position Package
• Symbol Specification
• Execution Context
---
# Output Contract
• Validated Order
• Validation Status
• Validation Report
• Validation Metadata
---
# Allowed Dependencies
✓ ExecutionEngine
✓ OrderManager
---
# Forbidden Dependencies
✗ BrokerGateway
✗ OrderRouter
✗ ExecutionMonitor
✗ Decision Layer
---
# Runtime Contract
1. Order Structure tekshirilishi shart.
2. Price tekshirilishi shart.
3. Volume tekshirilishi shart.
4. SL/TP tekshirilishi shart.
5. Symbol parametrlarini tekshirish majburiy.
6. VALID bo'lmagan Order OrderManager'ga uzatilmaydi.
7. Validation Report yaratilishi shart.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Order qabul qilinadi.
✓ Structure tekshiriladi.
✓ Price tekshiriladi.
✓ Volume tekshiriladi.
✓ SL/TP tekshiriladi.
✓ Validation Report yaratiladi.
✓ Validated Order OrderManager'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
OrderValidator Contract GoldBot Execution Layer ichidagi barcha Order parametrlarini tekshirish, Validation Report yaratish va faqat VALID holatdagi Order'larni OrderManager moduliga uzatishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
