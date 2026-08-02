# Text To Speech Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat TextToSpeech ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
VoiceAI
↓
TextToSpeech
↓
User
```
---
# Module Architecture
```text
TextToSpeech
        │
        ├── Text Processor
        ├── Voice Selector
        ├── Speech Synthesizer
        ├── Emotion Controller
        ├── Audio Generator
        └── Metadata Generator
```
---
# Internal Components
## Text Processor
Matnni tayyorlaydi.
---
## Voice Selector
Senior yoki Seniorita ovozini tanlaydi.
---
## Speech Synthesizer
Ovozni yaratadi.
---
## Emotion Controller
Intonatsiya va hissiy ohangni boshqaradi.
---
## Audio Generator
Yakuniy audio oqimini yaratadi.
---
## Metadata Generator
Speech Metadata yaratadi.
---
# Allowed Dependencies
✓ PersonalAI
✓ PersonaManager
---
# Forbidden Dependencies
✗ SpeechToText
✗ KnowledgeAI
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
TextToSpeech VoiceAI ichidagi barcha Speech Synthesis jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
