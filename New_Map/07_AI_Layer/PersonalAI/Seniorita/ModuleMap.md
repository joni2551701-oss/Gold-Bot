# Seniorita Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Seniorita Persona ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
PersonalAI
↓
Seniorita
↓
KnowledgeAI
```
---
# Module Architecture
```text
Seniorita
        │
        ├── Friendly Persona
        ├── Trading Assistant
        ├── Education Assistant
        ├── Project Assistant
        └── Voice Persona
```
---
# Internal Components
## Friendly Persona
Do'stona va tabiiy muloqot uslubi.
---
## Trading Assistant
Trading bo'yicha yordam.
---
## Education Assistant
Ta'lim va tushuntirish.
---
## Project Assistant
GoldBot va boshqa loyihalarda yordam.
---
## Voice Persona
Kelajakdagi ovozli yordamchi Personasi.
---
# Allowed Dependencies
✓ PersonaManager
✓ KnowledgeAI
✓ AIEngine
---
# Forbidden Dependencies
✗ MemoryManager
✗ LearningEngine
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
Seniorita Friendly Persona bo'lib, barcha bilim va xotirani Shared AI Core orqali oladi.
