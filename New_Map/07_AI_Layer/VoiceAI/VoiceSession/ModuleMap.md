# Voice Session Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat VoiceSession ichki arxitekturasini tavsiflaydi (ichki submodullar implementatsiya bosqichida to'ldiriladi).
---
# Internal Architecture (Planned)
```text
VoiceSession
├── SessionManager
├── SessionState
├── VoiceProfile
└── SessionContext
```
---
# Module Position
```text
User Voice
↓
VoiceSession
↓
VoiceProvider
```
---
# Processing Pipeline (Planned)
```text
SessionManager → SessionState → VoiceProfile → SessionContext
```
---
# Dependency Map
```text
User Voice
↓
VoiceSession
↓
VoiceProvider
```
---
# Allowed Dependencies
✓ VoiceProvider
✓ SpeechToText
✓ TextToSpeech
---
# Forbidden Dependencies
✗ InteractionManager
✗ KnowledgeAI
✗ PersonalAI
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Runtime Flow
```text
Receive Input
↓
Process (VoiceSession)
↓
Emit Output
↓
VoiceProvider
```
---
# Summary
VoiceSession VoiceSession GoldBot VoiceAI ichidagi ovozli muloqot sessiyalarini boshqaruvchi yagona Canonical modul hisoblanadi. U ovozni qayta ishlamaydi — faqat sessiya konteksti va holatini ta'minlaydi.
