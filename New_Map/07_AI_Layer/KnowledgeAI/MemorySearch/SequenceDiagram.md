# Memory Search Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat MemorySearch Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
User Request
↓
MemorySearch
↓
Preprocess Query
↓
Search Personal Memory
↓
Search Shared Memory
↓
Rank Results
↓
Return Best Match
↓
KnowledgeAI
```
---
# Runtime Rules
1. Personal Memory birinchi tekshiriladi.
2. Shared Memory ikkinchi tekshiriladi.
3. Semantic Search ishlatiladi.
4. Ranking majburiy.
5. Faqat eng mos natija qaytariladi.
---
# State Flow
```text
Idle
↓
Receiving
↓
Searching
↓
Ranking
↓
Completed
or
No Match
```
---
# Summary
User Request
↓
MemorySearch
↓
Best Memory
↓
KnowledgeAI
