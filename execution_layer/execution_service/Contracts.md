# Execution Service Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat ExecutionService modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
ExecutionService quyidagilar uchun javobgar.
✓ Public Entry Point (Risk Layer'dan Execution Layer'ga kirish)
✓ Public Exit Point (Execution Layer'dan Trade Monitoring Layer'ga chiqish)
✓ Request Validation
✓ Response Serialization
✓ Session Management
✓ API Boundary Enforcement
ExecutionService bajarmaydi.
✗ Trading Decision
✗ Risk Validation
✗ Order Validation
✗ Order Management
✗ Order Routing
✗ Broker Communication
✗ Execution Monitoring
---
# Module Boundary
```text
Risk Layer
↓
ExecutionService (Entry)
↓
ExecutionEngine
↓
OrderValidator
↓
OrderManager
↓
OrderRouter
↓
BrokerGateway
↓
ExecutionMonitor
↓
ExecutionService (Exit)
↓
Trade Monitoring Layer
```
---
# Input Contract
Kirish tomonida (Risk Layer'dan):
• Risk Approval
• Risk Policy
• Position Package
• Execution Request
• Session Metadata

Chiqish tomonida (ExecutionMonitor'dan):
• Execution Result
---
# Output Contract
Kirish tomonida (ExecutionEngine'ga):
• Validated Execution Request

Chiqish tomonida (Trade Monitoring Layer'ga):
• Execution Response
• Execution Status
• Risk Policy
• Standard Response
• Service Metadata
---
# Allowed Dependencies
✓ ExecutionEngine
✓ ExecutionMonitor
---
# Forbidden Dependencies
✗ OrderValidator (to'g'ridan-to'g'ri)
✗ OrderManager (to'g'ridan-to'g'ri)
✗ OrderRouter (to'g'ridan-to'g'ri)
✗ BrokerGateway (to'g'ridan-to'g'ri)
✗ Decision Layer
✗ Risk Layer
✗ Database Layer
✗ Platform Layer
---
# Runtime Contract
1. Execution Layer'ga barcha kirish va chiqishlar ExecutionService orqali amalga oshirilishi shart (Boundary Gateway).
2. Har bir kirish Request Validation'dan o'tishi shart.
3. ExecutionService Business Logic bajarmaydi — faqat Entry/Exit Boundary vazifasini bajaradi.
4. Risk Policy Risk Layer'dan Trade Monitoring Layer'ga o'zgartirilmasdan uzatiladi.
5. Response standart formatda qaytarilishi shart.
6. ExecutionMonitor Layer tashqarisiga chiqmaydi — faqat ExecutionService orqali chiqadi.
7. Session holati boshqarilishi shart.
8. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Risk Layer'dan Request qabul qilinadi.
✓ Validation bajariladi.
✓ ExecutionEngine'ga uzatiladi.
✓ ExecutionMonitor'dan Execution Result qabul qilinadi.
✓ Response standartlashtiriladi.
✓ Trade Monitoring Layer'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
ExecutionService Contract GoldBot Execution Layer uchun ikki tomonlama (bidirectional) Boundary Gateway sifatida ishlashini — Risk Layer'dan kirish va Trade Monitoring Layer'ga chiqishni — belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
