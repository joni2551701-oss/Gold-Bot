# User Profile Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat UserProfile ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
InteractionManager
↓
UserProfile
↓
PersonaManager
```
---
# Module Architecture
```text
UserProfile
        │
        ├── Identity Manager
        ├── Settings Manager
        ├── Preference Manager
        ├── Trading Profile
        ├── AI Profile
        └── Platform Profile
```
---
# Internal Components
## Identity Manager
User identifikatsiyasini boshqaradi.
---
## Settings Manager
Asosiy sozlamalarni boshqaradi.
---
## Preference Manager
Foydalanuvchi preferensiyalarini boshqaradi.
---
## Trading Profile
Trading uslubi va parametrlarini saqlaydi.
---
## AI Profile
Persona va AI sozlamalarini saqlaydi.
---
## Platform Profile
Til, platforma va interfeys sozlamalarini boshqaradi.
---
# Allowed Dependencies
✓ InteractionManager
✓ PersonaManager
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
UserProfile foydalanuvchi konfiguratsiyasi va preferensiyalarini boshqaruvchi Canonical modul hisoblanadi.
