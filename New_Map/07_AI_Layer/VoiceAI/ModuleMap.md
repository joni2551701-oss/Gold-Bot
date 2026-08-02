# Voice AI Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat VoiceAI ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
User
↓
VoiceAI
↓
InteractionManager
↓
PersonalAI
```
---
# Module Architecture
```text
VoiceAI
        │
        ├── SpeechToText
        ├── TextToSpeech
        ├── VoiceCommands
        ├── WakeWord
        ├── Voice Session Manager
        └── Audio Processor
```
---
# Internal Components
## SpeechToText
Ovozni matnga aylantiradi.
---
## TextToSpeech
Matnni ovozga aylantiradi.
---
## VoiceCommands
Ovozli buyruqlarni aniqlaydi.
---
## WakeWord
AI chaqiruv so'zini aniqlaydi.
---
## Voice Session Manager
Ovozli sessiyani boshqaradi.
---
## Audio Processor
Audio oqimini qayta ishlaydi.
---
# Allowed Dependencies
✓ InteractionManager
✓ PersonalAI
---
# Forbidden Dependencies
✗ KnowledgeAI
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
VoiceAI GoldBot AI ichidagi barcha Voice Processing modullarini boshqaruvchi Canonical modul hisoblanadi.
