# Knowledge Manager Module Map
Status: CANONICAL
---
# Purpose
KnowledgeManager ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
KnowledgeAI
↓
KnowledgeManager
↓
KnowledgeBase
```
---
# Module Architecture
```text
KnowledgeManager
        │
        ├── Knowledge Registrar
        ├── Classification Engine
        ├── Version Manager
        ├── Metadata Manager
        ├── Lifecycle Manager
        └── Reference Manager
```
---
# Internal Components
## Knowledge Registrar
Knowledge ro'yxatdan o'tkazadi.
---
## Classification Engine
Knowledge turini aniqlaydi.
---
## Version Manager
Knowledge versiyalarini boshqaradi.
---
## Metadata Manager
Metadata yaratadi.
---
## Lifecycle Manager
Knowledge hayotiy siklini boshqaradi.
---
## Reference Manager
Knowledge ID va Reference boshqaradi.
---
# Allowed Dependencies
✓ KnowledgeBase
---
# Forbidden Dependencies
✗ MemoryManager
✗ MemorySearch
✗ ProviderRouter
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
KnowledgeManager Knowledge Lifecycle boshqaruvchi Canonical modul hisoblanadi.
