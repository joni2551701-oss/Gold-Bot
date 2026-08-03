# RAG Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat RAG Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
SystemKnowledge
↓
RAG
↓
Semantic Search
↓
KnowledgeBase
↓
Retrieve Documents
↓
Rank Results
↓
Build Context
↓
ProviderRouter
```
---
# Runtime Rules
1. Semantic Search ishlatilishi shart.
2. Faqat relevant hujjatlar olinadi.
3. Ranking majburiy.
4. Context yaratiladi.
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
Building Context
↓
Completed
or
No Result
```
---
# Summary
User Request
↓
RAG
↓
Knowledge Context
↓
ProviderRouter
