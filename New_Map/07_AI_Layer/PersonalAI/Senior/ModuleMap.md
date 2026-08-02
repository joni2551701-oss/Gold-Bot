# Senior Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Senior Persona ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
PersonalAI
↓
Senior
↓
KnowledgeAI
```
---
# Module Architecture
```text
Senior
        │
        ├── Professional Persona
        ├── Trading Assistant
        ├── Education Assistant
        ├── Project Assistant
        └── Voice Persona
```
---
# Internal Components
## Professional Persona
Professional javob uslubi.
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
✗ FundamentalAI
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
Senior Professional Persona bo'lib, barcha bilim va xotirani Shared AI Core orqali oladi.
