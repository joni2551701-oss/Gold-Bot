# Knowledge Base Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat KnowledgeBase ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
KnowledgeManager
↓
KnowledgeBase
↓
MemorySearch
```
---
# Module Architecture
```text
KnowledgeBase
        │
        ├── SystemKnowledge
        ├── PersonalKnowledge
        ├── Knowledge Index
        ├── Version Repository
        ├── Metadata Repository
        └── Repository Manager
```
---
# Internal Components
## SystemKnowledge
Barcha foydalanuvchilar uchun umumiy bilimlar.
---
## PersonalKnowledge
Har bir foydalanuvchining shaxsiy bilimlari.
---
## Knowledge Index
Knowledge indekslarini boshqaradi.
---
## Version Repository
Knowledge versiyalarini saqlaydi.
---
## Metadata Repository
Knowledge Metadata saqlaydi.
---
## Repository Manager
Repository boshqaruvini amalga oshiradi.
---
# Allowed Dependencies
✓ KnowledgeManager
✓ MemorySearch
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
KnowledgeBase GoldBot AI uchun markaziy Knowledge Repository hisoblanadi.
