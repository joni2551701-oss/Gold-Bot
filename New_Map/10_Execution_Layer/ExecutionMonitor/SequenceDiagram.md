# Execution Monitor Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat ExecutionMonitor Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
BrokerGateway
↓
ExecutionMonitor
↓
Receive Broker Response
↓
Track Status
↓
Detect Event
↓
Generate Execution Report
↓
Trade Monitoring Layer
```
---
# Runtime Rules
1. Broker Response mavjud bo'lishi shart.
2. Har bir Status tekshirilishi shart.
3. Execution Event aniqlanishi shart.
4. Execution Report yaratilishi shart.
---
# State Flow
```text
Idle
↓
Waiting Response
↓
Monitoring
↓
Detecting Event
↓
Reporting
↓
Completed
```
---
# Summary
BrokerGateway
↓
ExecutionMonitor
↓
Execution Report
↓
Trade Monitoring Layer
