# Voice AI Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat VoiceAI Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
User Voice
↓
VoiceAI
↓
WakeWord
↓
SpeechToText
↓
InteractionManager
↓
PersonalAI
↓
TextToSpeech
↓
Voice Output
```
---
# Runtime Rules
1. Wake Word tekshirilishi mumkin.
2. STT birinchi ishlaydi.
3. AI javobi matn ko'rinishida olinadi.
4. TTS oxirida ishlaydi.
---
# State Flow
```text
Idle
↓
Listening
↓
Recognizing
↓
Processing
↓
Speaking
↓
Completed
```
---
# Summary
User Voice
↓
VoiceAI
↓
PersonalAI
↓
Voice Response
