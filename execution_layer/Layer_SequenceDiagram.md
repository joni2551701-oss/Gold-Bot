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
# Runtime Rules
1. Risk Approval mavjud bo'lishi shart.
2. ExecutionService Execution Layer'ning yagona Entry va Exit nuqtasi hisoblanadi.
3. Order Validation muvaffaqiyatli o'tishi shart.
4. Broker Authentication bajarilishi shart.
5. Broker Response olinishi shart.
6. ExecutionMonitor yakuniy Status yaratadi, lekin Layer tashqarisiga chiqmaydi.
7. Trade Monitoring Layer Execution Result'ni ExecutionService orqali qabul qiladi.
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
