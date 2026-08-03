# Voice Commands Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat VoiceCommands Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
SpeechToText
↓
Recognized Text
↓
VoiceCommands
↓
Intent Detection
↓
Command Parsing
↓
Parameter Extraction
↓
InteractionManager
```
---
# Runtime Rules
1. Recognized Text mavjud bo'lishi shart.
2. Intent aniqlanishi shart.
3. Parameter Extraction bajarilishi shart.
4. AI Command yaratilishi shart.
---
# State Flow
```text
Idle
↓
Receiving Text
↓
Detecting Intent
↓
Parsing
↓
Building Command
↓
Completed
or
Unknown Command
```
---
# Summary
SpeechToText
↓
VoiceCommands
↓
AI Command
↓
InteractionManager
