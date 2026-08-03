# Order Validator Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat OrderValidator Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
ExecutionEngine
↓
OrderValidator
↓
Validate Order Structure
↓
Validate Price
↓
Validate Volume
↓
Validate SL/TP
↓
Generate Validation Report
↓
OrderManager
```
---
# Runtime Rules
1. Order Request mavjud bo'lishi shart.
2. Symbol Specification mavjud bo'lishi shart.
3. Validation yakunlanishi shart.
4. Validated Order OrderManager'ga uzatilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Validating
↓
Generating Report
↓
Completed
```
---
# Summary
ExecutionEngine
↓
OrderValidator
↓
Validated Order
↓
OrderManager
