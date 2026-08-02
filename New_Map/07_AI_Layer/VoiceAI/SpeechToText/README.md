# Speech To Text
Status: CANONICAL
---
# Purpose
SpeechToText GoldBot VoiceAI ichidagi Canonical Speech Recognition moduli hisoblanadi.
Uning asosiy vazifasi foydalanuvchining ovozini matnga aylantirish va AI Pipeline uchun standart Text Request yaratishdir.
SpeechToText AI javob bermaydi.
SpeechToText Voice Synthesis bajarmaydi.
SpeechToText faqat Speech Recognition bilan shug'ullanadi.
---
# Objective
SpeechToText quyidagi vazifalarni bajaradi.
• Audio Reception
• Speech Recognition
• Language Detection
• Text Extraction
• Transcript Generation
• Recognition Metadata
---
# Layer Position
```text
User Voice
↓
SpeechToText
↓
InteractionManager
```
---
# Responsibilities
SpeechToText
✓ Audio qabul qiladi
✓ Nutqni aniqlaydi
✓ Tilni aniqlaydi
✓ Matn yaratadi
✓ Transcript hosil qiladi
✓ Recognition Metadata yaratadi
---
# Not Responsible
SpeechToText
✗ AI Analysis
✗ Text To Speech
✗ Decision Making
✗ Knowledge Storage
✗ Learning
---
# Input
SpeechToText qabul qiladi.
• Audio Stream
• Voice Session
• Language Preference
---
# Output
SpeechToText yaratadi.
• Recognized Text
• Transcript
• Language
• Confidence Score
• Recognition Metadata
---
# Workflow
```text
Receive Audio
↓
Detect Language
↓
Recognize Speech
↓
Generate Transcript
↓
Return Text
↓
InteractionManager
```
---
# Golden Rules
1. Audio o'zgartirilmaydi.
2. Recognition imkon qadar real-time ishlaydi.
3. Confidence Score yaratiladi.
4. AI Logic bajarilmaydi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
SpeechToText/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
SpeechToText foydalanuvchi ovozini AI uchun standart matnga aylantiruvchi Canonical Speech Recognition moduli hisoblanadi.
