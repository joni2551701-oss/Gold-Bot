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
ExecutionService (Entry)
↓
Validate Request
↓
ExecutionEngine
↓
ExecutionService (Exit)
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
4. ExecutionMonitor natijasi ExecutionService orqali Trade Monitoring Layer'ga uzatiladi.
5. Standard Response yaratilishi shart.
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
