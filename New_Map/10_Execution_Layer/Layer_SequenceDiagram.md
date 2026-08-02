# Execution Layer Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Execution Layer Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Risk Layer
↓
ExecutionService
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
Trade Monitoring Layer
```
---
# Runtime Rules
1. Risk Approval mavjud bo'lishi shart.
2. Order Validation muvaffaqiyatli o'tishi shart.
3. Broker Authentication bajarilishi shart.
4. Broker Response olinishi shart.
5. ExecutionMonitor yakuniy Status yaratadi.
6. Trade Monitoring Layer Execution Result qabul qiladi.
---
# State Flow
```text
Idle
↓
Receiving Request
↓
Validating
↓
Managing Order
↓
Routing
↓
Broker Communication
↓
Monitoring
↓
Completed
```
---
# Summary
Risk Layer
↓
Execution Layer
↓
Trade Monitoring Layer
