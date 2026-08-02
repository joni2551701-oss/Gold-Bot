# Learning Engine Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat LearningEngine Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
ValidationEngine
↓
LearningEngine
↓
Analyze Knowledge
↓
Update Knowledge
↓
Update Memory
↓
Save Learning History
↓
Completed
```
---
# Runtime Rules
1. Validation muvaffaqiyatli bo'lishi shart.
2. Learning faqat tasdiqlangan bilim uchun ishlaydi.
3. Knowledge va Memory birgalikda yangilanadi.
4. Learning History yoziladi.
---
# State Flow
```text
Idle
↓
Receiving
↓
Learning
↓
Updating
↓
Completed
```
---
# Summary
ValidationEngine
↓
LearningEngine
↓
KnowledgeManager
↓
MemoryManager
