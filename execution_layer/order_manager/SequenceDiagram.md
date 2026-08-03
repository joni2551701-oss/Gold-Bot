# Order Manager Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat OrderManager Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
OrderValidator
↓
OrderManager
↓
Create Order
↓
Assign Order ID
↓
Initialize Lifecycle
↓
Generate Managed Order
↓
OrderRouter
```
---
# Runtime Rules
1. Order Validation yakunlangan bo'lishi shart.
2. Order ID yaratilishi shart.
3. Lifecycle boshlanishi shart.
4. Managed Order OrderRouter'ga uzatilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Creating
↓
Managing
↓
Completed
```
---
# Summary
OrderValidator
↓
OrderManager
↓
Managed Order
↓
OrderRouter
