# Voice Session Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat VoiceSession modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
VoiceSession quyidagilar uchun javobgar.
✓ Voice Session ochadi va yopadi
✓ Session holatini saqlaydi
✓ Foydalanuvchining Voice Profile'ini aniqlaydi
✓ Har bir foydalanuvchi sessiyasini izolyatsiya qiladi
✓ Session Context'ni SpeechToText/TextToSpeech uchun taqdim etadi
VoiceSession bajarmaydi.
✗ Speech Recognition
✗ Speech Synthesis
✗ AI Analysis
✗ Decision Making
✗ Learning
---
# Module Boundary
```text
User Voice
↓
VoiceSession
↓
VoiceProvider
```
---
# Input Contract
• Session Start Request
• User Identity
• Voice Profile Preference
• Session End Request
---
# Output Contract
• Voice Session
• Session State
• Resolved Voice Profile
• Session Metadata
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
# Runtime Contract
1. Har bir ovozli muloqot Voice Session ichida bo'lishi shart.
2. Sessiyalar foydalanuvchilar o'rtasida izolyatsiya qilinadi.
3. Voice Profile sessiya boshida aniqlanadi.
4. Sessiya yopilganda holat tozalanadi.
5. Audio saqlanmaydi (foydalanuvchi ruxsatisiz).
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Session ochiladi.
✓ Session State saqlanadi.
✓ Voice Profile qo'llanadi.
✓ Session yopiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
VoiceSession Contract VoiceSession GoldBot VoiceAI ichidagi ovozli muloqot sessiyalarini boshqaruvchi yagona Canonical modul hisoblanadi. U ovozni qayta ishlamaydi — faqat sessiya konteksti va holatini ta'minlaydi.
