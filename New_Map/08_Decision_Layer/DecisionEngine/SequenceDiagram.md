# Decision Engine Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat DecisionEngine Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Signal Package
↓
AI Package
↓
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
↓
DecisionService
```
---
# Runtime Rules
1. Signal Package mavjud bo'lishi shart.
2. AI Package mavjud bo'lishi shart.
3. Approval Result mavjud bo'lishi shart.
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
Signal + AI
↓
DecisionEngine
↓
Final Decision
