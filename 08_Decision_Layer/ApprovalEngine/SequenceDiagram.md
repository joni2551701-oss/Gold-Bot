# Approval Engine Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat ApprovalEngine Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
DecisionConfidence
↓
RuleEngine
↓
ApprovalEngine
↓
Validate Rules
↓
Validate Confidence
↓
Generate Approval
↓
DecisionEngine
```
---
# Runtime Rules
1. Rule Validation tugagan bo'lishi shart.
2. Decision Confidence mavjud bo'lishi shart.
3. Approval Status yaratilishi shart.
4. Reject bo'lsa sabab yaratilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Validating
↓
Approving
↓
Completed
```
---
# Summary
DecisionConfidence
↓
RuleEngine
↓
ApprovalEngine
↓
DecisionEngine
