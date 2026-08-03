# Persona Manager Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat PersonaManager ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
InteractionManager
↓
PersonaManager
↓
Senior
or
Seniorita
```
---
# Module Architecture
```text
PersonaManager
        │
        ├── Persona Loader
        ├── Persona Validator
        ├── Persona Router
        ├── Persona Switcher
        ├── Active Persona Manager
        └── Persona Settings
```
---
# Internal Components
## Persona Loader
Foydalanuvchi Persona'sini yuklaydi.
---
## Persona Validator
Persona mavjudligini tekshiradi.
---
## Persona Router
Request'ni kerakli Persona'ga yuboradi.
---
## Persona Switcher
Persona almashtiradi.
---
## Active Persona Manager
Faol Persona'ni boshqaradi.
---
## Persona Settings
Persona konfiguratsiyasini boshqaradi.
---
# Allowed Dependencies
✓ UserProfile
✓ Senior
✓ Seniorita
✓ InteractionManager
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
PersonaManager foydalanuvchi tanlagan Persona'ni boshqaruvchi Canonical Routing moduli hisoblanadi.
