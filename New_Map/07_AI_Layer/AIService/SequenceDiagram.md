# AI Service Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat AIService Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
Signal Layer
↓
AIService (Entry)
↓
Validate Request
↓
AIEngine
↓
AICoordinator (Module Execution)
↓
AIEngine
↓
AIService (Exit)
↓
Standardize Response
↓
Decision Layer
```
---
# Runtime Rules
1. Har bir Request tekshirilishi shart.
2. AIService AICoordinator yoki AI modullari bilan to'g'ridan-to'g'ri ishlamaydi — faqat AIEngine orqali.
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
Waiting (AIEngine)
↓
Receiving Response
↓
Completed
```
---
# Summary
Signal Layer
↓
AIService
↓
AIEngine
↓
AIService
↓
Decision Layer
