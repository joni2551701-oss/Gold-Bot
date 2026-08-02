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
VoiceCommands
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
3. STT natijasi VoiceCommands orqali AI Command'ga aylantiriladi.
4. AI javobi matn ko'rinishida olinadi.
5. TTS oxirida ishlaydi.
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
