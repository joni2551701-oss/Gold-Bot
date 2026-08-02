# Voice Commands
Status: CANONICAL
---
# Purpose
VoiceCommands GoldBot VoiceAI ichidagi Canonical Voice Command Processing moduli hisoblanadi.
Uning asosiy vazifasi foydalanuvchining ovozli buyruqlarini aniqlash, tahlil qilish va ularni standart AI Command formatiga o'tkazishdir.
VoiceCommands Speech Recognition bajarmaydi.
VoiceCommands AI Decision qabul qilmaydi.
VoiceCommands faqat Voice Intent va Command Processing bilan shug'ullanadi.
---
# Objective
VoiceCommands quyidagi vazifalarni bajaradi.
• Voice Intent Detection
• Command Parsing
• Command Classification
• Parameter Extraction
• Context Detection
• Command Routing
---
# Layer Position
```text
SpeechToText
↓
VoiceCommands
↓
InteractionManager
```
---
# Responsibilities
VoiceCommands
✓ Voice Intent aniqlaydi
✓ Command turini aniqlaydi
✓ Parametrlarni ajratadi
✓ Command Context yaratadi
✓ AI Command yaratadi
✓ InteractionManager'ga uzatadi
---
# Not Responsible
VoiceCommands
✗ Speech Recognition
✗ Text To Speech
✗ AI Analysis
✗ Knowledge Storage
✗ Learning
✗ Decision Making
---
# Input
VoiceCommands qabul qiladi.
• Recognized Text
• User Context
• Conversation Context
---
# Output
VoiceCommands yaratadi.
• AI Command
• Command Intent
• Parameters
• Command Metadata
---
# Workflow
```text
Recognized Text
↓
Detect Intent
↓
Parse Command
↓
Extract Parameters
↓
Build AI Command
↓
InteractionManager
```
---
# Golden Rules
1. Faqat STT natijasi bilan ishlaydi.
2. Har bir Command Intent aniqlanishi shart.
3. Parametrlar ajratilishi shart.
4. AI Logic bajarilmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
VoiceCommands/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
VoiceCommands GoldBot VoiceAI ichidagi ovozli buyruqlarni AI uchun standart Command formatiga aylantiruvchi Canonical modul hisoblanadi.
