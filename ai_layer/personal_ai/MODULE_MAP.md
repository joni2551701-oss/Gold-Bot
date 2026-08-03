# Personal AI Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat PersonalAI ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
AIEngine
↓
PersonalAI
↓
KnowledgeAI
```
---
# Module Architecture
```text
PersonalAI
        │
        ├── Senior
        ├── Seniorita
        ├── PersonaManager
        ├── UserProfile
        └── InteractionManager
```
---
# Internal Components
## Senior
Professional Persona.
---
## Seniorita
Alternative Persona.
---
## PersonaManager
Faol Persona'ni boshqaradi.
---
## UserProfile
Foydalanuvchi profilini boshqaradi.
---
## InteractionManager
Barcha foydalanuvchi-AI muloqotlarini boshqaradi.
---
# Allowed Dependencies
✓ KnowledgeAI
✓ AIEngine
✓ AICoordinator
---
# Forbidden Dependencies
✗ FundamentalAI
✗ VoiceAI
✗ VisionAI
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
PersonalAI GoldBot foydalanuvchilari uchun yagona Personal Intelligence modulidir.
