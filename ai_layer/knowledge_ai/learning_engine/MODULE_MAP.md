# Learning Engine Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat LearningEngine ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
ValidationEngine
↓
LearningEngine
↓
Knowledge Context
```
---
# Module Architecture
```text
LearningEngine
        │
        ├── Learning Analyzer
        ├── Pattern Learner
        ├── Knowledge Updater
        ├── Memory Updater
        ├── Experience Builder
        └── Learning History
```
---
# Internal Components
## Learning Analyzer
Yangi bilimni tahlil qiladi.
---
## Pattern Learner
Takrorlanuvchi naqshlarni o'rganadi.
---
## Knowledge Updater
KnowledgeBase'ni yangilaydi.
---
## Memory Updater
Shared Memory'ni yangilaydi.
---
## Experience Builder
AI tajribasini boyitadi.
---
## Learning History
Learning tarixini saqlaydi.
---
# Allowed Dependencies
✓ ValidationEngine
---
# Forbidden Dependencies
✗ ProviderRouter
✗ MemorySearch
✗ KnowledgeManager
✗ MemoryManager
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
LearningEngine GoldBot AI Self-Learning jarayonini boshqaruvchi Canonical modul hisoblanadi.
