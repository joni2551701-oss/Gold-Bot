# Decision Engine Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat DecisionEngine Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
ApprovalEngine
↓
DecisionEngine
↓
Validate Inputs
↓
Aggregate Results
↓
Create Final Decision
↓
DecisionLogger
```
---
# Runtime Rules
1. Approval Result mavjud bo'lishi shart.
2. Decision Confidence mavjud bo'lishi shart.
3. Rule Results mavjud bo'lishi shart.
4. Decision faqat bir marta yaratiladi.
---
# State Flow
```text
Idle
↓
Receiving
↓
Validating
↓
Aggregating
↓
Creating Decision
↓
Completed
```
---
# Summary
Approval + Confidence + Rules
↓
DecisionEngine
↓
Final Decision
