# Broker Gateway Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat BrokerGateway Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
OrderRouter
↓
BrokerGateway
↓
Load Broker Configuration
↓
Authenticate
↓
Send Order
↓
Receive Response
↓
Build Communication Report
↓
ExecutionMonitor
```
---
# Runtime Rules
1. Routed Order mavjud bo'lishi shart.
2. Broker Configuration yuklanishi shart.
3. Authentication muvaffaqiyatli bo'lishi shart.
4. Broker Response olinishi shart.
---
# State Flow
```text
Idle
↓
Connecting
↓
Authenticating
↓
Sending
↓
Waiting Response
↓
Completed
```
---
# Summary
OrderRouter
↓
BrokerGateway
↓
ExecutionMonitor
