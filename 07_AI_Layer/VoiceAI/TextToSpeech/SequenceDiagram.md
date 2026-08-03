# Text To Speech Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat TextToSpeech Runtime Sequence'ni tavsiflaydi.
---
# Runtime Sequence
```text
PersonalAI
↓
TextToSpeech
↓
Load Voice Profile
↓
Generate Speech
↓
Apply Speech Settings
↓
Return Audio
↓
User
```
---
# Runtime Rules
1. AI Response mavjud bo'lishi shart.
2. Voice Profile yuklanadi.
3. Speech Generation bajariladi.
4. Audio foydalanuvchiga uzatiladi.
---
# State Flow
```text
Idle
↓
Receiving Text
↓
Generating Audio
↓
Streaming
↓
Completed
or
Generation Failed
```
---
# Summary
PersonalAI
↓
TextToSpeech
↓
Voice Output
