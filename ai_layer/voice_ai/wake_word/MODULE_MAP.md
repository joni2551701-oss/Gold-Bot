# Wake Word Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat WakeWord ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
VoiceAI
↓
WakeWord
↓
SpeechToText
```
---
# Module Architecture
```text
WakeWord
        │
        ├── Audio Listener
        ├── Wake Detector
        ├── Trigger Validator
        ├── Session Activator
        ├── False Trigger Filter
        └── Wake Event Builder
```
---
# Internal Components
## Audio Listener
Audio oqimini doimiy tinglaydi.
---
## Wake Detector
Wake Word'ni aniqlaydi.
---
## Trigger Validator
Wake Word haqiqiyligini tekshiradi.
---
## Session Activator
Voice Session'ni ishga tushiradi.
---
## False Trigger Filter
Noto'g'ri faollashuvlarni kamaytiradi.
---
## Wake Event Builder
Wake Event obyektini yaratadi.
---
# Allowed Dependencies
✓ SpeechToText
---
# Forbidden Dependencies
✗ TextToSpeech
✗ KnowledgeAI
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Summary
WakeWord VoiceAI ichidagi Voice Activation jarayonini boshqaruvchi Canonical modul hisoblanadi.
