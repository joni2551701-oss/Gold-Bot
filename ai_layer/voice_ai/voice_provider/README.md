# Voice Provider
Status: CANONICAL
---
# Purpose
VoiceProvider GoldBot VoiceAI ichidagi Canonical Voice Provider Registry moduli hisoblanadi.
Uning asosiy vazifasi tashqi ovoz provayderlarini (OpenAI, ElevenLabs, Local, Custom) ro'yxatga olish, ularning ENABLED/DISABLED holatini boshqarish va yagona Provider Contract orqali taqdim etishdir.
VoiceProvider ovozni o'zi qayta ishlamaydi — u faqat provayderni tanlaydi va taqdim etadi.
---
# Objective
VoiceProvider quyidagi vazifalarni bajaradi.
• Provider Registration
• Provider Contract Enforcement
• Provider Selection
• Provider Status Management (ENABLED/DISABLED)
• Provider Adapter Isolation
• Provider Metadata
---
# Layer Position
```text
VoiceSession
↓
VoiceProvider
↓
SpeechToText / TextToSpeech
```
---
# Responsibilities
VoiceProvider
✓ Voice Provider'larni ro'yxatga oladi
✓ Har bir Provider uchun yagona Contract'ni majburlaydi
✓ Provider ENABLED/DISABLED holatini boshqaradi
✓ So'ralgan vazifa uchun mos Provider'ni tanlaydi
✓ Provider Adapter'larni tashqi SDK'lardan izolyatsiya qiladi
---
# Not Responsible
VoiceProvider
✗ Speech Recognition (SpeechToText vazifasi)
✗ Speech Synthesis (TextToSpeech vazifasi)
✗ AI Analysis
✗ Decision Making
✗ Knowledge Storage
---
# Input
VoiceProvider qabul qiladi.
• Provider Request
• Provider Configuration
• Owner Enable/Disable Intent
---
# Output
VoiceProvider yaratadi.
• Selected Provider
• Provider Descriptor
• Provider Status
• Provider Metadata
---
# Workflow
```text
VoiceSession
↓
VoiceProvider
↓
SpeechToText / TextToSpeech
```
---
# Internal Modules (Planned — implementatsiya bosqichida to'ldiriladi)
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
# Golden Rules
1. Har bir Provider yagona Provider Contract'ga bo'ysunishi shart.
2. Provider'lar sukut bo'yicha DISABLED holatida bo'ladi.
3. Provider faqat Owner ruxsati bilan ENABLED holatiga o'tadi.
4. Tashqi SDK chaqiruvlari faqat Provider Adapter ichida bo'ladi.
5. VoiceProvider ovoz mazmunini o'zgartirmaydi.
6. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
VoiceProvider/
├── README.md
├── Contracts.md
├── ModuleMap.md
└── SequenceDiagram.md
```
---
# Summary
VoiceProvider GoldBot VoiceAI ichidagi barcha tashqi ovoz provayderlarini boshqaruvchi yagona Canonical Provider Registry moduli hisoblanadi. U ovozni qayta ishlamaydi — faqat qaysi Provider ishlatilishini belgilaydi.
