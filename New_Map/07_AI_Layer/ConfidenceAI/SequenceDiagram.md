# Confidence AI Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat ConfidenceAI Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
AICoordinator
↓
ConfidenceAI
↓
Collect Context
↓
Evaluate Sources
↓
Check Consistency
↓
Calculate Confidence
↓
Generate Report
↓
Decision Layer
```
---
# Runtime Rules
1. Context mavjud bo'lishi shart.
2. Source Reliability tekshiriladi.
3. Context Consistency tekshiriladi.
4. Confidence Score hisoblanadi.
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
AI Context
↓
ConfidenceAI
↓
Confidence Report
↓
Decision Layer
