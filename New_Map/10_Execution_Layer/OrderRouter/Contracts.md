# Order Router Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat OrderRouter modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
OrderRouter quyidagilar uchun javobgar.
✓ Route Selection
✓ Broker Selection
✓ Exchange Selection
✓ Route Validation
✓ Routed Order Generation
✓ Routing Metadata Generation
OrderRouter bajarmaydi.
✗ Trading Decision
✗ Risk Validation
✗ Broker Communication
✗ Order Validation
✗ Execution Monitoring
✗ Position Monitoring
---
# Module Boundary
```text
OrderManager
↓
OrderRouter
↓
BrokerGateway
```
---
# Input Contract
• Managed Order
• Routing Policy
• Broker Configuration
• Execution Context
---
# Output Contract
• Routed Order
• Routing Context
• Routing Report
• Routing Metadata
---
# Allowed Dependencies
✓ OrderManager
✓ BrokerGateway
---
# Forbidden Dependencies
✗ ExecutionMonitor
✗ ExecutionService
✗ Decision Layer
✗ Risk Layer
---
# Runtime Contract
1. Managed Order mavjud bo'lishi shart.
2. Routing Policy yuklanishi shart.
3. Broker yoki Exchange deterministik tanlanishi shart.
4. Route Validation muvaffaqiyatli o'tishi shart.
5. Routed Order BrokerGateway'ga uzatilishi shart.
6. OrderRouter Broker API bilan bevosita ishlamaydi.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Managed Order qabul qilinadi.
✓ Routing Policy yuklanadi.
✓ Broker tanlanadi.
✓ Route tekshiriladi.
✓ Routed Order yaratiladi.
✓ BrokerGateway'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
OrderRouter Contract GoldBot Execution Layer ichidagi Order Routing, Broker/Exchange tanlash va Routed Order'ni BrokerGateway moduliga uzatish qoidalarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
