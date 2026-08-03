# Order Manager Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat OrderManager modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
OrderManager quyidagilar uchun javobgar.
✓ Order Creation
✓ Order ID Generation
✓ Order Lifecycle Management
✓ Order Status Management
✓ Order Package Generation
✓ Order Metadata Generation
OrderManager bajarmaydi.
✗ Trading Decision
✗ Risk Validation
✗ Broker Communication
✗ Order Routing
✗ Execution Monitoring
✗ Position Monitoring
---
# Module Boundary
```text
OrderValidator
↓
OrderManager
↓
OrderRouter
```
---
# Input Contract
• Validated Order
• Execution Context
• Position Package
• Order Metadata
---
# Output Contract
• Managed Order
• Order Lifecycle
• Order Context
• Order Metadata
---
# Allowed Dependencies
✓ OrderValidator
✓ OrderRouter
---
# Forbidden Dependencies
✗ BrokerGateway
✗ ExecutionMonitor
✗ Decision Layer
✗ Risk Layer
✗ Database Layer
✗ Platform Layer
---
# Runtime Contract
1. Faqat Validated Order qabul qilinadi.
2. Har bir Order uchun yagona Order ID yaratilishi shart.
3. Lifecycle NEW holatidan boshlanishi shart.
4. Order Status faqat OrderManager tomonidan o'zgartiriladi.
5. Managed Order OrderRouter'ga uzatilishi shart.
6. Broker bilan to'g'ridan-to'g'ri aloqa qilinmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Order qabul qilinadi.
✓ Order ID yaratiladi.
✓ Lifecycle boshlanadi.
✓ Order Status belgilanadi.
✓ Order Package yaratiladi.
✓ OrderRouter'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
OrderManager Contract GoldBot Execution Layer ichidagi Order Lifecycle'ni boshqarish, yagona Order ID yaratish, Order Status'ni nazorat qilish va OrderRouter moduliga standart Managed Order uzatishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
