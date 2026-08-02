# AI Service Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat AIService Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
External Layer
↓
AIService
↓
Validate Request
↓
AIEngine
↓
AICoordinator
↓
Receive AI Package
↓
Standardize Response
↓
Return Response
```
---
# Runtime Rules
1. Har bir Request tekshirilishi shart.
2. AIEngine yagona Processing markazi.
3. Response standart formatga o'tkaziladi.
4. Service Metadata qo'shiladi.
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
AIService
↓
AIEngine
↓
AI Response
