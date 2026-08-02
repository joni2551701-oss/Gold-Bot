# Order Router Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat OrderRouter Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
OrderManager
↓
OrderRouter
↓
Load Routing Policy
↓
Select Broker
↓
Validate Route
↓
Create Routed Order
↓
BrokerGateway
```
---
# Runtime Rules
1. Managed Order mavjud bo'lishi shart.
2. Routing Policy yuklanishi shart.
3. Route tekshirilishi shart.
4. Routed Order BrokerGateway'ga uzatilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Selecting Route
↓
Validating
↓
Dispatching
↓
Completed
```
---
# Summary
OrderManager
↓
OrderRouter
↓
BrokerGateway
