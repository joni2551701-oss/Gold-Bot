# Interaction Manager Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat InteractionManager ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
User
↓
InteractionManager
↓
UserProfile
↓
PersonaManager
```
---
# Module Architecture
```text
InteractionManager
        │
        ├── Request Receiver
        ├── Session Manager
        ├── Context Builder
        ├── Request Router
        ├── Interaction Validator
        └── Event Publisher
```
---
# Internal Components
## Request Receiver
Barcha AI Request'larni qabul qiladi.
---
## Session Manager
Interaction Session yaratadi va boshqaradi.
---
## Context Builder
Interaction Context yaratadi.
---
## Request Router
Request'ni kerakli AI Pipeline'ga yuboradi.
---
## Interaction Validator
Interaction to'g'riligini tekshiradi.
---
## Event Publisher
Interaction Event yaratadi.
---
# Allowed Dependencies
✓ UserProfile
✓ PersonaManager
✓ AIEngine
---
# Forbidden Dependencies
✗ MemoryManager
✗ KnowledgeManager
✗ LearningEngine
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
InteractionManager foydalanuvchi va AI o'rtasidagi barcha muloqotlarni boshqaruvchi Canonical Gateway modulidir.
