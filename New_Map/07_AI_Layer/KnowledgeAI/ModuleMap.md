# Knowledge AI Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat KnowledgeAI ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
PersonalAI
↓
KnowledgeAI
↓
AICoordinator
```
---
# Module Architecture
```text
KnowledgeAI
        │
        ├── KnowledgeManager
        ├── MemoryManager
        ├── MemorySearch
        ├── KnowledgeBase
        │      ├── SystemKnowledge
        │      └── PersonalKnowledge
        ├── LearningEngine
        ├── ValidationEngine
        ├── RAG
        └── ProviderRouter
```
---
# Internal Components
## KnowledgeManager
Knowledge Lifecycle'ni boshqaradi.
---
## MemoryManager
Shared Memory boshqaradi.
---
## MemorySearch
Memory qidiradi.
---
## KnowledgeBase
System va Personal Knowledge saqlaydi.
---
## LearningEngine
Tasdiqlangan bilimlarni o'rganadi.
---
## ValidationEngine
Yangi bilimni tekshiradi.
---
## RAG
Ichki hujjatlardan bilim topadi.
---
## ProviderRouter
External AI Provider'larni boshqaradi.
---
# Allowed Dependencies
✓ PersonalAI
✓ AIEngine
✓ AICoordinator
---
# Forbidden Dependencies
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Summary
KnowledgeAI GoldBot AI Layer ichidagi barcha Knowledge va Memory modullarini boshqaruvchi Canonical Knowledge Center hisoblanadi.
