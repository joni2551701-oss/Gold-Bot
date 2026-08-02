# AI Layer Sequence Diagram
Status: CANONICAL
---
# Runtime Sequence
```text
External Layer
↓
AIService
↓
AIEngine
↓
AICoordinator
↓
PersonalAI
↓
KnowledgeAI
↓
FundamentalAI
↓
VisionAI
↓
ExplanationAI
↓
ConfidenceAI
↓
AI Package
↓
Decision Layer
```
---
# Runtime Rules
1. AIService har doim birinchi.
2. AIEngine Pipeline boshlaydi.
3. AICoordinator modullarni boshqaradi.
4. ConfidenceAI oxirida ishlaydi.
5. Decision Layer AI Package qabul qiladi.
---
# State Flow
```text
Idle
↓
Receiving
↓
Processing
↓
Collecting
↓
Packaging
↓
Completed
```
---
# Summary
AI Layer barcha AI modullarini orkestratsiya qilib, Decision Layer uchun yagona AI Package yaratadi.
