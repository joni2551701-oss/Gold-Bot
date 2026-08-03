# Voice Commands Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat VoiceCommands ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
SpeechToText
↓
VoiceCommands
↓
InteractionManager
```
---
# Module Architecture
```text
VoiceCommands
        │
        ├── Intent Detector
        ├── Command Parser
        ├── Parameter Extractor
        ├── Context Analyzer
        ├── Command Builder
        └── Command Router
```
---
# Internal Components
## Intent Detector
Buyruq maqsadini aniqlaydi.
---
## Command Parser
Buyruqni sintaktik tahlil qiladi.
---
## Parameter Extractor
Buyruq parametrlarini ajratadi.
---
## Context Analyzer
Conversation Context'ni hisobga oladi.
---
## Command Builder
Standart AI Command yaratadi.
---
## Command Router
Command'ni InteractionManager'ga uzatadi.
---
# Allowed Dependencies
✓ SpeechToText
✓ InteractionManager
---
# Forbidden Dependencies
✗ TextToSpeech
✗ KnowledgeAI
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
VoiceCommands VoiceAI ichidagi barcha Voice Command Processing jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
