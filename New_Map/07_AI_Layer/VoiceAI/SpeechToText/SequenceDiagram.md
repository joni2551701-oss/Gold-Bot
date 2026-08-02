# Speech To Text Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat SpeechToText Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
User Voice
↓
SpeechToText
↓
Detect Language
↓
Recognize Speech
↓
Generate Transcript
↓
InteractionManager
```
---
# Runtime Rules
1. Audio qabul qilinishi shart.
2. Language aniqlanishi shart.
3. Transcript yaratilishi shart.
4. Confidence Score hisoblanishi shart.
---
# State Flow
```text
Idle
↓
Listening
↓
Recognizing
↓
Generating Transcript
↓
Completed
or
Recognition Failed
```
---
# Summary
User Voice
↓
SpeechToText
↓
Recognized Text
↓
InteractionManager
