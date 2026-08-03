# Knowledge Manager Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat KnowledgeManager Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
KnowledgeAI
↓
KnowledgeManager
↓
Classify Knowledge
↓
Generate Metadata
↓
Version Knowledge
↓
Register Knowledge
↓
KnowledgeBase
```
---
# Runtime Rules
1. Validation muvaffaqiyatli bo'lishi shart.
2. Knowledge klassifikatsiya qilinadi.
3. Metadata yaratiladi.
4. Version belgilanadi.
5. KnowledgeBase'ga uzatiladi.
---
# State Flow
```text
Idle
↓
Receiving
↓
Classifying
↓
Versioning
↓
Registering
↓
Completed
```
---
# Summary
Validation
↓
KnowledgeManager
↓
KnowledgeBase
