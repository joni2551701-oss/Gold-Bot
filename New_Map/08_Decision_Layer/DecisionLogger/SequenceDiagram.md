# Decision Logger Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat DecisionLogger Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
DecisionEngine
↓
DecisionLogger
↓
Receive Decision
↓
Build Audit Record
↓
Generate Metadata
↓
Write Log
↓
DecisionService
```
---
# Runtime Rules
1. Final Decision mavjud bo'lishi shart.
2. Audit Record yaratilishi shart.
3. Timestamp yozilishi shart.
4. Log DecisionService'ga uzatiladi (Database Layer'ga faqat DecisionService orqali yetadi).
---
# State Flow
```text
Idle
↓
Receiving
↓
Building Record
↓
Logging
↓
Completed
```
---
# Summary
DecisionEngine
↓
DecisionLogger
↓
Audit Record
↓
DecisionService
