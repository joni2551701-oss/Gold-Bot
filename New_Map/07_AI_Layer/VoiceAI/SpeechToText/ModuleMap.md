# Speech To Text Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat SpeechToText ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
VoiceAI
↓
SpeechToText
↓
InteractionManager
```
---
# Module Architecture
```text
SpeechToText
        │
        ├── Audio Receiver
        ├── Language Detector
        ├── Speech Recognizer
        ├── Transcript Builder
        ├── Confidence Evaluator
        └── Metadata Generator
```
---
# Internal Components
## Audio Receiver
Audio oqimini qabul qiladi.
---
## Language Detector
Nutq tilini aniqlaydi.
---
## Speech Recognizer
Nutqni matnga aylantiradi.
---
## Transcript Builder
Yakuniy transcript yaratadi.
---
## Confidence Evaluator
Aniqlik darajasini hisoblaydi.
---
## Metadata Generator
Recognition Metadata yaratadi.
---
# Allowed Dependencies
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
SpeechToText VoiceAI ichidagi Speech Recognition jarayonini boshqaruvchi Canonical modul hisoblanadi.
