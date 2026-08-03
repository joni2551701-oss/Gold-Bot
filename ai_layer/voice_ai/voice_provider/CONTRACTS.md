# Voice Provider Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat VoiceProvider modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
VoiceProvider quyidagilar uchun javobgar.
✓ Voice Provider'larni ro'yxatga oladi
✓ Har bir Provider uchun yagona Contract'ni majburlaydi
✓ Provider ENABLED/DISABLED holatini boshqaradi
✓ So'ralgan vazifa uchun mos Provider'ni tanlaydi
✓ Provider Adapter'larni tashqi SDK'lardan izolyatsiya qiladi
VoiceProvider bajarmaydi.
✗ Speech Recognition (SpeechToText vazifasi)
✗ Speech Synthesis (TextToSpeech vazifasi)
✗ AI Analysis
✗ Decision Making
✗ Knowledge Storage
---
# Module Boundary
```text
VoiceSession
↓
VoiceProvider
↓
SpeechToText / TextToSpeech
```
---
# Input Contract
• Provider Request
• Provider Configuration
• Owner Enable/Disable Intent
---
# Output Contract
• Selected Provider
• Provider Descriptor
• Provider Status
• Provider Metadata
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
# Runtime Contract
1. Har bir Provider yagona Provider Contract'ga bo'ysunishi shart.
2. Provider'lar sukut bo'yicha DISABLED holatida bo'ladi.
3. Provider faqat Owner ruxsati bilan ENABLED holatiga o'tadi.
4. Tashqi SDK chaqiruvlari faqat Provider Adapter ichida bo'ladi.
5. VoiceProvider ovoz mazmunini o'zgartirmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Provider ro'yxatga olinadi.
✓ Provider Contract majburlanadi.
✓ Provider Status boshqariladi.
✓ Mos Provider tanlanadi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
VoiceProvider Contract VoiceProvider GoldBot VoiceAI ichidagi barcha tashqi ovoz provayderlarini boshqaruvchi yagona Canonical Provider Registry moduli hisoblanadi. U ovozni qayta ishlamaydi — faqat qaysi Provider ishlatilishini belgilaydi.
