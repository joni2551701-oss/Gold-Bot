# Voice Session
Status: CANONICAL
---
# Purpose
VoiceSession GoldBot VoiceAI ichidagi Canonical Voice Session moduli hisoblanadi.
Uning asosiy vazifasi foydalanuvchining ovozli muloqot sessiyasini ochish, holatini saqlash, Voice Profile'ni qo'llash va sessiyani yopishdir.
VoiceSession AI javob yaratmaydi va ovozni qayta ishlamaydi.
---
# Objective
VoiceSession quyidagi vazifalarni bajaradi.
• Voice Session Lifecycle
• Session State Management
• Voice Profile Resolution
• Session Context Storage
• Multi-User Session Isolation
• Session Metadata
---
# Layer Position
```text
User Voice
↓
VoiceSession
↓
VoiceProvider
```
---
# Responsibilities
VoiceSession
✓ Voice Session ochadi va yopadi
✓ Session holatini saqlaydi
✓ Foydalanuvchining Voice Profile'ini aniqlaydi
✓ Har bir foydalanuvchi sessiyasini izolyatsiya qiladi
✓ Session Context'ni SpeechToText/TextToSpeech uchun taqdim etadi
---
# Not Responsible
VoiceSession
✗ Speech Recognition
✗ Speech Synthesis
✗ AI Analysis
✗ Decision Making
✗ Learning
---
# Input
VoiceSession qabul qiladi.
• Session Start Request
• User Identity
• Voice Profile Preference
• Session End Request
---
# Output
VoiceSession yaratadi.
• Voice Session
• Session State
• Resolved Voice Profile
• Session Metadata
---
# Workflow
```text
User Voice
↓
VoiceSession
↓
VoiceProvider
```
---
# Internal Modules (Planned — implementatsiya bosqichida to'ldiriladi)
```text
VoiceSession
├── SessionManager
├── SessionState
├── VoiceProfile
└── SessionContext
```
---
# Golden Rules
1. Har bir ovozli muloqot Voice Session ichida bo'lishi shart.
2. Sessiyalar foydalanuvchilar o'rtasida izolyatsiya qilinadi.
3. Voice Profile sessiya boshida aniqlanadi.
4. Sessiya yopilganda holat tozalanadi.
5. Audio saqlanmaydi (foydalanuvchi ruxsatisiz).
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
VoiceSession/
├── README.md
├── Contracts.md
├── ModuleMap.md
└── SequenceDiagram.md
```
---
# Summary
VoiceSession GoldBot VoiceAI ichidagi ovozli muloqot sessiyalarini boshqaruvchi yagona Canonical modul hisoblanadi. U ovozni qayta ishlamaydi — faqat sessiya konteksti va holatini ta'minlaydi.
