# Execution Service Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat ExecutionService Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Risk Layer
↓
ExecutionService
↓
Validate Request
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
Receive Execution Result
↓
Standardize Response
↓
Trade Monitoring Layer
```
---
# Runtime Rules
1. Risk Approval mavjud bo'lishi shart.
2. Request Validation bajarilishi shart.
3. Execution Pipeline muvaffaqiyatli yakunlanishi shart.
4. Standard Response yaratilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Validating
↓
Forwarding
↓
Receiving Result
↓
Completed
```
---
# Summary
Risk Layer
↓
ExecutionService
↓
Execution Layer
↓
Trade Monitoring Layer
