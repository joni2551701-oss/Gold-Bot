# Decision Confidence Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat DecisionConfidence Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Signal Package
↓
AI Package
↓
DecisionConfidence
↓
Evaluate Technical Score
↓
Merge AI Confidence
↓
Evaluate Signal Quality
↓
Calculate Confidence
↓
Generate Confidence Report
↓
RuleEngine
```
---
# Runtime Rules
1. Signal Package mavjud bo'lishi shart.
2. AI Package mavjud bo'lishi shart.
3. Technical Score hisoblanishi shart.
4. Yakuniy Confidence yaratilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Evaluating
↓
Calculating
↓
Completed
```
---
# Summary
Signal + AI
↓
DecisionConfidence
↓
Confidence Report
↓
RuleEngine
