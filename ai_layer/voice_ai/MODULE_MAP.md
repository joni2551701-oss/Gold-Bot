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
        ├── VoiceProvider
        └── VoiceSession
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
## VoiceProvider
Tashqi ovoz provayderlarini (OpenAI, ElevenLabs, Local, Custom) ro'yxatga oladi va tanlaydi. Audio oqimini qayta ishlash tashqi Provider Adapter zimmasida bo'ladi.
---
## VoiceSession
Ovozli muloqot sessiyasini ochadi, holatini saqlaydi va Voice Profile'ni qo'llaydi.
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
