# Decision Service Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat DecisionService Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
External Layer
↓
DecisionService
↓
Validate Request
↓
DecisionEngine
↓
DecisionLogger
↓
Receive Decision
↓
Standardize Response
↓
Risk Layer
```
---
# Runtime Rules
1. Request Validation bajarilishi shart.
2. DecisionEngine orqali Decision olinishi shart.
3. DecisionLogger Logging bajarishi shart.
4. Standard Response yaratilishi shart.
---
# State Flow
```text
Idle
↓
Receiving
↓
Validating
↓
Forwarding
↓
Receiving Response
↓
Completed
```
---
# Summary
External Layer
↓
DecisionService
↓
Decision Layer
↓
Risk Layer
