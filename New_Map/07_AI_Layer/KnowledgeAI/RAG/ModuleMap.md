# RAG Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat RAG ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
KnowledgeAI
↓
RAG
↓
ProviderRouter
```
---
# Module Architecture
```text
RAG
        │
        ├── Query Processor
        ├── Semantic Retriever
        ├── Document Retriever
        ├── Ranking Engine
        ├── Context Builder
        └── Retrieval Cache
```
---
# Internal Components
## Query Processor
So'rovni tayyorlaydi.
---
## Semantic Retriever
Ma'noga asoslangan qidiruvni bajaradi.
---
## Document Retriever
Kerakli hujjatlarni topadi.
---
## Ranking Engine
Natijalarni relevanti bo'yicha saralaydi.
---
## Context Builder
AI uchun Context yaratadi.
---
## Retrieval Cache
Tez-tez ishlatiladigan Retrieval natijalarini vaqtincha saqlaydi.
---
# Allowed Dependencies
✓ KnowledgeBase
✓ ProviderRouter
---
# Forbidden Dependencies
✗ MemoryManager
✗ LearningEngine
✗ ValidationEngine
✗ Decision Layer
✗ Risk Layer
---
# Summary
RAG GoldBot AI ichidagi hujjatlar va Knowledge Repository'lardan ma'lumot topuvchi Canonical Retrieval Engine hisoblanadi.
