# Voice Provider Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat VoiceProvider ichki arxitekturasini tavsiflaydi (ichki submodullar implementatsiya bosqichida to'ldiriladi).
---
# Internal Architecture (Planned)
```text
VoiceProvider
├── ProviderRegistry
├── ProviderContract
├── OpenAIAdapter
├── ElevenLabsAdapter
├── LocalAdapter
└── CustomAdapter
```
---
# Module Position
```text
VoiceSession
↓
VoiceProvider
↓
SpeechToText / TextToSpeech
```
---
# Processing Pipeline (Planned)
```text
ProviderRegistry → ProviderContract → OpenAIAdapter → ElevenLabsAdapter → LocalAdapter → CustomAdapter
```
---
# Dependency Map
```text
VoiceSession
↓
VoiceProvider
↓
SpeechToText / TextToSpeech
```
---
# Allowed Dependencies
✓ VoiceSession
✓ SpeechToText
✓ TextToSpeech
---
# Forbidden Dependencies
✗ VoiceCommands
✗ InteractionManager
✗ KnowledgeAI
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Runtime Flow
```text
Receive Input
↓
Process (VoiceProvider)
↓
Emit Output
↓
SpeechToText / TextToSpeech
```
---
# Summary
VoiceProvider VoiceProvider GoldBot VoiceAI ichidagi barcha tashqi ovoz provayderlarini boshqaruvchi yagona Canonical Provider Registry moduli hisoblanadi. U ovozni qayta ishlamaydi — faqat qaysi Provider ishlatilishini belgilaydi.
