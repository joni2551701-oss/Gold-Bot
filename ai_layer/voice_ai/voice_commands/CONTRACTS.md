# Voice Commands Contracts
Status: CANONICAL
---
# Purpose
Ushbu hujjat VoiceCommands modulining rasmiy Architecture Contract hujjati hisoblanadi.
---
# Module Responsibility
VoiceCommands quyidagilar uchun javobgar.
✓ Voice Intent Detection
✓ Command Parsing
✓ Parameter Extraction
✓ Context Analysis
✓ AI Command Generation
✓ Command Routing
VoiceCommands bajarmaydi.
✗ Speech Recognition
✗ Speech Synthesis
✗ AI Analysis
✗ Knowledge Storage
✗ Learning
✗ Decision Making
---
# Module Boundary
```text
SpeechToText
↓
VoiceCommands
↓
InteractionManager
```
---
# Input Contract
• Recognized Text
• User Context
• Conversation Context
---
# Output Contract
• AI Command
• Command Intent
• Parameters
• Command Metadata
---
# Allowed Dependencies
✓ SpeechToText
✓ InteractionManager
---
# Forbidden Dependencies
✗ TextToSpeech
✗ KnowledgeAI
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
---
# Runtime Contract
1. SpeechToText natijasi mavjud bo'lishi shart.
2. Har bir buyruq uchun Intent aniqlanishi shart.
3. Parametrlar avtomatik ajratilishi shart.
4. AI Command standart formatda yaratilishi shart.
5. AI Logic VoiceCommands ichida bajarilmaydi.
6. Unknown Command holati qo'llab-quvvatlanishi shart.
7. Circular Dependency qat'iyan taqiqlanadi.
---
# Acceptance Criteria
✓ Intent aniqlanadi.
✓ Command parse qilinadi.
✓ Parametrlar ajratiladi.
✓ AI Command yaratiladi.
✓ InteractionManager'ga uzatiladi.
✓ Architecture Boundary buzilmaydi.
---
# Summary
VoiceCommands Contract GoldBot VoiceAI ichidagi barcha ovozli buyruqlarni standart AI Command formatiga aylantirish va InteractionManager'ga uzatishni belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
