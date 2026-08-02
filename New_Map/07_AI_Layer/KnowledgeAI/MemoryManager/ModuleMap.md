# Memory Manager Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat MemoryManager ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
LearningEngine
↓
MemoryManager
↓
PersonalKnowledge
```
---
# Module Architecture
```text
MemoryManager
        │
        ├── Memory Registrar
        ├── Memory Storage
        ├── Version Manager
        ├── Metadata Manager
        ├── Lifecycle Manager
        └── Archive Manager
```
---
# Internal Components
## Memory Registrar
Memory'ni ro'yxatdan o'tkazadi.
---
## Memory Storage
Memory'ni saqlaydi.
---
## Version Manager
Memory versiyalarini boshqaradi.
---
## Metadata Manager
Memory Metadata yaratadi.
---
## Lifecycle Manager
Memory hayotiy siklini boshqaradi.
---
## Archive Manager
Eski Memory'larni arxivlaydi.
---
# Allowed Dependencies
✓ LearningEngine
✓ PersonalKnowledge
---
# Forbidden Dependencies
✗ MemorySearch
✗ KnowledgeManager
✗ ValidationEngine
✗ ProviderRouter
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
MemoryManager Shared Memory va Personal Memory Lifecycle boshqaruvchi Canonical modul hisoblanadi.
