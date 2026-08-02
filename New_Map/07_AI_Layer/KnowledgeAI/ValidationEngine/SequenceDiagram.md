# Validation Engine Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat ValidationEngine Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
New Knowledge
↓
ValidationEngine
↓
Validate Source
↓
Check Duplicate
↓
Evaluate Confidence
↓
Approve / Reject
↓
LearningEngine
```
---
# Runtime Rules
1. Source tekshirilishi shart.
2. Duplicate tekshirilishi shart.
3. Confidence hisoblanishi shart.
4. Approval yoki Rejection yaratilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Validating
↓
Evaluating
↓
Approved
or
Rejected
```
---
# Summary
New Knowledge
↓
ValidationEngine
↓
Approved Knowledge
↓
LearningEngine
