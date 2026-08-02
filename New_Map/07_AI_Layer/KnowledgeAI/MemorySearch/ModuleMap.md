# Memory Search Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat MemorySearch ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
KnowledgeAI
↓
MemorySearch
↓
MemoryManager
```
---
# Module Architecture
```text
MemorySearch
        │
        ├── Query Processor
        ├── Semantic Search
        ├── Context Matcher
        ├── Ranking Engine
        ├── Result Filter
        └── Result Builder
```
---
# Internal Components
## Query Processor
Qidiruv so'rovini tayyorlaydi.
---
## Semantic Search
Ma'noga asoslangan qidiruvni bajaradi.
---
## Context Matcher
Conversation Context bilan moslashtiradi.
---
## Ranking Engine
Natijalarni Score bo'yicha saralaydi.
---
## Result Filter
Mos kelmaydigan natijalarni chiqarib tashlaydi.
---
## Result Builder
Yakuniy Memory Result yaratadi.
---
# Allowed Dependencies
✓ MemoryManager
✓ KnowledgeBase
---
# Forbidden Dependencies
✗ LearningEngine
✗ ValidationEngine
✗ ProviderRouter
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
MemorySearch AI Memory Retrieval jarayonini boshqaruvchi Canonical modul hisoblanadi.
