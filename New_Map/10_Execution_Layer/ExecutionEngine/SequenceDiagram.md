# Execution Engine Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat ExecutionEngine Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
ExecutionService
↓
ExecutionEngine
↓
Validate Request
↓
Build Execution Context
↓
OrderValidator
```
---
# Runtime Rules
1. Validated Execution Request mavjud bo'lishi shart.
2. Execution Context yaratilishi shart.
3. Pipeline ketma-ket bajarilishi shart.
4. Execution Result yaratilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Validating
↓
Executing
↓
Collecting Results
↓
Completed
```
---
# Summary
ExecutionService
↓
ExecutionEngine
↓
Execution Context
↓
OrderValidator
