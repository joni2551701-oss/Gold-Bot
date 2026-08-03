# Personal Knowledge Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat PersonalKnowledge Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
MemoryManager
↓
PersonalKnowledge
↓
Store Knowledge
↓
Update Repository
↓
Ready For Retrieval
---
# Runtime Rules
1. User ID mavjud bo'lishi shart.
2. Validation muvaffaqiyatli bo'lishi shart.
3. Knowledge Version saqlanadi.
4. Repository yangilanadi.
---
# State Flow
Idle
↓
Receiving
↓
Storing
↓
Updating
↓
Completed
---
# Summary
KnowledgeManager
↓
PersonalKnowledge
↓
Personal Repository
